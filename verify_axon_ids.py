"""Validate the reserved Synapse public IDs against the canonical bank.

This does not publish a manifest or alter the question IDs used for progress.
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def verify_append_only(previous: dict, current: dict) -> None:
    old = previous["mappings"]
    if current["mappings"][: len(old)] != old or current["lastIssued"] < previous["lastIssued"]:
        raise ValueError("Published Axon ID mappings must be append-only")


def verify(against_parent: bool = False) -> None:
    ledger = json.loads((ROOT / "axon/ctfl-public-ids.json").read_text())
    if against_parent:
        result = subprocess.run(
            ["git", "show", "HEAD^:axon/ctfl-public-ids.json"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode:
            raise ValueError(f"Cannot read previous Axon ID ledger: {result.stderr.strip()}")
        verify_append_only(json.loads(result.stdout), ledger)
    bank = json.loads((ROOT / "synapse-question-bank.json").read_text())
    questions = {q["id"]: q for q in bank["questions"]}
    if len(questions) != len(bank["questions"]):
        raise ValueError("Duplicate internal question ID in canonical bank")

    if ledger["exam"] != "ctfl" or ledger["lang"] != "pt-BR":
        raise ValueError("Unexpected exam or canonical language")

    mappings = ledger["mappings"]
    if not mappings or ledger["lastIssued"] != len(mappings):
        raise ValueError("lastIssued must equal the number of reserved IDs")

    seen_internal = set()
    seen_public = set()
    for sequence, mapping in enumerate(mappings, start=1):
        internal_id = mapping["internalId"]
        public_id = mapping["publicId"]
        expected = f"SYN-CTFL-{sequence:05d}"
        if public_id != expected:
            raise ValueError(f"Unexpected public ID {public_id}; expected {expected}")
        if internal_id in seen_internal or public_id in seen_public:
            raise ValueError(f"Duplicate mapping: {mapping}")
        seen_internal.add(internal_id)
        seen_public.add(public_id)

        question = questions.get(internal_id)
        if not question or question.get("cert") != "CTFL" or question.get("pool") != "study":
            raise ValueError(f"{internal_id} is missing or outside the CTFL study pool")
        if not question.get("locales", {}).get("pt", {}).get("q"):
            raise ValueError(f"{internal_id} has no Portuguese statement")
        options = question["locales"]["pt"].get("options")
        if not isinstance(options, list) or len(options) < 2 or not all(
            isinstance(option, str) and option.strip() for option in options
        ):
            raise ValueError(f"{internal_id} has invalid Portuguese options")
        answer = question.get("answer")
        if type(answer) is not int or not 0 <= answer < len(options):
            raise ValueError(f"{internal_id} has invalid zero-based answer index")

    print(f"Validated {len(mappings)} CTFL study IDs; no exam question included")


if __name__ == "__main__":
    try:
        if sys.argv[1:] not in ([], ["--against-parent"]):
            raise ValueError("Usage: verify_axon_ids.py [--against-parent]")
        verify(against_parent="--against-parent" in sys.argv[1:])
    except (KeyError, TypeError, ValueError) as exc:
        print(f"Axon ID validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
