import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from topics import load_topics, per_source


class TopicsTest(unittest.TestCase):
    def test_load_topics(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "관심사.md"
            p.write_text("# 제목\n\n설명 문단\n\n- Jev | 판정형 모델 | 검색어: Jev, TypeSafe\n- 형식이 틀린 줄\n")
            self.assertEqual(load_topics(p), [{"name": "Jev", "desc": "판정형 모델", "terms": ["Jev", "TypeSafe"]}])
            self.assertEqual(load_topics(Path(d) / "없음.md"), [])

    def test_per_source_keeps_each_source(self):
        items = [{"source": "GitHub", "points": 900, "case": 1}] * 5 + [{"source": "Hacker News", "points": 50, "case": 1}] * 2
        out = per_source(items, 3, "case")
        self.assertEqual([x["source"] for x in out], ["Hacker News"] * 2 + ["GitHub"] * 3)


if __name__ == "__main__":
    unittest.main()
