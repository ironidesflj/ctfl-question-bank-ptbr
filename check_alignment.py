# -*- coding: utf-8 -*-
"""
check_alignment.py — heurística de alerta para desalinhamento PT/EN no banco.

USO:
  python3 check_alignment.py                  # compara contra a baseline, falha só em suspeitas NOVAS
  python3 check_alignment.py --update-baseline  # aceita o estado atual como baseline (use após revisão manual)
  python3 check_alignment.py --threshold N     # ajusta quantas suspeitas NOVAS são toleradas (default: 0)

O que faz:
  Para cada questão com locales.en, compara cada opção EN com a explicação
  EN usando SequenceMatcher. Se a opção com maior similaridade textual à
  explicação não for a opção apontada por `answer`, a questão é marcada
  como SUSPEITA.

IMPORTANTE — limitações conhecidas (não é uma prova de bug):
  - Esta heurística tem falsos positivos CONHECIDOS e estruturais: opções
    muito curtas/numéricas, ou explicações que não compartilham vocabulário
    com a opção correta mesmo estando tudo certo. No banco totalmente
    corrigido (2026-06), ela ainda sinaliza ~34 questões que foram
    manualmente confirmadas como CORRETAS — esse é o "ruído de fundo".
  - Por isso o script usa uma BASELINE (check_alignment_baseline.json):
    ele só falha quando aparecem suspeitas NOVAS (ids que não estavam na
    baseline), não pelo total absoluto. Isso evita que o ruído conhecido
    quebre o CI para sempre, mas ainda pega regressões reais introduzidas
    por expansões futuras do banco.
  - Esta ferramenta NUNCA corrige nada automaticamente. Toda suspeita nova
    deve ser lida manualmente (PT vs EN, par a par) antes de decidir
    corrigir — exatamente como foi feito nas correções de 2026-06
    (77 questões de tema + 87 de índice de resposta).

Saída:
  - Lista de suspeitas novas (fora da baseline) com a opção atual e a
    sugestão da heurística, para revisão humana.
  - Exit code 0 se nº de suspeitas novas <= threshold, 1 caso contrário.
"""

import json
import math
import sys
import argparse
from difflib import SequenceMatcher
from pathlib import Path

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
    """Detecta desalinhamento de TEMA entre pt.q e en.q usando z-score da similaridade.

    Marca como suspeita qualquer questão com similaridade(pt.q, en.q) abaixo de
    (média - 1.5 × desvio_padrão) do banco. Limiar adaptativo: não usa número fixo,
    reflete a distribuição real do banco.
    """
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
    from collections import Counter
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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bank-file", type=str, default="ctfl-questions-ptbr.json",
                         help="arquivo de banco a analisar")
    parser.add_argument("--threshold", type=int, default=0,
                         help="número de suspeitas NOVAS toleradas (default: 0)")
    parser.add_argument("--update-baseline", action="store_true")
    parser.add_argument("--update-topic-baseline", action="store_true")
    args = parser.parse_args()

    bank_path = Path(__file__).parent / args.bank_file
    bank_stem = args.bank_file.replace(".json", "")
    baseline_file = Path(__file__).parent / f"check_alignment_baseline.{bank_stem}.json"
    topic_baseline_file = Path(__file__).parent / f"check_alignment_topic_baseline.{bank_stem}.json"

    # --- Guarda 0: estrutural, determinística, ZERO tolerância, roda antes de tudo ---
    dup_ids = check_duplicate_ids(bank_path)
    if dup_ids:
        print(f"FALHA: {len(dup_ids)} ID(s) duplicado(s): {dup_ids}")
        sys.exit(1)

    bad_answers = check_invalid_answers(bank_path)
    if bad_answers:
        print(f"FALHA: {len(bad_answers)} questão(ões) com answer/schema inválido: {bad_answers}")
        sys.exit(1)

    # --- Guarda 1: opção vs. explicação (heurística, com baseline) ---
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

    # --- Guarda 2: tema PT/EN (heurística, com baseline) ---
    topic_suspects, mean, std, threshold_val, total = check_topic(bank_path)
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
        sys.exit(1)
    print(f"\nOK: {total_new} suspeita(s) nova(s), dentro do threshold de {args.threshold}.")
    sys.exit(0)


if __name__ == "__main__":
    main()
