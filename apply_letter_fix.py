"""
Aplica as reescritas da Spec 3 (desalinhamento de letra) nos dois arquivos
de banco. Testado e verificado pelo Lead contra os arquivos reais antes de
ser entregue — ver diff-stat esperado no briefing.

Rodar da raiz do repo ctfl-question-bank-ptbr:
    python3 apply_letter_fix.py \
        --audit letter-misalignment-audit-v2.json \
        --candidates letter-misalignment-candidates.json
"""
import argparse, json, sys
from pathlib import Path

def patch_file(path: Path, vps: list, cands: dict, ids_scope: set, label: str) -> bool:
    if not path.exists():
        print(f"[{label}] ABORT — arquivo não encontrado: {path}")
        return False
    raw = path.read_text(encoding="utf-8")

    errors = []
    replacements = []

    for a in vps:
        qid = a["id"]
        if qid not in ids_scope:
            continue
        c = cands[qid]
        old_pt = json.dumps(c["exp_pt"], ensure_ascii=False)
        new_pt = json.dumps(a["exp_pt_novo"], ensure_ascii=False)
        cnt = raw.count(old_pt)
        if cnt != 1:
            errors.append((qid, "pt", f"anchor_count={cnt}"))
        else:
            replacements.append((old_pt, new_pt, qid, "pt"))

        old_en = json.dumps(c["exp_en"], ensure_ascii=False)
        new_en = json.dumps(a["exp_en_novo"], ensure_ascii=False)
        cnt = raw.count(old_en)
        if cnt != 1:
            errors.append((qid, "en", f"anchor_count={cnt}"))
        else:
            replacements.append((old_en, new_en, qid, "en"))

    if errors:
        print(f"[{label}] ABORT — {len(errors)} âncora(s) falharam, ZERO escritas:")
        for e in errors[:30]:
            print("  ", e)
        return False

    new_raw = raw
    for old_frag, new_frag, qid, lang in replacements:
        assert new_raw.count(old_frag) == 1, f"âncora mudou de contagem em runtime: {qid}/{lang}"
        new_raw = new_raw.replace(old_frag, new_frag, 1)

    path.write_text(new_raw, encoding="utf-8")
    print(f"[{label}] OK — {len(replacements)} campo(s) trocado(s) ({len(replacements)//2} questões x pt+en)")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audit", default="letter-misalignment-audit-v2.json")
    ap.add_argument("--candidates", default="letter-misalignment-candidates.json")
    args = ap.parse_args()

    audit = json.loads(Path(args.audit).read_text(encoding="utf-8"))
    cands = {c["id"]: c for c in json.loads(Path(args.candidates).read_text(encoding="utf-8"))["candidates"]}
    vps = [a for a in audit if a["veredito"] == "VERDADEIRO_POSITIVO"]

    if len(vps) != 98:
        print(f"ABORT — esperado 98 VERDADEIRO_POSITIVO, encontrado {len(vps)}. Parando sem escrever nada.")
        sys.exit(1)

    synapse_ids = set(a["id"] for a in vps)
    ok1 = patch_file(Path("synapse-question-bank.json"), vps, cands, synapse_ids, "synapse-question-bank.json")

    ctfl_ids = set(a["id"] for a in vps if a["id"].split("-")[0].startswith("ch"))
    ok2 = patch_file(Path("ctfl-questions-ptbr.json"), vps, cands, ctfl_ids, "ctfl-questions-ptbr.json")

    sys.exit(0 if (ok1 and ok2) else 1)


if __name__ == "__main__":
    main()
