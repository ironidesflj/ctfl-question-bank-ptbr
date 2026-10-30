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
    references = json.loads((ROOT / "axon/ctfl-reference-candidates.json").read_text())
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
    ref_records = references["records"]
    if not mappings or ledger["lastIssued"] != len(mappings):
        raise ValueError("lastIssued must equal the number of reserved IDs")
    if len(ref_records) != len(mappings):
        raise ValueError("Every reserved ID must have an explicit reference review state")
    ref_by_id = {item["publicId"]: item for item in ref_records}
    if len(ref_by_id) != len(ref_records):
        raise ValueError("Duplicate public ID in reference review")

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

        review = ref_by_id.get(public_id)
        if not review or review.get("internalId") != internal_id:
            raise ValueError(f"{public_id} has no matching reference review")
        if review.get("state") == "candidate":
            url = review.get("reference", "")
            official_hosts = (
                "https://istqb.org/",
                "https://www.istqb.org/",
                "https://glossary.istqb.org/",
            )
            if not url.startswith(official_hosts) or not review.get("referenceTitle"):
                raise ValueError(f"{public_id} candidate has no official reference")
        elif review.get("state") == "held":
            if review.get("reference") is not None or review.get("referenceTitle") is not None:
                raise ValueError(f"{public_id} is held but contains a publishable reference")
        else:
            raise ValueError(f"{public_id} has an invalid review state")

    print(f"Validated {len(mappings)} CTFL study IDs; no exam question included")


if __name__ == "__main__":
    try:
        if sys.argv[1:] not in ([], ["--against-parent"]):
            raise ValueError("Usage: verify_axon_ids.py [--against-parent]")
        verify(against_parent="--against-parent" in sys.argv[1:])
    except (KeyError, TypeError, ValueError) as exc:
        print(f"Axon ID validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
