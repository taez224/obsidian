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
    # 블로그에서 실제 Slipbox를 재사용한 고유 링크 — 중복 링크는 edge 1개로 집계
    write(root, "01_Slipbox/재사용 노트.md", slip_fm + "[[연결된 노트]]\n")
    write(root, "20_Projects/blog/재사용 글.md",
          fm + "---\n[[재사용 노트]] [[재사용 노트]]\n")
    # 진행 중 시리즈 허브의 미래 글 링크는 의미 검토가 아닌 정보성 placeholder
    write(root, "20_Projects/blog/진행 중 연재.md",
          fm + "type: series\nstatus: active\n---\n[[다음 편]]\n")
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
    # Periodic 날짜 링크는 전체 죽은 링크에는 남지만 의미 검토가 아닌 정보성 placeholder
    write(root, "10_Periodic Notes/2026/W24/2026-06-12.md",
          fm + "---\n[[2026-06-11]]\n")
    # Articles: source·published·status 필수 — 누락 노트는 위반, 완비 노트는 통과
    write(root, "30_Resources/References/Articles/나쁜 아티클.md",
          fm + "---\n[[대상 노트]]\n")
    write(root, "30_Resources/References/Articles/좋은 아티클.md",
          fm + "source: https://example.com\npublished: 2026-06-01\nstatus: read\n---\n[[대상 노트]]\n")
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
    # .base: sortBy 오류 있는 파일 — 파일명이 _로 시작해도 검사돼야 함(.md의 _ 제외 규칙과 다름)
    write(root, "01_Slipbox/_index.base",
          "views:\n  - type: table\n    name: 뷰\n    sortBy:\n      property: file.mtime\n"
          "      direction: DESC\n")
    # .base: 정상 파일 — sort 키만 사용, issue 없어야 함
    write(root, "20_Projects/blog/_index.base",
          "views:\n  - type: table\n    name: 뷰\n    sort:\n      - property: file.mtime\n"
          "        direction: DESC\n")
    # .base: Archive는 검사 제외
    write(root, "40_Archive/_old.base", "views:\n  - type: table\n    sortBy:\n      property: x\n")


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
        assert dead_targets == {"없는노트", "2026-06-11", "다음 편"}, dead_targets
        # NFD·alias·Archive·png는 오탐 금지, 코드블록 무시
        assert r["periodic_placeholders"] == [
            {
                "source": "10_Periodic Notes/2026/W24/2026-06-12.md",
                "target": "2026-06-11",
            }
        ], r["periodic_placeholders"]
        assert r["series_placeholders"] == [
            {
                "source": "20_Projects/blog/진행 중 연재.md",
                "target": "다음 편",
            }
        ], r["series_placeholders"]

        issues = {i["path"]: i["issues"] for i in r["frontmatter_issues"]}
        bad = issues.get("01_Slipbox/나쁜 노트.md", [])
        assert any("created" in s for s in bad), bad
        assert any("#" in s for s in bad), bad
        assert any("type" in s for s in bad), bad
        assert "30_Resources/Development/DevLog/2026-06-12.md" not in issues, issues
        bad_article = issues.get("30_Resources/References/Articles/나쁜 아티클.md", [])
        for k in ("source", "published", "status"):
            assert any(k in s for s in bad_article), bad_article
        assert "30_Resources/References/Articles/좋은 아티클.md" not in issues, issues
        assert not any("_index" in p or "_workspace" in p or "_candidates" in p for p in
                       [*orphan_paths, *issues]), "제외 규칙 위반"
        assert "README.md" not in issues, "루트 인프라 문서는 제외돼야 함"

        assert r["stats"]["notes_scanned"] >= 7

        base_paths = {b["path"] for b in r["base_issues"]}
        assert "01_Slipbox/_index.base" in base_paths, base_paths
        assert all(b["key"] == "sortBy" for b in r["base_issues"]), r["base_issues"]
        # 정상 base(sort만 사용)는 안 걸려야 함, Archive의 base는 검사 제외
        assert "20_Projects/blog/_index.base" not in base_paths, base_paths
        assert "40_Archive/_old.base" not in base_paths, base_paths

        priorities = r["priorities"]
        assert priorities["mechanical"]["frontmatter_issues"] == len(r["frontmatter_issues"])
        assert priorities["mechanical"]["base_issues"] == len(r["base_issues"])
        assert priorities["meaning_review"]["slipbox_orphans"] == 1
        assert priorities["meaning_review"]["dead_links"] == 1
        assert priorities["informational"]["periodic_placeholders"] == 1
        assert priorities["informational"]["series_placeholders"] == 1
        assert priorities["informational"]["non_slipbox_orphans"] == sum(
            1 for orphan in r["orphans"] if not orphan["slipbox"]
        )

        reuse = r["stats"]["reuse"]
        assert reuse["blog_to_slipbox_edges"] == 1, reuse
        assert reuse["blog_notes_with_slipbox_refs"] == 1, reuse
        assert reuse["slipbox_notes_reused_by_blog"] == 1, reuse

        print("OK — all assertions passed")


if __name__ == "__main__":
    main()
