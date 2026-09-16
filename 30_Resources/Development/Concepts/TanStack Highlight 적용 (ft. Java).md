---
created: 2026-09-16
slug: tanstack-highlight-java
summary: 기존 Markdown 렌더러에 TanStack Highlight를 연결하고, 기본 지원에 없는 Java 구문 강조를 사용자 정의 토크나이저로 보완한 과정
tags:
  - 개발/TanStack
---

# TanStack Highlight 적용 (ft. Java)

TanStack Markdown과 TanStack Highlight를 알게 되어 생각 정원에 적용할 수 있을지 살펴봤다. 우선 적용한 것은 코드의 키워드와 문자열 등에 색을 입히는 Highlight다. 개발 노트에 자주 쓰는 Java가 기본 지원 언어에 없어, 이 부분은 직접 언어 정의를 추가했다. 적용한 버전은 2026년 9월에 나온 `@tanstack/highlight` 0.1.0이다.

## 두 라이브러리의 역할

[공식 소개 글](https://tanstack.com/blog/introducing-tanstack-markdown-and-highlight)에 따르면 두 라이브러리는 TanStack Docs 사이트의 Markdown 처리와 구문 강조에 드는 의존성 부담을 줄이려다 나왔다고 한다. 두 패키지 모두 2026년 6월에 npm에 처음 올라왔고, 아직 1.0 이전이라 지원 범위와 API가 이후 달라질 수 있다. [Shiki](https://shiki.style/) 같은 기존 라이브러리가 Markdown 파싱과 Highlight를 하나의 파이프라인으로 묶어서 처리하던 방식에서 벗어나기 위해 Tanstack에서 의도적으로 역할을 명확히 분리하여 독립된 라이브러리로 설계했다.

| 라이브러리 | 맡는 일 | 이 사이트의 적용 |
| --- | --- | --- |
| [TanStack Markdown](https://github.com/TanStack/markdown) | Markdown을 해석하고 HTML 등으로 렌더링 | 우선 기존 `markdown-it` 유지 |
| [TanStack Highlight](https://tanstack.com/highlight/latest/docs/overview) | 코드에서 키워드·문자열·주석을 구분해 구문 강조 | 노트의 코드 블록에 적용 |

TanStack Markdown은 블로그와 문서에 필요한 문법을 중심으로 만든 파서·렌더러다. 공식 설명에서 CommonMark, GFM, MDX 전체를 구현하는 범용 처리기를 목표로 하지는 않는다고 밝힌다.

Highlight는 동기식으로 동작하고 필요한 언어만 등록해서 구문 강조를 적용할 수 있다. 코드에서 색을 입힐 부분을 찾고, CSS 클래스를 붙인 HTML을 만든다. 색 자체는 스타일시트에서 정하므로 기존 사이트의 색상에 맞추기도 쉽다.

## 기존 렌더러에 연결

[[생각의 정원을 만들고 배포하는 과정|이 사이트의 Obsidian 노트 변환 과정]]에는 Obsidian 문법인 위키링크와 콜아웃 등을 처리하는 과정이 포함되어 있다. Markdown 렌더러를 교체하려면 이 동작들도 함께 마이그레이션 해야 했기에, 이번 적용에서는 `markdown-it`을 유지하고 코드 블록을 처리하는 `highlight` 옵션에 Tanstack Highlight를 적용했다.


Mermaid 코드 블록은 구문 강조가 아니라 [[Mermaid 12의 변경 사항|실제 다이어그램으로 변경]]되어야하므로 대상에서 제외했다.

## Java 언어 정의

2026년 9월 16일 기준 v0.1.0에서 Java는 구문 강조가 지원되지 않는다. 이 사이트 코드 블록의 절반 이상이 Java라 살짝 당황했지만, 다행히  [사용자 정의 언어를 등록하는 `defineLanguage`](https://tanstack.com/highlight/latest/docs/reference/core)가 있어, AI의 도움을 받아 직접 구현했다.

AI가 추가한 것은 Java 문법 전체를 분석하는 파서가 아니라 **구문 강조에 필요한 토크나이저**다. 주석·문자열·텍스트 블록을 먼저 구분한 뒤, 나머지 영역에서 어노테이션·키워드·기본 타입·숫자 등을 찾는 등의 역할을 한다. 
## 적용 범위와 한계

기존 노트 처리에 코드 강조만 추가할 수 있었고, Java는 별도의 언어 정의를 등록해 같은 방식으로 표시할 수 있었다. Tanstack에서 의도적으로 Markdown 파싱과 분리한 덕분에 이 사이트에서도 기존 파싱 과정 전체를 고치지 않고 필요한 부분만 보완할 수 있다는 점이 유용했다.

직접 만든 Java 토크나이저는 물론 완벽하지 않기에 기존 코드 블록 및 몇몇 예상되는 케이스에서 이상없음을 확인하고 마무리했다. 목표는 높은 완성도가 아니라 개발 노트의 예제를 읽기 쉽게 하는 정도면 충분하다. 물론 추후 버전에서 Java를 정식 지원하면 바로 교체할 예정이다.

TanStack Markdown은 우선 현재는 보류했다. 이후 교체를 검토한다면 현재 노트의 문법과 링크·콜아웃 등이 같은 결과로 나오는지 확인 후 진행한다.

> 관련 PR: [feat: tanstack/highlight 적용. 코드 구문 강조와 Java 언어 정의 추가](https://github.com/taez224/taez224.github.io/commit/2cf224d283ac48d3132d8a25d3294345bdd87e02)
