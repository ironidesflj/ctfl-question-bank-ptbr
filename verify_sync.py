"""Fail-closed checks for source/app synchronization; stdlib only."""
import argparse
import hashlib
import json
import re
from pathlib import Path

from check_alignment import LIVE_CERTS

BANKS = ("ctfl-questions-ptbr.json", "synapse-question-bank.json")


def version(bank):
    value = bank["meta"]["version"]
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)(?:-[A-Za-z0-9.-]+)?", value)
    if not match:
        raise ValueError(f"Unsupported bank version: {value!r}")
    return tuple(map(int, match.groups()))


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate(source, app, check_current=False):
    source, app = Path(source), Path(app)
    data = app / "src/data"
    canonical = read(source / BANKS[1])
    current = read(data / BANKS[1])
    if version(canonical) < version(current):
        raise ValueError("Downgrade blocked: app bank is newer than canonical source")
    match = re.search(r"VALID_CERTS\s*=\s*(\[[^\]]*\])", (app / "src/certs.js").read_text())
    if not match:
        raise ValueError("Cannot determine app VALID_CERTS")
    live = set(json.loads(match[1]))
    if {cert.upper() for cert in live} != LIVE_CERTS:
        raise ValueError("App VALID_CERTS and blocking LIVE_CERTS disagree")
    for cert in live:
        for key in ("examFormat", "examBlueprint", "chapterWeights"):
            if cert not in canonical["meta"].get(key, {}):
                raise ValueError(f"Missing canonical {key} for live {cert}")
    if check_current:
        if version(canonical) == version(current) and canonical != current:
            raise ValueError("Different content at the same version: version the source correction first")
        old_ids = {q["id"] for q in current["questions"]}
        new_ids = {q["id"] for q in canonical["questions"]}
        if not old_ids <= new_ids:
            raise ValueError("Question removal requires an explicit progress migration")
        return
    for name in BANKS:
        a, b = (source / name).read_bytes(), (data / name).read_bytes()
        if hashlib.sha256(a).digest() != hashlib.sha256(b).digest():
            raise ValueError(f"Source/app checksum mismatch: {name}")
    for cert in live:
        expected = {
            "meta": canonical["meta"],
            "questions": [q for q in canonical["questions"] if q.get("cert", "").lower() == cert],
        }
        if read(data / "banks" / f"{cert}.json") != expected:
            raise ValueError(f"Stale or modified derived slice: {cert}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("app", type=Path)
    parser.add_argument("--check-current", action="store_true")
    args = parser.parse_args()
    try:
        validate(args.source, args.app, args.check_current)
    except (ValueError, KeyError, OSError) as exc:
        parser.exit(1, f"FAIL: {exc}\n")
    print("PASS: anti-downgrade/live coverage" if args.check_current else "PASS: canonical checksums, live coverage and complete slices")


if __name__ == "__main__":
    main()
