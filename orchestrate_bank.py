#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Token-efficient orchestrator for analyzing, validating, and applying question batches.

Designed to run all structural, editorial, deduplication, alignment, psychometric,
and Axon ID checks deterministically in Python so LLM workflows only inspect
compact summaries or flagged exceptions.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
import unittest
import zipfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent

VALID_CERTS = {"CTFL", "CTFL-AT", "CTAL-TA", "CTAL-TM", "CT-AI"}
DOMAIN_BY_CERT = {
    "CTFL": {1: "fund", 2: "proc", 3: "est", 4: "tec", 5: "mgmt", 6: "fer"},
    "CTAL-TA": "analyst",
    "CTAL-TM": "manager",
    "CT-AI": "ai",
}
LETTER_RE = re.compile(
    r"(op[çc][ãa]o\s+[abcd]\b|alternativa\s+[abcd]\b|letra\s+[abcd]\b"
    r"|(?<!\()\b[abcd]\)\s|option\s+[abcd]\b|answer\s+[abcd]\b|choice\s+[abcd]\b)",
    re.I,
)
ALLNONE_RE = re.compile(
    r"(todas as anteriores|nenhuma das anteriores|todos os itens acima|"
    r"all of the above|none of the above|none of these)",
    re.I,
)

BASELINE_FILES = (
    "check_alignment_baseline.synapse-question-bank.json",
    "check_alignment_topic_baseline.synapse-question-bank.json",
    "check_alignment_baseline.ctfl-questions-ptbr.json",
    "check_alignment_topic_baseline.ctfl-questions-ptbr.json",
    "check_alignment_letter_baseline.synapse-question-bank.json",
    "check_alignment_letter_baseline.ctfl-questions-ptbr.json",
)


def strip_accents(text: str) -> str:
    """Lowercase and strip Unicode combining marks."""
    return "".join(
        ch for ch in unicodedata.normalize("NFD", text.lower())
        if unicodedata.category(ch) != "Mn"
    )


def stem_tokens(text: str) -> set[str]:
    """Tokenize a stem for lightweight Jaccard similarity checks."""
    return set(re.findall(r"[a-z0-9]{3,}", strip_accents(text)))


def jaccard(a: set[str], b: set[str]) -> float:
    """Compute Jaccard similarity between two token sets."""
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def read_json(path: Path):
    """Read UTF-8 JSON file."""
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data, indent: int = 1) -> None:
    """Write UTF-8 JSON file preserving non-ASCII characters."""
    path.write_text(json.dumps(data, ensure_ascii=False, indent=indent) + "\n", encoding="utf-8")


def extract_questions_payload(path: Path) -> list[dict]:
    """Load question list from either a list JSON or {'questions': [...]} dict."""
    data = read_json(path)
    if isinstance(data, dict) and isinstance(data.get("questions"), list):
        return data["questions"]
    if isinstance(data, list):
        return data
    raise ValueError(f"Unsupported question batch format in {path}")


def load_baseline_ids(path: Path) -> list[str]:
    """Load ID list from a baseline or baseline-additions JSON file."""
    data = read_json(path)
    if isinstance(data, dict) and isinstance(data.get("ids"), list):
        return list(data["ids"])
    if isinstance(data, list):
        return list(data)
    raise ValueError(f"Unsupported baseline format in {path}")


def merge_unique_ids(target_ids: list[str], additions: list[str]) -> int:
    """Append unseen IDs in order; returns number of newly added IDs."""
    seen = set(target_ids)
    added = 0
    for qid in additions:
        if qid not in seen:
            target_ids.append(qid)
            seen.add(qid)
            added += 1
    return added


def resolve_pack_dir(source: Path, tmp_dir: Path) -> Path:
    """Resolve a JSON file, directory, or .zip archive into an inspectable path."""
    if source.suffix.lower() == ".zip":
        dest = tmp_dir / source.stem
        dest.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(source) as zf:
            for member in zf.infolist():
                if "__MACOSX" not in member.filename:
                    zf.extract(member, dest)
        subdirs = [p for p in dest.iterdir() if p.is_dir() and p.name not in ("tools", "annexes")]
        if len(subdirs) == 1 and not list(dest.glob("*.json")):
            return subdirs[0]
        return dest
    return source


def discover_step(source: Path, tmp_dir: Path, mode: str = "auto") -> dict:
    """Normalize a CLI input path (.json, dir, or .zip) into a manifest step dict."""
    resolved = resolve_pack_dir(source, tmp_dir)
    if resolved.is_file():
        return {"name": source.stem, "mode": "add" if mode == "auto" else mode, "questions": str(resolved)}

    # Directory pack
    q_candidates = sorted(resolved.glob("synapse-new-questions-*.json"))
    req_candidates = sorted(resolved.glob("synapse-requalified-questions-*.json"))
    if mode == "auto":
        if q_candidates:
            inferred_mode = "add"
            q_file = q_candidates[0]
        elif req_candidates:
            inferred_mode = "replace"
            q_file = req_candidates[0]
        else:
            jsons = [p for p in sorted(resolved.glob("*.json")) if "baseline" not in p.name and "report" not in p.name]
            if not jsons:
                raise ValueError(f"No question JSON found in {source}")
            inferred_mode = "add"
            q_file = jsons[0]
    else:
        inferred_mode = mode
        q_file = (q_candidates or req_candidates)[0]

    step: dict = {"name": resolved.name, "mode": inferred_mode, "questions": str(q_file)}
    g1 = sorted(resolved.glob("baseline-*-guarda1-additions.json"))
    g2 = sorted(resolved.glob("baseline-*-guarda2-additions.json"))
    if g1:
        step["g1_additions"] = str(g1[0])
    if g2:
        step["g2_additions"] = str(g2[0])
    return step


def load_steps(inputs: list[str], manifest_path: str | None, tmp_dir: Path) -> dict:
    """Build an execution plan from --manifest or positional input paths."""
    if manifest_path:
        m = read_json(Path(manifest_path))
        if "steps" not in m or not isinstance(m["steps"], list):
            raise ValueError("Manifest JSON must contain a 'steps' list")
        return m
    if not inputs:
        raise ValueError("Provide batch paths or --manifest")
    steps = [discover_step(Path(p), tmp_dir) for p in inputs]
    return {"steps": steps}


def check_question_schema_and_editorial(
    q: dict,
    expected_existing: bool,
    known_ids: set[str],
    bank_stems: list[tuple[str, set[str]]],
    check_duplicates: bool = True,
) -> tuple[list[dict], list[dict]]:
    """Run deterministic schema, identity, anti-leak, and editorial checks on one question."""
    fails: list[dict] = []
    warns: list[dict] = []
    qid = str(q.get("id", "?"))

    required = ("id", "cert", "chapter", "domain", "kLevel", "answer", "locales")
    for key in required:
        if key not in q:
            fails.append({"id": qid, "gate": "SCHEMA", "msg": f"missing key: {key}"})

    cert = q.get("cert")
    if cert not in VALID_CERTS:
        fails.append({"id": qid, "gate": "SCHEMA", "msg": f"invalid cert: {cert!r}"})

    if expected_existing:
        if qid not in known_ids:
            fails.append({"id": qid, "gate": "IDENTITY", "msg": "replace target ID not found in bank"})
    else:
        if qid in known_ids:
            fails.append({"id": qid, "gate": "IDENTITY", "msg": "duplicate ID already in bank/queue"})

    ans = q.get("answer")
    if type(ans) is not int or not 0 <= ans <= 3:
        fails.append({"id": qid, "gate": "SCHEMA", "msg": f"invalid answer index: {ans!r}"})

    k_level = q.get("kLevel")
    if type(k_level) is not int or not 1 <= k_level <= 4:
        fails.append({"id": qid, "gate": "SCHEMA", "msg": f"invalid kLevel: {k_level!r}"})

    pool = q.get("pool")
    if pool is not None and pool not in ("study", "exam"):
        fails.append({"id": qid, "gate": "SCHEMA", "msg": f"invalid pool: {pool!r}"})

    expected_domain = DOMAIN_BY_CERT.get(cert)
    if isinstance(expected_domain, dict):
        if expected_domain.get(q.get("chapter")) != q.get("domain"):
            fails.append({"id": qid, "gate": "SCHEMA", "msg": f"chapter/domain mismatch: {q.get('chapter')}/{q.get('domain')}"})
    elif isinstance(expected_domain, str) and q.get("domain") != expected_domain:
        fails.append({"id": qid, "gate": "SCHEMA", "msg": f"domain mismatch for {cert}: {q.get('domain')}"})

    locales = q.get("locales")
    if not isinstance(locales, dict):
        fails.append({"id": qid, "gate": "SCHEMA", "msg": "locales must be an object"})
        return fails, warns

    for lang in ("pt", "en"):
        loc = locales.get(lang)
        if not isinstance(loc, dict):
            fails.append({"id": qid, "gate": "SCHEMA", "msg": f"missing locale: {lang}"})
            continue
        stem = loc.get("q", "")
        opts = loc.get("options")
        exp = loc.get("exp", "")
        if not isinstance(stem, str) or not stem.strip():
            fails.append({"id": qid, "gate": "SCHEMA", "msg": f"{lang}.q empty"})
        if not isinstance(exp, str) or not exp.strip():
            fails.append({"id": qid, "gate": "SCHEMA", "msg": f"{lang}.exp empty"})
        if not isinstance(opts, list) or len(opts) != 4 or any(not isinstance(o, str) or not o.strip() for o in opts):
            fails.append({"id": qid, "gate": "SCHEMA", "msg": f"{lang}.options must be 4 non-empty strings"})
            continue

        if LETTER_RE.search(exp):
            fails.append({"id": qid, "gate": "ANTI_LEAK", "msg": f"{lang}.exp references fixed letter A-D"})
        for idx, opt in enumerate(opts):
            if ALLNONE_RE.search(opt):
                fails.append({"id": qid, "gate": "OPTION_RULE", "msg": f"{lang}.options[{idx}] uses all/none of the above"})

        lens = [len(o.strip()) for o in opts]
        if max(lens) > 0 and (max(lens) - min(lens)) / max(lens) > 0.32:
            warns.append({"id": qid, "gate": "LEN_SPREAD", "msg": f"{lang} option length spread >32%"})

    pt_q = locales.get("pt", {}).get("q", "")
    en_q = locales.get("en", {}).get("q", "")
    if pt_q and en_q:
        ratio = len(en_q) / max(len(pt_q), 1)
        if ratio < 0.50 or ratio > 1.75:
            warns.append({"id": qid, "gate": "PARITY", "msg": f"EN/PT stem length ratio={ratio:.2f}"})

    if not expected_existing and check_duplicates and pt_q:
        toks = stem_tokens(pt_q)
        for other_id, other_toks in bank_stems:
            sim = jaccard(toks, other_toks)
            if sim >= 0.65:
                warns.append({"id": qid, "gate": "NEAR_DUP", "msg": f"PT stem Jaccard={sim:.2f} vs {other_id}"})
                break

    return fails, warns


def bump_semver(version: str, target_version: str | None) -> str:
    """Return explicit target_version or bump minor version cleanly."""
    if target_version:
        m = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)(?:-[A-Za-z0-9.-]+)?", target_version)
        if not m:
            raise ValueError(f"Invalid SemVer version: {target_version!r}")
        return target_version
    m = re.match(r"^(\d+)\.(\d+)\.(\d+)", version)
    if not m:
        raise ValueError(f"Cannot bump unsupported version: {version!r}")
    major, minor, _patch = map(int, m.groups())
    return f"{major}.{minor + 1}.0"


def simulate_plan(
    repo_dir: Path,
    plan: dict,
    sync_ctfl_legacy: bool = True,
    target_version: str | None = None,
    check_duplicates: bool = True,
) -> dict:
    """Execute full merge simulation in memory and validate against repo CI scripts."""
    synapse_bank = read_json(repo_dir / "synapse-question-bank.json")
    ctfl_bank = read_json(repo_dir / "ctfl-questions-ptbr.json")

    baselines = {name: read_json(repo_dir / name) for name in BASELINE_FILES}

    known_ids = {q["id"] for q in synapse_bank["questions"]}
    bank_stems = [
        (q["id"], stem_tokens(q.get("locales", {}).get("pt", {}).get("q", "")))
        for q in synapse_bank["questions"]
    ]
    ctfl_ids = {q["id"] for q in ctfl_bank["questions"]}

    fails: list[dict] = []
    warns: list[dict] = []
    step_summaries: list[dict] = []
    ctfl_touched = False

    for step in plan["steps"]:
        mode = step.get("mode", "add")
        name = step.get("name") or (Path(step["questions"]).stem if step.get("questions") else f"step-{mode}")
        step_fails = 0
        step_warns = 0

        if mode == "pool_swap":
            swaps = step.get("pool_swaps", [])
            qs = []
            syn_by_id = {q["id"]: q for q in synapse_bank["questions"] if "id" in q}
            ctfl_by_id = {q["id"]: q for q in ctfl_bank["questions"] if "id" in q}
            for pair in swaps:
                id_a, id_b = (pair["a"], pair["b"]) if isinstance(pair, dict) else tuple(pair)
                qa = syn_by_id.get(id_a)
                qb = syn_by_id.get(id_b)
                if qa is None or qb is None:
                    fails.append({"id": f"{id_a}<->{id_b}", "gate": "POOL_SWAP", "msg": "unknown question ID in pool_swap"})
                    step_fails += 1
                    continue
                if (qa.get("cert"), qa.get("chapter"), qa.get("kLevel")) != (qb.get("cert"), qb.get("chapter"), qb.get("kLevel")):
                    fails.append({"id": f"{id_a}<->{id_b}", "gate": "POOL_SWAP", "msg": "cell mismatch (cert/chapter/kLevel)"})
                    step_fails += 1
                    continue
                if {qa.get("pool"), qb.get("pool")} != {"study", "exam"}:
                    fails.append({"id": f"{id_a}<->{id_b}", "gate": "POOL_SWAP", "msg": "pool_swap requires one study and one exam question"})
                    step_fails += 1
                    continue
                qa["pool"], qb["pool"] = qb["pool"], qa["pool"]
                if sync_ctfl_legacy and qa.get("cert") == "CTFL":
                    ctfl_touched = True
                    if id_a in ctfl_by_id:
                        ctfl_by_id[id_a]["pool"] = qa["pool"]
                    if id_b in ctfl_by_id:
                        ctfl_by_id[id_b]["pool"] = qb["pool"]
        else:
            qs = extract_questions_payload(Path(step["questions"]))

            if mode == "add":
                for q in qs:
                    qf, qw = check_question_schema_and_editorial(
                        q, expected_existing=False, known_ids=known_ids, bank_stems=bank_stems, check_duplicates=check_duplicates
                    )
                    fails.extend(qf)
                    warns.extend(qw)
                    step_fails += len(qf)
                    step_warns += len(qw)
                    qid = q.get("id")
                    if qid and not any(x["gate"] == "IDENTITY" for x in qf):
                        known_ids.add(qid)
                        bank_stems.append((qid, stem_tokens(q.get("locales", {}).get("pt", {}).get("q", ""))))

                synapse_bank["questions"].extend(qs)

                if sync_ctfl_legacy:
                    ctfl_add = [q for q in qs if q.get("cert") == "CTFL"]
                    if ctfl_add:
                        ctfl_touched = True
                        for q in ctfl_add:
                            if q["id"] in ctfl_ids:
                                fails.append({"id": q["id"], "gate": "CTFL_LEGACY", "msg": "duplicate CTFL ID in ctfl-questions-ptbr.json"})
                            else:
                                ctfl_ids.add(q["id"])
                        ctfl_bank["questions"].extend(ctfl_add)

            elif mode == "replace":
                by_id = {q["id"]: q for q in qs if "id" in q}
                for q in qs:
                    qf, qw = check_question_schema_and_editorial(
                        q, expected_existing=True, known_ids=known_ids, bank_stems=bank_stems, check_duplicates=False
                    )
                    fails.extend(qf)
                    warns.extend(qw)
                    step_fails += len(qf)
                    step_warns += len(qw)

                for idx, existing in enumerate(synapse_bank["questions"]):
                    qid = existing["id"]
                    if qid in by_id:
                        synapse_bank["questions"][idx] = by_id[qid]

                if sync_ctfl_legacy:
                    ctfl_rep = {qid: q for qid, q in by_id.items() if q.get("cert") == "CTFL"}
                    if ctfl_rep:
                        ctfl_touched = True
                        for idx, existing in enumerate(ctfl_bank["questions"]):
                            qid = existing["id"]
                            if qid in ctfl_rep:
                                if "lo" in ctfl_rep[qid]:
                                    ctfl_bank["questions"][idx]["lo"] = ctfl_rep[qid]["lo"]
                                else:
                                    ctfl_bank["questions"][idx] = ctfl_rep[qid]
            else:
                raise ValueError(f"Unknown step mode: {mode!r}")

        # Merge explicitly supplied baseline additions
        g1_added = 0
        g2_added = 0
        ctfl_g1_added = 0
        ctfl_g2_added = 0

        if step.get("g1_additions"):
            add_ids = load_baseline_ids(Path(step["g1_additions"]))
            prefix = step.get("g1_filter_prefix")
            if prefix:
                add_ids = [qid for qid in add_ids if qid.startswith(prefix)]
            g1_added = merge_unique_ids(baselines["check_alignment_baseline.synapse-question-bank.json"]["ids"], add_ids)
            if sync_ctfl_legacy:
                ctfl_only = [qid for qid in add_ids if qid.startswith("ch")]
                ctfl_g1_added = merge_unique_ids(baselines["check_alignment_baseline.ctfl-questions-ptbr.json"]["ids"], ctfl_only)

        if step.get("g2_additions"):
            add_ids = load_baseline_ids(Path(step["g2_additions"]))
            g2_added = merge_unique_ids(baselines["check_alignment_topic_baseline.synapse-question-bank.json"]["ids"], add_ids)
            if sync_ctfl_legacy:
                ctfl_only = [qid for qid in add_ids if qid.startswith("ch")]
                ctfl_g2_added = merge_unique_ids(baselines["check_alignment_topic_baseline.ctfl-questions-ptbr.json"]["ids"], ctfl_only)

        # Optional meta patches declared in step
        for cert_name, cert_patch in step.get("meta_cert_patches", {}).items():
            if cert_name in synapse_bank["meta"].get("certifications", {}):
                synapse_bank["meta"]["certifications"][cert_name].update(cert_patch)

        step_summaries.append({
            "step": name,
            "mode": mode,
            "questions": len(qs),
            "total_after": len(synapse_bank["questions"]),
            "fails": step_fails,
            "warns": step_warns,
            "g1_added": g1_added,
            "g2_added": g2_added,
            "ctfl_g1_added": ctfl_g1_added,
            "ctfl_g2_added": ctfl_g2_added,
        })

    # Update metadata counts, poolSplit & versions
    today = dt.date.today().isoformat()
    cert_counts = Counter(q["cert"] for q in synapse_bank["questions"])
    synapse_bank["meta"]["totalQuestions"] = len(synapse_bank["questions"])
    for cert_name, count in cert_counts.items():
        if cert_name in synapse_bank["meta"].get("certifications", {}):
            synapse_bank["meta"]["certifications"][cert_name]["totalQuestions"] = count

    pool_split = synapse_bank["meta"].get("poolSplit")
    if isinstance(pool_split, dict):
        old_per_cert = pool_split.get("perCert") if isinstance(pool_split.get("perCert"), dict) else {}
        per_cert_stats: dict[str, dict[str, int]] = {}
        for q in synapse_bank["questions"]:
            ck = q["cert"].lower()
            st = per_cert_stats.setdefault(ck, {"exam": 0, "study": 0, "total": 0})
            st["total"] += 1
            if q.get("pool") == "exam":
                st["exam"] += 1
            elif q.get("pool") == "study":
                st["study"] += 1
        ordered_keys = [k for k in old_per_cert if k in per_cert_stats] + sorted(
            k for k in per_cert_stats if k not in old_per_cert
        )
        new_per_cert = {}
        for ck in ordered_keys:
            entry = dict(per_cert_stats[ck])
            note = old_per_cert.get(ck, {}).get("note") if isinstance(old_per_cert.get(ck), dict) else None
            if note:
                entry["note"] = note
            new_per_cert[ck] = entry
        pool_split["perCert"] = new_per_cert
        pool_split["generatedDate"] = today

    synapse_bank["meta"]["version"] = bump_semver(synapse_bank["meta"]["version"], target_version)
    synapse_bank["meta"]["generatedDate"] = today

    if ctfl_touched:
        ctfl_bank["meta"]["total"] = len(ctfl_bank["questions"])
        ctfl_bank["meta"]["version"] = bump_semver(ctfl_bank["meta"]["version"], plan.get("ctfl_target_version"))
        ctfl_bank["meta"]["generatedDate"] = today

    # Run repo CI scripts in an isolated temp directory
    ci_results = run_ci_in_temp(
        repo_dir=repo_dir,
        synapse_bank=synapse_bank,
        ctfl_bank=ctfl_bank,
        baselines=baselines,
        promote_live=plan.get("simulate_promote_live", []),
    )

    return {
        "ok": len(fails) == 0 and ci_results["all_passed"],
        "version_after": synapse_bank["meta"]["version"],
        "ctfl_version_after": ctfl_bank["meta"]["version"],
        "total_questions": len(synapse_bank["questions"]),
        "ctfl_legacy_questions": len(ctfl_bank["questions"]),
        "cert_counts": dict(sorted(cert_counts.items())),
        "steps": step_summaries,
        "fail_count": len(fails),
        "warn_count": len(warns),
        "fails": fails[:50],
        "warns": warns[:50],
        "ci": ci_results,
        "_artifacts": {
            "synapse_bank": synapse_bank,
            "ctfl_bank": ctfl_bank,
            "baselines": baselines,
        },
    }


def _compact_guard_summary(stdout: str) -> dict:
    """Extract only key guard status lines to keep output compact."""
    lines = []
    for ln in stdout.splitlines():
        s = ln.strip()
        if (
            s.startswith("[Guarda ")
            or s.startswith("OK:")
            or s.startswith("FALHA:")
            or s.startswith("RESUMO:")
            or s.startswith("→ [PASS]")
            or s.startswith("→ [FAIL]")
        ):
            lines.append(s)
    return {"highlights": lines}


def run_ci_in_temp(
    repo_dir: Path,
    synapse_bank: dict,
    ctfl_bank: dict,
    baselines: dict,
    promote_live: list[str] | None = None,
) -> dict:
    """Run check_alignment.py (both banks) and verify_axon_ids.py in an isolated temp dir."""
    with tempfile.TemporaryDirectory() as tmp:
        td = Path(tmp)
        for py_file in repo_dir.glob("*.py"):
            (td / py_file.name).write_bytes(py_file.read_bytes())
        (td / "axon").mkdir()
        for f in (repo_dir / "axon").glob("*.json"):
            (td / "axon" / f.name).write_bytes(f.read_bytes())

        write_json(td / "synapse-question-bank.json", synapse_bank, indent=1)
        write_json(td / "ctfl-questions-ptbr.json", ctfl_bank, indent=1)
        for name, obj in baselines.items():
            write_json(td / name, obj, indent=2)

        def run_cmd(cmd: list[str]) -> dict:
            p = subprocess.run(cmd, cwd=td, capture_output=True, text=True)
            out = {"exit": p.returncode, **_compact_guard_summary(p.stdout)}
            if p.returncode != 0:
                out["tail"] = "\n".join((p.stdout + "\n" + p.stderr).splitlines()[-25:])
            return out

        res_synapse = run_cmd([sys.executable, "check_alignment.py", "--bank-file", "synapse-question-bank.json", "--threshold", "0"])
        res_ctfl = run_cmd([sys.executable, "check_alignment.py", "--bank-file", "ctfl-questions-ptbr.json", "--threshold", "0"])

        p_axon = subprocess.run([sys.executable, "verify_axon_ids.py"], cwd=td, capture_output=True, text=True)
        res_axon = {"exit": p_axon.returncode, "msg": (p_axon.stdout or p_axon.stderr).strip()}

        extra_live = None
        if promote_live:
            ca_path = td / "check_alignment.py"
            ca_text = ca_path.read_text(encoding="utf-8")
            m = re.search(r"LIVE_CERTS\s*=\s*\{[^}]+\}", ca_text)
            if m:
                current_certs = re.findall(r'"([^"]+)"', m.group(0))
                merged_certs = sorted(set(current_certs) | set(promote_live))
                new_line = "LIVE_CERTS = {" + ", ".join(f'"{c}"' for c in merged_certs) + "}"
                ca_path.write_text(ca_text.replace(m.group(0), new_line, 1), encoding="utf-8")
                extra_live = run_cmd([sys.executable, "check_alignment.py", "--bank-file", "synapse-question-bank.json", "--threshold", "0"])

        all_passed = (
            res_synapse["exit"] == 0
            and res_ctfl["exit"] == 0
            and res_axon["exit"] == 0
            and (extra_live is None or extra_live["exit"] == 0)
        )
        return {
            "all_passed": all_passed,
            "check_alignment_synapse": res_synapse,
            "check_alignment_ctfl": res_ctfl,
            "verify_axon_ids": res_axon,
            "check_alignment_promoted_live": extra_live,
        }


def run_repo_post_apply_checks(repo_dir: Path) -> dict:
    """Run live repo checks after applying changes to disk."""
    cmds = {
        "unittest": [sys.executable, "-m", "unittest", "test_sync_protection.py", "test_editorial_batch.py", "test_axon_ids.py"],
        "verify_axon_ids": [sys.executable, "verify_axon_ids.py"],
        "check_alignment_ctfl": [sys.executable, "check_alignment.py", "--bank-file", "ctfl-questions-ptbr.json", "--threshold", "0"],
        "check_alignment_synapse": [sys.executable, "check_alignment.py", "--bank-file", "synapse-question-bank.json", "--threshold", "0"],
    }
    results = {}
    all_ok = True
    for name, cmd in cmds.items():
        p = subprocess.run(cmd, cwd=repo_dir, capture_output=True, text=True)
        if p.returncode != 0:
            all_ok = False
        results[name] = {
            "exit": p.returncode,
            "summary": ((p.stdout or "") + "\n" + (p.stderr or "")).strip().splitlines()[-5:],
        }
    return {"all_passed": all_ok, "checks": results}


def backup_repo_files(repo_dir: Path) -> Path:
    """Backup target JSON files into gitignored .cache/orchestrator-backups/."""
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    bdir = repo_dir / ".cache" / "orchestrator-backups" / stamp
    bdir.mkdir(parents=True, exist_ok=True)
    targets = ("synapse-question-bank.json", "ctfl-questions-ptbr.json", *BASELINE_FILES)
    for name in targets:
        src = repo_dir / name
        if src.exists():
            shutil.copy2(src, bdir / name)
    return bdir


def print_compact_summary(report: dict) -> None:
    """Print concise, token-efficient summary to stdout."""
    status = "PASS" if report["ok"] else "FAIL"
    print(f"[{status}] total={report['total_questions']} ctfl_legacy={report['ctfl_legacy_questions']} version={report['version_after']}")
    print("certs:", json.dumps(report["cert_counts"], ensure_ascii=False))
    for st in report["steps"]:
        print(
            f"  step={st['step']} ({st['mode']}) Q={st['questions']} -> {st['total_after']}"
            f" | fails={st['fails']} warns={st['warns']} | +g1={st['g1_added']} +g2={st['g2_added']}"
        )
    print(f"issues: fails={report['fail_count']} warns={report['warn_count']}")
    for f in report["fails"][:10]:
        print(f"  FAIL [{f['gate']}] {f['id']}: {f['msg']}")
    ci = report["ci"]
    print(
        f"ci: synapse={ci['check_alignment_synapse']['exit']}"
        f" ctfl={ci['check_alignment_ctfl']['exit']}"
        f" axon={ci['verify_axon_ids']['exit']}"
        + (f" live_promo={ci['check_alignment_promoted_live']['exit']}" if ci.get("check_alignment_promoted_live") else "")
    )
    if not ci["all_passed"]:
        for key in ("check_alignment_synapse", "check_alignment_ctfl", "check_alignment_promoted_live"):
            item = ci.get(key)
            if item and item["exit"] != 0:
                print(f"--- {key} tail ---\n{item.get('tail', '')}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    for cmd_name in ("analyze", "validate", "apply"):
        p = sub.add_parser(cmd_name)
        p.add_argument("inputs", nargs="*", help="Batch .json, .zip, or extracted pack directories")
        p.add_argument("--manifest", help="Ordered JSON manifest describing multi-round integration")
        p.add_argument("--repo", default=str(ROOT), help="Path to ctfl-question-bank-ptbr repo")
        p.add_argument("--version", default=None, help="Explicit target meta.version for synapse-question-bank.json")
        p.add_argument("--no-ctfl-legacy", action="store_true", help="Do not sync CTFL changes to ctfl-questions-ptbr.json")
        p.add_argument("--skip-dup-check", action="store_true", help="Skip stem Jaccard near-duplicate warnings")
        p.add_argument("--report", help="Write compact JSON report to path")
        if cmd_name == "apply":
            p.add_argument("--dry-run", action="store_true", help="Simulate without writing repo files")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    repo_dir = Path(args.repo).resolve()

    with tempfile.TemporaryDirectory() as tmp_extract:
        plan = load_steps(args.inputs, args.manifest, Path(tmp_extract))
        report = simulate_plan(
            repo_dir=repo_dir,
            plan=plan,
            sync_ctfl_legacy=not args.no_ctfl_legacy,
            target_version=args.version,
            check_duplicates=not args.skip_dup_check,
        )

    artifacts = report.pop("_artifacts")
    print_compact_summary(report)

    if args.command == "apply":
        if not report["ok"]:
            print("ABORT: validation failed; repo files left untouched.", file=sys.stderr)
            if args.report:
                write_json(Path(args.report), report, indent=2)
            return 1
        if args.dry_run:
            print("DRY-RUN: validation passed; no files modified.")
        else:
            bdir = backup_repo_files(repo_dir)
            write_json(repo_dir / "synapse-question-bank.json", artifacts["synapse_bank"], indent=1)
            write_json(repo_dir / "ctfl-questions-ptbr.json", artifacts["ctfl_bank"], indent=1)
            for name, obj in artifacts["baselines"].items():
                target = repo_dir / name
                if target.exists():
                    write_json(target, obj, indent=2)
            post = run_repo_post_apply_checks(repo_dir)
            report["post_apply"] = post
            report["backup_dir"] = str(bdir)
            print(f"APPLIED: backup={bdir} | post_apply_passed={post['all_passed']}")
            if not post["all_passed"]:
                print("ERROR: post-apply checks failed! Backup preserved at:", bdir, file=sys.stderr)
                if args.report:
                    write_json(Path(args.report), report, indent=2)
                return 1

    if args.report:
        write_json(Path(args.report), report, indent=2)

    if args.command in ("validate", "apply") and not report["ok"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
