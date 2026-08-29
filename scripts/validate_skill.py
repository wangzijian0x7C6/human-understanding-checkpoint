#!/usr/bin/env python3
"""Validate the skill package and its GitHub-facing documentation."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
EXPECTED_NAME = "human-understanding-checkpoint"

REQUIRED_FILES = (
    "AGENTS.md",
    "SKILL.md",
    "README.md",
    "README.zh-CN.md",
    "CONTRIBUTING.md",
    "CONTRIBUTING.zh-CN.md",
    "CHANGELOG.md",
    "RELEASE_CHECKLIST.md",
    "agents/openai.yaml",
    "references/patterns-and-cases.md",
    "docs/value-cases.md",
    "docs/value-cases.zh-CN.md",
    "benchmark/BENCHMARK.md",
    "benchmark/JUDGE_RUBRIC.md",
    "benchmark/cases.jsonl",
    "benchmark/config.json",
    "benchmark/splits.json",
    ".github/workflows/validate.yml",
)


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    try:
        frontmatter, _ = text[4:].split("\n---\n", 1)
    except ValueError as exc:
        raise ValueError("SKILL.md frontmatter must end with ---") from exc

    values: dict[str, str] = {}
    for line in frontmatter.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"unsupported frontmatter line: {line!r}")
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip("'\"")
    return values


def local_markdown_links(path: Path) -> list[Path]:
    text = path.read_text(encoding="utf-8")
    targets: list[Path] = []
    for raw in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
        target = raw.strip().strip("<>").split("#", 1)[0]
        if not target or "://" in target or target.startswith(("mailto:", "#")):
            continue
        targets.append((path.parent / target).resolve())
    return targets


def validate(release: bool) -> list[str]:
    errors: list[str] = []

    for relative in REQUIRED_FILES:
        if not (ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")

    if SKILL.is_file():
        skill_text = SKILL.read_text(encoding="utf-8")
        try:
            metadata = parse_frontmatter(skill_text)
        except ValueError as exc:
            errors.append(str(exc))
        else:
            if metadata.get("name") != EXPECTED_NAME:
                errors.append(f"frontmatter name must be {EXPECTED_NAME!r}")
            description = metadata.get("description", "")
            if not description:
                errors.append("frontmatter description is required")
            elif len(description) > 1024:
                errors.append("frontmatter description must not exceed 1024 characters")
            unknown = set(metadata) - {"name", "description"}
            if unknown:
                errors.append(f"unsupported frontmatter fields: {sorted(unknown)}")

        if "docs/" in skill_text or "value-cases" in skill_text:
            errors.append("SKILL.md must not load human-facing GitHub examples at runtime")
        if len(skill_text.splitlines()) > 500:
            errors.append("SKILL.md exceeds the 500-line runtime guidance limit")

    for markdown in ROOT.rglob("*.md"):
        if any(part in {".git", "work"} for part in markdown.parts):
            continue
        for target in local_markdown_links(markdown):
            if not target.exists():
                try:
                    shown = target.relative_to(ROOT)
                except ValueError:
                    shown = target
                errors.append(f"broken local link in {markdown.relative_to(ROOT)}: {shown}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8") if (ROOT / "README.md").is_file() else ""
    readme_zh = (
        (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
        if (ROOT / "README.zh-CN.md").is_file()
        else ""
    )
    if "[中文](README.zh-CN.md)" not in readme:
        errors.append("README.md must link to README.zh-CN.md")
    if "[English](README.md)" not in readme_zh:
        errors.append("README.zh-CN.md must link to README.md")

    if release:
        if "<owner>" in readme or "<owner>" in readme_zh:
            errors.append("replace <owner> placeholders before release")
        if not any((ROOT / name).is_file() for name in ("LICENSE", "LICENSE.md", "COPYING")):
            errors.append("add an owner-selected license before release")

    return sorted(set(errors))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--release",
        action="store_true",
        help="also require repository identity and an owner-selected license",
    )
    args = parser.parse_args(argv)
    errors = validate(args.release)
    if errors:
        print("Validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    mode = "release" if args.release else "development"
    print(f"Valid {EXPECTED_NAME} package ({mode} mode).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
