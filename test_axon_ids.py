import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import verify_axon_ids


class AxonIdGuardTests(unittest.TestCase):
    def copy_inputs(self, root):
        (root / "axon").mkdir()
        for path in ("axon/ctfl-public-ids.json", "axon/ctfl-reference-candidates.json", "synapse-question-bank.json"):
            (root / path).write_bytes((verify_axon_ids.ROOT / path).read_bytes())

    def test_published_id_cannot_be_remapped(self):
        previous = {"lastIssued": 1, "mappings": [{"internalId": "ch1-01", "publicId": "SYN-CTFL-00001"}]}
        current = {"lastIssued": 2, "mappings": [*previous["mappings"], {"internalId": "ch1-03", "publicId": "SYN-CTFL-00002"}]}
        verify_axon_ids.verify_append_only(previous, current)
        current["mappings"][0] = {"internalId": "ch1-04", "publicId": "SYN-CTFL-00001"}
        with self.assertRaisesRegex(ValueError, "append-only"):
            verify_axon_ids.verify_append_only(previous, current)

    def test_rejects_exam_question_in_public_ledger(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.copy_inputs(root)
            ledger = json.loads((verify_axon_ids.ROOT / "axon/ctfl-public-ids.json").read_text())
            bank = json.loads((verify_axon_ids.ROOT / "synapse-question-bank.json").read_text())
            exam_id = next(q["id"] for q in bank["questions"] if q["cert"] == "CTFL" and q["pool"] == "exam")
            ledger["mappings"][0]["internalId"] = exam_id
            (root / "axon/ctfl-public-ids.json").write_text(json.dumps(ledger))
            (root / "synapse-question-bank.json").write_text(json.dumps(bank))
            with patch.object(verify_axon_ids, "ROOT", root):
                with self.assertRaisesRegex(ValueError, "outside the CTFL study pool"):
                    verify_axon_ids.verify()

    def test_requires_reference_state_for_every_reserved_id(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.copy_inputs(root)
            path = root / "axon/ctfl-reference-candidates.json"
            references = json.loads(path.read_text())
            references["records"].pop()
            path.write_text(json.dumps(references))
            with patch.object(verify_axon_ids, "ROOT", root):
                with self.assertRaisesRegex(ValueError, "reference review state"):
                    verify_axon_ids.verify()


if __name__ == "__main__":
    unittest.main()
