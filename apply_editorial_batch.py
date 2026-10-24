"""Apply an explicitly reviewed, ID-scoped bilingual options patch."""
import argparse
import copy
import json
from pathlib import Path


def apply(bank, batch):
    result = copy.deepcopy(bank)
    by_id = {q['id']: q for q in result['questions']}
    if len(by_id) != len(result['questions']):
        raise ValueError('Duplicate IDs')
    for ident, update in batch['updates'].items():
        q = by_id[ident]
        if q['cert'] != 'CTAL-TM':
            raise ValueError('Unexpected certificate')
        for lang in ('pt', 'en'):
            options = update[lang]
            if len(options) != 4 or len(set(options)) != 4 or any(not s.strip() for s in options):
                raise ValueError('Invalid options')
            q['locales'][lang]['options'] = options
            if 'explanations' in update:
                q['locales'][lang]['exp'] = update['explanations'][lang]
    result['meta']['version'] = '1.6.1-editorial.1'
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('batch', type=Path)
    args = parser.parse_args()
    path = Path(__file__).with_name('synapse-question-bank.json')
    bank = json.loads(path.read_text())
    if bank['meta']['version'] not in ('1.6.0-ctaltm', '1.6.1-editorial.1'):
        parser.error('Unexpected input version; reconcile before applying')
    result = apply(bank, json.loads(args.batch.read_text()))
    path.write_text(json.dumps(result, ensure_ascii=False, indent=1) + '\n')
    print('Applied eight reviewed bilingual question patches; remaining editorial debt is not waived')
