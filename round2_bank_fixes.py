#!/usr/bin/env python3
"""
Fase E2E-Round2 — correções no banco de questões:
  Fase A: reescreve TODAS as citações por letra (opção A / Option B / alternativa C /
          Options A, C, and D) em referências por TEMA — imunes ao shuffle de opções
          que o app aplica em runtime.
  Fase B: rebalanceia o viés de gabarito do CTAL-TM (124/26/25/25 → 50/50/50/50),
          movendo a opção correta de índice 0 para outras posições (PT e EN juntos).
  Fase C: bump de versão do meta e verificação final.

Rodar na raiz do repo do banco. Idempotente por construção (se não achar os
padrões, não altera nada). Escreve diff-resumo no stdout para revisão manual.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parent
SYNAPSE = ROOT / "synapse-question-bank.json"
CTFL_ONLY = ROOT / "ctfl-questions-ptbr.json"

def snippet(text, limit=48):
    t = " ".join(str(text).split())
    if len(t) <= limit:
        return t
    cut = t[:limit]
    if " " in cut:
        cut = cut[: cut.rfind(" ")]
    return cut + "…"

# ── padrões de citação por letra (word-boundary, sem "about/sobre" seguinte) ──
PAT_PT_PAREN = re.compile(r"\b([AaÀà]\s+)(?:op[çc][ãa]o|alternativa)\s+([A-D])\s*\(([^)]{3,90})\)")
PAT_PT_BARE = re.compile(r"\b([Aa]\s+(?:outra\s+|última\s+)?)?(?:op[çc][ãa]o|alternativa)\s+([A-D])\b(?!\s*\()")
PAT_EN_PAREN = re.compile(r"\b([Tt]he\s+)?([Oo]ption)\s+([A-D])\s*\(([^)]{3,90})\)")
PAT_EN_LIST = re.compile(r"\b[Oo]ptions\s+([A-D])\s*(?:,|and)\s*([A-D])(?:\s*(?:,|and)\s*([A-D]))?\b")
PAT_EN_BARE = re.compile(r"\b([Tt]he\s+)?option\s+([A-D])\b(?!\s*\()")
PAT_PT_LIST = re.compile(r"\b(?:[Oo]p[çc][õo]es|[Aa]lternativas)\s+([A-D])\s*(?:,|e)\s*([A-D])(?:\s*(?:,|e)\s*([A-D]))?\b")

def rewrite_exp(exp, options, is_correct_idx):
    """Substitui citações por letra por referências por tema. Retorna (novo_exp, n_subst)."""
    n = 0
    out = exp

    def opt_snippet(idx):
        if 0 <= idx < len(options):
            return snippet(options[idx])
        return None

    # 1) PT com parêntese temático: "A opção A (tema) ..." → "A opção “tema” ..."
    def pt_paren(m):
        nonlocal n
        n += 1
        return f"{m.group(1)}opção “{m.group(3).strip()}”"
    out = PAT_PT_PAREN.sub(pt_paren, out)

    # 2) EN com parêntese temático: "Option A (theme) is..." → "The option “theme” is..."
    def en_paren(m):
        nonlocal n
        n += 1
        art = m.group(1) or ("The " if m.group(2)[0].isupper() else "the ")
        return f"{art}option “{m.group(4).strip()}”"
    out = PAT_EN_PAREN.sub(en_paren, out)

    # 3) Listas: "Options B, C, and D ..." / "Opções A, C e D ..." → "The other options" /
    #    "As demais opções" — SÓ se nenhuma letra listada é o gabarito.
    def en_list(m):
        nonlocal n
        letters = [x for x in m.groups()[1:] if x] if False else [m.group(1), m.group(2), m.group(3)]
        idxs = [ord(L) - 65 for L in letters if L]
        if any(i == is_correct_idx for i in idxs):
            return m.group(0)
        n += 1
        return "The other options" if m.group(0)[0].isupper() else "the other options"
    out = PAT_EN_LIST.sub(en_list, out)

    def pt_list(m):
        nonlocal n
        letters = [m.group(1), m.group(2), m.group(3)]
        idxs = [ord(L) - 65 for L in letters if L]
        if any(i == is_correct_idx for i in idxs):
            return m.group(0)
        n += 1
        return "As demais opções" if m.group(0)[0].isupper() else "as demais opções"
    out = PAT_PT_LIST.sub(pt_list, out)

    # 4) PT bare: "A opção B é/descreve..." → "A opção “<snippet da opção B>” ..."
    def pt_bare(m):
        nonlocal n
        idx = ord(m.group(2)) - 65
        s = opt_snippet(idx)
        if s is None:
            return m.group(0)
        n += 1
        art = "A " if m.group(0)[0] in "AÁ" or m.group(0)[0].isupper() else "a "
        return f"{art}opção “{s}”"
    out = PAT_PT_BARE.sub(pt_bare, out)

    # 5) EN bare: "Option B describes..." → "The option “<snippet>” describes..."
    def en_bare(m):
        nonlocal n
        idx = ord(m.group(2)) - 65
        s = opt_snippet(idx)
        if s is None:
            return m.group(0)
        n += 1
        art = m.group(1) or ("The " if m.group(0)[0].isupper() else "the ")
        return f"{art}option “{s}”"
    out = PAT_EN_BARE.sub(en_bare, out)

    return out, n

def process_bank(data, label):
    total_subst = 0
    changed_qs = 0
    for q in data["questions"]:
        ans = q["answer"]
        for lang in ["pt", "en"]:
            loc = q["locales"].get(lang)
            if not loc:
                continue
            new_exp, n = rewrite_exp(loc.get("exp", ""), loc.get("options", []), ans)
            if n:
                loc["exp"] = new_exp
                total_subst += n
                changed_qs += 1
    print(f"[{label}] reescritas por tema: {total_subst} citações em {changed_qs} questões×idioma")
    return total_subst

def rebalance_ctaltm(data):
    """Distribui gabaritos do CTAL-TM de 124/26/25/25 para 50/50/50/50."""
    ctaltm = [q for q in data["questions"] if q.get("cert") == "CTAL-TM"]
    dist = Counter(q["answer"] for q in ctaltm)
    print(f"[CTAL-TM] distribuição ANTES: {dict(sorted(dist.items()))}")
    target = {0: 50, 1: 50, 2: 50, 3: 50}
    moved = []
    # questões com answer=0 em ordem de id; as excedentes migram para 1/2/3
    zeros = sorted([q for q in ctaltm if q["answer"] == 0], key=lambda q: q["id"])
    excess = len(zeros) - target[0]
    # quantas cada destino precisa receber
    need = {t: target[t] - dist.get(t, 0) for t in (1, 2, 3)}
    plan = []
    for t in (1, 2, 3):
        plan += [t] * need[t]
    for q, t in zip(zeros[len(zeros) - excess:], plan):
        move_answer(q, t)
        moved.append((q["id"], 0, t))
    dist2 = Counter(q["answer"] for q in ctaltm)
    print(f"[CTAL-TM] distribuição DEPOIS: {dict(sorted(dist2.items()))} (movidas: {len(moved)})")
    assert dist2 == Counter({0: 50, 1: 50, 2: 50, 3: 50}), "rebalance não fechou em 50/50/50/50"
    return moved

def move_answer(q, new_idx):
    """Move a opção correta para new_idx preservando a ordem relativa dos distratores.
    Aplica a MESMA transformação em PT e EN (opções são indexadas igualmente)."""
    old_idx = q["answer"]
    assert old_idx != new_idx
    for lang in ["pt", "en"]:
        opts = q["locales"][lang]["options"]
        correct = opts[old_idx]
        distractors = [o for i, o in enumerate(opts) if i != old_idx]
        new_opts = list(distractors)
        new_opts.insert(new_idx, correct)
        assert len(new_opts) == len(opts)
        assert len(set(new_opts)) == len(new_opts), f"opções duplicadas em {q['id']}/{lang}"
        q["locales"][lang]["options"] = new_opts
    q["answer"] = new_idx

def verify(data, label):
    problems = []
    ids = [q["id"] for q in data["questions"]]
    dup_ids = [i for i, c in Counter(ids).items() if c > 1]
    if dup_ids:
        problems.append(f"IDs duplicados: {dup_ids[:5]}")
    pat = re.compile(
        r"\b(?:op[çc][ãa]o|options?|alternativas?|letras?|choices?)\s+[A-D]\b",
        re.IGNORECASE,
    )
    leftovers = []
    for q in data["questions"]:
        for lang in ["pt", "en"]:
            loc = q["locales"].get(lang, {})
            exp = loc.get("exp", "")
            # ignora os já-temáticos "the option about X"
            m = pat.search(exp)
            if m and not re.match(r"\s*(about|sobre)", exp[m.end():m.end()+8], re.IGNORECASE):
                leftovers.append(f"{q['id']}[{lang}]: …{exp[max(0,m.start()-20):m.end()+20]}…")
            n_opts = len(loc.get("options", []))
            if not (0 <= q["answer"] < n_opts):
                problems.append(f"{q['id']}: answer {q['answer']} fora de {n_opts} opções")
            if len(set(loc.get("options", []))) != n_opts:
                problems.append(f"{q['id']}[{lang}]: opções duplicadas")
    if leftovers:
        print(f"[{label}] ⚠ citações por letra RESTANTES: {len(leftovers)}")
        for l in leftovers[:10]:
            print("   ", l)
    else:
        print(f"[{label}] ✓ zero citações por letra restantes")
    if problems:
        print(f"[{label}] ✗ PROBLEMAS:")
        for p in problems[:10]:
            print("   ", p)
        sys.exit(1)
    print(f"[{label}] ✓ verificação estrutural OK")

def main():
    syn = json.loads(SYNAPSE.read_text(encoding="utf-8"))
    ctfl = json.loads(CTFL_ONLY.read_text(encoding="utf-8"))

    print("═" * 60)
    print("FASE A — reescrita de citações por letra → tema")
    print("═" * 60)
    process_bank(syn, "synapse")
    process_bank(ctfl, "ctfl-only")

    print()
    print("═" * 60)
    print("FASE B — rebalance CTAL-TM")
    print("═" * 60)
    rebalance_ctaltm(syn)

    print()
    print("═" * 60)
    print("FASE C — meta + persistência")
    print("═" * 60)
    syn["meta"]["version"] = "1.4.0-e2e-round2"
    syn["meta"]["generatedDate"] = "2026-10-14"
    ctfl["meta"]["version"] = syn["meta"]["version"]
    ctfl["meta"]["generatedDate"] = syn["meta"]["generatedDate"]

    verify(syn, "synapse")
    verify(ctfl, "ctfl-only")

    SYNAPSE.write_text(json.dumps(syn, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    CTFL_ONLY.write_text(json.dumps(ctfl, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print()
    print("✓ arquivos salvos")

if __name__ == "__main__":
    main()
