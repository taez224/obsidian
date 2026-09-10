import tempfile
import unittest
from pathlib import Path

from check_guides import check_guides


class GuideLinksTest(unittest.TestCase):
    def test_relative_paths_spaces_and_external_links(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".agents/guides").mkdir(parents=True)
            (root / "문서 이름.md").write_text("# 제목\n")
            (root / "AGENTS.md").write_text("[문서](<문서 이름.md>)\n[웹](https://example.com)\n[절](#title)\n")
            (root / ".agents/guides/writing.md").write_text("[문서](<../../문서 이름.md#제목>)\n")
            self.assertEqual(check_guides(root), [])

    def test_missing_skill_reports_source_and_target(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "AGENTS.md").write_text("[스킬](.agents/skills/missing/SKILL.md)\n")
            errors = check_guides(root)
            self.assertEqual(len(errors), 1)
            self.assertIn("AGENTS.md:1", errors[0])
            self.assertIn("missing/SKILL.md", errors[0])

    def test_missing_entrypoint(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(check_guides(directory), ["Missing guide: AGENTS.md"])


if __name__ == "__main__":
    unittest.main()
