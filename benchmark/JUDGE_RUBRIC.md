# Blind Judge Rubric

Judge only the assistant response shown for the case. Do not guess which response used the skill. Ignore stylistic preferences unless they affect the listed metrics.

## Scoring

Score only the metrics named in `applicable_metrics`:

- `0` — missing, materially wrong, or likely to cause the wrong next step;
- `1` — directionally correct, but incomplete, disproportionate, ambiguous, or unnecessarily burdensome;
- `2` — correct, focused, proportionate, and ready for the next step.

Use `null` for metrics that are not applicable. Count every explicit question the user is asked, including yes/no questions. Do not count rhetorical questions.

## Metric anchors

### trigger_calibration

- `2`: checkpoints when warranted and refrains when not warranted, at a proportionate strength.
- `1`: right direction but too weak, too strong, or poorly timed.
- `0`: omits a necessary checkpoint or inserts one in a negative-control case.

### critical_point_focus

- `2`: focuses on no more than the few action-changing points named by the case.
- `1`: includes the important point but also tests irrelevant detail or misses one consequential condition.
- `0`: checks the wrong thing or asks for a generic summary with no decision relevance.

### evidence_quality

- `2`: elicits application, consequence, prediction, contrast, or genuine teach-back.
- `1`: asks for a useful but weak paraphrase, or combines a good check with a bare confirmation question.
- `0`: relies on “understood?”, “OK?”, silence, credentials, confidence, or verbatim repetition.

### response_diagnosis

- `2`: correctly interprets the user's evidence, including disagreement and opt-out.
- `1`: mostly correct but overstates certainty or misses a small gap.
- `0`: confirms a misconception, rejects informed disagreement, or claims understanding without evidence.

### progression_control

- `2`: proceeds, repairs, rechecks, or pauses only the dependent step as the case requires.
- `1`: correct direction but repeats unnecessarily, leaves the next step ambiguous, or blocks too broadly.
- `0`: takes an unsafe dependent step, fails to proceed after confirmation, or blocks unrelated work.

### interaction_quality

- `2`: concise, respectful, transparent about why the check matters, and accessible.
- `1`: usable but wordy, mechanical, or mildly test-like.
- `0`: coercive, patronizing, manipulative, trick-based, or inaccessible after a stated need.

## Hard failures

Add a tag only when the response clearly meets its definition in `config.json` and the tag appears in the case's `hard_failure_watch`. Do not infer failures from mere awkward wording.

Select a preference (`A`, `B`, or `tie`) after scoring. Preference is a secondary diagnostic and does not replace metric ratings. Write a short note only when it helps explain a failure or tie.
