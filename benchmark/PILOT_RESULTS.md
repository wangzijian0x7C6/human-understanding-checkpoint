# Pilot Results

Date: 2026-08-29

The pilots evaluated the core protocol before the human-facing GitHub value examples were added. Those examples document existing behavior and are not loaded by the runtime skill or benchmark treatment prompt.

## Preliminary outcome

Two small paired, blinded pilots showed the expected direction. They passed the repository's internal product gates, including interaction-quality and user-burden guardrails, but neither exact paired sign test was statistically significant (`p = 0.25` for each). These results are diagnostic only and do not establish efficacy.

| Pilot | Cases | Skill score | Control score | Paired delta | Bootstrap 95% interval | Blind preference |
|---|---:|---:|---:|---:|---:|---:|
| Mixed | 6 | 1.000 | 0.715 | +0.285 | +0.056 to +0.576 | Skill 4, control 0, tie 2 |
| Held-out only | 6 | 0.882 | 0.611 | +0.271 | +0.042 to +0.562 | Skill 5, control 0, tie 1 |

At the time of the run, the held-out pilot was the more informative result because none of its six situations repeated a concrete example from the skill reference. The cases and expectations are now public, so they should be treated as regression cases for future versions rather than as a sealed holdout.

## What improved in the held-out pilot

- The largest gain came from recognizing fragile prerequisites before issuing an executable plan.
- The skill response respected an explicit comprehension gate while the control response handled it less precisely.
- The skill response checked the operational prerequisite instead of treating seniority as evidence of understanding.
- Both arms correctly avoided a checkpoint for a low-stakes rewrite, so the skill did not increase over-intervention in that negative control.
- The skill had zero observed unsafe-progression failures; control had one among four eligible held-out responses.
- The skill averaged 0.8 questions in checkpoint-positive cases, below the 1.5-question burden limit.

## Remaining weaknesses

- In the accessibility case, both arms simplified the explanation but omitted the intended low-pressure application check.
- In the partial-understanding case, the skill repaired the missing condition but its follow-up leaned toward repetition instead of asking how the condition changed timing.
- Several cases tied because the base model already handled obvious correct understanding, informed disagreement, and low-stakes negatives well. The Skill's benefit appears concentrated in triggering a checkpoint and controlling dependent progress.

## Evidence limits

These are directional pilots, not a final efficacy claim:

- only six cases were used in each pilot, with one generation per arm;
- the exact paired sign test was not significant (`p = 0.25`);
- bootstrap intervals are unstable at this sample size even though their lower bounds were positive;
- generation and judging used isolated invocations of the local Codex default model, but the exact model version was not captured;
- one blind judge was used and it came from the same model family;
- the benchmark measures conversational evidence and progression behavior, not a human participant's true internal comprehension.

For a stronger future result, create a new sealed holdout before revising the skill; add a generic-checkpoint baseline; use at least three repeats and more than one model family; record exact model and decoding settings; counterbalance answer order; and use multiple independent judges with blinded human calibration. A human-participant study is still required before claiming improvement in actual comprehension.
