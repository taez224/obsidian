import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from claims import import_checkbox_feedback, sentences, register_checkbox_snapshot
from reading import feedback_state, events_at, add_feedback


class CheckboxFeedbackTest(unittest.TestCase):
    def test_checked_and_markers(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d)
            (out / "2026-09-28.md").write_text("\n".join([
                "- [x] 0.97 [A](https://arxiv.org/abs/2609.00001v1) - arXiv",
                "- [ ] 0.90 [B](https://example.org/b) - GeekNews 이미앎",
                "- [x] 0.85 [C](https://example.org/c) - Hacker News 관심밖",
                "- [ ] 0.82 [D](https://example.org/d) - arXiv",
                "    - → [[주장]] ← \"sentence\"",
                "- 0.80 [E](https://example.org/e) - 예전 형식",
            ]))
            added = import_checkbox_feedback(out)
            self.assertEqual(sorted(a for _, a in added), ["already_known", "off_topic", "useful"])
            self.assertEqual(import_checkbox_feedback(out), [])  # 두 번 기록하지 않는다
            events = [json.loads(l) for l in (out / "reading-feedback.jsonl").read_text().splitlines()]
            self.assertEqual(len(events), 3)

    def test_title_and_url_are_not_reactions(self):
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)
            (out/'2026-09-26.md').write_text('- [ ] [내 관심 밖의 기술 읽기](https://example.org/관심밖) - source\n')
            self.assertEqual(import_checkbox_feedback(out), [])

    def test_change_back_and_uncheck_preserves_direct_read(self):
        with tempfile.TemporaryDirectory() as d:
            out=Path(d);p=out/'2026-09-26-reading.md';url='https://example.org/a'
            add_feedback(out,url,'read')
            for suffix,check,wanted in [('', 'x', 'useful'),(' 관심밖',' ', 'off_topic'),('', 'x','useful')]:
                p.write_text(f'- [{check}] [A]({url}){suffix}\n')
                import_checkbox_feedback(out)
                self.assertEqual(feedback_state(events_at(out))[url]['rating'], wanted)
            p.write_text(f'- [ ] [A]({url})\n');import_checkbox_feedback(out)
            state=feedback_state(events_at(out))[url]
            self.assertNotIn('rating',state);self.assertNotIn('useful',state);self.assertIn('read',state)
            self.assertEqual(import_checkbox_feedback(out),[])

    def test_marker_removal_and_repeated_snooze(self):
        with tempfile.TemporaryDirectory() as d:
            out=Path(d);p=out/'2026-09-26.md';url='https://example.org/a'
            for suffix in [' 지금아님','',' 지금아님']:
                p.write_text(f'- [ ] [A]({url}){suffix}\n');import_checkbox_feedback(out)
            events=events_at(out)
            self.assertEqual(sum(e['action']=='not_now' for e in events),2)
            self.assertIn('not_now',feedback_state(events)[url])

    def test_generated_defaults_are_not_user_undo(self):
        with tempfile.TemporaryDirectory() as d:
            out=Path(d);p=out/'2026-09-26-reading.md';url='https://example.org/a'
            p.write_text(f'- [x] [A]({url})\n');import_checkbox_feedback(out)
            p.write_text(f'- [ ] [A]({url})\n');register_checkbox_snapshot(out,p)
            self.assertEqual(import_checkbox_feedback(out),[])
            self.assertEqual(feedback_state(events_at(out))[url]['rating'],'useful')

    def test_sentences_korean(self):
        text = ("한국어 초록의 첫 문장은 충분히 길어서 하나의 선택지로 들어가야 한다. "
                "두 번째 문장도 마찬가지로 길어서 앞 문장과 따로 나뉘어야 맞다. "
                "The third sentence is written in English and is long enough.")
        self.assertEqual(len(sentences(text)), 3)

    def test_sentences_korean_noun_endings(self):
        text = ("즉시 발효되지만 효력을 유지하려면 120일 이내 의회 승인이 필요함 "
                "이용자는 10월 5일까지 잔액을 반환받을 수 있으며 앱스토어 배포도 중단됨 "
                "업계는 이번 조치가 다른 나라로 확산될 수 있다고 우려하는 분위기임")
        self.assertEqual(len(sentences(text)), 3)

    def test_sentences_limit(self):
        text = " ".join(f"Sentence number {i} is long enough to count." for i in range(400))
        self.assertLessEqual(len(sentences(text)), 250)


if __name__ == "__main__":
    unittest.main()
