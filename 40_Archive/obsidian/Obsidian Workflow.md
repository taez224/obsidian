> [!info] 이 문서는 vault 초기 설계 스케치입니다 (2025-08 작성).
> 최신 워크플로우와 폴더 구조는 [[CLAUDE]] 와 [[README]] 를 참조하세요.

## 일일 ~ 월간 흐름

1. 매일 아침 `Daily Note` 생성 →
	1. `quickAdd: Create Daily Note`
	2. `10_Periodic Notes`, `Tasks Plugin` 자동 Due 확인
2. `Daily Note`나 생활 중 나온 배움·생각 → `00_Inbox`
3. 책, 블로그 등 외부 자료 → `30_Resources`
4. `주간 검토(Weekly)`에서 `Inbox → Resources → Slipbox`로 승격
5. 프로젝트 진행 중 발견·학습 → `프로젝트 노트 + Slipbox`에 병기
6. `월간 노트(Monthly)`에서 `Slipbox/Projects/Resources` 전반 리뷰

## 현재 폴더 구조

```
📦 Vault Root
├─ 📁 00_Inbox/             # 빠른 캡처
├─ 📁 01_Slipbox/           # 영구 노트 (Zettelkasten)
├─ 📁 10_Periodic Notes/    # Daily / Weekly / Monthly
├─ 📁 20_Projects/          # 진행 중 프로젝트
├─ 📁 30_Resources/
│   ├─ 📁 Development/      # DevLog, Tools
│   └─ 📁 References/       # Books, Articles, etc
├─ 📁 40_Archive/           # 완료/폐기
├─ 📁 99_Templates/         # 템플릿 + _property-schema.md
└─ 📁 Clippings/            # 외부 클리핑 원본
```

> [!note]- 초기 설계 스케치 (참고용)
> 처음에는 `30_Resources/Development/` 아래에 `Codebase/`, `Career/` 같은 세분화된 서브폴더를 두려 했으나, 운영해보니 폴더 깊이가 늘어나는 문제가 있어 현재는 **태그 기반**으로 분류하는 방향으로 정리했습니다. (예: `개발/Java`, `커리어/성장`)
