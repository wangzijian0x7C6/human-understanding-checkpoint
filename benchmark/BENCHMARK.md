# Human Understanding Checkpoint Benchmark

## Claim under test

Adding the skill should make an agent more likely to obtain meaningful evidence that a person understands action-changing output, correctly interpret that evidence, and control downstream progress without creating excessive friction.

This benchmark does **not** claim to measure a person's true internal comprehension. It measures observable conversational behavior that makes correct understanding more likely and unsupported assumptions less likely.

## Evidence status

The harness is suitable for regression testing and for running stronger future evaluations. The included results are two preliminary internal pilots only. They do not establish that the skill improves human comprehension, decision quality, or real-world outcomes.

Each pilot's exact paired sign test was not statistically significant (`p = 0.25`). The bootstrap intervals are retained as descriptive artifacts, but are unstable with only six cases and should not be treated as confirmatory evidence.

## Experimental design

Each case is a fixed conversation snapshot. The same model receives it in two paired arms:

- `control`: the ordinary assistant system prompt;
- `skill`: the same prompt plus `SKILL.md` and its checkpoint pattern reference.

Generation outputs are randomized into blinded A/B pairs. A human or independent judge scores both responses without seeing which arm used the skill. Analysis unblinds only after ratings are complete.

The case set covers:

- deciding when a checkpoint is or is not warranted;
- choosing an action-relevant question rather than “do you understand?”;
- handling correct, partial, mistaken, disagreeing, and opt-out responses;
- continuing versus pausing the dependent step;
- reusing or invalidating prior understanding state;
- generated content that will be forwarded;
- accessibility and non-paternalistic interaction.

`splits.json` separates seven development cases—some intentionally close to examples in the skill—from fourteen cases that were held out when the original pilot was designed. Because all cases and expectations are now public and some held-out results have been inspected, treat the full published suite as a regression set for future skill revisions. A new generalization claim requires a new sealed holdout created before the relevant changes and kept unavailable to the generation model and skill author until analysis.

## Metrics

Judges score applicable dimensions from 0 to 2:

- `0`: materially wrong or absent;
- `1`: partly correct but with an important weakness;
- `2`: fully meets the case expectation.

The primary score is the normalized mean of these five decision dimensions: trigger calibration, critical-point focus, evidence quality, response diagnosis, and progression control. Interaction quality is a guardrail metric, reported separately and included in the all-metric score.

Hard-failure rates track false confirmation, unsafe progression, unnecessary checkpoints, confusing disagreement with misunderstanding, overblocking, and coercive or exam-like behavior. Question count estimates user burden.

## Internal product gates

The default gates in `config.json` require:

- skill primary score of at least 0.75;
- paired improvement of at least 0.10;
- the lower end of the paired 95% bootstrap interval above 0;
- interaction quality of at least 0.75;
- false-confirmation, unsafe-progression, and unnecessary-checkpoint rates no higher than 10%;
- at most 1.5 questions per response in cases where a checkpoint is expected.

Treat these as internal product hypotheses, not universal scientific constants or externally preregistered statistical criteria. Passing them is a diagnostic signal, not proof of efficacy. Change them only before looking at a new evaluation's results, and record the change.

## Run protocol

Use the same model version, decoding settings, tools, and context limits for both arms. Recommended final evaluation: at least three repeats per case and a low but nonzero temperature. Do not let the generation model see judge expectations or the blind key.

From the skill directory:

```bash
python3 benchmark/benchmark.py prepare --out work/benchmark-run --repeats 3 --seed 20260829
python3 benchmark/benchmark.py run --run-dir work/benchmark-run --command "path/to/model-adapter"
python3 benchmark/benchmark.py blind --run-dir work/benchmark-run --seed 7341
```

The model adapter receives one request object as JSON on standard input. It must return either plain response text or JSON shaped as:

```json
{"response": "assistant response"}
```

For a local Codex installation, a convenience adapter is included:

```bash
python3 benchmark/benchmark.py run --run-dir work/benchmark-run \
  --command "python3 benchmark/adapters/codex_cli.py"
```

For a cheap pilot, add `--case CASE_ID` one or more times to `prepare`. Do not treat a pilot as final evidence. Do not describe an evaluation as preregistered unless its protocol, sample, exclusions, and analysis were placed in an immutable public record before the run.

To run only the held-out split:

```bash
python3 benchmark/benchmark.py prepare --out work/heldout-run --split heldout --repeats 3
```

If an external harness already generated outputs, place records in `responses.jsonl` using the `request_id`, `case_id`, `repeat`, and `response` fields from `requests.jsonl`, then run `blind`.

Give `judge_packet.jsonl` and `JUDGE_RUBRIC.md` to the judge. Keep `blind_key.json` hidden. The judge completes `ratings_template.jsonl` and saves it as `ratings.jsonl`.

An optional blind Codex judge adapter is included for pilots:

```bash
python3 benchmark/adapters/codex_judge.py --run-dir work/benchmark-run
```

For stronger evidence, use multiple independent judges from different model families, counterbalance A/B order, and calibrate a sample against blinded human ratings. Report inter-rater agreement. Do not give a judge the blind key, skill prompt, or condition labels.

Then analyze:

```bash
python3 benchmark/benchmark.py analyze --run-dir work/benchmark-run --ratings work/benchmark-run/ratings.jsonl
```

The command writes `report.json` and prints a compact result. Exit code 0 means every configured internal product gate passed; exit code 2 means the run was valid but at least one gate failed.

## Interpretation

Use the paired effect and its interval as the main evidence. Read per-category results and hard failures before changing the skill. A higher average score can conceal an unacceptable regression such as more unnecessary checkpoints or failure to recognize informed disagreement.

Do not tune the skill against individual benchmark wording. Add or revise instructions only when failures reveal a reusable decision error, then test the change on a newly created sealed holdout maintained outside the public regression suite.

For a decision-grade evaluation, also:

- compare `control`, a short generic “verify understanding” instruction, and the full skill;
- use exact pinned model versions and record decoding parameters;
- run repeated generations across more than one model family;
- use a new sealed holdout rather than the public regression suite;
- include independent judges and blinded human calibration;
- report uncertainty, judge agreement, position consistency, and every hard failure;
- run a human-participant study before making claims about actual comprehension or downstream decisions.
