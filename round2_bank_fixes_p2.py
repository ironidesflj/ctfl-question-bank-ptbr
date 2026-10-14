#!/usr/bin/env python3
"""Fase A.2 — limpa as 57 citações restantes (formas que escaparam da fase A):
   1. PT/EN com parêntese NUMÉRICO curto: "A opção B (18) seria..." → "A opção “18” seria..."
   2. EN bare com "Option" maiúsculo: "Option B describes..." → "Another option describes..."
      (ou snippet, quando o verbo não é "describes" ou a letra é o gabarito)
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
FILES = [ROOT / "synapse-question-bank.json", ROOT / "ctfl-questions-ptbr.json"]

def snippet(text, limit=48):
    t = " ".join(str(text).split())
    if len(t) <= limit:
        return t
    cut = t[:limit]
    if " " in cut:
        cut = cut[: cut.rfind(" ")]
    return cut + "…"

PAT_PT_SHORTPAREN = re.compile(r"\b([Aa]\s+)op[çc][ãa]o\s+([A-D])\s*\(([^)]{1,2})\)")
PAT_EN_SHORTPAREN = re.compile(r"\b([Tt]he\s+)?[Oo]ption\s+([A-D])\s*\(([^)]{1,2})\)")
PAT_EN_BARE_CI = re.compile(r"\b([Tt]he\s+)?([Oo]ption)s?\s+([A-D])\b(?!\s*\()")
PAT_PT_BARE_CI = re.compile(r"\b([Aa]\s+)?(op[çc][ãa]o|alternativa)\s+([A-D])\b(?!\s*[(0-9])")

def fix_pt_shortparen(m, options):
    letter, paren = m.group(2), m.group(3).strip()
    idx = ord(letter) - 65
    s = snippet(options[idx]) if 0 <= idx < len(options) else paren
    art = m.group(1)
    # se o parêntese é exatamente o valor da opção, ele é absorvido pelo snippet
    if s.strip() == paren or paren in s:
        return f"{art}opção “{s}”"
    return f"{art}opção “{s}” ({paren})"

def fix_en_shortparen(m, options):
    letter, paren = m.group(2), m.group(3).strip()
    idx = ord(letter) - 65
    s = snippet(options[idx]) if 0 <= idx < len(options) else paren
    art = m.group(1) or ("The " if m.group(0).startswith("Option") or m.group(0).startswith("The") else "the ")
    if s.strip() == paren or paren in s:
        return f"{art}option “{s}”"
    return f"{art}option “{s}” ({paren})"

def fix_en_bare(m, options, answer, following):
    letter = m.group(3)
    idx = ord(letter) - 65
    art = m.group(1) or ("The " if m.group(2)[0].isupper() else "the ")
    s = snippet(options[idx]) if 0 <= idx < len(options) else None
    if s is None:
        return m.group(0)
    # "Another option describes X" quando X é um distrator e o verbo é "describes"
    if idx != answer and re.match(r"\s*describes\b", following, re.IGNORECASE):
        return ("Another option" if m.group(2)[0].isupper() else "another option")
    return f"{art}option “{s}”"

def fix_pt_bare(m, options, answer, following):
    letter = m.group(3)
    idx = ord(letter) - 65
    starts_upper = m.group(0)[0] in "AO"
    art = m.group(1) or ("A " if starts_upper else "a ")
    s = snippet(options[idx]) if 0 <= idx < len(options) else None
    if s is None:
        return m.group(0)
    if idx != answer and re.match(r"\s*descreve\b", following, re.IGNORECASE):
        return ("Outra opção" if starts_upper else "outra opção")
    return f"{art}opção “{s}”"

def main():
    grand = 0
    all_data = {}
    for path in FILES:
        data = json.loads(path.read_text(encoding="utf-8"))
        n_file = 0
        for q in data["questions"]:
            ans = q["answer"]
            for lang in ["pt", "en"]:
                loc = q["locales"].get(lang)
                if not loc:
                    continue
                exp = loc.get("exp", "")
                opts = loc.get("options", [])
                # 1) short-paren primeiro (mais específico)
                if lang == "pt":
                    exp2 = PAT_PT_SHORTPAREN.sub(lambda m: fix_pt_shortparen(m, opts), exp)
                else:
                    exp2 = PAT_EN_SHORTPAREN.sub(lambda m: fix_en_shortparen(m, opts), exp)
                # 2) bare com IGNORECASE efetivo, olhando o que vem depois
                def en_repl(m, opts=opts, ans=ans):
                    following = exp2[m.end():m.end() + 20]
                    return fix_en_bare(m, opts, ans, following)
                def pt_repl(m, opts=opts, ans=ans):
                    following = exp2[m.end():m.end() + 20]
                    return fix_pt_bare(m, opts, ans, following)
                if lang == "pt":
                    exp3 = PAT_PT_BARE_CI.sub(pt_repl, exp2)
                else:
                    exp3 = PAT_EN_BARE_CI.sub(en_repl, exp2)
                if exp3 != exp:
                    loc["exp"] = exp3
                    n_file += 1
        all_data[path] = data
        grand += n_file
        print(f"[{path.name}] questões×idioma ajustadas: {n_file}")

    # verificação final — zero citações (nos dados JÁ modificados, em memória)
    pat = re.compile(r"\b(?:op[çc][ãa]o|options?|alternativas?|letras?|choices?)\s+[A-D]\b", re.IGNORECASE)
    leftovers = 0
    for path, data in all_data.items():
        for q in data["questions"]:
            for lang in ["pt", "en"]:
                exp = q["locales"].get(lang, {}).get("exp", "")
                for m in pat.finditer(exp):
                    tail = exp[m.end():m.end() + 8]
                    if not re.match(r"\s*(about|sobre)", tail, re.IGNORECASE):
                        leftovers += 1
                        if leftovers <= 10:
                            print(f"  RESTA {q['id']}[{lang}]: …{exp[max(0,m.start()-25):m.end()+25]}…")
    if leftovers:
        print(f"✗ ainda restam {leftovers} citações — NÃO salvar")
        sys.exit(1)
    print("✓ zero citações por letra em ambos os arquivos")

    for path, data in all_data.items():
        path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("✓ arquivos salvos")

if __name__ == "__main__":
    main()
