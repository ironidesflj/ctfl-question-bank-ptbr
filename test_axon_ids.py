import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import verify_axon_ids


class AxonIdGuardTests(unittest.TestCase):
    def copy_inputs(self, root):
        (root / "axon").mkdir()
        paths = ["synapse-question-bank.json"]
        for exam in ("ctfl", "ctal-ta", "ctal-tm"):
            paths.extend(
                [
                    f"axon/{exam}-public-ids.json",
                    f"axon/{exam}-reference-candidates.json",
                ]
            )
        for path in paths:
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

    def test_corrected_questions_keep_answer_identity_and_publishable_references(self):
        expected = {
            "ch1-40": 3, "ch2-18": 2, "ch4-70": 0, "ch4-81": 3,
            "ctalta-194": 1, "ctalta-196": 3, "ctalta-200": 1, "ctaltm-125": 0,
        }
        bank = json.loads((verify_axon_ids.ROOT / "synapse-question-bank.json").read_text())
        questions = {question["id"]: question for question in bank["questions"]}
        references = {
            record["internalId"]: record
            for exam in ("ctfl", "ctal-ta", "ctal-tm")
            for record in json.loads(
                (verify_axon_ids.ROOT / f"axon/{exam}-reference-candidates.json").read_text()
            )["records"]
        }
        for question_id, answer in expected.items():
            with self.subTest(question_id=question_id):
                question = questions[question_id]
                self.assertEqual(question["pool"], "study")
                self.assertEqual(question["answer"], answer)
                self.assertEqual(references[question_id]["state"], "candidate")
                self.assertTrue(references[question_id]["reference"])
                for lang in ("pt", "en"):
                    self.assertEqual(len(question["locales"][lang]["options"]), 4)
        for question_id in ("ch4-70", "ch4-81"):
            self.assertIn("complementar", questions[question_id]["locales"]["pt"]["q"].lower())
            self.assertIn("supplementary", questions[question_id]["locales"]["en"]["q"].lower())

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
