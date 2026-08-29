#!/usr/bin/env python3
"""Adapter from benchmark JSON stdin to an isolated `codex exec` response."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def build_prompt(request: dict) -> str:
    messages = request.get("messages")
    if not isinstance(request.get("system_prompt"), str) or not isinstance(messages, list):
        raise ValueError("input requires system_prompt and messages")
    transcript = []
    for message in messages:
        role = message.get("role")
        content = message.get("content")
        if role not in {"user", "assistant"} or not isinstance(content, str):
            raise ValueError("messages require user/assistant roles and string content")
        transcript.append(f"<{role}>\n{content}\n</{role}>")
    return (
        request["system_prompt"].strip()
        + "\n\nContinue the conversation below. Return only the assistant's next message. "
        "Do not use tools, inspect files, discuss the benchmark, or add meta-commentary.\n\n"
        + "\n\n".join(transcript)
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model")
    parser.add_argument("--timeout", type=float, default=180.0)
    args = parser.parse_args()
    try:
        request = json.loads(sys.stdin.read())
        prompt = build_prompt(request)
        with tempfile.TemporaryDirectory(prefix="huc-benchmark-") as temporary:
            output_path = Path(temporary) / "last-message.txt"
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
                str(output_path),
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
            response = output_path.read_text(encoding="utf-8").strip()
            if not response:
                raise RuntimeError("codex exec produced no final response")
        print(json.dumps({"response": response}, ensure_ascii=False))
        return 0
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
