#!/usr/bin/env python3
"""lint_scan.py 픽스처 테스트. 실행: python3 test_lint_scan.py"""
import json
import os
import subprocess
import sys
import tempfile
import unicodedata

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lint_scan.py")


def write(root, rel, text):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def build_fixture(root):
    fm = "---\ncreated: 2026-06-12\ntags:\n  - AI\n"
    slip_fm = fm + "type: permanent\nstatus: seedling\n---\n"
    # 정상 Slipbox 노트: NFC 링크 3종 — 일반 / NFD 파일 / Archive 파일 + 죽은 링크 + 첨부 임베드
    write(root, "01_Slipbox/연결된 노트.md",
          slip_fm + "[[대상 노트]] [[단상]] [[옛노트]] [[없는노트]] ![[그림.png]]\n"
          + "```\n[[코드블록 링크는 무시]]\n```\n")
    # alias로만 링크되는 노트
    write(root, "01_Slipbox/별명 노트.md",
          fm + "type: permanent\nstatus: seedling\naliases:\n  - 별명\n---\n[[연결된 노트]]\n")
    write(root, "30_Resources/대상 노트.md", fm + "---\n[[별명]]\n")
    # NFD 파일명 (디스크) — NFC 링크 [[단상]]이 해석되어야 함
    write(root, "00_Inbox/" + unicodedata.normalize("NFD", "단상") + ".md", fm + "---\n본문\n")
    # Archive: 해석 집합에는 포함, 검사 대상에선 제외
    write(root, "40_Archive/옛노트.md", fm + "---\n[[고립 아님]]\n")
    # Archive에서만 백링크를 받는 노트 → 고립 아님
    write(root, "30_Resources/고립 아님.md", fm + "---\n본문\n")
    # 진짜 고립 (Slipbox) → slipbox 플래그
    write(root, "01_Slipbox/고립 노트.md", slip_fm + "본문뿐\n")
    # frontmatter 위반: created 누락 + 태그에 # + Slipbox 필수(type/status) 누락
    write(root, "01_Slipbox/나쁜 노트.md", "---\ntags:\n  - '#ai'\n---\n[[대상 노트]]\n")
    # DevLog: created 없이 date만 → 위반 아님
    write(root, "30_Resources/Development/DevLog/2026-06-12.md",
          "---\ndate: 2026-06-12\ntags:\n  - 개발/DevLog\n---\n[[대상 노트]]\n")
    # 첨부파일 실물
    write(root, "_attachments/그림.png", "png-bytes")
    # 제외 대상: _ 파일, _workspace
    write(root, "01_Slipbox/_index.md", "no frontmatter but excluded\n")
    write(root, "_workspace/tmp.md", "excluded\n")
    # 회귀: 표 안의 이스케이프된 파이프 \| — 죽은 링크 오탐 금지
    write(root, "20_Projects/표 노트.md", fm + "---\n| [[대상 노트\\|표시]] |\n")
    # 회귀: _ 접두 중간 폴더와 루트 인프라 문서는 검사 제외
    write(root, "20_Projects/blog/_candidates/c1.md", "no frontmatter\n")
    write(root, "README.md", "no frontmatter, root infra doc\n")


def main():
    with tempfile.TemporaryDirectory() as root:
        build_fixture(root)
        out = subprocess.run([sys.executable, SCRIPT, root], capture_output=True, text=True)
        assert out.returncode == 0, out.stderr
        r = json.loads(out.stdout)

        orphan_paths = {o["path"] for o in r["orphans"]}
        assert "01_Slipbox/고립 노트.md" in orphan_paths, orphan_paths
        assert all(o["slipbox"] for o in r["orphans"] if o["path"].startswith("01_Slipbox/"))
        # NFD 파일·alias·Archive 대상·백링크만 있는 노트는 고립 아님
        nfc_orphans = {unicodedata.normalize("NFC", q) for q in orphan_paths}
        for p in ("00_Inbox/단상.md", "01_Slipbox/별명 노트.md", "30_Resources/고립 아님.md"):
            assert unicodedata.normalize("NFC", p) not in nfc_orphans, p

        dead_targets = {d["target"] for d in r["dead_links"]}
        assert dead_targets == {"없는노트"}, dead_targets  # NFD·alias·Archive·png는 오탐 금지, 코드블록 무시

        issues = {i["path"]: i["issues"] for i in r["frontmatter_issues"]}
        bad = issues.get("01_Slipbox/나쁜 노트.md", [])
        assert any("created" in s for s in bad), bad
        assert any("#" in s for s in bad), bad
        assert any("type" in s for s in bad), bad
        assert "30_Resources/Development/DevLog/2026-06-12.md" not in issues, issues
        assert not any("_index" in p or "_workspace" in p or "_candidates" in p for p in
                       [*orphan_paths, *issues]), "제외 규칙 위반"
        assert "README.md" not in issues, "루트 인프라 문서는 제외돼야 함"

        assert r["stats"]["notes_scanned"] >= 7
        print("OK — all assertions passed")


if __name__ == "__main__":
    main()
