# blog-review-polish 실행 리포트 — 2026-06-10-001

대상: `20_Projects/blog/AI로 개인은 빨라졌는데, 왜 팀의 속도는 그대로일까.md`
실행: Cowork 에이전트 (러너 미지원 환경 — 워크플로 단계를 수동 수행)

## Fact-check (critical 5건)

| 주장 | 판정 | 비고 |
| --- | --- | --- |
| BOK 3.8% / 주당 1.5시간 / 상관계수 0 / 생산성 단절 / 자율성 집단 | verified | 아주경제 2026-06-07 보도로 확인 |
| BOK 발행일 | wrong → 수정 | 06-08 → **06-07** (본문 반영 완료) |
| 소프트웨어 절감률 9.8% | unverifiable | 보도엔 "소프트웨어 개발 등 인지적 업무일수록 효과 큼"까지. 본문에 %% 주석 플래그 — **발행 전 원문 PDF 확인 필요** |
| Ahmad, Comprehension Debt (arXiv 2604.13277) | verified | 실재·정의 일치. 단 학부 프로젝트(207명) 기반 → 참고문헌에 맥락 1줄 추가 완료 |
| Microsoft Scaffolding (arXiv 2604.08678) | verified | 행동 프로토콜 강제 → 품질·생산량 하락 ✓ (Fortune 500 리테일 388명, AM/PM confound 등 한계 있음) |
| Cohen & Levinthal 1990 / HBR Workslop 2025-09 | verified | 정전급 출처 |

## Editorial (이전 첨삭 세션에서 수행)

- 구체 장면 보강 3곳 (시크릿 검증 사건, 점검 명문화, 비우지 않는 맵)
- 템플릿 자기모순 해소 1곳

## Final-gate

- slop-lint: **PASS** (6,222자, high 0 · medium 0 · low 0)
- 구조 회귀: frontmatter ✓ / 섹션 10개 ✓ / 이미지 2개 실재 ✓ / wikilink 10개 깨짐 없음 ✓

## 남은 사람 몫

1. 9.8% 수치 — 이슈노트 원문 PDF 대조 후 %% 주석 제거
2. `_slop-gate` 7항목 음독 사인오프 → `slop_check: passed` 복원
3. (선택) status: insight → 발행 단계 값으로
