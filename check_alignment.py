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
import sys
import argparse
from difflib import SequenceMatcher
from pathlib import Path

BANK_FILE = Path(__file__).parent / "ctfl-questions-ptbr.json"
BASELINE_FILE = Path(__file__).parent / "check_alignment_baseline.json"
DEFAULT_THRESHOLD = 0  # qualquer suspeita NOVA (fora da baseline) já merece revisão


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def check(bank_path: Path = BANK_FILE):
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


def load_baseline():
    if not BASELINE_FILE.exists():
        return set()
    with open(BASELINE_FILE, encoding="utf-8") as f:
        data = json.load(f)
    return set(data.get("ids", []))


def save_baseline(suspects):
    data = {
        "_comentario": "Falsos positivos conhecidos da heuristica de similaridade, confirmados manualmente como CORRETOS (PT/EN alinhados). Gerado por check_alignment.py --update-baseline.",
        "ids": sorted(s["id"] for s in suspects),
    }
    with open(BASELINE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--threshold", type=int, default=DEFAULT_THRESHOLD,
                         help=f"número de suspeitas NOVAS (fora da baseline) tolerado sem falhar (default: {DEFAULT_THRESHOLD})")
    parser.add_argument("--update-baseline", action="store_true",
                         help="aceita o estado atual como nova baseline (use só após revisão manual confirmando que são falsos positivos)")
    args = parser.parse_args()

    suspects = check()
    baseline_ids = load_baseline()
    new_suspects = [s for s in suspects if s["id"] not in baseline_ids]

    if args.update_baseline:
        save_baseline(suspects)
        print(f"Baseline atualizada com {len(suspects)} id(s) em {BASELINE_FILE}")
        sys.exit(0)

    print(f"{len(suspects)} suspeita(s) no total | {len(baseline_ids)} na baseline | "
          f"{len(new_suspects)} NOVA(S) (threshold: {args.threshold})\n")

    if new_suspects:
        print("ATENÇÃO: heurística de alerta, NÃO prova de bug. Leia PT/EN par a par antes de corrigir.\n")
        for s in new_suspects:
            print(f"  {s['id']}: answer={s['answer']} -> {s['opcao_atual_en']!r}")
            print(f"    sugestão (não confirmada): índice {s['indice_sugerido']} -> {s['opcao_sugerida_en']!r}")

    if len(new_suspects) > args.threshold:
        print(f"\nFALHA: {len(new_suspects)} suspeita(s) NOVA(S) excede o threshold de {args.threshold}.")
        print("Revise manualmente. Se forem falsos positivos confirmados, rode com --update-baseline.")
        sys.exit(1)

    print(f"\nOK: {len(new_suspects)} suspeita(s) nova(s), dentro do threshold de {args.threshold}.")
    sys.exit(0)


if __name__ == "__main__":
    main()
