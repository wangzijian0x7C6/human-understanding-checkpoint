import json
import sys
import tempfile
import unittest
from pathlib import Path


BENCHMARK_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BENCHMARK_DIR))

import benchmark as bench  # noqa: E402


class BenchmarkHarnessTests(unittest.TestCase):
    def test_real_suite_is_valid(self):
        cases = bench.load_jsonl(bench.DEFAULT_CASES)
        config = bench.load_json(bench.DEFAULT_CONFIG)
        bench.validate_suite(cases, config)
        self.assertGreaterEqual(len(cases), 20)
        self.assertTrue(any(case["checkpoint_expected"] for case in cases))
        self.assertTrue(any(not case["checkpoint_expected"] for case in cases))

    def test_prepare_creates_paired_arms_without_judge_leakage(self):
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = Path(temporary) / "run"
            result = bench.main(["prepare", "--out", str(run_dir), "--repeats", "2", "--seed", "7"])
            self.assertEqual(result, 0)
            cases = bench.load_jsonl(bench.DEFAULT_CASES)
            requests = bench.load_jsonl(run_dir / "requests.jsonl")
            self.assertEqual(len(requests), len(cases) * 4)
            grouped = {}
            for request in requests:
                grouped.setdefault((request["case_id"], request["repeat"]), set()).add(request["arm"])
                self.assertNotIn("judge", request)
            self.assertTrue(all(arms == {"control", "skill"} for arms in grouped.values()))
            control = next(record for record in requests if record["arm"] == "control")
            skill = next(record for record in requests if record["arm"] == "skill")
            self.assertNotIn("# Human Understanding Checkpoint", control["system_prompt"])
            self.assertIn("# Human Understanding Checkpoint", skill["system_prompt"])

    def test_blind_and_analyze_full_synthetic_run(self):
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = Path(temporary) / "run"
            self.assertEqual(bench.main(["prepare", "--out", str(run_dir), "--seed", "11"]), 0)
            requests = bench.load_jsonl(run_dir / "requests.jsonl")
            responses = [
                {
                    "request_id": request["request_id"],
                    "case_id": request["case_id"],
                    "repeat": request["repeat"],
                    "response": f"synthetic {request['arm']} response",
                    "error": None,
                    "latency_ms": 1,
                }
                for request in requests
            ]
            bench.write_jsonl(run_dir / "responses.jsonl", responses)
            self.assertEqual(bench.main(["blind", "--run-dir", str(run_dir), "--seed", "13"]), 0)

            packets = {record["pair_id"]: record for record in bench.load_jsonl(run_dir / "judge_packet.jsonl")}
            keys = {record["pair_id"]: record for record in bench.load_jsonl(run_dir / "blind_key.jsonl")}
            templates = bench.load_jsonl(run_dir / "ratings_template.jsonl")
            self.assertEqual(set(packets), set(keys))
            self.assertTrue(all("arm" not in json.dumps(packet) for packet in packets.values()))

            ratings = []
            for template in templates:
                pair_id = template["pair_id"]
                key = keys[pair_id]
                packet = packets[pair_id]
                skill_label = next(label for label, arm in key["labels"].items() if arm == "skill")
                control_label = "B" if skill_label == "A" else "A"
                for label, value in ((skill_label, 2), (control_label, 0)):
                    template["scores"][label]["metrics"] = {
                        metric: value for metric in packet["applicable_metrics"]
                    }
                    template["scores"][label]["hard_failures"] = []
                    template["scores"][label]["question_count"] = (
                        1 if label == skill_label and packet["checkpoint_expected"] else 0
                    )
                template["preference"] = skill_label
                ratings.append(template)
            ratings_path = run_dir / "ratings.jsonl"
            bench.write_jsonl(ratings_path, ratings)
            result = bench.main(
                [
                    "analyze",
                    "--run-dir",
                    str(run_dir),
                    "--ratings",
                    str(ratings_path),
                    "--bootstrap-samples",
                    "500",
                    "--seed",
                    "17",
                ]
            )
            self.assertEqual(result, 0)
            report = bench.load_json(run_dir / "report.json")
            self.assertTrue(report["passed"])
            self.assertEqual(report["arm_summary"]["skill"]["primary_score"], 1.0)
            self.assertEqual(report["arm_summary"]["control"]["primary_score"], 0.0)
            self.assertEqual(report["paired_effect"]["mean_skill_minus_control"], 1.0)

    def test_adapter_output_contract(self):
        self.assertEqual(bench.parse_adapter_output("plain text"), "plain text")
        self.assertEqual(bench.parse_adapter_output('{"response":"hello"}'), "hello")
        with self.assertRaises(bench.BenchmarkError):
            bench.parse_adapter_output('{"text":"wrong field"}')


if __name__ == "__main__":
    unittest.main()
