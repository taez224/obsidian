import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from suggest import names, suggest


class SuggestTest(unittest.TestCase):
    def test_names_with_korean_particles(self):
        found = names("Simon Willison의 글과 GPT-6 Astra를 봤다. Don't 같은 축약형은 빼야 한다.")
        self.assertIn("Simon Willison", found)
        self.assertIn("GPT-6 Astra", found)
        self.assertNotIn("Don", found)

    def test_recent_burst_and_exclusions(self):
        with tempfile.TemporaryDirectory() as d:
            v = Path(d)
            inbox = v / "00_Inbox"
            inbox.mkdir(parents=True)
            for i in range(3):
                (inbox / f"new{i}.md").write_text(f"---\ncreated: 2026-09-2{i}\n---\nNewTool 과 OldThing 이야기")
            for i in range(5):
                (inbox / f"old{i}.md").write_text(f"---\ncreated: 2026-01-0{i + 1}\n---\nOldThing 이야기")
            interest = v / "관심사.md"
            interest.write_text("- Jev | 모델 | 검색어: Jev\n\n## 제외\n\n- Ignored\n")
            rows, n = suggest(v, interest, {}, today=date(2026, 9, 26))
            self.assertEqual(n, 3)
            self.assertEqual(rows[0][1], "NewTool")
            self.assertTrue(all(r[1] != "Jev" for r in rows))


if __name__ == "__main__":
    unittest.main()
