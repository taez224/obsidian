import importlib.util
import json
from datetime import date
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest

spec = importlib.util.spec_from_file_location('reading', Path(__file__).with_name('reading.py'))
r = importlib.util.module_from_spec(spec);spec.loader.exec_module(r)


def item(i, score=.85, features=(), source='arXiv', kind='study'):
    values = {k: {'choice': 'present' if k in features else 'unknown', 'confidence': .9} for k in r.FEATURES}
    values['kind'] = {'choice': kind, 'confidence': .9}
    return {'title': 'Different topic ' + str(i), 'url': f'https://example.org/{i}', 'date':'2026-09-26',
            'summary': 'Public abstract ' + str(i), 'source': source, 'comprehension_debt': score, 'features': values}


class ReadingTests(unittest.TestCase):
    def test_canonical_duplicate_versions(self):
        a = item(1);b = item(2)
        a['url']='http://arxiv.org/abs/2609.12345v2';b['url']='https://huggingface.co/papers/2609.12345'
        self.assertEqual(len(r.dedupe([a,b])),1)
        self.assertEqual(r.canonical('https://doi.org/10.1234/ABC'), 'https://doi.org/10.1234/abc')

    def test_explicit_intro_alias_excludes_saved_article(self):
        with tempfile.TemporaryDirectory() as d:
            vault=Path(d);folder=vault/'30_Resources/References/Clippings';folder.mkdir(parents=True)
            (folder/'a.md').write_text('source: https://original.org/post\n\n> [!note] 저장 맥락\n> GeekNews 소개글(https://news.hada.io/topic?id=42)에서 원문을 저장했다.\n\n다른 인용 https://news.hada.io/topic?id=43\n')
            aliases=r.source_aliases(vault)
            self.assertEqual(aliases,{'https://news.hada.io/topic?id=42':'https://original.org/post'})
            a=item(1);a['url']='https://news.hada.io/topic?id=42';b=item(2);b['url']='https://original.org/post'
            rows=r.dedupe([a,b],aliases)
            self.assertEqual(len(rows),1)
            self.assertFalse(r.eligible(rows[0],{}, {'https://original.org/post'},date(2026,9,26),r.DEFAULT))

    def test_unclassified_model_unknown_low_confidence_separate(self):
        class Client:
            def system_one(self,state,questions,model):
                cs={k:SimpleNamespace(choice='unknown',confidence=.9,probabilities={'unknown':.9}) for k in questions}
                cs['delayed']=SimpleNamespace(choice='present',confidence=.4,probabilities={'present':.6})
                return SimpleNamespace(choices=cs,usage=SimpleNamespace(input_tokens=1))
        with tempfile.TemporaryDirectory() as d:
            missing=item(2);missing['summary']=''
            rows,usage=r.classify([item(1),missing],Path(d),r.DEFAULT,Client())
            self.assertEqual(rows[0]['features']['professionals']['assessment'],'model_unknown')
            self.assertEqual(rows[0]['features']['delayed']['assessment'],'low_confidence')
            self.assertEqual(rows[1]['classification_status'],'no_summary')
            self.assertNotIn('features', rows[1])

    def test_unknown_is_not_absence(self):
        x=item(1,features=['delayed']);x['features']['delayed']['confidence']=.4
        self.assertEqual(r.feature_values(x,r.DEFAULT),set())
        self.assertIn('Never infer absence',r.question_contract()['delayed']['criteria']['unknown'])

    def test_bundle_budget_and_reference_gap(self):
        ref=item('ref',features=['understanding'])
        old=item('old',.91,features=['understanding'])
        novel=item('novel',.80,features=['delayed','unassisted','professionals'])
        cfg={**r.DEFAULT,'reading_minutes':15}
        result=r.select_bundle([ref,old,novel],{}, {ref['url']},date(2026,9,26),cfg)
        self.assertEqual(result['selected'][0]['url'],novel['url'])
        self.assertEqual(result['reading_minutes'],15)
        self.assertEqual(result['baseline'][0]['url'],old['url'])
        self.assertEqual(result['reference_features'],{'understanding':1})

    def test_saved_reference_without_date_is_retained(self):
        with tempfile.TemporaryDirectory() as d:
            x=item('saved',features=['delayed']);x['date']=''
            _,result=r.make_report([x],Path(d),{},saved_urls=[x['url']],today=date(2026,9,26))
            self.assertEqual(result['reference_count'],1)
            self.assertEqual(result['selected'],[])

    def test_no_reference_no_gap_claim(self):
        out=r.select_bundle([item(1)],{},set(),date(2026,9,26),r.DEFAULT)
        self.assertEqual(out['reference_count'],0)
        self.assertEqual(out['reference_features'],{})

    def test_shown_is_not_read_and_snooze_expires(self):
        x=item(1);ev=[{'url':x['url'],'action':'shown','at':'2026-09-26T00:00:00Z'}]
        state=r.feedback_state(ev)
        self.assertTrue(r.eligible(x,state,set(),date(2026,9,26),r.DEFAULT))
        ev.append({'url':x['url'],'action':'not_now','at':'2026-09-26T01:00:00Z'})
        self.assertFalse(r.eligible(x,r.feedback_state(ev),set(),date(2026,9,27),r.DEFAULT))
        self.assertTrue(r.eligible(x,r.feedback_state(ev),set(),date(2026,10,3),r.DEFAULT))
        ev.append({'url':x['url'],'action':'read','at':'2026-09-27T01:00:00Z'})
        self.assertFalse(r.eligible(x,r.feedback_state(ev),set(),date(2026,10,3),r.DEFAULT))

    def test_explicit_feedback_shrinkage(self):
        xs=[item(i,features=['delayed']) for i in range(8)]
        states={x['url']:{'rating':'useful'} for x in xs}
        small,n=r.affinity(xs[:7],states,r.DEFAULT)
        self.assertEqual(small['delayed'],1)
        learned,n=r.affinity(xs,states,r.DEFAULT)
        self.assertGreater(learned['delayed'],1)
        self.assertLess(learned['delayed'],1.25)
        self.assertEqual(learned['professionals'],1)

    def test_uncertain_failures_and_cache_no_api(self):
        class Client:
            calls=0
            def system_one(self,state,questions,model):
                self.calls+=1
                choices={k:SimpleNamespace(choice='present' if k!='kind' else 'study',confidence=.3,
                                           probabilities={'present':.5,'unknown':.5}) for k in questions}
                return SimpleNamespace(choices=choices,usage=SimpleNamespace(input_tokens=200))
        with tempfile.TemporaryDirectory() as d:
            client=Client();out=Path(d)
            rows,usage=r.classify([item(1)],out,r.DEFAULT,client)
            self.assertEqual(rows[0]['features']['delayed']['choice'],'unknown')
            rows,usage=r.classify([item(1)],out,r.DEFAULT,client)
            self.assertEqual(client.calls,1);self.assertEqual(usage['cache_hits'],1)
            self.assertNotEqual(r.cache_key(item(1),r.DEFAULT),r.cache_key(item(1),{**r.DEFAULT,'model':'new'}))
            rows,usage=r.classify([item(2)],out,{**r.DEFAULT,'max_cost_usd':0},client)
            self.assertEqual(client.calls,1);self.assertEqual(usage['errors'][0]['error'],'budget_limit')

    def test_replay_preserves_feedback_and_exploration(self):
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)
            r.add_feedback(out,'https://example.org/a','not_now','2026-09-26T00:00:00Z')
            before=(out/'reading-feedback.jsonl').read_bytes()
            a=item('a');b=item('b',.1)
            report,result=r.make_report([a,b],out,{},today=date(2026,9,26))
            self.assertEqual(before,(out/'reading-feedback.jsonl').read_bytes())
            self.assertEqual(result['exploration'][0]['url'],b['url'])
            self.assertEqual(result['usage']['api_calls'],0)
            self.assertIn('기준 자료가 없어',report)


if __name__=='__main__':unittest.main()
