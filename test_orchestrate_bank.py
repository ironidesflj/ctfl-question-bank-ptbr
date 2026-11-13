import json
import tempfile
import unittest
from pathlib import Path

import orchestrate_bank


def make_question(qid="ch1-999", cert="CTFL", chapter=1, domain="fund", pool="study"):
    return {
        "id": qid,
        "cert": cert,
        "chapter": chapter,
        "domain": domain,
        "kLevel": 2,
        "lo": "FL-1.1.1",
        "answer": 1,
        "pool": pool,
        "locales": {
            "pt": {
                "q": "Qual afirmativa descreve corretamente um princípio fundamental de teste de software?",
                "options": [
                    "Testar prova ausência total de defeitos em produção.",
                    "Testar demonstra presença de defeitos, não sua ausência.",
                    "Teste exaustivo é viável em qualquer sistema comercial.",
                    "Depuração e teste são exatamente a mesma atividade.",
                ],
                "exp": "O primeiro princípio afirma que testar mostra presença de defeitos, enquanto provas de ausência são inviáveis.",
            },
            "en": {
                "q": "Which statement accurately describes a fundamental principle of software testing?",
                "options": [
                    "Testing proves complete absence of defects in production.",
                    "Testing shows the presence of defects, not their absence.",
                    "Exhaustive testing is feasible in any commercial system.",
                    "Debugging and testing are the exact same activity.",
                ],
                "exp": "The first principle states that testing shows the presence of defects rather than proving their absence.",
            },
        },
    }


class OrchestrateBankTests(unittest.TestCase):
    def test_rejects_duplicate_id_on_add(self):
        q = make_question(qid="ch1-01")
        fails, _ = orchestrate_bank.check_question_schema_and_editorial(
            q, expected_existing=False, known_ids={"ch1-01"}, bank_stems=[]
        )
        self.assertTrue(any(f["gate"] == "IDENTITY" for f in fails))

    def test_rejects_letter_leak_and_all_none_options(self):
        q = make_question(qid="ch1-998")
        q["locales"]["pt"]["exp"] += " Portanto, a opção B está correta."
        q["locales"]["en"]["options"][3] = "All of the above"
        fails, _ = orchestrate_bank.check_question_schema_and_editorial(
            q, expected_existing=False, known_ids=set(), bank_stems=[]
        )
        gates = {f["gate"] for f in fails}
        self.assertIn("ANTI_LEAK", gates)
        self.assertIn("OPTION_RULE", gates)

    def test_allows_parenthesized_prose_enumeration(self):
        q = make_question(qid="aitest-152")
        q["cert"] = "CT-AI"
        q["chapter"] = 1
        q["domain"] = "ai"
        q["locales"]["en"]["exp"] = (
            "Release is blocked because (a) OOV is untested; (b) safety fails; and (c) fairness fails."
        )
        fails, _ = orchestrate_bank.check_question_schema_and_editorial(
            q, expected_existing=True, known_ids={"aitest-152"}, bank_stems=[]
        )
        self.assertEqual(fails, [])

    def test_bump_semver(self):
        self.assertEqual(orchestrate_bank.bump_semver("1.7.4", None), "1.8.0")
        self.assertEqual(orchestrate_bank.bump_semver("1.7.4", "2.0.0"), "2.0.0")
        with self.assertRaises(ValueError):
            orchestrate_bank.bump_semver("1.7.4", "invalid")

    def test_apply_is_fail_closed_when_validation_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            # Minimal repo stub
            (root / "axon").mkdir()
            bad_batch = root / "bad.json"
            bad_q = make_question(qid="ch1-01")
            bad_q["locales"]["pt"]["exp"] = "Escolha a alternativa A."
            bad_batch.write_text(json.dumps([bad_q]), encoding="utf-8")

            # Copy canonical scripts & banks
            repo_src = orchestrate_bank.ROOT
            for f in repo_src.glob("*.py"):
                (root / f.name).write_bytes(f.read_bytes())
            for f in repo_src.glob("*.json"):
                (root / f.name).write_bytes(f.read_bytes())
            for f in (repo_src / "axon").glob("*.json"):
                (root / "axon" / f.name).write_bytes(f.read_bytes())

            before = (root / "synapse-question-bank.json").read_bytes()
            rc = orchestrate_bank.main(["apply", str(bad_batch), "--repo", str(root)])
            after = (root / "synapse-question-bank.json").read_bytes()
            self.assertEqual(rc, 1)
            self.assertEqual(before, after)

    def test_pool_swap_updates_pool_split_and_rejects_cell_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "axon").mkdir()
            repo_src = orchestrate_bank.ROOT
            for f in repo_src.glob("*.py"):
                (root / f.name).write_bytes(f.read_bytes())
            for f in repo_src.glob("*.json"):
                (root / f.name).write_bytes(f.read_bytes())
            for f in (repo_src / "axon").glob("*.json"):
                (root / "axon" / f.name).write_bytes(f.read_bytes())

            syn = orchestrate_bank.read_json(root / "synapse-question-bank.json")
            ctfl_a = next(q for q in syn["questions"] if q["id"] == "ch1-96")
            ctfl_b = next(q for q in syn["questions"] if q["id"] == "ch1-76")
            orig_a_pool, orig_b_pool = ctfl_a["pool"], ctfl_b["pool"]
            self.assertEqual({orig_a_pool, orig_b_pool}, {"study", "exam"})

            res = orchestrate_bank.simulate_plan(
                root,
                {
                    "steps": [{"name": "swap", "mode": "pool_swap", "pool_swaps": [["ch1-96", "ch1-76"]]}],
                    "ctfl_target_version": "1.5.1",
                },
                target_version="1.8.1",
            )
            self.assertTrue(res["ok"])
            new_syn = res["_artifacts"]["synapse_bank"]
            new_ctfl = res["_artifacts"]["ctfl_bank"]
            self.assertEqual(next(q for q in new_syn["questions"] if q["id"] == "ch1-96")["pool"], orig_b_pool)
            self.assertEqual(next(q for q in new_syn["questions"] if q["id"] == "ch1-76")["pool"], orig_a_pool)
            self.assertEqual(next(q for q in new_ctfl["questions"] if q["id"] == "ch1-96")["pool"], orig_b_pool)
            self.assertEqual(new_syn["meta"]["poolSplit"]["perCert"]["ctfl"], {"exam": 158, "study": 342, "total": 500})
            self.assertIn("ct-ai", new_syn["meta"]["poolSplit"]["perCert"])

            bad = orchestrate_bank.simulate_plan(
                root,
                {"steps": [{"name": "bad-swap", "mode": "pool_swap", "pool_swaps": [["ch1-96", "ch5-81"]]}]},
                target_version="1.8.1",
            )
            self.assertFalse(bad["ok"])
            self.assertEqual(bad["fails"][0]["gate"], "POOL_SWAP")


if __name__ == "__main__":
    unittest.main()
