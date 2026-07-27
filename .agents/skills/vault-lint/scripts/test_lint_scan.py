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
    # ── 블록 앵커 픽스처 ────────────────────────────────────
    # 앵커는 줄 끝에서만 유효하다: 단독 줄과 텍스트 뒤는 OK, 줄 앞은 블록 ID가 아니다
    write(root, "01_Slipbox/앵커 대상.md", slip_fm +
          "첫 문단\n\n^good-standalone\n\n둘째 문단 ^good-inline\n\n"
          "^bad-leading 앵커가 줄 앞에 있으면 Obsidian이 블록 ID로 보지 않는다\n")
    write(root, "30_Resources/앵커 참조.md", fm + "---\n"
          "- [[앵커 대상#^good-standalone]] - 단독 줄 앵커\n"
          "- [[앵커 대상#^good-inline]] - 텍스트 뒤 앵커\n"
          "- [[앵커 대상#^missing-anchor]] - 없는 앵커\n"
          "- [[앵커 대상#^bad-leading]] - 줄 앞이라 인식 안 됨\n"
          "- [[앵커 대상#헤딩 링크]] - 헤딩 링크는 이 검사 대상 아님\n"
          "- [[없는노트#^whatever]] - 문서 자체가 미해석이면 dead_links 소관\n"
          "```\n- [[앵커 대상#^in-code]] - 코드블록은 무시\n```\n")
    # ── 재사용 판정 픽스처 ──────────────────────────────────
    # 출처 표지 문구가 붙은 단방향 링크 → 재사용에서 제외
    write(root, "01_Slipbox/출처 있는 노트.md", slip_fm + "본문\n")
    write(root, "30_Resources/References/Articles/원자료.md",
          fm + "source: https://example.com\npublished: 2026-06-01\nstatus: read\n---\n"
          "- [[출처 있는 노트]] - 이 자료에서 정제한 결과\n")
    # Inbox에서 온 링크는 보류 (README: Inbox는 현재 입장의 근거가 아니다)
    write(root, "00_Inbox/초안.md", fm + "---\n- [[출처 있는 노트]] - 이 생각의 출발점\n")
    # 상호 + 읽은 자료 → 출처 관계로 보고 재사용에서 제외
    write(root, "01_Slipbox/상호 노트.md", slip_fm + "- [[읽은 자료]] - 원문 근거\n")
    write(root, "30_Resources/References/Books/읽은 자료.md",
          fm + "---\n- [[상호 노트]] - 이 책이 다룬 개념\n")
    # 블로그는 상호여도 재사용 (블로그가 노트를 낳기도 하고 인용하기도 해서 상호로 안 갈림)
    write(root, "01_Slipbox/블로그 상호 노트.md", slip_fm + "- [[블로그 상호 글]] - 적용 사례\n")
    write(root, "20_Projects/blog/블로그 상호 글.md",
          fm + "---\n- [[블로그 상호 노트]] - 이 글에서 인용한 개념\n")
    # 운영 문서는 상호여도 자료가 아니라 적용처 → 재사용
    write(root, "01_Slipbox/운영 노트.md", slip_fm + "- [[운영 문서]] - 이 원칙을 적용한 기준\n")
    write(root, "30_Resources/운영 문서.md", fm + "---\n- [[운영 노트]] - 운영 경계\n")
    # 맨 "승격"은 본문 개념어일 뿐 출처 표지가 아니다 (마커 오탐 회귀)
    write(root, "01_Slipbox/마커 오탐 노트.md", slip_fm + "본문\n")
    write(root, "20_Projects/blog/승격 언급 글.md",
          fm + "---\n- [[마커 오탐 노트]] - 조회 경로는 승격 때 설계해야 한다\n")
    # ───────────────────────────────────────────────────────
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
        # 없는노트 2건: 평범한 링크 + 앵커 링크(문서 자체가 미해석이라 dead_links 소관)
        assert priorities["meaning_review"]["dead_links"] == 2
        assert priorities["informational"]["periodic_placeholders"] == 1
        assert priorities["informational"]["series_placeholders"] == 1
        assert priorities["informational"]["non_slipbox_orphans"] == sum(
            1 for orphan in r["orphans"] if not orphan["slipbox"]
        )

        # 블록 앵커: 없는 앵커와 줄 앞 앵커만 잡고, 유효한 형태는 오탐하지 않는다
        broken = {b["anchor"] for b in r["broken_anchors"]}
        assert broken == {"missing-anchor", "bad-leading"}, r["broken_anchors"]
        assert all(
            unicodedata.normalize("NFC", b["target"]) == "01_Slipbox/앵커 대상.md"
            for b in r["broken_anchors"]
        ), r["broken_anchors"]
        assert r["stats"]["broken_anchors"] == 2
        assert priorities["meaning_review"]["broken_anchors"] == 2

        reuse = r["stats"]["reuse"]
        assert reuse["blog_to_slipbox_edges"] == 3, reuse
        assert reuse["blog_notes_with_slipbox_refs"] == 3, reuse
        assert reuse["slipbox_notes_reused_by_blog"] == 3, reuse

        by_note = {unicodedata.normalize("NFC", e["path"]): e for e in r["reuse_by_note"]}

        def reasons(note, bucket):
            return {x["reason"] for x in by_note[unicodedata.normalize("NFC", note)][bucket]}

        def count(note):
            return by_note[unicodedata.normalize("NFC", note)]["reuse_count"]

        # 출처 표지 문구가 붙은 링크는 재사용으로 세지 않는다
        assert count("01_Slipbox/출처 있는 노트.md") == 0, by_note
        assert reasons("01_Slipbox/출처 있는 노트.md", "excluded") == {"출처 표지 문구"}
        # Inbox 링크는 보류 — 출처도 재사용도 아니다
        assert reasons("01_Slipbox/출처 있는 노트.md", "pending") == {"Inbox 초안 — 근거로 세지 않음"}
        # 상호 + 읽은 자료 → 출처
        assert count("01_Slipbox/상호 노트.md") == 0, by_note
        assert reasons("01_Slipbox/상호 노트.md", "excluded") == {"상호 + 읽은 자료"}
        # 블로그는 상호여도 재사용 (상호 링크 규칙을 블로그에 적용하지 않는다)
        assert count("01_Slipbox/블로그 상호 노트.md") == 1, by_note
        assert reasons("01_Slipbox/블로그 상호 노트.md", "reused_by") == {"블로그 인용"}
        # 운영 문서는 적용처라 상호여도 재사용
        assert count("01_Slipbox/운영 노트.md") == 1, by_note
        assert reasons("01_Slipbox/운영 노트.md", "reused_by") == {"상호지만 상대가 적용처"}
        # 맨 "승격"은 출처 표지가 아니다
        assert count("01_Slipbox/마커 오탐 노트.md") == 1, by_note
        assert by_note[unicodedata.normalize("NFC", "01_Slipbox/마커 오탐 노트.md")]["excluded"] == []
        # 고립 노트는 재사용 0이지만 목록에는 남는다 (0회가 이 지표의 핵심 산출물)
        assert count("01_Slipbox/고립 노트.md") == 0, by_note

        assert reuse["slipbox_notes_total"] == len(r["reuse_by_note"]), reuse
        assert reuse["slipbox_notes_reused"] + reuse["slipbox_notes_unused"] == \
            reuse["slipbox_notes_total"], reuse
        assert reuse["pending_edges"] == 1, reuse
        assert r["priorities"]["informational"]["pending_reuse_edges"] == 1
        assert r["priorities"]["informational"]["seedling_with_reuse"] == \
            sum(1 for e in r["reuse_by_note"]
                if e["reuse_count"] > 0 and e["status"] == "seedling")
        # 재사용 많은 순 정렬
        counts = [e["reuse_count"] for e in r["reuse_by_note"]]
        assert counts == sorted(counts, reverse=True), counts

        print("OK — all assertions passed")


if __name__ == "__main__":
    main()
