import copy
import json
import unittest
from pathlib import Path

from apply_editorial_batch import apply


class EditorialBatchTests(unittest.TestCase):
    def test_patch_preserves_identity_answers_pools_and_other_certificates(self):
        batch = json.loads((Path(__file__).parent / 'editorial/ctaltm-batch-01.json').read_text())
        original = {'meta': {'version': '1.6.0-ctaltm'}, 'questions': []}
        for ident in [*batch['updates'], *batch['reviewed_unchanged'], 'ctfl-example']:
            original['questions'].append({
                'id': ident, 'cert': 'CTFL' if ident == 'ctfl-example' else 'CTAL-TM',
                'answer': 2, 'pool': 'study', 'chapter': 1, 'kLevel': 2, 'lo': 'TM-1.1.1',
                'locales': {lang: {'q': 'question', 'options': ['a','b','c','d'], 'exp': 'explanation'} for lang in ('pt','en')},
            })
        snapshot = copy.deepcopy(original)
        result = apply(original, batch)
        self.assertEqual(original, snapshot)
        self.assertEqual(result['meta']['version'], '1.6.1-editorial.1')
        for before, after in zip(original['questions'], result['questions']):
            for key in ('id', 'cert', 'answer', 'pool', 'chapter', 'kLevel', 'lo'):
                self.assertEqual(before[key], after[key])
            if before['id'] not in batch['updates']:
                self.assertEqual(before, after)
            else:
                for lang in ('pt','en'):
                    self.assertEqual(after['locales'][lang]['options'], batch['updates'][before['id']][lang])
                    self.assertEqual(after['locales'][lang]['q'], before['locales'][lang]['q'])
        self.assertEqual(apply(result, batch), result)


if __name__ == '__main__':
    unittest.main()
