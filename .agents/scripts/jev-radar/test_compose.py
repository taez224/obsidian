import unittest

from compose import DEFAULT, josa, pair, parse_report, skim

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


if __name__ == "__main__":
    unittest.main()
