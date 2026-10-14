#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""r13 — Partição exclusiva de pools: ESTUDO × SIMULADO.

Requisito: as questões usadas nos simulados de cada certificação NUNCA podem
aparecer nos modos de estudo (quiz, erradas, salvas, SRS, pontos fracos).
As de estudo, por definição, também nunca entram nos simulados.

DECISÃO DE DESIGN (ver meta.poolSplit no JSON de saída):
- Particionar o banco AUDITADO existente em vez de redigir questões novas:
  qualidade já verificada (check_alignment.py, ledger FASE4), origem 100%
  oficial (syllabus ISTQB), zero risco de alucinação e custo determinístico.
- Pool de simulado = F conjuntos do blueprint oficial (capítulo × K-level,
  ISTQB Exam Structures & Rules): garante provas fiéis ao exame real e
  F provas disjuntas para retomadas.
- Sem inflar dificuldade artificial: a dificuldade oficial É o blueprint
  (K-mix) — a exclusividade já elimina o efeito de memorização.

Execução (idempotente — re-rodar gera exatamente o mesmo resultado):
  python3 partition_pools.py
"""
import json
import sys
from collections import Counter, defaultdict

BANK = "synapse-question-bank.json"
SEED = 0x5A12E5  # fixo: partição determinística e reproduzível entre árvores
FORMS = 2         # provas completas disjuntas garantidas por célula

def mulberry32(seed):
    state = seed & 0xFFFFFFFF
    def rnd():
        nonlocal state
        state = (state + 0x6D2B79F5) & 0xFFFFFFFF
        t = state
        t = ((t ^ (t >> 15)) * t) & 0xFFFFFFFF
        t = ((t ^ (t >> 7)) * (t | 0x61C88647)) & 0xFFFFFFFF
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296
    return rnd

def pick_balanced(candidates, need, rnd):
    """Seleciona `need` questões da célula com gabarito equilibrado.

    Embaralha com PRNG semeado e escolhe greedy preferindo o índice de
    gabarito menos representado até o momento (anti-viés do banco — o
    CTAL-TM historicamente concentra alternativas no índice 0).
    Determinístico: mesma seed ⇒ mesma seleção.
    """
    order = sorted(candidates, key=lambda q: q["id"])  # estabilidade pré-shuffle
    arr = list(order)
    for i in range(len(arr) - 1, 0, -1):
        j = int(rnd() * (i + 1))
        arr[i], arr[j] = arr[j], arr[i]
    picked = []
    counts = Counter()
    while len(picked) < need and arr:
        # alvo: distribuição mais plana possível de gabaritos
        target = (len(picked) + 1) // 4 + (1 if (len(picked) + 1) % 4 else 0)
        idx = next((k for k, q in enumerate(arr) if counts[q["answer"]] < target), 0)
        q = arr.pop(idx)
        counts[q["answer"]] += 1
        picked.append(q)
    return picked

def main():
    with open(BANK, encoding="utf-8") as f:
        bank = json.load(f)
    meta = bank["meta"]
    questions = bank["questions"]
    blueprints = meta.get("examBlueprint") or {}

    # limpa marcações anteriores (idempotência)
    for q in questions:
        q.pop("pool", None)

    rnd = mulberry32(SEED)
    report = {}
    problems = []

    for cert_id, bp in sorted(blueprints.items()):
        cert_qs = [q for q in questions if str(q.get("cert", "")).lower() == cert_id]
        if not cert_qs:
            problems.append(f"{cert_id}: cert sem questões")
            continue
        cells = defaultdict(list)  # (chapter, k) -> [questões]
        for q in cert_qs:
            cells[(str(q["chapter"]), "K%d" % q["kLevel"])].append(q)
        exam_ids = set()
        for ch, spec in sorted(bp["chapters"].items(), key=lambda kv: int(kv[0])):
            for k, want_n in sorted((spec.get("kLevels") or {}).items()):
                want = int(want_n or 0)
                if want <= 0:
                    continue
                pool = cells.get((str(ch), k), [])
                need = min(FORMS * want, len(pool))
                if len(pool) < want:
                    problems.append(f"{cert_id} ch{ch} {k}: pool {len(pool)} < blueprint {want}")
                    need = len(pool)
                elif len(pool) < FORMS * want:
                    print(f"  aviso: {cert_id} ch{ch} {k}: pool {len(pool)} < {FORMS}×{want} (usando {need})")
                for q in pick_balanced(pool, need, rnd):
                    exam_ids.add(q["id"])
        # marca pools (explícito nos dois lados — dado auto-documentável)
        for q in cert_qs:
            q["pool"] = "exam" if q["id"] in exam_ids else "study"
        n_exam = len(exam_ids)
        n_study = len(cert_qs) - n_exam
        # células do blueprint precisam continuar atendíveis (≥1×) no pool de exame
        for ch, spec in bp["chapters"].items():
            for k, want_n in (spec.get("kLevels") or {}).items():
                want = int(want_n or 0)
                if want <= 0:
                    continue
                have = sum(1 for q in cert_qs if q["pool"] == "exam"
                           and str(q["chapter"]) == str(ch) and "K%d" % q["kLevel"] == k)
                if have < want:
                    problems.append(f"{cert_id} ch{ch} {k}: pool de exame {have} < blueprint {want}")
        report[cert_id] = {"exam": n_exam, "study": n_study, "total": len(cert_qs)}
        print(f"{cert_id}: {n_exam} de simulado (exclusivas) + {n_study} de estudo = {len(cert_qs)}")

    # certs sem blueprint ficam 100% estudo (não há simulado p/ eles ainda)
    for q in questions:
        q.setdefault("pool", "study")

    # ── validações dura ────────────────────────────────────────────────
    ids = [q["id"] for q in questions]
    assert len(ids) == len(set(ids)) == 1100, "total de questões mudou!"
    per_cert = Counter(q["cert"] for q in questions)
    assert dict(per_cert) == {"CTFL": 300, "CTFL-AT": 200, "CTAL-TA": 200,
                              "CTAL-TM": 200, "CT-AI": 200}, "distribuição por cert mudou!"
    assert all(q["pool"] in ("study", "exam") for q in questions), "pool inválido"
    # invariante central: cada questão pertence a EXATAMENTE um pool
    assert all(isinstance(q["pool"], str) for q in questions)
    for cert_id, r in report.items():
        assert r["exam"] + r["study"] == r["total"], cert_id
    if problems:
        print("FALHOU:", *problems, sep="\n  ")
        sys.exit(1)

    meta["poolSplit"] = {
        "source": "partition_pools.py (seed fixa, determinístico)",
        "seed": SEED,
        "forms": FORMS,
        "rule": "pool de simulado = F×blueprint por célula (capítulo × K-level), "
                "gabarito balanceado; o resto é pool de estudo. Certs sem "
                "examBlueprint ficam 100% estudo até ganharem blueprint.",
        "perCert": report,
        "generatedDate": "2026-10-14",
    }
    meta["version"] = "1.5.0-pools"

    with open(BANK, "w", encoding="utf-8") as f:
        json.dump(bank, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("OK — pools gravados. Re-executar split-bank.mjs nas árvores do app.")

if __name__ == "__main__":
    main()
