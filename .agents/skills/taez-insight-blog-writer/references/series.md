# 연재 글

연재의 한 편을 쓰거나 검토할 때 읽는다. 연재가 아닌 글에는 적용하지 않는다.

## 연재 허브 확인

근거를 모으기 전에 확인한다.

- Inspect the target article frontmatter and the user request for a `series` name.
- If a series is identified, read `20_Projects/blog/<series>.md` first. If that exact file does not exist, search project-note titles and aliases for the series name rather than inventing a new hub.
- Treat the series hub as the editorial source of truth for the central question, article role, order, and unresolved follow-ups. Do not silently change the series plan; report a proposed hub update when the article reveals a meaningful change.
- When a series article is marked `published` with a confirmed `published` date, sync the hub's `last_published` to the latest known publication date. Change the hub's `status` or `ended` only when the user explicitly decides to pause or complete the series.

## 연재 글의 구조

연재의 한 편을 쓸 때는 직전 1~2편을 목차가 아니라 **본문으로** 읽는다. 아래는 초안 전 선택이자 검수 시 확인 항목이며, 연재 관련 판단은 여기 모아 둔다.

- **각 편은 서로 다른 국소 결론에 착지한다.** 시즌의 중심 주제를 함께 밀 수는 있지만, 앞 편의 국소 결론을 새 소재로 다시 증명하는 데 그치면 별도 회차보다 각주에 가깝다.
- **이어짐은 재진술이 아니라 다음 문제로 표시한다.** "앞 편에서 말한 X가 여기서 이어집니다" 같은 문장으로 연결을 설명하기보다, 앞 편이 남긴 미해결 질문·비용·예외·모순 중 하나를 이번 편의 출발점으로 삼는다.
- **같은 움직임이 연속되면 재료 때문인지 습관 때문인지 확인한다.** 재료가 실제로 그렇다면 연속해도 된다. 다만 도입 장면과 마지막 문단의 역할까지 같아지면 독자에게는 같은 글이므로 둘 중 하나를 바꾼다. 다양성을 만들려고 재료에 없는 움직임을 씌우지는 않는다.
- **원자료의 마찰을 지우지 않는다.** 실패·비용·한계·미해결 지점이 실제로 있는데 원칙이 매번 통하는 장면만 남기지 않았는지 확인한다. 없으면 만들지 않는다.
- 허브의 회차 역할과 실제 초안의 착지점이 어긋나면 허브 갱신 후보로 보고한다.
- 파일 단위 lint는 편 사이의 반복을 보지 못한다. 이 확인은 사람이나 검수 단계에서만 걸린다.

## 검수

초안을 검토할 때 위 구조 항목을 다시 훑는다. 여기서 실제로 확인할 것은 하나다 - 직전 편과 이번 편을 이어 읽었을 때 같은 악장이 반복되는가. 소재만 바뀐 채 "오해 → 사실은 아니었다 → 원칙"이 다시 돌면 구조로 돌아간다.
