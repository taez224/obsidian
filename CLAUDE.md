# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is an **Obsidian Vault** - a personal knowledge management system based on PARA methodology and Zettelkasten. It contains Markdown notes, not source code.

## Vault Structure (PARA + Zettelkasten)

```
00_Inbox/          빠른 캡처, 미분류 아이디어 (정기적으로 정리 필요)
01_Slipbox/        영구 보관용 노트 (Zettelkasten 방식, 상호 연결)
10_Periodic Notes/ 시간 기반 노트 (일간/주간/월간)
  └─ YYYY/W##/     주차별 폴더 (2025-W01.md, 2025-01-01.md)
20_Projects/       진행 중인 프로젝트별 폴더
30_Resources/      참고 자료
  ├─ Development/  개발 자료 (DevLog, Codebase, Career)
  └─ References/   외부 자료 (Books, Articles)
40_Archive/        완료/보관 자료
99_Templates/      노트 템플릿 (Templater 문법 사용)
```

## Workflow (Knowledge Flow)

```
Daily Note/생활 → 00_Inbox → (주간 정리) → 30_Resources 또는 01_Slipbox
                              ↓
                    20_Projects (프로젝트 진행 중 학습)
```

- **매일**: Daily Note 생성, 빠른 캡처는 Inbox로
- **주간**: Inbox → Resources/Slipbox로 승격 정리
- **월간**: 전체 시스템 리뷰, MOC(Maps of Content) 업데이트

## Tag System (태그 체계)

계층형 태그 구조를 사용합니다. Frontmatter에서 `#` 기호 없이 작성합니다.

```yaml
tags:
  - AI
  - 개발/Java
  - 커리어/성장
```

### 주제별 태그

| 카테고리 | 태그 예시 | 용도 |
|----------|-----------|------|
| `AI/` | `AI`, `AI/에이전트`, `AI/프롬프트` | AI 관련 콘텐츠 |
| `개발/` | `개발/Java`, `개발/도구`, `개발/DevLog`, `개발/플랫폼`, `개발/트러블슈팅`, `개발/인프라` | 개발 관련 |
| `커리어/` | `커리어/성장`, `커리어/동기부여`, `커리어/이직`, `커리어/시니어` | 커리어/자기계발 |
| `프로젝트/` | `프로젝트/onlyoffice` | 프로젝트별 구분 |
| `철학` | `철학` | 철학/사상 |

### 노트 타입 태그

| 태그 | 용도 |
|------|------|
| `slipbox` | 01_Slipbox 영구 노트 |
| `blog` | 블로그 발행용 |
| `📚독서` | 책 노트 (메타데이터용) |
| `📰article` | 아티클/기사 스크랩 |

### 태그 규칙

- Frontmatter에서 `#` 기호 사용하지 않음 (❌ `"#ai"` → ✅ `AI`)
- 계층 구분은 `/` 사용 (`개발/Java`)
- 인라인 태그(`#task`, `#next`)는 본문에서만 사용

## Linking Best Practices (노트 연결)

Zettelkasten 원칙에 따라 노트 간 연결을 적극 활용합니다.

### 핵심 규칙

| 규칙 | 설명 |
|------|------|
| **최소 1개 링크** | 모든 영구 노트(Slipbox)는 최소 1개 이상의 연결 필수 |
| **3-5개 최적** | 노트당 3-5개의 의미 있는 연결이 이상적 |
| **Backlinks 활용** | 역링크는 Backlinks 패널로 확인 (수동 역연결 불필요) |

### 연결 섹션 형식

노트 하단에 `## 연결된 노트` 섹션을 추가합니다:

```markdown
## 연결된 노트

- [[관련 노트 1]] - 연결 이유 (간단한 설명)
- [[관련 노트 2]] - 어떤 맥락에서 연결되는지
```

### 연결 유형

| 유형 | 설명 | 예시 |
|------|------|------|
| **같은 주제** | 동일 개념의 다른 관점 | AI의 능력 ↔ AI의 책임 |
| **상위/하위** | 추상화 수준 연결 | 성장 철학 → 구체적 실천법 |
| **근거/적용** | 이론과 사례 | 철학 개념 → 실제 적용 사례 |

## Working with This Vault

- 노트 생성/편집 시 해당 타입의 템플릿 구조를 따를 것
- Wikilinks `[[]]`로 노트 간 연결 유지
- Frontmatter (YAML) 형식 준수
- 한글 파일명 사용 가능 (URL 인코딩 불필요)
