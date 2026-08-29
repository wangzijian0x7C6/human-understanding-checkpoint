# Maintainer Handoff

This file is the persistent handoff for agents continuing work in this repository. Keep it concise and update it when a decision below changes.

## Start here

This repository contains three distinct layers:

1. `SKILL.md`, `references/`, and `agents/` define runtime behavior.
2. `README*`, `docs/`, and contributor files explain the project to people.
3. `benchmark/` is a public regression and evaluation harness.

Read `SKILL.md` first. For evaluation work, then read `benchmark/BENCHMARK.md`, `benchmark/PILOT_RESULTS.md`, and `benchmark/JUDGE_RUBRIC.md`. Use `CHANGELOG.md` for release history and `benchmark/OVERLAP_RESEARCH.md` for positioning against related skills.

## Preserve these decisions

- The skill seeks conversational evidence of understanding; it does not prove a person's internal comprehension, legal consent, medical capacity, or professional competence.
- Keep runtime instructions limited to content that changes agent behavior. Human-facing value examples belong in `docs/`, not runtime references.
- Default to proportional, adaptive intervention. Do not turn low-risk conversation into an exam or confuse informed disagreement with misunderstanding.
- When a domain-specific comprehension gate already produced evidence, reuse it rather than running a second independent quiz.
- All cases committed in `benchmark/` are public regression fixtures, including those still named `heldout` for historical compatibility. Do not use them for a new generalization claim after their wording or results have informed a change.
- The two published six-case pilots are preliminary and non-significant (`p = 0.25` for each). Do not restore the score table to the README or describe the pilots as efficacy evidence.

## Change workflow

- Keep English and Simplified Chinese user-facing documentation aligned.
- Work on a feature branch, inspect the exact diff, and preserve unrelated changes.
- Before committing, run:

```sh
python3 scripts/validate_skill.py --release
python3 benchmark/benchmark.py validate
python3 -m unittest discover -s benchmark/tests -p 'test_*.py'
```

- For runtime behavior changes, run a paired blinded evaluation and report hard failures as well as average scores. Do not tune to individual public case wording.
- For a new efficacy claim, use a newly created sealed holdout, a generic-checkpoint baseline, repeated generations across model families, independent judges with human calibration, and exact model manifests. Claims about actual human comprehension require a participant study.
- Record user-visible changes in `CHANGELOG.md`. Create a versioned GitHub release only after CI succeeds on the release commit.

## Current state and next work

- Latest release at handoff: `v0.1.1`.
- Repository: `https://github.com/wangzijian0x7C6/human-understanding-checkpoint`.
- Runtime skill behavior was unchanged in `v0.1.1`; that release clarified evaluation claims.
- Useful future work includes an independently maintained sealed evaluation, a three-arm baseline, exact model capture, cross-family judges, human calibration, a participant study, and optional skills.sh submission.

These are possible next steps, not standing authorization. Confirm the user's requested scope before external publication, paid evaluation, participant recruitment, or other consequential actions.
