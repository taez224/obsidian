import unittest
import tempfile
from datetime import date
from pathlib import Path
from unittest.mock import patch

from compose import DEFAULT, discover, josa, make_page, pair, parse_report, render, skim
from claims import checkbox_controls
from reading import canonical

REPORT = """# Jev 레이더 2026-09-28

## 요즘 관심사: Jev

### 활용 사례

- [ ] 12점 · [A](https://a.example) - Hacker News
- [ ] 6점 · [B](https://b.example) - Hacker News
- [ ] ★733 · [C](https://c.example) - GitHub

### 소식·논의

- [ ] 125점 · [D](https://d.example) - Hacker News

## 요즘 관심사: Muse

### 활용 사례

- 없음

### 소식·논의

- [ ] 143점 · [E](https://e.example) - Hacker News

## 이해 부채

관련 노트: x

- [ ] 0.81 [F](https://f.example) - arXiv
- [ ] 0.92 [G](https://g.example) - GeekNews

## 이번 주 AI

### 화제

- 495점 [H](https://h.example) - Hacker News
- 추천 231 [I](https://i.example) - Hugging Face Papers

## 믿고 보는 저자

- 없음
"""


class ComposeTest(unittest.TestCase):
    def test_skim_takes_one_case_per_source_and_orders_interest_by_score(self):
        sections = dict(skim(parse_report(REPORT, {"이해 부채"}), DEFAULT))
        self.assertEqual([x["title"] for x in sections["요즘 관심사: Jev"]], ["A", "C", "D"])
        self.assertEqual([x["title"] for x in sections["요즘 관심사: Muse"]], ["E"])
        self.assertEqual([x["title"] for x in sections["관심 질문 근처"]], ["G", "F"])
        self.assertEqual([x["title"] for x in sections["화제"]], ["H"])  # HF 논문은 화제 훑어보기에 넣지 않는다
        self.assertNotIn("믿고 보는 저자", sections)

    def test_pair_prefers_narrow_claim(self):
        link = lambda claim: {"claim": claim, "p": 0.9, "confidence": 0.9, "sentence": "s"}
        items = [{"url": "n1", "links": [link("넓은 주장"), link("좁은 주장")]}]
        refs = [{"card": f"r{i}", "links": [link("넓은 주장")]} for i in range(5)] + \
               [{"card": "narrow", "links": [link("좁은 주장")]}]
        self.assertEqual(pair(items, refs, DEFAULT)["n1"], ("narrow", "좁은 주장"))

    def test_pair_uses_each_ref_once(self):
        link = {"claim": "c", "p": 0.9, "confidence": 0.9, "sentence": "s"}
        items = [{"url": "n1", "links": [link]}, {"url": "n2", "links": [link]}]
        chosen = pair(items, [{"card": "only", "links": [link]}], DEFAULT)
        self.assertEqual(len(chosen), 1)

    def test_pair_ignores_weak_item_links(self):
        items = [{"url": "n1", "links": [{"claim": "c", "p": 0.95, "confidence": 0.3, "sentence": "s"}]}]
        refs = [{"card": "r", "links": [{"claim": "c", "p": 0.95, "confidence": 0.9, "sentence": "s"}]}]
        self.assertEqual(pair(items, refs, DEFAULT), {})

    def test_josa(self):
        self.assertEqual(josa("만든다"), "와")
        self.assertEqual(josa("역량"), "과")


class DiscoveryTest(unittest.TestCase):
    REPORT = REPORT.replace("## 믿고 보는 저자\n\n- 없음", """## 믿고 보는 저자

- [T1](https://t.example/1) - Author One, 2026-10-01
- [T2](https://t.example/2) - Author Two, 2026-10-02
- [T3](https://t.example/3) - Author Three, 2026-10-03
""")

    def setUp(self):
        self.groups = parse_report(self.REPORT, {"이해 부채"})
        self.sections = skim(self.groups, DEFAULT)

    @staticmethod
    def items(sections):
        return [x for _, items in sections for x in items]

    def test_replaces_one_slot_without_more_recommendations(self):
        selected = discover(self.sections, self.groups, DEFAULT)
        self.assertEqual(len(self.items(selected)), len(self.items(self.sections)))
        extra = dict(selected)["다른 글도 한 편"]
        self.assertEqual([x["title"] for x in extra], ["T3"])
        self.assertEqual(len(dict(selected)["관심 질문 근처"]), 1)
        self.assertIn("믿고 보는 저자", extra[0]["discovery_reason"])
        self.assertEqual(len(dict(self.sections)["관심 질문 근처"]), 2)  # 원본을 바꾸지 않음

    def test_known_claim_link_is_excluded_but_missing_link_is_not_a_rejection(self):
        linked = self.REPORT.replace("- [T3](https://t.example/3) - Author Three, 2026-10-03",
                                   '- [T3](https://t.example/3) - Author Three, 2026-10-03\n    - → [[기존 주장]] ← "s"')
        groups = parse_report(linked, {"이해 부채"})
        self.assertTrue(groups[("trusted",)][-1]["claim_linked"])
        self.assertEqual(discover(skim(groups, DEFAULT), groups, DEFAULT), self.sections[: -1] + [
            ("믿고 보는 저자", groups[("trusted",)][:2])])

    def test_news_does_not_need_to_be_a_practical_case(self):
        cfg = {**DEFAULT, "topic_news": 0, "trusted": 0}
        groups = {k: v for k, v in self.groups.items() if k != ("trusted",)}
        selected = discover(skim(groups, cfg), groups, cfg)
        extra = dict(selected)["다른 글도 한 편"][0]
        self.assertEqual(extra["title"], "D")
        self.assertIn("활용 사례 여부와 별개", extra["discovery_reason"])

    def test_claim_link_in_another_section_excludes_the_same_article(self):
        for url, title in [
            ("https://t.example/3", "T3"),
            ("https://t.example/3/?utm_source=feed#part", "다른 제목"),
            ("https://reprint.example/article", "T3"),
        ]:
            with self.subTest(url=url, title=title):
                report = self.REPORT.replace(
                    "## 이번 주 AI",
                    '- [ ] 0.80 [T3](https://t.example/3) - GeekNews\n'
                    '    - → [[기존 주장]] ← "관련 근거"\n\n## 이번 주 AI',
                ).replace("[T3](https://t.example/3) - Author Three",
                          f"[{title}]({url}) - Author Three")
                report += "\n- [T4](https://t.example/4) - Author Four, 2026-10-04\n"
                groups = parse_report(report, {"이해 부채"})
                cfg = {**DEFAULT, "interest": 1}
                sections = skim(groups, cfg)
                selected = discover(sections, groups, cfg)
                self.assertEqual([x["title"] for x in dict(selected)["다른 글도 한 편"]], ["T4"])
                self.assertEqual(len(self.items(selected)), len(self.items(sections)))

    def test_saved_prepared_read_and_negative_feedback_are_not_rediscovered(self):
        url = canonical("https://t.example/3")
        today = date(2026, 10, 21)
        for excluded, state in [
            (["https://t.example/3/?utm_source=test#part"], {}),
            ([], {url: {"read": "2026-10-20"}}),
            ([], {url: {"saved": "2026-10-20"}}),
            ([], {url: {"useful": "2026-10-20"}}),
            ([], {url: {"already_known": "2026-10-20"}}),
            ([], {url: {"rating": "off_topic"}}),
            ([], {url: {"latest_action": "not_now", "not_now": "2026-10-20"}}),
        ]:
            with self.subTest(excluded=excluded, state=state):
                result = discover(self.sections, self.groups, DEFAULT, excluded, state, today)
                self.assertNotIn("다른 글도 한 편", dict(result))
                self.assertEqual(result, self.sections)
        expired = {url: {"latest_action": "not_now", "not_now": "2026-10-01"}}
        self.assertIn("다른 글도 한 편", dict(discover(self.sections, self.groups, DEFAULT, states=expired, today=today)))

    def test_count_budget_and_duplicate_urls_or_titles(self):
        for interest in range(4):
            for trusted in range(4):
                cfg = {**DEFAULT, "interest": interest, "trusted": trusted}
                sections = skim(self.groups, cfg)
                selected = self.items(discover(sections, self.groups, cfg))
                self.assertLessEqual(len(selected), len(self.items(sections)))
                self.assertEqual(len({canonical(x["url"]) for x in selected}), len(selected))
        cfg = {**DEFAULT, "interest": 0, "hot": 0, "topic_cases": 0, "topic_news": 0, "trusted": 0}
        self.assertEqual(discover([], self.groups, cfg), [])
        self.assertEqual(discover(self.sections, self.groups, {**DEFAULT, "discovery": False}), self.sections)
        duplicate = {**self.groups[("trusted",)][-1], "title": "T1", "url": "https://other.example/reprint"}
        groups = {**self.groups, ("trusted",): self.groups[("trusted",)][:2] + [duplicate]}
        self.assertNotIn("다른 글도 한 편", dict(discover(self.sections, groups, DEFAULT)))

    def test_render_preserves_reaction_controls_without_claim_pair(self):
        selected = discover(self.sections, self.groups, DEFAULT)
        page = render("2026-10-21", selected, {"https://t.example/3": ("참고노트", "주장")}, "전체")
        extra = page.split("## 다른 글도 한 편", 1)[1]
        self.assertIn("믿고 보는 저자", extra)
        self.assertNotIn("↔", extra)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "2026-10-21.md"
            path.write_text(page)
            controls = checkbox_controls(path)
            self.assertTrue(all(x["action"] is None for x in controls.values()))
            path.write_text(page.replace('- [ ] [T3]', '- [x] [T3]'))
            rated = [x for x in checkbox_controls(path).values() if x["url"] == canonical("https://t.example/3")]
            self.assertEqual(rated[0]["action"], "useful")

    def test_make_page_does_not_fetch_or_judge_the_discovery_item(self):
        config = {"interests": {"test": {"label": "이해 부채"}}, "compose": {}, "backlog": {}, "claim_links": {}}
        with tempfile.TemporaryDirectory() as directory, \
                patch("claims.published_claims", return_value=[]), \
                patch("compose.saved_refs", return_value=[]), \
                patch("backlog.cached_text", return_value={"text": "x" * 500}) as fetch, \
                patch("backlog.card_links", return_value=([], 0)):
            root = Path(directory)
            original, _, _ = make_page(root, root, "2026-10-21", self.REPORT, object(),
                                       {**config, "compose": {"discovery": False}}, "전체")
            old_calls = fetch.call_count
            fetch.reset_mock()
            page, tokens, errors = make_page(root, root, "2026-10-21", self.REPORT, object(), config, "전체")
            self.assertEqual(page.count("- [ ] "), original.count("- [ ] "))
            self.assertLessEqual(fetch.call_count, old_calls)
            self.assertNotIn("https://t.example/3", [c.args[0]["url"] for c in fetch.call_args_list])
            self.assertEqual((tokens, errors), (0, []))
            (root / "2026-10-21-함께읽기.md").write_text("- [T3](https://t.example/3)")
            page, _, _ = make_page(root, root, "2026-10-21", self.REPORT, object(), config, "전체")
            self.assertNotIn("## 다른 글도 한 편", page)
            self.assertEqual(page.count("https://t.example/3"), 1)
            (root / "2026-10-21-함께읽기.md").write_text("- [T3](https://original.example/reposted)")
            page, _, _ = make_page(root, root, "2026-10-21", self.REPORT, object(), config, "전체")
            self.assertNotIn("https://t.example/3", page)
            self.assertNotIn("## 다른 글도 한 편", page)



class EngineeringTest(unittest.TestCase):
    def test_independent_section_is_balanced_and_bounded(self):
        text = "## 관련 없는 섹션\n"
        text += "- [무시할 글](https://ignored.example) - Other\n"
        text += "## 엔지니어링 읽을거리\n"
        text += "- [A1](https://a/1) - A, 2026-10-20\n"
        text += "- [A2](https://a/2) - A, 2026-10-22\n"
        text += "- [B1](https://b/1) - B, 2026-10-21\n"
        groups = parse_report(text, set())
        selected = dict(skim(groups, {**DEFAULT, "engineering": 2}, "2026-10-23"))["엔지니어링 읽을거리"]
        self.assertEqual({x["source"] for x in selected}, {"A", "B"})
        self.assertNotIn("무시할 글", [x["title"] for x in selected])
        self.assertIn("A2", [x["title"] for x in selected])

class InterestBalanceTest(unittest.TestCase):
    def test_high_scoring_axis_does_not_hide_career_or_writing(self):
        text = '''## 설계
- 0.99 [A](https://a.example) - Engineering, 2026-10-20
- 0.98 [B](https://b.example) - Engineering, 2026-10-22
## 글쓰기
- 0.85 [C](https://c.example) - Writer
## 커리어
- 0.81 [D](https://d.example) - Career
'''
        groups = parse_report(text, {'설계', '글쓰기', '커리어'})
        cfg = {**DEFAULT, 'interest_balanced': True, 'interest': 3}
        got = dict(skim(groups, cfg, '2026-10-23'))['관심 질문 근처']
        self.assertEqual({x['title'] for x in got}, {'A', 'C', 'D'})
        self.assertEqual(len({x['url'] for x in got}), 3)


if __name__ == "__main__":
    unittest.main()
