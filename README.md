# Human Understanding Checkpoint

English | [中文](README.zh-CN.md)

An Agent Skill that verifies whether a person understands action-changing model output before a dependent decision, handoff, forwarding step, or consequential action continues.

It is **not an approval dialog** and **not a tutoring system**. It is a general-purpose comprehension-state protocol for human–LLM collaboration: identify the smallest critical point, ask for usable evidence, repair only the gap, and continue at the right boundary.

> [!NOTE]
> This project is a research preview. It provides conversational evidence of understanding, not proof of a person's internal state, legal consent, medical capacity, or professional competence.

## Why this exists

Model output is often copied into a decision, document, or message without the human noticing an assumption, uncertainty, or commitment. A polite “yes” or “understood” does not show that the point can be applied correctly.

The skill adds a proportional checkpoint only when misunderstanding could change the next step.

| Situation | Ordinary failure | Checkpoint behavior |
|---|---|---|
| Forwarding an AI-written recommendation | Estimated evidence becomes a human-endorsed fact | Ask the sender to explain the key claim and commitment before polishing the final draft |
| Later work depends on an earlier distinction | “Understood” is treated as durable evidence | Test the distinction through the real next step and track its conditions |
| The user understands but disagrees | The model repeats warnings or blocks progress | Mark the tradeoff confirmed and respect the informed choice |
| A prior assumption changes | Old confidence is reused in a new situation | Revalidate only the affected topic, not the whole conversation |

See [value cases](docs/value-cases.md) for complete before/after scenarios.

## How it works

1. Identify at most three propositions that could change the user's next action.
2. Choose the lightest sufficient checkpoint: `light`, `active`, or explicitly gated.
3. Ask one application, teach-back, consequence, disambiguation, or prediction question.
4. Classify the evidence as `confirmed`, `partial`, `misconception`, or `unverified`.
5. Continue, narrowly repair and recheck, or pause only the dependent step.

Confirmed understanding is stored as conditional topic state and reused until the underlying facts, assumptions, or required precision change.

## Modes

- `adaptive` — default; intervene only when the consequences justify it.
- `always` — checkpoint each substantive response that introduces a new decision-relevant concept.
- `gate` — do not perform the dependent step until understanding is verified; use only when the user explicitly requests gating or another rule requires it.

## Install

Install from GitHub:

```sh
npx skills add wangzijian0x7C6/human-understanding-checkpoint
```

For a manual Codex installation:

```sh
git clone https://github.com/wangzijian0x7C6/human-understanding-checkpoint.git \
  ~/.codex/skills/human-understanding-checkpoint
```

Then invoke it explicitly when needed:

```text
Use $human-understanding-checkpoint to verify the points I must understand before I send this proposal.
```

The skill can also activate automatically when correct understanding is a meaningful dependency.

## Benchmark

The repository includes a paired, blinded benchmark with 21 fixed conversation cases: 7 development cases and 14 held-out cases. It evaluates trigger calibration, critical-point focus, evidence quality, response diagnosis, progression control, interaction quality, hard failures, and question burden.

Two six-case directional pilots produced the following results:

| Pilot | Skill | Control | Paired improvement | Bootstrap 95% interval |
|---|---:|---:|---:|---:|
| Mixed | 1.000 | 0.715 | +0.285 | +0.056 to +0.576 |
| Held-out only | 0.882 | 0.611 | +0.271 | +0.042 to +0.562 |

These pilots passed the prespecified product gates but are not decision-grade efficacy evidence: the samples were small, used one generation per arm, and relied on a single same-family judge. Read the [benchmark design](benchmark/BENCHMARK.md) and [full limitations](benchmark/PILOT_RESULTS.md) before citing the numbers.

## Validate locally

No third-party Python packages are required for the structural checks or benchmark harness tests.

```sh
python3 scripts/validate_skill.py
python3 benchmark/benchmark.py validate
python3 -m unittest discover -s benchmark/tests -p 'test_*.py'
```

See [BENCHMARK.md](benchmark/BENCHMARK.md) to run paired generations, blind the outputs, collect ratings, and analyze results.

## Project layout

```text
SKILL.md                      Runtime behavior contract
references/                  Runtime patterns loaded only when needed
agents/openai.yaml           Skill display metadata
docs/                        Human-facing examples and design notes
benchmark/                   Cases, blinded harness, rubric, and pilot results
scripts/validate_skill.py    Repository and skill validation
.github/                     CI and contribution templates
```

## Related work

The closest reviewed public skills focus on irreversible software operations or teaching to mastery. This project instead targets general conversation state, forwarding, proportional intervention, informed disagreement, and dependent-step-only gating. The evidence and comparison table are in [related-skill research](benchmark/OVERLAP_RESEARCH.md).

## Contributing

Contributions are welcome, especially new held-out scenarios, accessibility improvements, adapter support, and independent replications. Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

Before making the repository public, complete the [release checklist](RELEASE_CHECKLIST.md), including selecting a license and replacing the repository owner placeholder.
