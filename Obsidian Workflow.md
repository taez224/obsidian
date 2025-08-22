1. 매일 아침 `Daily Note` 생성 →
	1. `quickAdd: Create Daily Note`
	2. `10_Periodic Notes`, `Tasks Plugin` 자동 Due 확인
2. `Daily Note`나 생활 중 나온 배움·생각 → `00_Inbox`
3. 책, 블로그 등 외부 자료 → `30_Resources`
4. `주간 검토(Weekly)`에서 `Inbox → Resources → Slipbox`로 승격
5. 프로젝트 진행 중 발견·학습 → `프로젝트 노트 + Slipbox`에 병기
6. `월간 노트(Monthly)`에서 `Slipbox/Projects/Resources` 전반 리뷰


```
📦 Vault Root
├─ 📁 00_Inbox/                  # 빠른 캡처, 미분류 아이디어 및 임시 메모
│   └─ YYYYMMDD-HHmmss_new-blog-idea.md 
│ 
├─ 📁 01_Slipbox/                # 영구 보관용 노트, 정기적 MOC 반영
│   └─ AI 시대에 필요한 개발자의 마인드.md
│
├─ 📁 10_Periodic Notes/         # 데일리 노트, task 추적
│   └─ 📁 2025/
│       ├─ 📁 Monthly/
│       │   └─ 2025-01.md        # 월간 노트
│       └─ 📁 W01/               
│           ├─ 2025-W01.md       # 주간 노트
│           └─ 2025-01-01.md     # 일간 노트
│
├─ 📁 20_Projects/               # 진행 중 프로젝트
│   ├─ 📁 ProjectA/
│   │   ├─ 00_Overview.md        # 프로젝트 개요, 목표, 현황
│   │   ├─ 01_Planning.md        # 기획 및 요구사항
│   │   ├─ 02_Design.md          # 설계문서, 아키텍처
│   │   ├─ 03_Implementation.md  # 개발 진행 기록
│   │   └─ 04_Retrospective.md   # 회고
│   └─ 📁 ProjectB/
│
├─ 📁 30_Resources/              # 참고용으로 쓰일 자료
│   ├─ 📁 Development/           # 개발 관련 자료들
│   │   ├─ 📁 Codebase/          # 스니펫, 라이브러리 예제 등등
│   │   │   ├─ 📁 Python/     
│   │   │   │   └─ zip-stream.md   
│   │   ├─ 📁 DevLog/            # 개발일지, 단위 지식, 참고 노트 가능
│   │   │   └─ 📁 Java/
│   │   │       └─ ApplicationContextException_REGISTER_BEAN.md   
│   │   └─ 📁 Career/            # 커리어 관련
│   │
│   ├─ 📁 References/            # 참고 자료 (책, 유튜브, 블로그 등)
│   │   └─ 📁 Books/           
│   │       └─ Building a Second Brain.md   
│   └─ 📁 ....
│
├─ 📁 40_Archive/               # 완료된 프로젝트, 폐기 자료
│
└─ 📁 99_Templates/             # 템플릿 모음 (Daily, Project 등)
```