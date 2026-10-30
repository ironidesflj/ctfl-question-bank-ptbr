import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import verify_axon_ids


class AxonIdGuardTests(unittest.TestCase):
    def test_rejects_exam_question_in_public_ledger(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "axon").mkdir()
            ledger = json.loads((verify_axon_ids.ROOT / "axon/ctfl-public-ids.json").read_text())
            bank = json.loads((verify_axon_ids.ROOT / "synapse-question-bank.json").read_text())
            exam_id = next(q["id"] for q in bank["questions"] if q["cert"] == "CTFL" and q["pool"] == "exam")
            ledger["mappings"][0]["internalId"] = exam_id
            (root / "axon/ctfl-public-ids.json").write_text(json.dumps(ledger))
            (root / "synapse-question-bank.json").write_text(json.dumps(bank))
            with patch.object(verify_axon_ids, "ROOT", root):
                with self.assertRaisesRegex(ValueError, "outside the CTFL study pool"):
                    verify_axon_ids.verify()


if __name__ == "__main__":
    unittest.main()
