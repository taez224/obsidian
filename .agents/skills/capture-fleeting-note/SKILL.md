---
name: capture-fleeting-note
description: 사용자가 "메모해줘", "이 생각 저장해줘", "Inbox에 넣어줘", "빠르게 기록해줘", "나중에 생각할 수 있게 남겨줘"라고 하거나 아직 다듬지 않은 개인 단상을 Obsidian에 포착하려 할 때 사용한다. 생각을 확장하거나 영구 노트로 완성하지 않고 00_Inbox에 Quick Capture로 저장한다. 사용자가 명시적으로 Slipbox·영구 노트 승격을 요청하면 permanent-note를 사용한다.
---

# Capture fleeting note

떠오른 생각의 골든타임을 놓치지 않도록 최소한의 가공만 거쳐 `00_Inbox/`에 저장한다.

## 원칙

1. **속도가 완성도보다 중요하다.** 저장에 필요하지 않은 질문을 하지 않는다.
2. **해석하지 않는다.** 오타·음성 인식 오류만 바로잡고 주장, 사례, 감정의 결을 보존한다.
3. **확장하지 않는다.** 관련 자료, 반례, AI의 보충 설명, 태그 추천, 링크 검색을 추가하지 않는다.
4. **분류를 미룬다.** Slipbox·Resources·Project 중 어디로 갈지는 주간 검토에서 결정한다.

## 절차

### 1. 한 줄 hook 만들기

입력에서 가장 가까운 표현을 골라 `무엇을 기록하는가`의 한 줄로 사용한다. 멋진 제목으로 바꾸지 않는다.

파일명은 `<YYYY-MM-DD HHmm> <짧은 hook>.md`로 만들고 `/ \\ : # ^ [ ] |`를 제거한다. 같은 파일이 있으면 초 단위 시각을 붙인다.

### 2. Quick Capture 작성하기

`date '+%F %H%M'`으로 시각을 확인하고 다음 형식을 사용한다.

```markdown
---
created: <YYYY-MM-DD>
tags:
  - inbox
next_action: ""
---

# 📝 Quick Capture — <YYYY-MM-DD HH:mm>

## 무엇을 기록하는가

> <사용자의 표현에 가까운 한 줄>

## 본문

<오타와 명백한 음성 인식 오류만 교정한 원문>

## 출처 / 링크

- <사용자가 함께 준 출처가 있을 때만 기록>

---

## 🔁 다음 액션

- [ ] 📚 **Slipbox**로 승격 → `next_action: promote-slipbox`
- [ ] 📁 **Resources**로 보관 → `next_action: archive-resources`
- [ ] 🚀 **Project**에 흡수 → `next_action: link-project/<id>`
- [ ] 🗑️ **삭제**
```

출처가 없으면 `출처 / 링크` 섹션을 생략한다. 본문이 한 줄뿐이어도 억지로 늘리지 않는다.

> 이 형식의 정본은 `99_Templates/quick-capture.md`다 (Templater로 수동 캡처할 때 사용).
> 어느 한쪽을 바꾸면 반드시 함께 갱신한다.

### 3. 보고하기

생성 경로와 한 줄 hook만 짧게 알린다. 연관 노트 검색, QMD 갱신, 자동 커밋은 하지 않는다.

## 경계

- 외부 URL의 내용을 읽고 정리하는 작업은 이 스킬의 범위가 아니다.
- 이미 충분히 정제된 생각이어도 사용자가 단순 저장만 요청했다면 Inbox에 둔다.
- 사용자가 즉시 영구 노트화를 명시했을 때만 `permanent-note`로 넘긴다.
