"""Validate and simulate agent proposals; never change the canonical bank."""
import copy
import json
import tempfile
from collections import Counter
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from check_alignment import NEW_GUARD_REGISTRY, _GUARD_FUNCS


def review():
    bank = json.loads((ROOT / 'synapse-question-bank.json').read_text())
    current = {q['id']: q for q in bank['questions']}
    candidate = copy.deepcopy(bank)
    proposed = {q['id']: q for q in candidate['questions']}
    seen = set()
    counts = Counter()
    pending = []
    for number in range(2, 8):
        path = ROOT / 'editorial' / f'ctaltm-proposal-{number}-r2.json'
        batch = json.loads(path.read_text())
        expected = {f'ctaltm-{i}' for i in range(batch['range'][0], batch['range'][1] + 1)}
        actual = [r['id'] for r in batch['reviews']]
        assert len(actual) == len(set(actual)) and set(actual) == expected, path
        for row in batch['reviews']:
            ident = row['id']
            assert ident not in seen, ident
            seen.add(ident)
            q = current[ident]
            assert q['cert'] == 'CTAL-TM' and row['answer'] == q['answer'], ident
            counts[row['status']] += 1
            for lang in ('pt', 'en'):
                options = row.get(lang, q['locales'][lang]['options'])
                assert lang in row or row['status'] == 'UNCHANGED', ident
                assert len(options) == 4 and len(set(options)) == 4, ident
                assert all(isinstance(s, str) and s.strip() for s in options), ident
            if row['status'] not in ('REVISED', 'UNCHANGED'):
                pending.append({'id': ident, 'status': row['status'], 'reason': row['reason']})
                continue
            if row['status'] == 'REVISED':
                for lang in ('pt', 'en'):
                    proposed[ident]['locales'][lang]['options'] = row[lang]
                    if 'explanations' in row:
                        proposed[ident]['locales'][lang]['exp'] = row['explanations'][lang]
    assert seen == {f'ctaltm-{i}' for i in range(13, 201)}
    guards = {}
    with tempfile.TemporaryDirectory(prefix='synapse-r2-') as directory:
        target = Path(directory) / 'synapse-question-bank.json'
        target.write_text(json.dumps(candidate, ensure_ascii=False))
        for baseline in ROOT.glob('*baseline*.json'):
            (Path(directory) / baseline.name).write_bytes(baseline.read_bytes())
        for name, _, _ in NEW_GUARD_REGISTRY:
            passed, evidence = _GUARD_FUNCS[name](target)
            guards[name] = {'passed_for_live_certs': passed, 'evidence': evidence}
    return {'scope': 'Simulation only; structural validation is not semantic approval',
            'coverage': len(seen), 'statuses': dict(counts), 'pending_semantic_decisions': pending,
            'guards': guards, 'canonical_bank_changed': False}


if __name__ == '__main__':
    report = review()
    output = ROOT / 'editorial' / 'round2-validation.json'
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))
