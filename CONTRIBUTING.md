# Contributing

English | [中文](CONTRIBUTING.zh-CN.md)

Thank you for helping improve Human Understanding Checkpoint.

## Good contributions

- New cases that expose a reusable failure mode, especially held-out scenarios unlike existing examples.
- Better calibration between under-checking and unnecessary friction.
- Accessibility, multilingual, and adult-to-adult interaction improvements.
- Independent benchmark replications, human ratings, and model adapters.
- Clearer documentation of limitations or related work.

## Before changing the runtime skill

Keep human-facing explanation in `README*` or `docs/`. Add text to `SKILL.md` or `references/` only when it changes model behavior. Prefer one general rule over several scenario-specific scripts.

Do not tune against held-out wording. If a held-out case informs a change, retire or replace it before using the suite for a new generalization claim.

## Validate your change

```sh
python3 scripts/validate_skill.py
python3 benchmark/benchmark.py validate
python3 -m unittest discover -s benchmark/tests -p 'test_*.py'
```

For behavior changes, run a paired blinded evaluation described in [benchmark/BENCHMARK.md](benchmark/BENCHMARK.md). Report regressions and hard failures, not only the average score.

## Pull request checklist

- Explain the behavior or documentation problem being solved.
- Keep English and Chinese user-facing documentation aligned.
- Add or update tests when the harness changes.
- State whether benchmark cases or success gates changed.
- Do not include blind keys, private prompts, credentials, or participant data.
- Preserve the distinction between conversational evidence and proof of a person's internal understanding.
