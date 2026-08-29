#!/usr/bin/env python3
"""Paired, blinded benchmark for the human-understanding-checkpoint skill."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import shlex
import statistics
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable


BENCHMARK_DIR = Path(__file__).resolve().parent
SKILL_DIR = BENCHMARK_DIR.parent
DEFAULT_CASES = BENCHMARK_DIR / "cases.jsonl"
DEFAULT_CONFIG = BENCHMARK_DIR / "config.json"
DEFAULT_SPLITS = BENCHMARK_DIR / "splits.json"
DEFAULT_SKILL = SKILL_DIR / "SKILL.md"
DEFAULT_PATTERNS = SKILL_DIR / "references" / "patterns-and-cases.md"

PRIMARY_METRICS = (
    "trigger_calibration",
    "critical_point_focus",
    "evidence_quality",
    "response_diagnosis",
    "progression_control",
)
INTERACTION_METRIC = "interaction_quality"


class BenchmarkError(ValueError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise BenchmarkError(f"Cannot read JSON from {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise BenchmarkError(f"Expected a JSON object in {path}")
    return value


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise BenchmarkError(f"Cannot read {path}: {exc}") from exc
    for line_number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise BenchmarkError(f"Invalid JSON at {path}:{line_number}: {exc}") from exc
        if not isinstance(value, dict):
            raise BenchmarkError(f"Expected an object at {path}:{line_number}")
        records.append(value)
    return records


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, records: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records)
    path.write_text(text, encoding="utf-8")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def validate_suite(cases: list[dict[str, Any]], config: dict[str, Any]) -> None:
    metrics = set(config.get("metrics", {}))
    hard_tags = set(config.get("hard_failure_tags", {}))
    if not metrics or not hard_tags:
        raise BenchmarkError("config.json must define metrics and hard_failure_tags")
    if not set(PRIMARY_METRICS).issubset(metrics) or INTERACTION_METRIC not in metrics:
        raise BenchmarkError("config.json is missing required benchmark metrics")

    seen: set[str] = set()
    positive = negative = 0
    for case in cases:
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id:
            raise BenchmarkError("Every case needs a non-empty string id")
        if case_id in seen:
            raise BenchmarkError(f"Duplicate case id: {case_id}")
        seen.add(case_id)
        expected = case.get("checkpoint_expected")
        if not isinstance(expected, bool):
            raise BenchmarkError(f"{case_id}: checkpoint_expected must be boolean")
        positive += int(expected)
        negative += int(not expected)
        messages = case.get("messages")
        if not isinstance(messages, list) or not messages:
            raise BenchmarkError(f"{case_id}: messages must be a non-empty list")
        for message in messages:
            if not isinstance(message, dict) or message.get("role") not in {"user", "assistant"}:
                raise BenchmarkError(f"{case_id}: each message needs role user/assistant")
            if not isinstance(message.get("content"), str) or not message["content"].strip():
                raise BenchmarkError(f"{case_id}: every message needs non-empty content")
        applicable = case.get("applicable_metrics")
        if not isinstance(applicable, list) or not applicable:
            raise BenchmarkError(f"{case_id}: applicable_metrics must be non-empty")
        unknown_metrics = set(applicable) - metrics
        if unknown_metrics:
            raise BenchmarkError(f"{case_id}: unknown metrics {sorted(unknown_metrics)}")
        judge = case.get("judge")
        if not isinstance(judge, dict) or not isinstance(judge.get("expectation"), str):
            raise BenchmarkError(f"{case_id}: judge.expectation is required")
        watches = judge.get("hard_failure_watch", [])
        if not isinstance(watches, list) or set(watches) - hard_tags:
            raise BenchmarkError(f"{case_id}: unknown hard_failure_watch tags")
    if positive == 0 or negative == 0:
        raise BenchmarkError("Suite needs checkpoint-positive and negative-control cases")


def validate_splits(cases: list[dict[str, Any]], splits: dict[str, Any]) -> None:
    case_ids = {case["id"] for case in cases}
    if set(splits) != {"dev", "heldout"}:
        raise BenchmarkError("splits.json must contain exactly dev and heldout")
    dev = splits["dev"]
    heldout = splits["heldout"]
    if not isinstance(dev, list) or not isinstance(heldout, list):
        raise BenchmarkError("dev and heldout splits must be lists")
    if len(dev) != len(set(dev)) or len(heldout) != len(set(heldout)):
        raise BenchmarkError("split ids must be unique")
    if set(dev) & set(heldout):
        raise BenchmarkError("dev and heldout splits must be disjoint")
    if set(dev) | set(heldout) != case_ids:
        raise BenchmarkError("dev and heldout splits must cover every case exactly once")


def command_validate(args: argparse.Namespace) -> int:
    cases = load_jsonl(args.cases)
    config = load_json(args.config)
    splits = load_json(args.splits)
    validate_suite(cases, config)
    validate_splits(cases, splits)
    categories = sorted({case["category"] for case in cases})
    expected = sum(bool(case["checkpoint_expected"]) for case in cases)
    print(
        f"Valid suite: {len(cases)} cases, {len(categories)} categories, "
        f"{expected} checkpoint-positive, {len(cases) - expected} negative; "
        f"{len(splits['dev'])} dev and {len(splits['heldout'])} held-out."
    )
    return 0


def treatment_prompt(base: str, skill_text: str, patterns_text: str) -> str:
    return (
        base.rstrip()
        + "\n\nThe current conversation is being handled with the following skill. "
        "Apply it faithfully without mentioning the skill or evaluation to the user.\n\n"
        + skill_text.strip()
        + "\n\nThe skill's referenced checkpoint patterns and cases follow:\n\n"
        + patterns_text.strip()
    )


def command_prepare(args: argparse.Namespace) -> int:
    cases = load_jsonl(args.cases)
    config = load_json(args.config)
    splits = load_json(args.splits)
    validate_suite(cases, config)
    validate_splits(cases, splits)
    all_case_ids = {case["id"] for case in cases}
    if args.split:
        split_ids = set(splits[args.split])
        cases = [case for case in cases if case["id"] in split_ids]
    if args.case:
        requested = set(args.case)
        unknown = requested - all_case_ids
        if unknown:
            raise BenchmarkError(f"Unknown --case id(s): {sorted(unknown)}")
        if args.split and not requested.issubset({case["id"] for case in cases}):
            raise BenchmarkError("Every --case must belong to the selected --split")
        cases = [case for case in cases if case["id"] in requested]
    if args.repeats < 1:
        raise BenchmarkError("--repeats must be at least 1")

    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    skill_text = args.skill.read_text(encoding="utf-8")
    patterns_text = args.patterns.read_text(encoding="utf-8")
    base_prompt = config["base_system_prompt"]
    prompts = {
        "control": base_prompt,
        "skill": treatment_prompt(base_prompt, skill_text, patterns_text),
    }

    records: list[dict[str, Any]] = []
    for case in cases:
        for repeat in range(1, args.repeats + 1):
            for arm in ("control", "skill"):
                records.append(
                    {
                        "request_id": f"{case['id']}::r{repeat}::{arm}",
                        "case_id": case["id"],
                        "repeat": repeat,
                        "arm": arm,
                        "system_prompt": prompts[arm],
                        "messages": case["messages"],
                    }
                )
    random.Random(args.seed).shuffle(records)
    write_jsonl(out / "requests.jsonl", records)
    write_json(
        out / "manifest.json",
        {
            "benchmark_version": config.get("benchmark_version"),
            "seed": args.seed,
            "split": args.split or "all",
            "repeats": args.repeats,
            "case_count": len(cases),
            "request_count": len(records),
            "skill_sha256": sha256_text(skill_text),
            "patterns_sha256": sha256_text(patterns_text),
            "cases_sha256": sha256_text(args.cases.read_text(encoding="utf-8")),
        },
    )
    print(f"Prepared {len(records)} requests in {out}")
    return 0


def parse_adapter_output(stdout: str) -> str:
    text = stdout.strip()
    if not text:
        raise BenchmarkError("adapter returned empty output")
    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        return text
    if isinstance(value, dict) and isinstance(value.get("response"), str):
        return value["response"]
    raise BenchmarkError("adapter JSON output must contain a string field named 'response'")


def command_run(args: argparse.Namespace) -> int:
    run_dir = args.run_dir.resolve()
    requests = load_jsonl(run_dir / "requests.jsonl")
    command = shlex.split(args.command)
    if not command:
        raise BenchmarkError("--command cannot be empty")
    if args.limit is not None:
        if args.limit < 1:
            raise BenchmarkError("--limit must be at least 1")
        requests = requests[: args.limit]

    outputs: list[dict[str, Any]] = []
    failures = 0
    for index, request in enumerate(requests, 1):
        adapter_input = {
            "system_prompt": request["system_prompt"],
            "messages": request["messages"],
        }
        started = time.monotonic()
        try:
            completed = subprocess.run(
                command,
                input=json.dumps(adapter_input, ensure_ascii=False),
                text=True,
                capture_output=True,
                timeout=args.timeout,
                check=False,
            )
            if completed.returncode != 0:
                raise BenchmarkError(
                    f"adapter exit {completed.returncode}: {completed.stderr.strip()[:500]}"
                )
            response = parse_adapter_output(completed.stdout)
            error = None
        except (OSError, subprocess.TimeoutExpired, BenchmarkError) as exc:
            response = ""
            error = str(exc)
            failures += 1
        outputs.append(
            {
                "request_id": request["request_id"],
                "case_id": request["case_id"],
                "repeat": request["repeat"],
                "response": response,
                "error": error,
                "latency_ms": round((time.monotonic() - started) * 1000),
            }
        )
        print(f"[{index}/{len(requests)}] {request['case_id']} r{request['repeat']}")
    write_jsonl(run_dir / "responses.jsonl", outputs)
    if failures:
        print(f"Completed with {failures} adapter failure(s).", file=sys.stderr)
        return 1
    print(f"Wrote {len(outputs)} responses to {run_dir / 'responses.jsonl'}")
    return 0


def command_blind(args: argparse.Namespace) -> int:
    run_dir = args.run_dir.resolve()
    requests = load_jsonl(run_dir / "requests.jsonl")
    responses = load_jsonl(run_dir / "responses.jsonl")
    cases = load_jsonl(args.cases)
    config = load_json(args.config)
    validate_suite(cases, config)
    cases_by_id = {case["id"]: case for case in cases}
    request_by_id = {request["request_id"]: request for request in requests}
    response_by_id: dict[str, dict[str, Any]] = {}
    for response in responses:
        request_id = response.get("request_id")
        if request_id in response_by_id:
            raise BenchmarkError(f"Duplicate response for {request_id}")
        response_by_id[request_id] = response
    missing = set(request_by_id) - set(response_by_id)
    if missing:
        raise BenchmarkError(f"Missing {len(missing)} responses; first: {sorted(missing)[0]}")
    failed = [record for record in responses if record.get("error") or not record.get("response")]
    if failed:
        raise BenchmarkError(f"Cannot blind {len(failed)} failed or empty responses")

    grouped: dict[tuple[str, int], dict[str, tuple[dict[str, Any], dict[str, Any]]]] = defaultdict(dict)
    for request_id, request in request_by_id.items():
        grouped[(request["case_id"], request["repeat"])][request["arm"]] = (
            request,
            response_by_id[request_id],
        )

    rng = random.Random(args.seed)
    packets: list[dict[str, Any]] = []
    keys: list[dict[str, Any]] = []
    templates: list[dict[str, Any]] = []
    for case_id, repeat in sorted(grouped):
        arms = grouped[(case_id, repeat)]
        if set(arms) != {"control", "skill"}:
            raise BenchmarkError(f"{case_id} repeat {repeat} does not have both arms")
        labels = ["control", "skill"]
        rng.shuffle(labels)
        label_to_arm = {"A": labels[0], "B": labels[1]}
        pair_id = f"{case_id}::r{repeat}"
        case = cases_by_id[case_id]
        packet = {
            "pair_id": pair_id,
            "case_id": case_id,
            "repeat": repeat,
            "category": case["category"],
            "checkpoint_expected": case["checkpoint_expected"],
            "messages": case["messages"],
            "applicable_metrics": case["applicable_metrics"],
            "judge": case["judge"],
            "response_A": arms[label_to_arm["A"]][1]["response"],
            "response_B": arms[label_to_arm["B"]][1]["response"],
        }
        key = {
            "pair_id": pair_id,
            "case_id": case_id,
            "repeat": repeat,
            "labels": label_to_arm,
            "request_ids": {
                label: arms[arm][0]["request_id"] for label, arm in label_to_arm.items()
            },
        }
        score_shape = {
            "metrics": {metric: None for metric in case["applicable_metrics"]},
            "hard_failures": [],
            "question_count": None,
        }
        template = {
            "pair_id": pair_id,
            "scores": {"A": json.loads(json.dumps(score_shape)), "B": json.loads(json.dumps(score_shape))},
            "preference": None,
            "notes": "",
        }
        packets.append(packet)
        keys.append(key)
        templates.append(template)

    write_jsonl(run_dir / "judge_packet.jsonl", packets)
    write_jsonl(run_dir / "blind_key.jsonl", keys)
    write_jsonl(run_dir / "ratings_template.jsonl", templates)
    print(f"Created {len(packets)} blinded pairs and rating templates in {run_dir}")
    return 0


def mean_or_none(values: list[float]) -> float | None:
    return statistics.fmean(values) if values else None


def percentile(values: list[float], probability: float) -> float:
    if not values:
        raise BenchmarkError("Cannot compute percentile of an empty list")
    ordered = sorted(values)
    position = (len(ordered) - 1) * probability
    low = math.floor(position)
    high = math.ceil(position)
    if low == high:
        return ordered[low]
    fraction = position - low
    return ordered[low] * (1 - fraction) + ordered[high] * fraction


def paired_bootstrap_ci(deltas: list[float], samples: int, seed: int) -> tuple[float, float]:
    if samples < 100:
        raise BenchmarkError("--bootstrap-samples must be at least 100")
    rng = random.Random(seed)
    n = len(deltas)
    estimates = [statistics.fmean(deltas[rng.randrange(n)] for _ in range(n)) for _ in range(samples)]
    return percentile(estimates, 0.025), percentile(estimates, 0.975)


def two_sided_sign_test(deltas: list[float]) -> dict[str, Any]:
    wins = sum(delta > 1e-12 for delta in deltas)
    losses = sum(delta < -1e-12 for delta in deltas)
    ties = len(deltas) - wins - losses
    n = wins + losses
    if n == 0:
        p_value = 1.0
    else:
        tail = min(wins, losses)
        probability = sum(math.comb(n, k) for k in range(tail + 1)) / (2**n)
        p_value = min(1.0, 2 * probability)
    return {"wins": wins, "losses": losses, "ties": ties, "p_value": p_value}


def validate_rating(
    rating: dict[str, Any],
    case: dict[str, Any],
    hard_tags: set[str],
) -> None:
    if rating.get("preference") not in {"A", "B", "tie"}:
        raise BenchmarkError(f"{rating.get('pair_id')}: preference must be A, B, or tie")
    for label in ("A", "B"):
        score = rating.get("scores", {}).get(label)
        if not isinstance(score, dict):
            raise BenchmarkError(f"{rating.get('pair_id')} {label}: missing score object")
        metric_scores = score.get("metrics")
        if not isinstance(metric_scores, dict) or set(metric_scores) != set(case["applicable_metrics"]):
            raise BenchmarkError(f"{rating.get('pair_id')} {label}: metric keys do not match case")
        for metric, value in metric_scores.items():
            if not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0 or value > 2:
                raise BenchmarkError(f"{rating.get('pair_id')} {label}: {metric} must be between 0 and 2")
        failures = score.get("hard_failures")
        if not isinstance(failures, list) or len(failures) != len(set(failures)):
            raise BenchmarkError(f"{rating.get('pair_id')} {label}: invalid hard_failures")
        if set(failures) - hard_tags:
            raise BenchmarkError(f"{rating.get('pair_id')} {label}: unknown hard failure tag")
        watched = set(case["judge"].get("hard_failure_watch", []))
        if set(failures) - watched:
            raise BenchmarkError(f"{rating.get('pair_id')} {label}: hard failure not watched by case")
        question_count = score.get("question_count")
        if not isinstance(question_count, int) or isinstance(question_count, bool) or question_count < 0:
            raise BenchmarkError(f"{rating.get('pair_id')} {label}: question_count must be a nonnegative integer")


def command_analyze(args: argparse.Namespace) -> int:
    run_dir = args.run_dir.resolve()
    cases = load_jsonl(args.cases)
    config = load_json(args.config)
    splits = load_json(args.splits)
    validate_suite(cases, config)
    validate_splits(cases, splits)
    cases_by_id = {case["id"]: case for case in cases}
    keys = {record["pair_id"]: record for record in load_jsonl(run_dir / "blind_key.jsonl")}
    ratings = load_jsonl(args.ratings)
    if set(keys) != {record.get("pair_id") for record in ratings}:
        raise BenchmarkError("Ratings must contain every blinded pair exactly once")

    hard_tags = set(config["hard_failure_tags"])
    rows: list[dict[str, Any]] = []
    preference_counts = {"skill": 0, "control": 0, "tie": 0}
    seen_pairs: set[str] = set()
    for rating in ratings:
        pair_id = rating.get("pair_id")
        if pair_id in seen_pairs:
            raise BenchmarkError(f"Duplicate rating pair: {pair_id}")
        seen_pairs.add(pair_id)
        key = keys[pair_id]
        case = cases_by_id[key["case_id"]]
        validate_rating(rating, case, hard_tags)
        preference = rating["preference"]
        if preference == "tie":
            preference_counts["tie"] += 1
        else:
            preference_counts[key["labels"][preference]] += 1
        for label in ("A", "B"):
            arm = key["labels"][label]
            score = rating["scores"][label]
            metric_scores = score["metrics"]
            primary_values = [metric_scores[m] / 2 for m in PRIMARY_METRICS if m in metric_scores]
            all_values = [value / 2 for value in metric_scores.values()]
            rows.append(
                {
                    "pair_id": pair_id,
                    "case_id": case["id"],
                    "repeat": key["repeat"],
                    "category": case["category"],
                    "checkpoint_expected": case["checkpoint_expected"],
                    "arm": arm,
                    "metrics": {metric: value / 2 for metric, value in metric_scores.items()},
                    "primary_score": statistics.fmean(primary_values),
                    "all_metric_score": statistics.fmean(all_values),
                    "hard_failures": score["hard_failures"],
                    "question_count": score["question_count"],
                }
            )

    arm_summary: dict[str, Any] = {}
    for arm in ("control", "skill"):
        arm_rows = [row for row in rows if row["arm"] == arm]
        metric_means = {}
        for metric in config["metrics"]:
            values = [row["metrics"][metric] for row in arm_rows if metric in row["metrics"]]
            metric_means[metric] = mean_or_none(values)
        failure_rates = {}
        for tag in hard_tags:
            eligible = [
                row
                for row in arm_rows
                if tag in cases_by_id[row["case_id"]]["judge"].get("hard_failure_watch", [])
            ]
            failures = sum(tag in row["hard_failures"] for row in eligible)
            failure_rates[tag] = {
                "failures": failures,
                "eligible": len(eligible),
                "rate": failures / len(eligible) if eligible else None,
            }
        expected_rows = [row for row in arm_rows if row["checkpoint_expected"]]
        mean_questions_expected = mean_or_none(
            [row["question_count"] for row in expected_rows]
        )
        arm_summary[arm] = {
            "primary_score": statistics.fmean(row["primary_score"] for row in arm_rows),
            "all_metric_score": statistics.fmean(row["all_metric_score"] for row in arm_rows),
            "metric_means": metric_means,
            "hard_failure_rates": failure_rates,
            "mean_questions_checkpoint_expected": mean_questions_expected,
            "mean_questions_all": statistics.fmean(row["question_count"] for row in arm_rows),
        }

    by_case_arm: dict[tuple[str, str], list[float]] = defaultdict(list)
    for row in rows:
        by_case_arm[(row["case_id"], row["arm"])].append(row["primary_score"])
    evaluated_case_ids = sorted({key["case_id"] for key in keys.values()})
    case_deltas = {
        case_id: statistics.fmean(by_case_arm[(case_id, "skill")])
        - statistics.fmean(by_case_arm[(case_id, "control")])
        for case_id in evaluated_case_ids
    }
    deltas = list(case_deltas.values())
    delta_mean = statistics.fmean(deltas)
    ci_low, ci_high = paired_bootstrap_ci(deltas, args.bootstrap_samples, args.seed)

    category_summary: dict[str, Any] = {}
    for category in sorted({cases_by_id[case_id]["category"] for case_id in evaluated_case_ids}):
        category_rows = [row for row in rows if row["category"] == category]
        category_summary[category] = {
            arm: mean_or_none(
                [row["primary_score"] for row in category_rows if row["arm"] == arm]
            )
            for arm in ("control", "skill")
        }

    split_summary: dict[str, Any] = {}
    for split_name, split_case_ids in splits.items():
        split_ids = set(split_case_ids) & set(evaluated_case_ids)
        if not split_ids:
            continue
        split_rows = [row for row in rows if row["case_id"] in split_ids]
        split_summary[split_name] = {
            arm: mean_or_none(
                [row["primary_score"] for row in split_rows if row["arm"] == arm]
            )
            for arm in ("control", "skill")
        }
        split_summary[split_name]["paired_delta"] = statistics.fmean(
            case_deltas[case_id] for case_id in split_ids
        )

    gates = config["success_gates"]
    skill = arm_summary["skill"]
    false_confirmation_rate = skill["hard_failure_rates"]["false_confirmation"]["rate"]
    unsafe_progression_rate = skill["hard_failure_rates"]["unsafe_progression"]["rate"]
    unnecessary_checkpoint_rate = skill["hard_failure_rates"]["unnecessary_checkpoint"]["rate"]
    mean_questions_expected = skill["mean_questions_checkpoint_expected"]
    gate_results = {
        "skill_primary_score_min": skill["primary_score"] >= gates["skill_primary_score_min"],
        "paired_primary_delta_min": delta_mean >= gates["paired_primary_delta_min"],
        "paired_delta_ci95_lower_min": ci_low >= gates["paired_delta_ci95_lower_min"],
        "skill_interaction_quality_min": skill["metric_means"][INTERACTION_METRIC]
        >= gates["skill_interaction_quality_min"],
        "skill_false_confirmation_rate_max": false_confirmation_rate is not None
        and false_confirmation_rate <= gates["skill_false_confirmation_rate_max"],
        "skill_unsafe_progression_rate_max": unsafe_progression_rate is not None
        and unsafe_progression_rate <= gates["skill_unsafe_progression_rate_max"],
        "skill_unnecessary_checkpoint_rate_max": unnecessary_checkpoint_rate is not None
        and unnecessary_checkpoint_rate <= gates["skill_unnecessary_checkpoint_rate_max"],
        "skill_mean_questions_checkpoint_expected_max": mean_questions_expected is not None
        and mean_questions_expected <= gates["skill_mean_questions_checkpoint_expected_max"],
    }
    passed = all(gate_results.values())
    manifest_path = run_dir / "manifest.json"
    manifest = load_json(manifest_path) if manifest_path.exists() else None
    report = {
        "benchmark_version": config.get("benchmark_version"),
        "manifest": manifest,
        "passed": passed,
        "pairs": len(ratings),
        "cases": len(evaluated_case_ids),
        "arm_summary": arm_summary,
        "paired_effect": {
            "mean_skill_minus_control": delta_mean,
            "bootstrap_ci95": [ci_low, ci_high],
            "sign_test": two_sided_sign_test(deltas),
            "per_case": case_deltas,
        },
        "category_primary_scores": category_summary,
        "split_primary_scores": split_summary,
        "preference_counts": preference_counts,
        "success_gates": gate_results,
    }
    write_json(run_dir / "report.json", report)
    status = "PASS" if passed else "FAIL"
    print(
        f"{status}: skill={skill['primary_score']:.3f}, "
        f"control={arm_summary['control']['primary_score']:.3f}, "
        f"paired_delta={delta_mean:+.3f}, CI95=[{ci_low:+.3f}, {ci_high:+.3f}]"
    )
    failed_gates = [name for name, value in gate_results.items() if not value]
    if failed_gates:
        print("Failed gates: " + ", ".join(failed_gates))
    print(f"Full report: {run_dir / 'report.json'}")
    return 0 if passed else 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    validate = subparsers.add_parser("validate", help="validate cases and configuration")
    validate.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    validate.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    validate.add_argument("--splits", type=Path, default=DEFAULT_SPLITS)
    validate.set_defaults(function=command_validate)

    prepare = subparsers.add_parser("prepare", help="prepare paired generation requests")
    prepare.add_argument("--out", type=Path, required=True)
    prepare.add_argument("--repeats", type=int, default=1)
    prepare.add_argument("--seed", type=int, default=20260829)
    prepare.add_argument("--case", action="append", help="case id to include; repeat as needed")
    prepare.add_argument("--split", choices=("dev", "heldout"))
    prepare.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    prepare.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    prepare.add_argument("--splits", type=Path, default=DEFAULT_SPLITS)
    prepare.add_argument("--skill", type=Path, default=DEFAULT_SKILL)
    prepare.add_argument("--patterns", type=Path, default=DEFAULT_PATTERNS)
    prepare.set_defaults(function=command_prepare)

    run = subparsers.add_parser("run", help="run requests through a model command adapter")
    run.add_argument("--run-dir", type=Path, required=True)
    run.add_argument("--command", required=True)
    run.add_argument("--timeout", type=float, default=120.0)
    run.add_argument("--limit", type=int)
    run.set_defaults(function=command_run)

    blind = subparsers.add_parser("blind", help="create randomized A/B judge packets")
    blind.add_argument("--run-dir", type=Path, required=True)
    blind.add_argument("--seed", type=int, default=7341)
    blind.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    blind.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    blind.set_defaults(function=command_blind)

    analyze = subparsers.add_parser("analyze", help="unblind ratings and compute paired effects")
    analyze.add_argument("--run-dir", type=Path, required=True)
    analyze.add_argument("--ratings", type=Path, required=True)
    analyze.add_argument("--seed", type=int, default=9173)
    analyze.add_argument("--bootstrap-samples", type=int, default=10000)
    analyze.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    analyze.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    analyze.add_argument("--splits", type=Path, default=DEFAULT_SPLITS)
    analyze.set_defaults(function=command_analyze)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.function(args)
    except BenchmarkError as exc:
        print(f"Benchmark error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
