import importlib.util
from datetime import date
from pathlib import Path
import sys
import tempfile
from types import ModuleType, SimpleNamespace
import unittest

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))


def load(name):
    spec = importlib.util.spec_from_file_location(name, HERE / f'{name}.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


c = load('central')
r = load('reading')
compose = load('compose')
claims = load('claims')

CFG = {**c.DEFAULT, 'enabled': True}
INTERESTS = {'topic': {'question': 'Does this item discuss the topic?'}}


def item(url, noul, central=None, source='arXiv'):
    x = {'title': 'Title ' + url, 'url': url, 'summary': 'Abstract', 'source': source, 'topic': noul}
    if central is not None:
        x['central'] = {'topic': {'score': central, 'confidence': .8}}
    return x


class CentralTests(unittest.TestCase):
    def test_only_candidates_over_floor_are_asked(self):
        self.assertEqual(c.targets(item('a', .7), INTERESTS, CFG), ['topic'])
        self.assertEqual(c.targets(item('b', .5), INTERESTS, CFG), [])
        self.assertIn('Topic: Does this item', c.question_specs(item('a', .7), INTERESTS, CFG)['topic']['instructions'])

    def test_trial_mode_keeps_noul_selection(self):
        passing_mention = item('a', .95, central=.1)
        self.assertTrue(c.selectable(passing_mention, 'topic', .8, CFG))
        self.assertFalse(c.selectable(item('b', .7, central=1.9), 'topic', .8, CFG))
        self.assertEqual(c.rank_key(passing_mention, 'topic', CFG), (-.95,))

    def test_apply_mode_filters_passing_mentions_and_ranks_by_centrality(self):
        cfg = {**CFG, 'apply': True}
        self.assertFalse(c.selectable(item('a', .95, central=.1), 'topic', .8, cfg))
        self.assertTrue(c.selectable(item('b', .7, central=1.9), 'topic', .8, cfg))
        # 중심도 판정이 없으면 기존 Noul 문턱으로 돌아간다
        self.assertTrue(c.selectable(item('c', .85), 'topic', .8, cfg))
        self.assertFalse(c.selectable(item('d', .7), 'topic', .8, cfg))
        ranked = sorted([item('x', .95, 1.0), item('y', .7, 1.9)], key=lambda x: c.rank_key(x, 'topic', cfg))
        self.assertEqual([x['url'] for x in ranked], ['y', 'x'])

    def test_label_and_promoted(self):
        self.assertEqual(c.label(item('a', .9, .4), 'topic', CFG), '중심도 0.4 스쳐 언급')
        self.assertEqual(c.label(item('a', .9, 1.2), 'topic', CFG), '중심도 1.2 부분')
        self.assertEqual(c.label(item('a', .9, 1.8), 'topic', CFG), '중심도 1.8 중심')
        self.assertEqual(c.label(item('a', .9), 'topic', CFG), '')
        pool = [item('shown', .7, 1.9), item('low', .7, 1.2), item('best', .66, 2.0), item('over', .9, 2.0), item('next', .75, 1.6)]
        self.assertEqual([x['url'] for x in c.promoted(pool, 'topic', .8, CFG, exclude={'shown'})], ['best', 'next'])

    def test_attach_records_scores_and_errors(self):
        sdk = ModuleType('typesafe_sdk')
        sdk.Score = lambda **kw: kw
        sys.modules['typesafe_sdk'] = sdk

        class Client:
            def system_one(self, state, questions, model):
                if state['title'].endswith('boom'):
                    raise RuntimeError('boom')
                return SimpleNamespace(scores={k: SimpleNamespace(score=1.234, confidence=.9) for k in questions},
                                       usage=SimpleNamespace(input_tokens=100))

        items = [item('ok', .9), item('boom', .9), item('skip', .3)]
        self.assertEqual(c.attach(items, INTERESTS, Client(), CFG, workers=1), 100)
        self.assertEqual(items[0]['central'], {'topic': {'score': 1.23, 'confidence': .9}})
        self.assertIn('boom', items[1]['central_error'])
        self.assertNotIn('central', items[2])

    def test_annotated_line_still_parses(self):
        x = item('https://example.org/p', .91, 1.8)
        line = f"- [ ] {x['topic']:.2f} · {c.label(x, 'topic', CFG)} [{x['title']}]({x['url']}) - {x['source']} 관심밖"
        m = compose.ITEM.match(line)
        self.assertEqual(m[3], 'https://example.org/p')
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'list.md'
            path.write_text(line + '\n')
            self.assertEqual([v['action'] for v in claims.checkbox_controls(path).values()], ['off_topic'])


class ReadingCentralTests(unittest.TestCase):
    def bundle(self, apply):
        cfg = {**r.DEFAULT, 'max_bundle': 1, 'central': {**CFG, 'apply': apply}}
        a = {**item('https://example.org/a', .95, .2), 'comprehension_debt': .95, 'date': '2026-09-26'}
        b = {**item('https://example.org/b', .7, 1.9), 'comprehension_debt': .7, 'date': '2026-09-26'}
        for x in (a, b):
            x['central'] = {'comprehension_debt': x.pop('central')['topic']}
        return r.select_bundle([a, b], {}, set(), date(2026, 9, 30), cfg)['selected']

    def test_trial_mode_keeps_noul_ranking(self):
        self.assertEqual([x['url'] for x in self.bundle(False)], ['https://example.org/a'])

    def test_apply_mode_drops_passing_mention(self):
        self.assertEqual([x['url'] for x in self.bundle(True)], ['https://example.org/b'])


if __name__ == '__main__':
    unittest.main()
