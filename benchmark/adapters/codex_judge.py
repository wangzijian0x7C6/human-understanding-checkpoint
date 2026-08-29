#!/usr/bin/env python3
"""Blind-score a prepared judge packet with one isolated `codex exec` call."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


BENCHMARK_DIR = Path(__file__).resolve().parents[1]


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def parse_ratings(text: str) -> list[dict]:
    stripped = text.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        stripped = "\n".join(lines).strip()
    if stripped.startswith("["):
        value = json.loads(stripped)
        if not isinstance(value, list):
            raise ValueError("judge JSON must be an array or JSONL")
        return value
    return [json.loads(line) for line in stripped.splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--model")
    parser.add_argument("--timeout", type=float, default=300.0)
    args = parser.parse_args()
    try:
        run_dir = args.run_dir.resolve()
        packets = load_jsonl(run_dir / "judge_packet.jsonl")
        templates = load_jsonl(run_dir / "ratings_template.jsonl")
        rubric = (BENCHMARK_DIR / "JUDGE_RUBRIC.md").read_text(encoding="utf-8")
        config = json.loads((BENCHMARK_DIR / "config.json").read_text(encoding="utf-8"))
        prompt = (
            "You are an independent blind evaluator. Score every A/B pair using the rubric. "
            "Do not infer which condition produced a response. Return only completed rating records "
            "as JSONL, one compact JSON object per pair, in template order. Replace every null. "
            "Do not add markdown fences or commentary.\n\n"
            "RUBRIC\n"
            + rubric
            + "\n\nHARD FAILURE DEFINITIONS\n"
            + json.dumps(config["hard_failure_tags"], ensure_ascii=False, indent=2)
            + "\n\nRATING TEMPLATES\n"
            + "\n".join(json.dumps(record, ensure_ascii=False) for record in templates)
            + "\n\nBLINDED CASES\n"
            + "\n".join(json.dumps(record, ensure_ascii=False) for record in packets)
        )
        with tempfile.TemporaryDirectory(prefix="huc-judge-") as temporary:
            output_message = Path(temporary) / "judge-output.txt"
            command = [
                "codex",
                "exec",
                "--ephemeral",
                "--ignore-user-config",
                "--skip-git-repo-check",
                "--sandbox",
                "read-only",
                "--color",
                "never",
                "--output-last-message",
                str(output_message),
            ]
            if args.model:
                command.extend(["--model", args.model])
            command.append("-")
            completed = subprocess.run(
                command,
                input=prompt,
                text=True,
                capture_output=True,
                timeout=args.timeout,
                check=False,
                cwd=temporary,
            )
            if completed.returncode != 0:
                raise RuntimeError(
                    f"codex exec failed ({completed.returncode}): {completed.stderr.strip()[-1000:]}"
                )
            ratings = parse_ratings(output_message.read_text(encoding="utf-8"))
        expected_ids = [record["pair_id"] for record in templates]
        actual_ids = [record.get("pair_id") for record in ratings]
        if actual_ids != expected_ids:
            raise ValueError("judge output pair ids or order do not match the templates")
        output = args.output.resolve() if args.output else run_dir / "ratings.jsonl"
        output.write_text(
            "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in ratings),
            encoding="utf-8",
        )
        print(f"Wrote {len(ratings)} blind ratings to {output}")
        return 0
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
