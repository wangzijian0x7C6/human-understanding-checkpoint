# Human Understanding Checkpoint

English | [中文](README.zh-CN.md)

An Agent Skill that seeks usable evidence of a person's understanding before action-changing model output is used in a dependent decision, handoff, forwarding step, or consequential action.

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
| Unverified model-derived number | A conversational estimate is treated as an audited result | Separate understanding from validity and surface the remaining verification |
| Model-recalled citation, policy, or “done” claim | A confidently wrong reference or unanchored execution claim is relied on | Label it unverified, offer a deterministic check, and verify intended use |

See [value cases](docs/value-cases.md) for complete before/after scenarios.

## How it works

1. Identify at most three propositions that could change the user's next action.
2. Choose the lightest sufficient checkpoint: `light`, `active`, or explicitly gated.
3. Ask one application, teach-back, consequence, disambiguation, or prediction question.
4. Classify the evidence as `confirmed`, `partial`, `misconception`, or `unverified`.
5. Continue, narrowly repair and recheck, or pause only the dependent step.

Confirmed understanding is stored as conditional topic state and reused; revalidation is generally triggered only when facts or assumptions change, the user later contradicts it, much time or context has passed, or the downstream action requires greater precision.

Understanding and content validity are tracked separately. The same unverified-claim treatment covers five known LLM reliability limitations: informal quantitative reasoning, traceable references (citations, statutes, clause and API names), current-state facts that may predate the knowledge cutoff, execution claims without an anchored tool result, and detail extracted from images, PDFs, tables, or long documents. The checkpoint verifies that the user understands a claim's status and intended use, not the claim's correctness itself.

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

## Preliminary evaluation

The repository includes a paired, blinded evaluation harness with 23 fixed conversation cases. It measures observable **agent behavior**—such as checkpoint calibration, evidence quality, progression control, hard failures, and question burden—not a person's true comprehension.

Two internal pilots of six cases each showed a positive direction, but they used one generation per arm, one same-family judge, and an unrecorded exact model version. Their exact paired sign tests were not statistically significant (`p = 0.25` for each). They should not be cited as evidence that the skill improves human understanding.

The harness, rubric, cases, and raw pilot artifacts remain public for reproducibility. Read the [evaluation design](benchmark/BENCHMARK.md) and [preliminary pilot report](benchmark/PILOT_RESULTS.md). Future efficacy claims require a new sealed holdout, stronger baselines, repeated generations, and independent or human judging.

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
docs/                        Human-facing value cases
benchmark/                   Cases, blinded harness, rubric, and pilot results
scripts/validate_skill.py    Repository and skill validation
.github/                     CI and contribution templates
```

## Related work

The closest reviewed public skills focus on irreversible software operations or teaching to mastery. This project instead targets general conversation state, forwarding, proportional intervention, informed disagreement, and dependent-step-only gating. The evidence and comparison table are in [related-skill research](benchmark/OVERLAP_RESEARCH.md).

## Contributing

Contributions are welcome, especially new regression scenarios, independently maintained sealed evaluations, accessibility improvements, adapter support, and replications. Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

Release status and remaining optional distribution steps are tracked in the [release checklist](RELEASE_CHECKLIST.md).
