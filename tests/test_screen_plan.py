import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/screen_plan.py"
spec = importlib.util.spec_from_file_location("screen_plan", SCRIPT)
s = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s)


def packet():
    text = "quote and bundle both call _unit; _unit caches by sku while provider reads sku and tier."
    return {"id": "unit-case", "contract": "Prices depend on SKU and tier. Cache each pair once.",
            "plan": "Clear the quote cache; test the reported quote sequence.",
            "plan_refs": ["source"], "evidence": [{"id": "source", "origin": "synthetic source inspection",
            "text": text, "sha256": hashlib.sha256(text.encode()).hexdigest()}]}


def response(choice="supported"):
    return {"model": "fixture-only", "usage": {"input_tokens": 12, "output_tokens": 8},
            "answers": {key: {"type": "choice", "choice": choice, "confidence": 1.0,
            "probabilities": {label: float(label == choice) for label in s.CRITERIA}} for key in s.FOCI}}


def replay(p, r):
    return s.screen(p, "test-model", "replay", {"request_sha256": s.digest(s.request_for(p, "test-model")), "response": r})


class ScreeningTests(unittest.TestCase):
    def test_prepare_does_not_call_provider(self):
        with patch.object(s, "call_api", side_effect=AssertionError("network forbidden")):
            result = s.screen(packet(), "test-model")
        self.assertEqual(result["status"], "prepared_not_evaluated")
        self.assertNotIn("response", result)

    def test_missing_credentials_do_not_call_provider(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(s, "call_api") as call:
            result = s.screen(packet(), "test-model", "live")
        call.assert_not_called()
        self.assertEqual(result["error"], "missing_TYPESAFE_API_KEY")
        self.assertTrue(result["review_required"])

    def test_high_confidence_never_approves(self):
        result = replay(packet(), response())
        self.assertEqual(result["status"], "advisory_only")
        self.assertFalse(result["approval_granted"])
        self.assertTrue(result["review_required"])

    def test_empty_evidence_cannot_be_hidden_by_supported_label(self):
        p = packet()
        p.update(evidence=[], plan_refs=[])
        result = replay(p, response())
        self.assertEqual(result["mechanical_flags"], ["no_evidence", "no_plan_references"])
        self.assertTrue(result["review_required"])

    def test_gap_and_unknown_remain_visible(self):
        for label in ("gap", "unknown"):
            with self.subTest(label=label):
                self.assertEqual(set(replay(packet(), response(label))["attention"]), set(s.FOCI))

    def test_not_applicable_requires_reviewer(self):
        result = replay(packet(), response("not_applicable"))
        self.assertEqual(set(result["not_applicable_needs_review"]), set(s.FOCI))
        self.assertFalse(result["approval_granted"])

    def test_corrupt_or_missing_answers_unavailable(self):
        mutations = [lambda r: r["answers"].pop("scope"),
                     lambda r: r["answers"]["scope"].update(choice="approved"),
                     lambda r: r["answers"]["scope"].update(confidence=float("nan")),
                     lambda r: r["answers"]["scope"].update(confidence=10**400),
                     lambda r: r["answers"]["scope"]["probabilities"].update(gap=True),
                     lambda r: r["answers"]["scope"]["probabilities"].update(gap=0.7),
                     lambda r: r["answers"]["scope"].update(choice="gap"),
                     lambda r: r["usage"].update(input_tokens=-1)]
        for index, mutate in enumerate(mutations):
            with self.subTest(index=index):
                r = response()
                mutate(r)
                result = replay(packet(), r)
                self.assertEqual(result["status"], "unavailable")
                self.assertNotIn("response", result)

    def test_evidence_tampering_and_unresolved_refs_stop_request(self):
        for mutate in (lambda p: p["evidence"][0].update(text="changed"),
                       lambda p: p["plan_refs"].append("missing"),
                       lambda p: p["evidence"].append(copy.deepcopy(p["evidence"][0]))):
            p = packet()
            mutate(p)
            with self.assertRaises(ValueError):
                s.request_for(p, "test-model")

    def test_labels_cannot_enter_request(self):
        p = packet()
        p["expected"] = {"scope": "supported"}
        with self.assertRaises(ValueError):
            s.request_for(p, "test-model")

    def test_stale_replay_rejected(self):
        p = packet()
        fixture = {"request_sha256": s.digest(s.request_for(p, "test-model")), "response": response()}
        p["plan"] = "A different plan"
        result = s.screen(p, "test-model", "replay", fixture)
        self.assertEqual(result["status"], "unavailable")

    def test_error_body_does_not_expose_secret_or_retry(self):
        with patch.dict(os.environ, {"TYPESAFE_API_KEY": "test-secret-only"}), \
             patch.object(s, "call_api", side_effect=OSError("test-secret-only")) as call:
            result = s.screen(packet(), "test-model", "live")
        self.assertEqual(call.call_count, 1)
        self.assertNotIn("test-secret-only", json.dumps(result))
        self.assertEqual(result["status"], "unavailable")

    def test_documented_wire_response_through_mock_transport(self):
        with patch.dict(os.environ, {"TYPESAFE_API_KEY": "test-secret-only"}), \
             patch.object(s, "call_api", return_value=response("gap")) as call:
            result = s.screen(packet(), "test-model", "live")
        self.assertEqual(call.call_count, 1)
        sent, key = call.call_args.args
        self.assertEqual(set(sent), {"model", "state", "questions"})
        self.assertEqual(sent["state"], packet())
        self.assertEqual(key, "test-secret-only")
        self.assertEqual(result["status"], "advisory_only")

    def test_duplicate_and_nonfinite_json_rejected(self):
        for raw in ('{"x":1,"x":2}', '{"x":NaN}'):
            with self.assertRaises(ValueError):
                s.strict_json(raw)

    def test_redirect_is_not_followed(self):
        self.assertIsNone(s.NoRedirect().redirect_request(None, None, 307, "", {}, "https://example.com"))

    def test_cli_output_is_new_and_prepare_is_default(self):
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory)
            (p / "packet.json").write_text(json.dumps(packet()))
            argv = [sys.executable, "-B", str(SCRIPT), str(p / "packet.json"),
                    "--model", "test-model", "--out", str(p / "result.json")]
            first = subprocess.run(argv, capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            raw = (p / "result.json").read_bytes()
            self.assertEqual(json.loads(raw)["status"], "prepared_not_evaluated")
            second = subprocess.run(argv, capture_output=True, text=True)
            self.assertNotEqual(second.returncode, 0)
            self.assertEqual((p / "result.json").read_bytes(), raw)


if __name__ == "__main__":
    unittest.main()
