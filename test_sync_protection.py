import copy
import json
import tempfile
import unittest
import subprocess
import sys
from pathlib import Path

from check_alignment import LIVE_CERTS, guard_length_bias, guard_runs_test
from verify_sync import validate


class SyncProtectionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source, self.app = self.root / "bank", self.root / "app"
        self.source.mkdir()
        (self.app / "src/data/banks").mkdir(parents=True)
        self.live = sorted(cert.lower() for cert in LIVE_CERTS)
        self.bank = {
            "meta": {"version": "1.6.0-ctaltm", **{k: {c: {} for c in self.live} for k in ("examFormat", "examBlueprint", "chapterWeights")}},
            "questions": [{"id": c, "cert": c.upper(), "answer": 0} for c in self.live],
        }
        (self.app / "src/certs.js").write_text(f"export const VALID_CERTS = {json.dumps(self.live)};")
        for name in ("synapse-question-bank.json", "ctfl-questions-ptbr.json"):
            self.write(self.source / name, self.bank)
            self.write(self.app / "src/data" / name, self.bank)
        for cert in self.live:
            self.write(self.app / "src/data/banks" / f"{cert}.json", {"meta": self.bank["meta"], "questions": [q for q in self.bank["questions"] if q["id"] == cert]})

    def write(self, path, obj):
        path.write_text(json.dumps(obj))

    def test_identical_banks_and_slices_pass(self):
        validate(self.source, self.app)
        validate(self.source, self.app, True)

    def test_downgrade_is_blocked_before_copy(self):
        self.bank["meta"]["version"] = "1.5.0-pools"
        self.write(self.source / "synapse-question-bank.json", self.bank)
        with self.assertRaisesRegex(ValueError, "Downgrade"):
            validate(self.source, self.app, True)

    def test_same_version_divergence_is_blocked(self):
        self.bank["questions"][0]["answer"] = 1
        self.write(self.source / "synapse-question-bank.json", self.bank)
        with self.assertRaisesRegex(ValueError, "same version"):
            validate(self.source, self.app, True)

    def test_checksum_mismatch_is_blocked(self):
        (self.app / "src/data/ctfl-questions-ptbr.json").write_text('{}')
        with self.assertRaisesRegex(ValueError, "checksum"):
            validate(self.source, self.app)

    def test_modified_slice_with_same_ids_is_blocked(self):
        path = self.app / "src/data/banks/ctfl.json"
        obj = json.loads(path.read_text())
        obj["questions"][0]["answer"] = 2
        self.write(path, obj)
        with self.assertRaisesRegex(ValueError, "slice"):
            validate(self.source, self.app)

    def test_missing_live_guard_is_blocked(self):
        (self.app / "src/certs.js").write_text('export const VALID_CERTS = ["ctfl", "ctal-ta"];')
        with self.assertRaisesRegex(ValueError, "LIVE_CERTS"):
            validate(self.source, self.app)

    def test_missing_blueprint_is_blocked(self):
        del self.bank["meta"]["examBlueprint"]["ctal-tm"]
        self.write(self.source / "synapse-question-bank.json", self.bank)
        with self.assertRaisesRegex(ValueError, "examBlueprint"):
            validate(self.source, self.app, True)

    def test_question_removal_requires_migration(self):
        self.bank["meta"]["version"] = "1.6.1"
        self.bank["questions"].pop()
        self.write(self.source / "synapse-question-bank.json", self.bank)
        with self.assertRaisesRegex(ValueError, "removal"):
            validate(self.source, self.app, True)

    def test_ctaltm_quality_debt_is_blocking(self):
        self.assertIn("CTAL-TM", LIVE_CERTS)
        bank = copy.deepcopy(self.bank)
        bank["questions"] = [
            {"id": f"tm-{i}", "cert": "CTAL-TM", "answer": i % 4 if i < 100 else (i - 100) // 50,
             "locales": {lang: {"options": ["long correct answer " * 10 if j == (i % 4 if i < 100 else (i - 100) // 50) else "short" for j in range(4)]} for lang in ("pt", "en")}}
            for i in range(200)
        ]
        path = self.source / "bad.json"
        self.write(path, bank)
        self.assertFalse(guard_length_bias(path)[0])
        self.assertFalse(guard_runs_test(path)[0])

    def test_sync_quality_gate_runs_before_copy_and_pr(self):
        workflow = (Path(__file__).parent / ".github/workflows/sync-app.yml").read_text()
        self.assertLess(workflow.index("Block sync on canonical quality failures"), workflow.index("Copy canonical files"))
        self.assertLess(workflow.index("Enforce checksums"), workflow.index("Open reviewed sync PR"))
        self.assertNotIn("|| true", workflow)
        self.assertNotIn("continue-on-error", workflow)

    def test_absolute_bank_path_reuses_baselines(self):
        root = Path(__file__).parent
        result = subprocess.run([sys.executable, str(root / "check_alignment.py"), "--bank-file", str(root / "synapse-question-bank.json"), "--threshold", "0"], capture_output=True, text=True)
        self.assertIn("existing guards: PASS", result.stdout)


if __name__ == "__main__":
    unittest.main()
