---
title: google-labs-code/design.md
source: https://github.com/google-labs-code/design.md
author:
  - Google Labs
published: 2026-04-21
created: 2026-09-12
description: Google Labs가 Apache-2.0으로 공개한 DESIGN.md 포맷 명세 저장소다. 코딩 에이전트에 디자인 시스템을 전달하기 위해 YAML 디자인 토큰과 마크다운 산문을 한 파일에 담는 형식을 규정하고, 검증용 CLI와 예제 파일을 함께 제공한다.
status: unread
my_take: ""
---

> [!note] 저장 맥락
> Nick Babich의 GPT-6 Astra 영상 두 편이 참조한 Google 공식 명세를 확인하려고 찾았다.

## 내용 요약

- DESIGN.md를 브랜드와 제품의 시각적 정체성을 담은 자족적인 평문 문서로 정의한다. 파일은 기계가 읽는 디자인 토큰을 담은 YAML frontmatter와 사람이 읽는 근거·지침을 담은 마크다운 본문 두 층으로 이루어지며, 토큰이 규범적인 값이고 산문은 그 값을 어떻게 적용할지 알려 주는 맥락이라고 규정한다. Google Labs의 UI 디자인 도구 Stitch에서 쓰던 포맷을 2026년 4월 21일에 초안으로 공개했다.
- 명세 자체의 버전은 `alpha`이고 `main` 브랜치의 `docs/spec.md`가 항상 최신본이다. GitHub 릴리스 태그 0.1.0부터 0.4.0까지는 npm 패키지 `@google/design.md` CLI의 버전이며 릴리스 노트도 린터 수정과 내보내기 형식 추가를 다룬다. Components 절에는 이 부분이 아직 변하는 중이라는 주석이 붙어 있다.
- 토큰 체계는 Design Token JSON 명세에서 타입이 있는 토큰 그룹 개념과 `{path.to.token}` 참조 문법을 가져왔고, `tokens.json`·Figma 변수·Tailwind 테마 설정과 서로 변환된다. 최상위 키는 `version`, `name`, `description`, `omitted`, `colors`, `typography`, `rounded`, `spacing`, `components`다.
- 색상은 hex·이름·`rgb()`·`oklch()`·`color-mix()` 등 유효한 CSS 색상 문자열을 모두 받으며 내부적으로 sRGB로 변환해 WCAG 대비를 검사한다. 치수의 단위는 `px`, `em`, `rem`만 허용하고, `lineHeight`에 단위 없는 숫자를 쓰면 글꼴 크기의 배수로 해석한다. `omitted`에 의도적으로 뺀 절과 그 이유를 적으면 린터가 누락 경고를 내지 않는다.
- 본문의 절은 Overview, Colors, Typography, Layout, Elevation & Depth, Shapes, Components, Do's and Don'ts 여덟 개이며 모두 `##` 헤딩을 쓴다. 필요 없는 절은 빼도 되지만 넣은 절은 이 순서를 지켜야 한다. 모르는 절 제목과 토큰 이름은 오류 없이 보존하거나 수용하고, 모르는 컴포넌트 속성은 경고와 함께 통과시키며, 파일을 거부하는 경우는 같은 절 제목이 두 번 나올 때뿐이다.
- `npx @google/design.md lint DESIGN.md`로 깨진 토큰 참조, 순환 참조, 유효하지 않은 값, WCAG 대비를 검사해 구조화된 JSON을 받는다. 두 파일의 토큰 변경과 회귀 여부를 비교하는 `diff`, Tailwind v4 CSS·Tailwind v3 JSON·DTCG 토큰으로 내보내는 `export`, 명세 문서를 생성하는 `spec` 명령이 함께 있다. 출력은 사람이 아니라 에이전트가 읽고 조치하도록 설계했다고 밝힌다.
- 저장소의 `PHILOSOPHY.md`는 디자인이 사는 곳은 산문이며 문서의 나머지는 그 산문을 뒷받침하려고 존재한다고 선언한다. 토큰 값은 렌더링 지시가 아니라 산문이 참조할 맥락이고, 생성 결과의 품질은 값의 정밀도보다 의도를 얼마나 분명히 서술했는지로 결정된다고 본다. 형용사 나열은 영역을 가리켜 평범한 결과를 낳지만 구체적인 참조 하나는 여백·서체·장식의 부재까지 함께 전달하며, 참조가 충분히 구체적이면 하지 말아야 할 것들은 따로 적지 않아도 따라온다고 설명한다.
