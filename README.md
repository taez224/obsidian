# 🧠 Second Brain — Thinking Garden

개인 기록과 소프트웨어 개발, AI 활용을 오가며 생긴 생각을 연결해 가는 개인 지식 정원입니다.

완성된 글뿐 아니라 아직 발전 중인 주장과 참고자료도 있습니다. 하나의 결론을 찾기보다, 노트마다 다른 역할과 상태를 살피며 생각이 이어지는 과정을 따라 읽어 주세요.

## 🌱 처음 읽는다면

- [생각의 정원](./01_Slipbox/%EC%83%9D%EA%B0%81%EC%9D%98%20%EC%A0%95%EC%9B%90.md) - 핵심 질문의 입구
- [AI 활용](./01_Slipbox/AI%20%ED%99%9C%EC%9A%A9.md) - AI 활용에 관한 생각
- [나의 일하는 방식.md](01_Slipbox/%EB%82%98%EC%9D%98%20%EC%9D%BC%ED%95%98%EB%8A%94%20%EB%B0%A9%EC%8B%9D.md) - 강점과 지속 가능성
- [세컨드 브레인은 퍼스트 브레인의 사고를 보조해야 한다](./01_Slipbox/%EC%84%B8%EC%BB%A8%EB%93%9C%20%EB%B8%8C%EB%A0%88%EC%9D%B8%EC%9D%80%20%ED%8D%BC%EC%8A%A4%ED%8A%B8%20%EB%B8%8C%EB%A0%88%EC%9D%B8%EC%9D%98%20%EC%82%AC%EA%B3%A0%EB%A5%BC%20%EB%B3%B4%EC%A1%B0%ED%95%B4%EC%95%BC%20%ED%95%9C%EB%8B%A4.md) - AI와 지식관리의 경계
- [Think with AI](./20_Projects/blog/Think%20with%20AI.md) - AI와 함께 생각하기
- [블로그 글](./20_Projects/blog/) - 블로그 글 모음
- [개발 문제 해결 기록](./30_Resources/Development/Troubleshooting/) - 재사용 가능한 해결 기록

## 🧭 이 저장소를 읽는 방법

| 위치                          | 역할                              | 해석 기준                                          |
| --------------------------- | ------------------------------- | ---------------------------------------------- |
| `20_Projects/blog/`         | 외부 독자를 염두에 두고 쓴 글과 연재            | 초안과 발행본이 함께 있을 수 있으므로 frontmatter의 `status` 확인 |
| `01_Slipbox/`               | 다시 쓰려고 정리한 독립적인 주장과 주제 지도        | 지금 채택해 발전시키는 생각이지만 완결된 정답은 아님                  |
| `30_Resources/References/`  | 책·아티클·발표 같은 외부 자료를 읽고 남긴 기록      | 출처의 주장, 인용, 작성자의 반응을 나눠서 읽기                     |
| `30_Resources/Development/` | 개발 도구와 다시 쓸 수 있는 문제 해결 기록         | 특정 프로젝트 경험에서 시작했어도 공개 가능한 일반 지식으로 정리한 자료       |
| `00_Inbox/`                 | 아직 검토되지 않은 개인 단상과 질문            | 현재 입장이나 확정된 주장으로 간주하지 않기                       |
| `40_Archive/`               | 완료되었거나 과거 맥락으로 보관한 자료           | 현재 생각과 다를 수 있는 역사적 기록                          |

노트의 `type`, `status`, `source`, `my_take` 같은 속성은 문서가 무슨 역할을 하고 어디까지 다듬어졌는지 보여줍니다. 링크가 많거나 글이 길다고 더 중요하거나 완성된 노트는 아닙니다.

## 🤖 AI·자동화 도구를 위한 읽기 규칙

- 작성자의 현재 생각을 찾는다면 `20_Projects/blog/`와 `01_Slipbox/`부터 읽습니다.
- `References`의 요약과 인용은 원문의 내용일 수 있습니다. 작성자의 입장으로 바로 받아들이지 말고 `my_take`나 따로 표시한 해석을 확인합니다.
- `Inbox`와 `Archive`는 탐색 단서로 쓸 수 있지만 현재 입장의 근거로 삼지 않습니다.
- Quick Capture의 `AI 생성` 영역과 AI가 제안한 후보는 사용자가 명시적으로 채택하기 전까지 작성자의 주장이 아닙니다.
- 중요한 판단은 검색 결과의 일부 문장만으로 내리지 않습니다. 원문 전체와 연결된 근거까지 확인합니다.
- 노트를 인용하거나 요약할 때는 문서 제목과 경로를 함께 남기고, 확인한 내용과 해석을 나눠 적습니다.

## 📂 Vault 구조

```text
00_Inbox/             빠른 캡처와 미분류 아이디어
01_Slipbox/           영구 노트와 주제별 허브
10_Periodic Notes/    일간·주간·월간 기록
20_Projects/          진행 중인 결과물과 블로그
30_Resources/         개발 지식과 외부 참고자료
40_Archive/           완료·보관 자료
99_Templates/         노트 템플릿과 속성 스키마
```

이 Vault는 PARA와 Zettelkasten을 참고하지만, 폴더 분류 자체보다 다시 찾고 연결해 쓰는 데 초점을 둡니다.

```text
오늘의 기록 ───────────────→ 10_Periodic Notes
개인 단상 ────────────────→ 00_Inbox ─────┐
외부 자료 ────────────────→ 30_Resources ─┴─ 검토 → 보관 / Project 흡수 / Slipbox 승격
완료할 결과물 ────────────→ 20_Projects
재사용할 독립 주장 ───────→ 01_Slipbox
```

## ⚙️ 운영 원칙

- 사람이 반복할 운영 흐름: [Obsidian 운영 워크플로](./30_Resources/Obsidian%20%EC%9A%B4%EC%98%81%20%EC%9B%8C%ED%81%AC%ED%94%8C%EB%A1%9C.md)
- 에이전트의 검색·수정·승인 경계: [AGENTS.md](./AGENTS.md)
- frontmatter 표준: [property schema](./99_Templates/_property-schema.md)

Obsidian Bases로 Inbox 정리 부채, 프로젝트 상태, Slipbox 연결, 참고자료를 읽은 상태를 살펴봅니다. AI에는 검색·구조화·초안·검증을 맡기되, 어떤 연결을 남기고 영구 노트로 승격할지는 사용자가 검토하고 결정합니다.

## 🔗 참고

- [PARA](https://fortelabs.com/blog/para/)
- [Zettelkasten](https://zettelkasten.de/)
- [Obsidian Bases](https://help.obsidian.md/bases)
