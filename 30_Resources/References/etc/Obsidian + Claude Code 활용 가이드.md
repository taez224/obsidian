# Obsidian + Claude Code 활용 가이드 (2026 최신)

> 2026년 1월 기준 최신 정보를 바탕으로 정리한 가이드

## 1. 핵심 개념

Obsidian vault는 본질적으로 **마크다운 파일 기반 코드베이스**입니다. Claude Code가 파일 탐색과 수정에 탁월하므로 자연스럽게 통합됩니다.

---

## 2. Skills 기반 설정 (권장)

### kepano/obsidian-skills (Obsidian CEO 공식 제공)

**설치 방법:**
```bash
# 방법 1: Claude Code 플러그인 마켓플레이스
/plugin marketplace add kepano/obsidian-skills
/plugin install obsidian@obsidian-skills

# 방법 2: 수동 설치
# vault 루트에 /.claude 폴더 생성 후 저장소 내용 복사
```

**제공 Skills:**

| Skill | 대상 파일 | 기능 |
|-------|----------|------|
| `obsidian-markdown` | `.md` | Wiki links, embeds, callouts, Frontmatter 지원 |
| `obsidian-bases` | `.base` | Obsidian Bases(DB) 필터/공식/집계 |
| `json-canvas` | `.canvas` | Canvas JSON 구조 생성/편집 |

---

## 3. CLAUDE.md 설정 패턴

vault 루트에 `CLAUDE.md` 또는 `/.claude/CLAUDE.md` 파일 생성:

```markdown
# Obsidian Vault Context

## 역할
이 vault는 개인 지식 관리 시스템입니다.

## 폴더 구조
- 00_Inbox/: 정제되지 않은 노트
- 01_Slipbox/: 영구 노트
- 10_Periodic Notes/: 일간/주간 노트
- 20_Projects/: 프로젝트별 자료
- 30_Resources/: 참고자료
- 99_Templates/: 템플릿

## 규칙
- Wiki link 형식: [[파일명]] 또는 [[파일명|표시텍스트]]
- 태그: #태그명 형식
- 새 노트 생성 시 적절한 폴더에 배치
- Frontmatter 필수: created, tags
```

---

## 4. 실용적 워크플로우

### A. 일일 자동화 커맨드

```
/today - 어제 저장 내용, PR, 오래된 노트 수집
/wrapup - 진행상황 검토 및 아카이빙
```

### B. 노트 정리 작업

```
"오늘 저널에서 언급된 모든 사람, 장소, 책에 backlink 추가해줘"
→ Claude가 기존 노트 검색 → 없으면 생성 → wiki-link 삽입
```

### C. 콘텐츠 변환

```
"이 bullet point 메모를 구조화된 서평으로 변환해줘"
"회의 녹음 전사본을 액션아이템 형식으로 정리해줘"
```

### D. 대규모 정리

```
"모든 노트에서 누락된 frontmatter 추가해줘"
"01_Slipbox의 노트들을 주제별로 분류해줘"
```

---

## 5. MCP 서버 통합 (고급)

### obsidian-claude-code-mcp 플러그인

**기능:**
- 듀얼 트랜스포트: WebSocket(Claude Code) + HTTP/SSE(Claude Desktop)
- 자동 연결: Claude Code 실행 시 vault 자동 감지
- 파일 작업: view, create, str_replace, insert
- 워크스페이스: get_current_file, get_workspace_files

**설치:**
1. Obsidian 커뮤니티 플러그인에서 "Claude Code" 검색
2. 포트 22360 기본 사용

### obsidian-http-mcp (stdio 버그 우회용)

- 빠른 응답 (<200ms)
- 실수 방지를 위한 soft delete
- 오타 허용 fuzzy search

---

## 6. 품질 제어 패턴

### Git 기반 검토
```bash
# Claude가 변경 후 diff 확인
git diff
```

### AI 제안 태그 방식
```markdown
<ai-suggestion>
이 부분은 AI가 제안한 내용입니다. 검토 후 결정하세요.
</ai-suggestion>
```

### 폴더 권한 제한
- 민감한 개인 정보는 별도 폴더로 분리
- `claude-workspace/` 같은 전용 작업 폴더 사용

---

## 7. 고급 활용법

### "내 관점에서 질문하기"
```
"내 노트에 기반해서, 내가 AI 시대 생존 전략에 대해 뭐라고 했을까?"
```
→ Claude가 당신의 축적된 지식에서 답변

### Canvas로 플로우차트 생성
```
"이 프로젝트의 워크플로우를 canvas 파일로 만들어줘"
```

### Progressive Disclosure Memory
- 에이전트가 메모리 확인 후 작업
- 완료 시 결과 저장
- 불필요한 컨텍스트 로딩 최소화

---

## 8. 바로 시도해볼 수 있는 작업

```
"00_Inbox 폴더의 노트들을 분석해서 적절한 폴더로 이동 제안해줘"
"weekly 템플릿을 개선해줘"
"최근 수정된 노트들에서 누락된 backlink 찾아줘"
```

---

## References

- [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills)
- [Obsidian × Claude Code: The Ultimate Workflow Guide](https://www.axtonliu.ai/newsletters/ai-2/posts/obsidian-claude-code-workflows)
- [obsidian-claude-code-mcp](https://github.com/iansinnott/obsidian-claude-code-mcp)
- [Obsidian Skills 심층 가이드](https://claudecn.com/en/blog/obsidian-skills-for-claude-code/)
- [Claude + Obsidian + MCP 활용기](https://www.eleanorkonik.com/p/how-claude-obsidian-mcp-solved-my)
- [obsidian-http-mcp](https://github.com/NasAndNora/obsidian-http-mcp)