import unittest
from feeds import balanced

class FeedTests(unittest.TestCase):
    def test_diversity_newest_and_duplicate(self):
        items = [{"source": "A", "url": "a1", "date": "2026-10-01"},
                 {"source": "A", "url": "a2", "date": "2026-10-20"},
                 {"source": "B", "url": "b", "date": "2026-10-10"},
                 {"source": "C", "url": "b#same", "date": "2026-10-10"}]
        got = balanced(items, 10, "2026-10-23")
        self.assertEqual(len(got), 3)
        self.assertEqual(len({x["source"] for x in balanced(items[:3], 2, "2026-10-23")}), 2)
        self.assertLess([x["url"] for x in got].index("a2"), [x["url"] for x in got].index("a1"))

    def test_weekly_rotation_and_empty(self):
        items = [{"source": x, "url": x} for x in "ABC"]
        self.assertNotEqual(balanced(items, 1, "2026-10-23"), balanced(items, 1, "2026-10-30"))
        self.assertEqual(balanced([], 4), [])
