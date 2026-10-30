"""Validate Axon public IDs and reference states against the canonical bank.

This does not publish a manifest or alter the question IDs used for progress.
Only study-pool questions for the active exams are eligible.
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXAMS = {
    "ctfl": ("CTFL", "CTFL", "SYN-CTFL-", 220),
    "ctal-ta": ("CTAL-TA", "CTALTA", "SYN-CTALTA-", 110),
    "ctal-tm": ("CTAL-TM", "CTALTM", "SYN-CTALTM-", 101),
}
APPROVED_REFERENCE_PREFIXES = (
    "https://istqb.org/",
    "https://www.istqb.org/",
    "https://glossary.istqb.org/",
    # Primary ODC source cited for the Trigger attribute; the syllabus cites ODC
    # but does not detail this specific attribute.
    "https://research.ibm.com/publications/orthogonal-defect-classificationa-concept-for-in-process-measurements",
    "https://asq.org/quality-progress/articles/fishbone-stories?id=5c9adae78e3242588621ab300378d40b",
)


def verify_append_only(previous: dict, current: dict) -> None:
    old = previous["mappings"]
    if current["mappings"][: len(old)] != old or current["lastIssued"] < previous["lastIssued"]:
        raise ValueError("Published Axon ID mappings must be append-only")
    if previous.get("exam") != current.get("exam") or previous.get("lang") != current.get("lang"):
        raise ValueError("Axon ID ledger identity cannot change")


def _read_parent_ledger(path: str, exam: str) -> dict:
    result = subprocess.run(
        ["git", "show", f"HEAD^:{path}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        return json.loads(result.stdout)

    exists = subprocess.run(
        ["git", "cat-file", "-e", f"HEAD^:{path}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if exists.returncode == 0:
        raise ValueError(f"Cannot read previous Axon ID ledger: {result.stderr.strip()}")
    return {"exam": exam, "lang": "pt-BR", "lastIssued": 0, "mappings": []}


def verify(against_parent: bool = False) -> None:
    bank = json.loads((ROOT / "synapse-question-bank.json").read_text())
    questions = {q["id"]: q for q in bank["questions"]}
    if len(questions) != len(bank["questions"]):
        raise ValueError("Duplicate internal question ID in canonical bank")

    seen_internal = set()
    seen_public = set()
    total = 0
    counts = {}

    for exam_slug, (cert, exam_code, prefix, expected_count) in EXAMS.items():
        ledger_path = f"axon/{exam_slug}-public-ids.json"
        references_path = ROOT / f"axon/{exam_slug}-reference-candidates.json"
        ledger = json.loads((ROOT / ledger_path).read_text())
        references = json.loads(references_path.read_text())

        if ledger["exam"] != exam_slug or ledger["lang"] != "pt-BR":
            raise ValueError(f"Unexpected exam or canonical language in {ledger_path}")
        if references.get("exam") != exam_slug or references.get("lang") != "pt-BR":
            raise ValueError(f"Reference map identity does not match {exam_slug}")
        if against_parent:
            verify_append_only(_read_parent_ledger(ledger_path, exam_slug), ledger)

        mappings = ledger["mappings"]
        ref_records = references["records"]
        if len(mappings) != expected_count or ledger["lastIssued"] != len(mappings):
            raise ValueError(
                f"{exam_slug} lastIssued/mapping count must equal {expected_count}"
            )
        if len(ref_records) != len(mappings):
            raise ValueError(f"Every {exam_slug} ID needs an explicit reference review state")
        ref_by_id = {item["publicId"]: item for item in ref_records}
        if len(ref_by_id) != len(ref_records):
            raise ValueError(f"Duplicate public ID in {exam_slug} reference review")

        for sequence, mapping in enumerate(mappings, start=1):
            internal_id = mapping["internalId"]
            public_id = mapping["publicId"]
            expected_id = f"{prefix}{sequence:05d}"
            if public_id != expected_id:
                raise ValueError(f"Unexpected public ID {public_id}; expected {expected_id}")
            if internal_id in seen_internal or public_id in seen_public:
                raise ValueError(f"Duplicate mapping across exam ledgers: {mapping}")
            seen_internal.add(internal_id)
            seen_public.add(public_id)

            question = questions.get(internal_id)
            if not question or question.get("cert") != cert or question.get("pool") != "study":
                raise ValueError(f"{internal_id} is missing or outside the {cert} study pool")
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
            if not review.get("reviewNote"):
                raise ValueError(f"{public_id} has no editorial review note")
            if review.get("confidence") not in ("alta", "média", "baixa"):
                raise ValueError(f"{public_id} has an invalid confidence value")
            if review.get("state") == "candidate":
                url = review.get("reference", "")
                if not url.startswith(APPROVED_REFERENCE_PREFIXES) or not review.get("referenceTitle"):
                    raise ValueError(f"{public_id} candidate has no approved primary reference")
            elif review.get("state") == "held":
                if review.get("reference") is not None or review.get("referenceTitle") is not None:
                    raise ValueError(f"{public_id} is held but contains a publishable reference")
            else:
                raise ValueError(f"{public_id} has an invalid review state")

        # Axon IDs have exactly PREFIX-EXAM-SEQ; the exam segment cannot contain
        # a hyphen (e.g. CTALTA, not CTAL-TA).
        if any(mapping["publicId"].split("-")[1] != exam_code for mapping in mappings):
            raise ValueError(f"{exam_slug} Axon IDs must use exam code {exam_code}")

        counts[cert] = len(mappings)
        total += len(mappings)

    print(
        f"Validated {total} study IDs ("
        + ", ".join(f"{cert} {count}" for cert, count in counts.items())
        + "); no exam question included"
    )


if __name__ == "__main__":
    try:
        if sys.argv[1:] not in ([], ["--against-parent"]):
            raise ValueError("Usage: verify_axon_ids.py [--against-parent]")
        verify(against_parent="--against-parent" in sys.argv[1:])
    except (KeyError, TypeError, ValueError) as exc:
        print(f"Axon ID validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
