# 🧠 Second Brain - Obsidian Knowledge Management System

> **개발자를 위한 체계적인 지식 관리 시스템**  
> AI 시대의 개발자로서 필요한 역량을 체계적으로 축적하고 활용하는 개인 지식 베이스

---

## 📋 프로젝트 개요

이 프로젝트는 **PARA 방법론**과 **Zettelkasten 시스템**을 기반으로 한 개인 지식 관리 시스템입니다. 개발자의 일상적인 학습, 프로젝트 관리, 문제 해결 과정을 체계적으로 기록하고 활용할 수 있도록 설계되었습니다.

### 🎯 주요 목표
- **지식의 체계적 축적**: 학습한 내용을 영구적으로 보관하고 연결
- **생산성 향상**: 반복적인 작업의 템플릿화와 자동화
- **지속적 성장**: 개인 역량의 지수적 성장을 위한 시스템 구축
- **AI 시대 최적화**: AI 시대에 더욱 중요해진 개인 지식의 데이터베이스화

---

## 🏗️ 폴더 구조

```
📦 Second Brain
├─ 📁 00_Inbox/                  # 빠른 캡처, 미분류 아이디어
├─ 📁 01_Slipbox/                # 영구 보관용 노트 (Zettelkasten)
├─ 📁 10_Periodic Notes/         # 시간 기반 노트 (일간/주간/월간)
├─ 📁 20_Projects/               # 진행 중인 프로젝트
├─ 📁 30_Resources/              # 참고 자료 (개발, 책, 아티클)
├─ 📁 40_Archive/                # 완료된 프로젝트, 보관 자료
└─ 📁 99_Templates/              # 노트 템플릿 모음
```

### 📁 폴더별 상세 설명

#### **00_Inbox** - 진입점
- 임시 아이디어와 빠른 메모
- 나중에 체계적으로 분류할 예정
- 하루에 한 번 이상 정리

#### **01_Slipbox** - 영구 지식 저장소
- 정제된 영구 노트들
- 상호 연결된 지식 네트워크
- 정기적인 MOC(Maps of Content) 업데이트

#### **10_Periodic Notes** - 시간 기반 관리
- **일간 노트**: 작업 추적, 회고, 학습 기록
- **주간 노트**: 주간 목표, 진행 상황, 다음 주 계획
- **월간 노트**: 전체 시스템 리뷰, 장기 목표 점검

#### **20_Projects** - 프로젝트 관리
- 진행 중인 프로젝트별 폴더
- 프로젝트 개요, 기획, 설계, 구현, 회고 문서
- 체계적인 프로젝트 문서화

#### **30_Resources** - 참고 자료
- **Development/**: 개발 관련 자료
  - `DevLog/`: 개발 일지, 트러블슈팅
  - `Codebase/`: 코드 스니펫, 라이브러리 예제
  - `Career/`: 커리어 관련 자료
- **References/**: 외부 참고 자료
  - `Books/`: 책 노트, 독서 기록
  - `Articles/`: 블로그, 아티클 요약

#### **40_Archive** - 보관소
- 완료된 프로젝트
- 더 이상 사용하지 않는 자료
- 첨부 파일과 깊은 보관소

#### **99_Templates** - 템플릿 모음
- 일간/주간/월간 노트 템플릿
- 프로젝트 노트 템플릿
- 기술 노트, 트러블슈팅 템플릿
- 책 노트, 리소스 요약 템플릿

---

## 🔄 워크플로우

### 📅 일간 워크플로우
1. **매일 아침**: `Daily Note` 생성
   - `quickAdd: Create Daily Note` 사용
   - `10_Periodic Notes`에서 Tasks Plugin 자동 Due 확인
2. **하루 종일**: 빠른 캡처와 작업 기록
3. **저녁**: 일간 회고 및 내일 계획 수립

### 📊 주간 워크플로우
1. **주간 검토**: Inbox → Resources → Slipbox 승격
2. **프로젝트 진행**: 프로젝트 노트 + Slipbox 병기
3. **다음 주 계획**: 주간 목표 설정

### 📈 월간 워크플로우
1. **전체 시스템 리뷰**: Slipbox/Projects/Resources 전반 점검
2. **MOC 업데이트**: 지식 네트워크 재구성
3. **장기 목표 점검**: 개인 성장 방향 재정립

---

## 🛠️ 주요 기능

### 📝 노트 템플릿
- **일간 노트**: 작업 추적, 회고, 학습 기록
- **프로젝트 노트**: 체계적인 프로젝트 문서화
- **기술 노트**: 트러블슈팅과 학습 내용
- **책 노트**: 독서 기록과 인사이트

### 🔗 연결 시스템
- **Wiki 링크**: `[[노트명]]` 형태의 내부 링크
- **태그 시스템**: `#개발 #AI #프로젝트` 등
- **MOC**: Maps of Content로 관련 노트 그룹화

### 📊 추적 시스템
- **작업 추적**: 일간/주간/월간 목표 관리
- **학습 추적**: 기술 스택과 학습 진도
- **프로젝트 추적**: 진행 상황과 마일스톤

---

## 🚀 시작하기

### 1. Obsidian 설치
```bash
# macOS (Homebrew)
brew install --cask obsidian

# 또는 공식 웹사이트에서 다운로드
# https://obsidian.md/
```

### 2. 필수 플러그인 설치
- **Templater**: 동적 템플릿 생성
- **QuickAdd**: 빠른 노트 생성
- **Periodic Notes**: 시간 기반 노트 자동 생성
- **Tasks**: 작업 관리
- **Dataview**: 데이터베이스 기능

### 3. 초기 설정
1. 이 저장소를 Obsidian Vault로 열기
2. 플러그인 활성화 및 설정
3. 템플릿 경로 설정
4. 단축키 등록

---

## 📚 사용 예시

### 일간 노트 작성

```bash
# 일간 노트 생성 (QuickAdd 사용)
Cmd/Ctrl + P → QuickAdd: Create Daily Note
```

```markdown
# 📅 2025-01-15 Daily Note

## ✅ 오늘의 주요 작업
- [ ] API 설계 문서 작성
- [ ] React 컴포넌트 리팩토링
- [ ] 코드 리뷰 참여

## 📘 오늘 배운 내용
- 개념: React Query의 optimistic updates
- 참고: [[React Query Best Practices]]

## 🔥 회고
- ✅ API 설계를 체계적으로 진행했다
- ❌ 코드 리뷰 시간이 부족했다
```

### 슬립박스 노트 작성
```markdown
# 🌟 React Query Optimistic Updates

> 낙관적 업데이트를 통한 사용자 경험 향상

## 핵심 개념
- 서버 응답을 기다리지 않고 UI를 즉시 업데이트
- 실패 시 자동 롤백

## 사용 예시
```javascript
const mutation = useMutation({
  mutationFn: updateTodo,
  onMutate: async (newTodo) => {
    // 낙관적 업데이트
    ...
  }
})
```

## 관련 노트
- [[React Query Best Practices]]
- [[User Experience Patterns]]


---

## 🔗 관련 자료

- [Obsidian 공식 문서](https://help.obsidian.md/)
- [PARA 방법론](https://fortelabs.co/blog/para/)
- [Zettelkasten 방법론](https://zettelkasten.de/)
- [Second Brain 개념](https://www.buildingasecondbrain.com/)

