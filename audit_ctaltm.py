"""Generate a reproducible triage report, never edit questions or baselines."""
import argparse
import hashlib
import json
from pathlib import Path

from check_alignment import (
    HEDGE_WORDS_EN, HEDGE_WORDS_PT, _has_hedge,
    NEW_GUARD_REGISTRY, _GUARD_FUNCS,
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bank", type=Path, default=Path(__file__).with_name("synapse-question-bank.json"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    bank = json.loads(args.bank.read_text())
    questions = [q for q in bank["questions"] if q.get("cert") == "CTAL-TM"]
    rows = []
    batch = json.loads(Path(__file__).with_name('editorial').joinpath('ctaltm-batch-01.json').read_text())
    for q in questions:
        locales = {}
        for lang, words in (("pt", HEDGE_WORDS_PT), ("en", HEDGE_WORDS_EN)):
            options = q["locales"][lang]["options"]
            lengths = [len(option) for option in options]
            locales[lang] = {
                "option_lengths": lengths,
                "pick_longest_hits_answer": lengths.index(max(lengths)) == q["answer"],
                "correct_has_absolute_qualifier": _has_hedge(options[q["answer"]], words),
                "distractors_with_absolute_qualifier": [i for i, option in enumerate(options) if i != q["answer"] and _has_hedge(option, words)],
            }
        status = 'PENDING_REVIEW'
        if q['id'] in batch['updates']:
            status = 'REVISED_AWAITING_SECOND_REVIEW'
        elif q['id'] in batch['reviewed_unchanged']:
            status = 'READ_AWAITING_SECOND_REVIEW'
        rows.append({"id": q["id"], "chapter": q["chapter"], "kLevel": q["kLevel"], "pool": q["pool"],
                     "answer": q["answer"], "editorial_status": status, "locales": locales})
    report = {
        "bank_version": bank["meta"]["version"],
        "bank_sha256": hashlib.sha256(args.bank.read_bytes()).hexdigest(),
        "scope": "CTAL-TM triage; flags are not semantic verdicts",
        "count": len(rows),
        "guards": {},
        "questions": rows,
    }
    for name, _, _ in NEW_GUARD_REGISTRY:
        passed, lines = _GUARD_FUNCS[name](args.bank)
        report["guards"][name] = {"passed_for_live_certs": passed, "evidence": lines}
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(f"Triage saved: {len(rows)} questions; semantic review is still pending")


if __name__ == "__main__":
    main()
