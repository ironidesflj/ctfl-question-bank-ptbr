# -*- coding: utf-8 -*-
"""
check_alignment.py — heurística de alerta para desalinhamento PT/EN no banco
                       + guards psicométricos de bias (F1.3).

USO:
  python3 check_alignment.py                              # compara contra a baseline do ctfl-questions-ptbr.json
  python3 check_alignment.py --bank-file synapse-question-bank.json --threshold 2
  python3 check_alignment.py synapse-question-bank.json   # forma posicional
  python3 check_alignment.py --guards length_bias,hedge_ratio synapse-question-bank.json
  python3 check_alignment.py --list-guards
  python3 check_alignment.py --update-baseline            # aceita o estado atual como baseline
  python3 check_alignment.py --threshold N                # ajusta quantas suspeitas NOVAS são toleradas (default: 0)

GUARDS EXISTENTES (0, 1, 2) — preservados:
  Guarda 0: estrutural (IDs duplicados, answer/schema inválido) — zero tolerância
  Guarda 1: opção vs. explicação (heurística SequenceMatcher, com baseline)
  Guarda 2: tema PT/EN (z-score da similaridade, com baseline)

NOVOS GUARDS PSICOMÉTRICOS (10-15) — F1.3:
  Guarda 10  LENGTH_BIAS          — pick-longest hit rate > 0.40 por cert (PT + EN)
  Guarda 11  LENGTH_EFFECT_SIZE   — Cohen's d > 0.50 por cert (correct vs distractor lengths)
  Guarda 12  HEDGE_RATIO          — ratio (correct_hedge / distractor_hedge) < 0.5 OU > 2.0
  Guarda 13  ANSWER_INDEX_CHI2    — chi2 goodness-of-fit vs uniforme, p < 0.01 (certs com ≥50 Q)
  Guarda 14  RUNS_TEST            — Wald-Wolfowitz z-score < -5.0 (clustering)
  Guarda 15  BLUEPRINT_MATCH      — drift > 15pp vs meta.chapterWeights + validação K-levels

Os novos guards usam APENAS stdlib (json, math, statistics, sys, collections, re,
unicodedata, argparse, difflib, pathlib). Não dependem de scipy/numpy — o ambiente
de CI pode não tê-los. O p-value do chi2 usa a aproximação normal de Wilson-Hilferty
para df=3 (4 categorias de answer index). O runs test usa a fórmula padrão de
Wald-Wolfowitz sobre a sequência "mesmo-anterior?" derivada da ordem do banco.

IMPORTANTE — limitações conhecidas dos guards existentes (não é prova de bug):
  - A heurística do Guarda 1 tem falsos positivos CONHECIDOS e estruturais; por isso
    usa baseline (check_alignment_baseline.<bank>.json) e só falha em suspeitas NOVAS.
  - Esta ferramenta NUNCA corrige nada automaticamente. Toda suspeita nova deve ser
    lida manualmente.

Saída:
  - Cada guard novo imprime [PASS] ou [FAIL] com detalhes por cert.
  - Resumo final: "X/6 new guards passed, Y failed".
  - Exit code 0 se todos os guards passarem, 1 caso contrário.
"""

import json
import math
import sys
import re
import argparse
import unicodedata
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path

# ============================================================================
# Constants for the new psychometric guards
# ============================================================================

CERTS_CANONICAL = ["CTFL", "CTFL-AT", "CTAL-TA", "CTAL-TM", "CT-AI"]

# Certs reachable in the app today (VALID_CERTS in ctfl-app/src/certs.js).
# CTFL-AT/CTAL-TM/CT-AI are LATENT: real data-quality debt, but not user-facing
# until promoted to live, so their guard failures are reported (visibility)
# but must NOT block CI for the two certs Fase 1 actually fixed. Without this
# scoping, the 6 new guards below would exit non-zero forever, since the 3
# untouched certs will always fail length_bias/effect_size/chi2/runs_test.
LIVE_CERTS = {"CTFL", "CTAL-TA"}

# Guard 12 — hedge/absolute lexicon (as specified in F1.3 task).
# These are "absolutist" qualifiers; the guard name says "hedge" but the word
# list is the one mandated by the task spec. We match them as whole tokens
# (accent-insensitive) inside each option text.
HEDGE_WORDS_PT = {
    "sempre", "nunca", "todos", "todas", "qualquer", "apenas", "somente",
    "deve", "exatamente", "unicamente", "impossivel",
}
HEDGE_WORDS_EN = {
    "always", "never", "all", "every", "any", "only", "must",
    "exactly", "solely", "impossible",
}

# Thresholds (single source of truth — easy to tune)
LEN_BIAS_THRESHOLD = 0.40          # Guard 10
LEN_EFFECT_SIZE_THRESHOLD = 0.50   # Guard 11
HEDGE_RATIO_MIN = 0.5              # Guard 12
HEDGE_RATIO_MAX = 2.0              # Guard 12
CHI2_P_THRESHOLD = 0.01            # Guard 13
CHI2_MIN_N = 50                    # Guard 13 — only test certs with ≥50 questions
RUNS_Z_THRESHOLD = -5.0            # Guard 14
BLUEPRINT_PP_THRESHOLD = 15.0      # Guard 15 — percentage-point drift

# Map of guard CLI names → guard display names (used by --guards filter).
NEW_GUARD_REGISTRY = [
    ("length_bias",         "LENGTH_BIAS",         10),
    ("length_effect_size",  "LENGTH_EFFECT_SIZE",  11),
    ("hedge_ratio",         "HEDGE_RATIO",         12),
    ("answer_index_chi2",   "ANSWER_INDEX_CHI2",   13),
    ("runs_test",           "RUNS_TEST",           14),
    ("blueprint_match",     "BLUEPRINT_MATCH",     15),
]


# ============================================================================
# Existing helpers — preserved exactly from the original check_alignment.py
# ============================================================================

def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def check(bank_path: Path):
    with open(bank_path, encoding="utf-8") as f:
        bank = json.load(f)

    suspects = []
    for q in bank["questions"]:
        en = q["locales"].get("en")
        if not en:
            continue
        ans = q["answer"]
        exp_en = en["exp"].lower()
        scores = [similarity(o.lower(), exp_en) for o in en["options"]]
        best_idx = max(range(len(scores)), key=lambda i: scores[i])
        if best_idx != ans:
            suspects.append({
                "id": q["id"],
                "answer": ans,
                "opcao_atual_en": en["options"][ans],
                "indice_sugerido": best_idx,
                "opcao_sugerida_en": en["options"][best_idx],
            })
    return suspects


def check_topic(bank_path: Path):
    """Detecta desalinhamento de TEMA entre pt.q e en.q usando z-score da similaridade."""
    with open(bank_path, encoding="utf-8") as f:
        bank = json.load(f)

    pairs = []
    for q in bank["questions"]:
        en = q["locales"].get("en")
        if not en:
            continue
        pt = q["locales"].get("pt", {})
        score = similarity(pt.get("q", ""), en.get("q", ""))
        pairs.append({"id": q["id"], "score": score})

    if not pairs:
        return []

    scores = [p["score"] for p in pairs]
    mean = sum(scores) / len(scores)
    variance = sum((s - mean) ** 2 for s in scores) / len(scores)
    std = math.sqrt(variance)
    threshold = mean - 1.5 * std

    suspects = [
        {"id": p["id"], "score": round(p["score"], 4), "media_banco": round(mean, 4)}
        for p in pairs
        if p["score"] < threshold
    ]
    return suspects, round(mean, 4), round(std, 4), round(threshold, 4), len(pairs)


def check_duplicate_ids(bank_path: Path) -> list[str]:
    with open(bank_path, encoding="utf-8") as f:
        bank = json.load(f)
    ids = [q.get("id") for q in bank["questions"]]
    counts = Counter(ids)
    return sorted(str(k) for k, v in counts.items() if v > 1)


def check_invalid_answers(bank_path: Path) -> list[dict]:
    with open(bank_path, encoding="utf-8") as f:
        bank = json.load(f)
    bad = []
    for q in bank["questions"]:
        qid = q.get("id", "<sem id>")
        ans = q.get("answer")
        opts = q.get("locales", {}).get("pt", {}).get("options")
        if not isinstance(opts, list):
            bad.append({"id": qid, "problema": "locales.pt.options ausente ou não é lista"})
            continue
        if not isinstance(ans, int) or not (0 <= ans < len(opts)):
            bad.append({"id": qid, "answer": ans, "n_options": len(opts)})
    return bad


def load_baseline(baseline_file: Path):
    if not baseline_file.exists():
        return set()
    with open(baseline_file, encoding="utf-8") as f:
        data = json.load(f)
    return set(data.get("ids", []))


def save_baseline(suspects, baseline_file: Path):
    data = {
        "_comentario": "Falsos positivos conhecidos da heuristica de similaridade, confirmados manualmente como CORRETOS (PT/EN alinhados). Gerado por check_alignment.py --update-baseline.",
        "ids": sorted(s["id"] for s in suspects),
    }
    with open(baseline_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_topic_baseline(topic_baseline_file: Path):
    if not topic_baseline_file.exists():
        return set()
    with open(topic_baseline_file, encoding="utf-8") as f:
        data = json.load(f)
    return set(data.get("ids", []))


def save_topic_baseline(suspects, topic_baseline_file: Path):
    data = {
        "_comentario": "Falsos positivos conhecidos da heuristica de desalinhamento de TEMA PT/EN, confirmados manualmente. Gerado por check_alignment.py --update-topic-baseline.",
        "ids": sorted(s["id"] for s in suspects),
    }
    with open(topic_baseline_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ============================================================================
# New psychometric helpers (stdlib-only)
# ============================================================================

def _strip_accents(s: str) -> str:
    """NFD normalize + drop combining marks → ASCII-ish token for matching."""
    return "".join(
        c for c in unicodedata.normalize("NFD", s)
        if unicodedata.category(c) != "Mn"
    )


def _tokens(s: str) -> set:
    """Lowercased, accent-stripped whole-word tokens for hedge-word matching."""
    if not s:
        return set()
    raw = re.findall(r"[A-Za-zÀ-ÿ]+", s.lower())
    return {_strip_accents(w) for w in raw}


def _has_hedge(text: str, hedge_set: set) -> bool:
    """True if any hedge word appears as a whole token in text (accent-insensitive)."""
    return bool(_tokens(text) & hedge_set)


def _cert_of(q: dict) -> str:
    """Return a question's cert; treat missing/None as 'CTFL' (legacy file shape)."""
    c = q.get("cert")
    return c if c else "CTFL"


def _cohen_d(correct: list, distractors: list) -> float:
    """Cohen's d = (mean_correct - mean_distract) / pooled_sd.

    pooled_sd = sqrt(((n1-1)*s1^2 + (n2-1)*s2^2) / (n1+n2-2))
    Returns 0.0 when undefined (degenerate inputs or zero pooled SD).
    """
    n1, n2 = len(correct), len(distractors)
    if n1 < 2 or n2 < 2:
        return 0.0
    m1 = sum(correct) / n1
    m2 = sum(distractors) / n2
    v1 = sum((x - m1) ** 2 for x in correct) / (n1 - 1)
    v2 = sum((x - m2) ** 2 for x in distractors) / (n2 - 1)
    denom = n1 + n2 - 2
    if denom <= 0:
        return 0.0
    pooled = math.sqrt(((n1 - 1) * v1 + (n2 - 1) * v2) / denom)
    if pooled == 0:
        return 0.0
    return (m1 - m2) / pooled


def _chi_square_uniform_p(counts: list) -> tuple:
    """Chi-square goodness-of-fit vs uniform expected, df = k-1.

    Returns (chi2_stat, df, p_value) using the Wilson-Hilferty normal
    approximation for the chi-square CDF. Pure stdlib (math.erfc).

    For 4 answer-index categories → df = 3.
    Wilson-Hilferty: for X ~ chi2(k), ((X/k)^(1/3) - (1 - 2/(9k))) / sqrt(2/(9k)) ~ N(0,1)
    so P(X > x) ≈ 0.5 * erfc(z / sqrt(2)).

    Verified against critical values for df=3:
      chi2=11.345 → p≈0.0100 (the 0.01 critical value)
      chi2= 7.815 → p≈0.0503 (the 0.05 critical value)
      chi2=16.266 → p≈0.0010 (the 0.001 critical value)
    """
    n = sum(counts)
    k = len(counts)
    if n == 0 or k < 2:
        return (0.0, k - 1, 1.0)
    expected = n / float(k)
    if expected == 0:
        return (0.0, k - 1, 1.0)
    chi2 = sum((c - expected) ** 2 / expected for c in counts)
    df = k - 1
    if chi2 <= 0:
        return (0.0, df, 1.0)
    # Wilson-Hilferty upper-tail p
    z = ((chi2 / df) ** (1.0 / 3.0) - (1.0 - 2.0 / (9.0 * df))) / math.sqrt(2.0 / (9.0 * df))
    p = 0.5 * math.erfc(z / math.sqrt(2.0))
    # Numerical safety
    if p < 0.0:
        p = 0.0
    if p > 1.0:
        p = 1.0
    return (chi2, df, p)


def _runs_test_z(seq: list) -> tuple:
    """Wald-Wolfowitz runs test on the binary 'same-as-previous?' sequence
    derived from `seq` (the answer-index sequence in bank order).

    A run is a maximal stretch of identical binary values. Under H0 (random
    order), the number of runs is approximately normal with:
        mu    = 2*n1*n2/n + 1
        sigma = sqrt(2*n1*n2*(2*n1*n2 - n) / (n^2 * (n-1)))
        z     = (runs - mu) / sigma
    where n1 = #same-as-previous pairs, n2 = #different pairs, n = n1+n2.

    Negative z ⇒ fewer runs than expected ⇒ clustering (long same-answer runs).
    Returns (num_runs, expected_runs, z, n1, n2). Returns (0, 0, 0.0, 0, 0) for
    degenerate inputs.
    """
    if len(seq) < 2:
        return (0, 0.0, 0.0, 0, 0)
    binary = [1 if seq[i] == seq[i - 1] else 0 for i in range(1, len(seq))]
    n = len(binary)
    n1 = sum(binary)
    n2 = n - n1
    if n1 == 0 or n2 == 0:
        return (1, 1.0, 0.0, n1, n2)
    runs = 1
    for i in range(1, n):
        if binary[i] != binary[i - 1]:
            runs += 1
    mu = (2.0 * n1 * n2) / n + 1.0
    var_num = 2.0 * n1 * n2 * (2.0 * n1 * n2 - n)
    var_den = n * n * (n - 1)
    if var_den == 0:
        return (runs, mu, 0.0, n1, n2)
    sigma = math.sqrt(var_num / var_den)
    if sigma == 0:
        return (runs, mu, 0.0, n1, n2)
    z = (runs - mu) / sigma
    return (runs, mu, z, n1, n2)


def _get_chapter_weights(meta: dict, cert: str):
    """Return {chapter_str: weight} for `cert`, or None if not declared.

    Handles both shapes:
      - synapse: meta.chapterWeights = {lowercase_cert_id: {ch: w}, ...}
      - legacy:  meta.chapterWeights = {ch: w, ...}  (flat, CTFL-only)
    """
    cw = meta.get("chapterWeights")
    if not isinstance(cw, dict):
        return None
    cert_lower = cert.lower()
    if cert_lower in cw and isinstance(cw[cert_lower], dict):
        return {str(k): v for k, v in cw[cert_lower].items()}
    # Legacy flat shape — only valid for CTFL
    if cert == "CTFL" and all(isinstance(v, (int, float)) for v in cw.values()):
        return {str(k): v for k, v in cw.items()}
    return None


def _get_declared_klevels(meta: dict, cert: str):
    """Return the declared K-level list (e.g. ['K1','K2','K3']) or None."""
    certs = meta.get("certifications") or {}
    if cert in certs and isinstance(certs[cert], dict):
        kl = certs[cert].get("kLevels")
        if isinstance(kl, list):
            return kl
    return None


def _klevel_to_int(k):
    """'K3' → 3 ; 3 → 3 ; None → None."""
    if k is None:
        return None
    if isinstance(k, int):
        return k
    if isinstance(k, str):
        m = re.match(r"^K(\d+)$", k.strip())
        if m:
            return int(m.group(1))
    return None


# ============================================================================
# New psychometric guards (10–15)
# Each returns (passed: bool, detail_lines: list[str])
# ============================================================================

def guard_length_bias(bank_path: Path) -> tuple:
    """Guard 10 — pick-longest hit rate per cert, both PT and EN.

    FAIL if hit rate > 0.40 for any cert (in either locale).
    """
    with open(bank_path, encoding="utf-8") as f:
        bank = json.load(f)
    certs_present = sorted({_cert_of(q) for q in bank["questions"]})
    failures = []
    lines = ["[Guarda 10] LENGTH_BIAS — pick-longest hit rate (limiar: > %.0f%%)" % (LEN_BIAS_THRESHOLD * 100)]
    lines.append("  %-10s %5s %10s %10s" % ("Cert", "N", "PT_hit%", "EN_hit%"))
    for cert in certs_present:
        qs = [q for q in bank["questions"] if _cert_of(q) == cert]
        row = {"cert": cert, "n": 0, "pt_hit": None, "en_hit": None}
        for lang in ("pt", "en"):
            hit = 0
            n = 0
            for q in qs:
                opts = (q.get("locales", {}).get(lang) or {}).get("options")
                if not isinstance(opts, list) or len(opts) != 4:
                    continue
                ans = q.get("answer")
                if not isinstance(ans, int) or not (0 <= ans < 4):
                    continue
                lens = [len(o) for o in opts]
                # pick-longest = first index achieving max (matches length_bias_analysis.py mode A)
                pick = lens.index(max(lens))
                if pick == ans:
                    hit += 1
                n += 1
            rate = (hit / n) if n else 0.0
            row["n"] = n
            row[lang + "_hit"] = rate
            if rate > LEN_BIAS_THRESHOLD:
                failures.append((cert, lang, rate))
        lines.append("  %-10s %5d %9.1f%% %9.1f%%" % (
            cert, row["n"],
            (row["pt_hit"] or 0) * 100, (row["en_hit"] or 0) * 100))
    blocking = [f for f in failures if f[0] in LIVE_CERTS]
    if failures:
        lines.append("  → [FAIL] %d cert/locale(s) acima do limiar:" % len(failures))
        for cert, lang, rate in failures:
            tag = "" if cert in LIVE_CERTS else " (LATENT — não bloqueia CI)"
            lines.append("      %s/%s: %.1f%% > %.0f%%%s" % (cert, lang.upper(), rate * 100, LEN_BIAS_THRESHOLD * 100, tag))
    if blocking:
        return (False, lines)
    lines.append("  → [PASS] certs LIVE (%s) abaixo do limiar em ambos os idiomas." % ", ".join(sorted(LIVE_CERTS)))
    return (True, lines)


def guard_length_effect_size(bank_path: Path) -> tuple:
    """Guard 11 — Cohen's d between correct-option and distractor-option lengths.

    FAIL if d > 0.50 for any cert (computed on PT option lengths; EN reported too).
    """
    with open(bank_path, encoding="utf-8") as f:
        bank = json.load(f)
    certs_present = sorted({_cert_of(q) for q in bank["questions"]})
    failures = []
    lines = ["[Guarda 11] LENGTH_EFFECT_SIZE — Cohen's d correct vs distractor (limiar: d > %.2f)" % LEN_EFFECT_SIZE_THRESHOLD]
    lines.append("  %-10s %5s %10s %10s %10s %10s" % ("Cert", "N", "PT_d", "EN_d", "PT_mΔ", "EN_mΔ"))
    for cert in certs_present:
        qs = [q for q in bank["questions"] if _cert_of(q) == cert]
        n = 0
        d_pt = 0.0
        d_en = 0.0
        delta_pt = 0.0
        delta_en = 0.0
        for lang, d_ref, delta_ref in (("pt", "d_pt", "delta_pt"), ("en", "d_en", "delta_en")):
            correct_lens = []
            distract_lens = []
            for q in qs:
                opts = (q.get("locales", {}).get(lang) or {}).get("options")
                if not isinstance(opts, list) or len(opts) != 4:
                    continue
                ans = q.get("answer")
                if not isinstance(ans, int) or not (0 <= ans < 4):
                    continue
                lens = [len(o) for o in opts]
                correct_lens.append(lens[ans])
                for i in range(4):
                    if i != ans:
                        distract_lens.append(lens[i])
                n = max(n, len(correct_lens))
            d = _cohen_d(correct_lens, distract_lens)
            if correct_lens and distract_lens:
                m_c = sum(correct_lens) / len(correct_lens)
                m_d = sum(distract_lens) / len(distract_lens)
                delta = m_c - m_d
            else:
                delta = 0.0
            if lang == "pt":
                d_pt, delta_pt = d, delta
            else:
                d_en, delta_en = d, delta
            if d > LEN_EFFECT_SIZE_THRESHOLD:
                failures.append((cert, lang, d))
        lines.append("  %-10s %5d %10.3f %10.3f %10.1f %10.1f" % (
            cert, n, d_pt, d_en, delta_pt, delta_en))
    blocking = [f for f in failures if f[0] in LIVE_CERTS]
    if failures:
        lines.append("  → [FAIL] %d cert/locale(s) com d > %.2f:" % (len(failures), LEN_EFFECT_SIZE_THRESHOLD))
        for cert, lang, d in failures:
            tag = "" if cert in LIVE_CERTS else " (LATENT — não bloqueia CI)"
            lines.append("      %s/%s: d=%.3f > %.2f%s" % (cert, lang.upper(), d, LEN_EFFECT_SIZE_THRESHOLD, tag))
    if blocking:
        return (False, lines)
    lines.append("  → [PASS] certs LIVE (%s) com d ≤ %.2f." % (", ".join(sorted(LIVE_CERTS)), LEN_EFFECT_SIZE_THRESHOLD))
    return (True, lines)


def guard_hedge_ratio(bank_path: Path) -> tuple:
    """Guard 12 — hedge-rate ratio (correct / distractor) per cert, PT + EN.

    FAIL if ratio < 0.5 (correct hedges much less than distractors — the known
    leak where distractors are more absolute) OR ratio > 2.0 (reverse leak).
    """
    with open(bank_path, encoding="utf-8") as f:
        bank = json.load(f)
    certs_present = sorted({_cert_of(q) for q in bank["questions"]})
    failures = []
    lines = ["[Guarda 12] HEDGE_RATIO — correct_hedge%% / distractor_hedge%% (faixa ok: %.1f–%.1f)" % (HEDGE_RATIO_MIN, HEDGE_RATIO_MAX)]
    lines.append("  %-10s %5s %16s %16s" % ("Cert", "N", "PT(c%/d%→r)", "EN(c%/d%→r)"))
    for cert in certs_present:
        qs = [q for q in bank["questions"] if _cert_of(q) == cert]
        row = {"cert": cert, "n": 0, "pt": None, "en": None}
        for lang in ("pt", "en"):
            hset = HEDGE_WORDS_PT if lang == "pt" else HEDGE_WORDS_EN
            h_c = 0
            h_d = 0
            n_c = 0
            n_d = 0
            for q in qs:
                opts = (q.get("locales", {}).get(lang) or {}).get("options")
                if not isinstance(opts, list) or len(opts) != 4:
                    continue
                ans = q.get("answer")
                if not isinstance(ans, int) or not (0 <= ans < 4):
                    continue
                if _has_hedge(opts[ans], hset):
                    h_c += 1
                n_c += 1
                for i in range(4):
                    if i != ans:
                        if _has_hedge(opts[i], hset):
                            h_d += 1
                        n_d += 1
            rc = (h_c / n_c) if n_c else 0.0
            rd = (h_d / n_d) if n_d else 0.0
            ratio = (rc / rd) if rd > 0 else float("inf")
            row[lang] = (rc, rd, ratio, n_c)
            if ratio < HEDGE_RATIO_MIN or ratio > HEDGE_RATIO_MAX:
                failures.append((cert, lang, rc, rd, ratio))
        pt = row["pt"]
        en = row["en"]
        lines.append("  %-10s %5d   %4.1f/%4.1f→%5.2f   %4.1f/%4.1f→%5.2f" % (
            cert, pt[3],
            pt[0] * 100, pt[1] * 100, pt[2],
            en[0] * 100, en[1] * 100, en[2]))
    blocking = [f for f in failures if f[0] in LIVE_CERTS]
    if failures:
        lines.append("  → [FAIL] %d cert/locale(s) fora da faixa [%.1f, %.1f]:" % (len(failures), HEDGE_RATIO_MIN, HEDGE_RATIO_MAX))
        for cert, lang, rc, rd, ratio in failures:
            rstr = "%.3f" % ratio if ratio != float("inf") else "∞"
            tag = "" if cert in LIVE_CERTS else " (LATENT — não bloqueia CI)"
            lines.append("      %s/%s: ratio=%s (correct=%.1f%%, distractor=%.1f%%)%s" % (
                cert, lang.upper(), rstr, rc * 100, rd * 100, tag))
    if blocking:
        return (False, lines)
    lines.append("  → [PASS] certs LIVE (%s) dentro da faixa [%.1f, %.1f]." % (", ".join(sorted(LIVE_CERTS)), HEDGE_RATIO_MIN, HEDGE_RATIO_MAX))
    return (True, lines)


def guard_answer_index_chi2(bank_path: Path) -> tuple:
    """Guard 13 — chi-square goodness-of-fit on answer-index distribution.

    FAIL if p < 0.01 for any cert with ≥ 50 questions.
    """
    with open(bank_path, encoding="utf-8") as f:
        bank = json.load(f)
    certs_present = sorted({_cert_of(q) for q in bank["questions"]})
    failures = []
    skipped = []
    lines = ["[Guarda 13] ANSWER_INDEX_CHI2 — goodness-of-fit vs uniforme (limiar: p < %.3f para certs ≥ %d Q)" % (CHI2_P_THRESHOLD, CHI2_MIN_N)]
    lines.append("  %-10s %5s %7s %7s %7s %7s %9s %6s %8s" % (
        "Cert", "N", "idx0", "idx1", "idx2", "idx3", "chi2", "df", "p"))
    for cert in certs_present:
        qs = [q for q in bank["questions"] if _cert_of(q) == cert]
        ans_counter = Counter()
        for q in qs:
            ans = q.get("answer")
            if isinstance(ans, int) and 0 <= ans < 4:
                ans_counter[ans] += 1
        counts = [ans_counter.get(i, 0) for i in range(4)]
        n = sum(counts)
        if n < CHI2_MIN_N:
            lines.append("  %-10s %5d %7d %7d %7d %7d %9s %6s %8s" % (
                cert, n, counts[0], counts[1], counts[2], counts[3], "—", "—", "skip (<%d)" % CHI2_MIN_N))
            skipped.append((cert, n))
            continue
        chi2, df, p = _chi_square_uniform_p(counts)
        lines.append("  %-10s %5d %7d %7d %7d %7d %9.3f %6d %8.4f" % (
            cert, n, counts[0], counts[1], counts[2], counts[3], chi2, df, p))
        if p < CHI2_P_THRESHOLD:
            failures.append((cert, chi2, p, counts))
    if skipped:
        lines.append("  (skip: %s — n < %d)" % (", ".join("%s(%d)" % (c, n) for c, n in skipped), CHI2_MIN_N))
    blocking = [f for f in failures if f[0] in LIVE_CERTS]
    if failures:
        lines.append("  → [FAIL] %d cert(s) com p < %.3f:" % (len(failures), CHI2_P_THRESHOLD))
        for cert, chi2, p, counts in failures:
            tag = "" if cert in LIVE_CERTS else " (LATENT — não bloqueia CI)"
            lines.append("      %s: chi2=%.3f, p=%.4f, counts=%s%s" % (cert, chi2, p, counts, tag))
    if blocking:
        return (False, lines)
    lines.append("  → [PASS] certs LIVE (%s) com n ≥ %d têm p ≥ %.3f." % (", ".join(sorted(LIVE_CERTS)), CHI2_MIN_N, CHI2_P_THRESHOLD))
    return (True, lines)


def guard_runs_test(bank_path: Path) -> tuple:
    """Guard 14 — Wald-Wolfowitz runs test on the answer-index sequence in bank order.

    FAIL if z < -5.0 (fewer runs than expected → clustering, e.g. CTFL ch5's
    31-consecutive same-answer run).
    """
    with open(bank_path, encoding="utf-8") as f:
        bank = json.load(f)
    certs_present = sorted({_cert_of(q) for q in bank["questions"]})
    failures = []
    lines = ["[Guarda 14] RUNS_TEST — Wald-Wolfowitz sobre 'mesmo-anterior?' (limiar: z < %.1f)" % RUNS_Z_THRESHOLD]
    lines.append("  %-10s %5s %8s %10s %9s %8s" % ("Cert", "N", "runs", "expected", "z", "verdict"))
    # Also flag the longest consecutive same-answer run, for human context.
    for cert in certs_present:
        qs = [q for q in bank["questions"] if _cert_of(q) == cert]
        seq = [q.get("answer") for q in qs if isinstance(q.get("answer"), int) and 0 <= q.get("answer") < 4]
        n = len(seq)
        if n < 2:
            lines.append("  %-10s %5d %8s %10s %9s %8s" % (cert, n, "—", "—", "—", "skip"))
            continue
        runs, mu, z, n1, n2 = _runs_test_z(seq)
        # longest consecutive same-answer run (context only)
        longest = 1
        cur = 1
        for i in range(1, n):
            if seq[i] == seq[i - 1]:
                cur += 1
                if cur > longest:
                    longest = cur
            else:
                cur = 1
        verdict = "FAIL" if z < RUNS_Z_THRESHOLD else "ok"
        lines.append("  %-10s %5d %8d %10.1f %9.2f %8s (longest_same_run=%d)" % (
            cert, n, runs, mu, z, verdict, longest))
        if z < RUNS_Z_THRESHOLD:
            failures.append((cert, z, runs, mu, longest))
    blocking = [f for f in failures if f[0] in LIVE_CERTS]
    if failures:
        lines.append("  → [FAIL] %d cert(s) com z < %.1f (clustering detectado):" % (len(failures), RUNS_Z_THRESHOLD))
        for cert, z, runs, mu, longest in failures:
            tag = "" if cert in LIVE_CERTS else " (LATENT — não bloqueia CI)"
            lines.append("      %s: z=%.2f (runs=%d, expected=%.1f, longest_same_run=%d)%s" % (
                cert, z, runs, mu, longest, tag))
    if blocking:
        return (False, lines)
    lines.append("  → [PASS] certs LIVE (%s) com z ≥ %.1f." % (", ".join(sorted(LIVE_CERTS)), RUNS_Z_THRESHOLD))
    return (True, lines)


def guard_blueprint_match(bank_path: Path) -> tuple:
    """Guard 15 — blueprint match: chapter distribution + K-level validation.

    Chapter check (only for certs WITH meta.chapterWeights):
      Compute exam-weight-% from chapterWeights and bank-actual-%; FAIL if any
      chapter mismatches by > 15 percentage points.

    K-level check (for every cert with meta.certifications[cert].kLevels):
      FAIL if any declared K-level has 0 questions OR any present K-level is
      not in the declared list.
    """
    with open(bank_path, encoding="utf-8") as f:
        bank = json.load(f)
    meta = bank.get("meta") or {}
    certs_present = sorted({_cert_of(q) for q in bank["questions"]})
    failures = []
    lines = ["[Guarda 15] BLUEPRINT_MATCH — drift capítulos vs meta.chapterWeights + validação K-levels"]
    # ---- chapter-weight drift ----
    lines.append("  [chapter-weight drift]")
    lines.append("  %-10s %18s %18s %12s %8s" % ("Cert", "ch", "exam_wt%", "bank_act%", "Δpp")
                 )
    for cert in certs_present:
        cw = _get_chapter_weights(meta, cert)
        if cw is None:
            lines.append("  %-10s %18s" % (cert, "(sem chapterWeights no meta — skip com warning)"))
            continue
        qs = [q for q in bank["questions"] if _cert_of(q) == cert]
        n_total = len(qs)
        bank_counts = Counter(str(q.get("chapter")) for q in qs)
        wt_sum = sum(cw.values()) or 1
        for ch in sorted(cw.keys(), key=lambda x: (int(x) if str(x).isdigit() else 999, str(x))):
            exam_pct = (cw[ch] / wt_sum) * 100.0
            bank_pct = (bank_counts.get(ch, 0) / n_total * 100.0) if n_total else 0.0
            diff = exam_pct - bank_pct
            flag = "FAIL" if abs(diff) > BLUEPRINT_PP_THRESHOLD else "ok"
            lines.append("  %-10s %18s %17.2f%% %17.2f%% %8.2f %6s" % (
                cert, "ch%s" % ch, exam_pct, bank_pct, diff, flag))
            if abs(diff) > BLUEPRINT_PP_THRESHOLD:
                failures.append(("%s ch%s" % (cert, ch), "chapter drift %.2fpp > %.0fpp" % (abs(diff), BLUEPRINT_PP_THRESHOLD)))
        # bank chapters not in chapterWeights → warning (not a hard fail)
        extra = set(bank_counts.keys()) - set(cw.keys())
        if extra:
            lines.append("  %-10s %18s %s" % (
                cert, "(warning)", "capítulos no bank mas ausentes do chapterWeights: %s" % sorted(extra)))
    # ---- K-level validation ----
    lines.append("  [K-level validation]")
    lines.append("  %-10s %20s %20s %8s" % ("Cert", "declared", "present", "verdict"))
    for cert in certs_present:
        declared = _get_declared_klevels(meta, cert)
        if not declared:
            lines.append("  %-10s %20s" % (cert, "(sem meta.certifications[cert].kLevels — skip com warning)"))
            continue
        declared_ints = sorted({_klevel_to_int(k) for k in declared if _klevel_to_int(k) is not None})
        qs = [q for q in bank["questions"] if _cert_of(q) == cert]
        present_ints = sorted({q.get("kLevel") for q in qs
                               if isinstance(q.get("kLevel"), int)})
        # declared but missing in bank
        missing = [k for k in declared_ints if k not in present_ints]
        # present in bank but not declared
        undeclared = [k for k in present_ints if k not in declared_ints]
        verdict = "ok"
        if missing:
            verdict = "FAIL"
            failures.append(("%s klevel" % cert,
                             "K-levels declarados sem questões: K%s" % ",".join(str(k) for k in missing)))
        if undeclared:
            verdict = "FAIL"
            failures.append(("%s klevel" % cert,
                             "K-levels presentes mas não declarados: K%s" % ",".join(str(k) for k in undeclared)))
        lines.append("  %-10s %20s %20s %8s" % (
            cert,
            "K" + ",K".join(str(k) for k in declared_ints) if declared_ints else "—",
            "K" + ",K".join(str(k) for k in present_ints) if present_ints else "—",
            verdict))
    blocking = [f for f in failures if f[0].split(" ")[0] in LIVE_CERTS]
    if failures:
        lines.append("  → [FAIL] %d problema(s) de blueprint:" % len(failures))
        for where, why in failures:
            tag = "" if where.split(" ")[0] in LIVE_CERTS else " (LATENT — não bloqueia CI)"
            lines.append("      %s: %s%s" % (where, why, tag))
    if blocking:
        return (False, lines)
    lines.append("  → [PASS] certs LIVE (%s) com chapterWeights dentro de ±%.0fpp e K-levels consistentes." % (", ".join(sorted(LIVE_CERTS)), BLUEPRINT_PP_THRESHOLD))
    return (True, lines)


# Registry mapping CLI name → (guard function, display name)
_GUARD_FUNCS = {
    "length_bias": guard_length_bias,
    "length_effect_size": guard_length_effect_size,
    "hedge_ratio": guard_hedge_ratio,
    "answer_index_chi2": guard_answer_index_chi2,
    "runs_test": guard_runs_test,
    "blueprint_match": guard_blueprint_match,
}


def run_new_guards(bank_path: Path, selected: list) -> tuple:
    """Run the selected new guards. Returns (passed_count, failed_count, failed_names)."""
    passed = 0
    failed = 0
    failed_names = []
    print()
    print("=" * 80)
    print("NOVOS GUARDS PSICOMÉTRICOS (F1.3)")
    print("=" * 80)
    for cli_name in selected:
        func = _GUARD_FUNCS[cli_name]
        ok, lines = func(bank_path)
        for ln in lines:
            print(ln)
        print()
        if ok:
            passed += 1
        else:
            failed += 1
            failed_names.append(cli_name)
    return (passed, failed, failed_names)


# ============================================================================
# Orchestration / main
# ============================================================================

def run_existing_guards(args, bank_path: Path, baseline_file: Path, topic_baseline_file: Path) -> bool:
    """Run the original guards 0/1/2 exactly as before. Returns True if the
    script should continue (i.e. no early sys.exit happened), False otherwise.

    Note: this function mirrors the original main() logic verbatim; the only
    change is that it does NOT call sys.exit on threshold failure — instead it
    returns False so the caller can decide to still run the new guards and then
    exit. (Baseline-update modes DO sys.exit here, preserving original behavior.)
    """
    # --- Guard 0: structural, deterministic, zero tolerance ---
    dup_ids = check_duplicate_ids(bank_path)
    if dup_ids:
        print(f"FALHA: {len(dup_ids)} ID(s) duplicado(s): {dup_ids}")
        sys.exit(1)

    bad_answers = check_invalid_answers(bank_path)
    if bad_answers:
        print(f"FALHA: {len(bad_answers)} questão(ões) com answer/schema inválido: {bad_answers}")
        sys.exit(1)

    # --- Guard 1: option vs. explanation (heuristic, with baseline) ---
    suspects = check(bank_path)
    baseline_ids = load_baseline(baseline_file)
    new_suspects = [s for s in suspects if s["id"] not in baseline_ids]

    if args.update_baseline:
        save_baseline(suspects, baseline_file)
        print(f"Baseline (opção/exp) atualizada com {len(suspects)} id(s) em {baseline_file}")
        if not args.update_topic_baseline:
            sys.exit(0)

    print(f"[Guarda opção/exp | {args.bank_file}] {len(suspects)} suspeita(s) total | "
          f"{len(baseline_ids)} na baseline | {len(new_suspects)} NOVA(S) (threshold: {args.threshold})\n")
    if new_suspects:
        print("ATENÇÃO: heurística de alerta, NÃO prova de bug. Leia PT/EN par a par antes de corrigir.\n")
        for s in new_suspects:
            print(f"  {s['id']}: answer={s['answer']} -> {s['opcao_atual_en']!r}")
            print(f"    sugestão (não confirmada): índice {s['indice_sugerido']} -> {s['opcao_sugerida_en']!r}")

    # --- Guard 2: topic PT/EN (heuristic, with baseline) ---
    topic_result = check_topic(bank_path)
    if not topic_result:
        topic_suspects, mean, std, threshold_val, total = [], 0, 0, 0, 0
    else:
        topic_suspects, mean, std, threshold_val, total = topic_result
    topic_baseline_ids = load_topic_baseline(topic_baseline_file)
    new_topic_suspects = [s for s in topic_suspects if s["id"] not in topic_baseline_ids]

    if args.update_topic_baseline:
        save_topic_baseline(topic_suspects, topic_baseline_file)
        print(f"Baseline (tema) atualizada com {len(topic_suspects)} id(s) em {topic_baseline_file}")
        sys.exit(0)

    print(f"\n[Guarda tema | {args.bank_file}] {total} questões bilíngues | média={mean} desvio={std} limiar={threshold_val}")
    print(f"  {len(topic_suspects)} suspeita(s) total | {len(topic_baseline_ids)} na baseline | "
          f"{len(new_topic_suspects)} NOVA(S)\n")
    if new_topic_suspects:
        print("Suspeitas de desalinhamento de TEMA:\n")
        for s in new_topic_suspects:
            print(f"  {s['id']}: similaridade={s['score']} (média banco={s['media_banco']})")

    total_new = len(new_suspects) + len(new_topic_suspects)
    if total_new > args.threshold:
        print(f"\nFALHA: {total_new} suspeita(s) NOVA(S) excedem o threshold de {args.threshold}.")
        return False
    print(f"\nOK: {total_new} suspeita(s) nova(s), dentro do threshold de {args.threshold}.")
    return True


def _parse_guards(spec: str) -> list:
    """Parse 'length_bias,hedge_ratio' → ['length_bias','hedge_ratio'].
    Validates against the registry; unknown names raise SystemExit with a helpful message.
    """
    if not spec:
        return [name for name, _, _ in NEW_GUARD_REGISTRY]
    names = [s.strip().lower() for s in spec.split(",") if s.strip()]
    valid = {name for name, _, _ in NEW_GUARD_REGISTRY}
    invalid = [n for n in names if n not in valid]
    if invalid:
        print(f"ERRO: --guards recebeu nome(s) desconhecido(s): {invalid}")
        print("  Guards válidos: %s" % ", ".join(name for name, _, _ in NEW_GUARD_REGISTRY))
        sys.exit(2)
    # Preserve canonical order
    return [name for name, _, _ in NEW_GUARD_REGISTRY if name in set(names)]


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("bank_positional", nargs="?", default=None,
                        help="arquivo de banco a analisar (forma posicional; sobrescreve --bank-file)")
    parser.add_argument("--bank-file", type=str, default="ctfl-questions-ptbr.json",
                        help="arquivo de banco a analisar")
    parser.add_argument("--threshold", type=int, default=0,
                        help="número de suspeitas NOVAS toleradas (default: 0)")
    parser.add_argument("--update-baseline", action="store_true")
    parser.add_argument("--update-topic-baseline", action="store_true")
    parser.add_argument("--guards", type=str, default=None,
                        help="rodar apenas os novos guards listados (csv). Ex.: --guards length_bias,hedge_ratio. "
                             "Use --list-guards para ver todos.")
    parser.add_argument("--list-guards", action="store_true",
                        help="lista os novos guards disponíveis e sai")
    args = parser.parse_args()

    if args.list_guards:
        print("Novos guards psicométricos disponíveis (--guards name1,name2,...):")
        for name, display, num in NEW_GUARD_REGISTRY:
            print("  %-22s  (Guarda %d)  %s" % (name, num, display))
        sys.exit(0)

    # Resolve bank file (positional overrides --bank-file)
    bank_file_name = args.bank_positional if args.bank_positional else args.bank_file
    args.bank_file = bank_file_name  # used by existing guard print messages

    bank_path = Path(__file__).parent / bank_file_name
    if not bank_path.exists():
        # Allow absolute paths too
        alt = Path(bank_file_name)
        if alt.exists():
            bank_path = alt
        else:
            print(f"ERRO: arquivo de banco não encontrado: {bank_file_name}")
            sys.exit(2)
    bank_stem = bank_file_name.replace(".json", "")
    baseline_file = Path(__file__).parent / f"check_alignment_baseline.{bank_stem}.json"
    topic_baseline_file = Path(__file__).parent / f"check_alignment_topic_baseline.{bank_stem}.json"

    # Parse --guards
    selected_guards = _parse_guards(args.guards) if args.guards else [n for n, _, _ in NEW_GUARD_REGISTRY]

    # Baseline-update modes take precedence (preserve original behavior exactly)
    if args.update_baseline or args.update_topic_baseline:
        run_existing_guards(args, bank_path, baseline_file, topic_baseline_file)
        sys.exit(0)  # run_existing_guards sys.exits internally if needed

    # --guards filter mode: skip existing guards entirely, run only listed new guards
    if args.guards:
        passed, failed, failed_names = run_new_guards(bank_path, selected_guards)
        print("=" * 80)
        print(f"RESUMO: {passed}/{len(selected_guards)} guard(s) passed, {failed} failed.")
        if failed_names:
            print("  Failed: %s" % ", ".join(failed_names))
        print("=" * 80)
        sys.exit(1 if failed > 0 else 0)

    # Default mode: run existing guards, then all new guards
    existing_ok = run_existing_guards(args, bank_path, baseline_file, topic_baseline_file)
    passed, failed, failed_names = run_new_guards(bank_path, selected_guards)
    print("=" * 80)
    print(f"RESUMO: {passed}/6 new guards passed, {failed} failed. "
          f"(existing guards: {'PASS' if existing_ok else 'FAIL'})")
    if failed_names:
        print("  Failed new guards: %s" % ", ".join(failed_names))
    print("=" * 80)
    # Exit 1 if EITHER existing guards failed (threshold exceeded) OR any new guard failed
    sys.exit(1 if (not existing_ok or failed > 0) else 0)


if __name__ == "__main__":
    main()
