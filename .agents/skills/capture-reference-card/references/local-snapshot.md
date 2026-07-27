# 개인용 원문 스냅샷

사용자가 접근 권한이 있는 자료의 전문을 개인적으로 로컬 보관해 달라고 명시적으로 요청한 경우에만 적용한다. 전문은 자동으로 저장하지 않는다.

## 저장 위치

자료카드와 같은 파일명으로 저장한다.

```text
30_Resources/References/Clippings/_local-snapshots/<자료카드 파일명>.md
```

작업 전에 `.gitignore`가 `_local-snapshots/`를 제외하는지 확인한다.

## 형식

```markdown
---
title: <원문 제목>
source: <canonical URL 또는 입력 URL>
author:
  - <확인된 저자>
published: <확인된 원본 공개일 또는 "">
created: <로컬 보관일>
card: "[[자료카드 파일명]]"
---

# <원문 제목>

<원문 Markdown 본문>
```

- Frontmatter 아래에는 확보한 원문 언어의 Markdown 본문을 그대로 둔다.
- 원문 전체를 callout이나 blockquote로 감싸지 않는다. 헤딩·표·코드 블록·이미지·인용 구조를 불필요하게 바꾸지 않는다.
- `description`, 내용 요약, `my_take`, `status`는 자료카드에만 둔다.
- 추적 카드에는 로컬 파일 링크를 만들지 않는다. 다른 clone에서 죽은 링크가 되기 때문이다.
- `_local-snapshots/`는 QMD 연결 후보와 vault-lint 대상에서 제외한다.
- 기존 추적 카드의 전문을 옮길 때는 로컬 파일 생성과 내용 확인을 먼저 마친 뒤 카드에서 제거한다.

완료 후 Git 제외 여부와 저장 경로만 보고하고 스냅샷은 열지 않는다.
