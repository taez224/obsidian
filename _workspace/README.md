---
created: 2026-06-10
tags:
  - meta
---

# _workspace — 파이프라인 실행 산출물

> 블로그 윤문 파이프라인(`blog-review-polish` 등)이 세션별로 남기는 작업 폴더.
> 형식: `YYYY-MM-DD-NNN/` (metrics, detection, rewrite, audit, final.md, summary.md)

## 수명 정책

- **7일 이내**: 유지 (재검토·디버깅용)
- **7일 경과**: 삭제. 산출물은 재현 가능하고, 삭제 전 상태는 git 히스토리에 남는다.
- 가치 있는 결론이 있다면 삭제 전에 본문 노트(블로그 초안·DevLog)로 옮길 것 — 이 폴더는 보관소가 아니다.

> 정리 명령: `find _workspace -maxdepth 1 -type d -name "20*" -mtime +7 -exec rm -rf {} +`
> (실행 전 git 커밋 권장)
