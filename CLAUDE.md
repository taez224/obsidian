@AGENTS.md

## Claude Code 전용

- `obsidian-markdown`, `obsidian-bases`, `obsidian-cli`, `json-canvas`, `defuddle`는 `obsidian-skills` 플러그인이 준다. `.agents/skills/`에 있는 같은 이름의 사본은 Codex용이므로 Claude에서는 플러그인 것을 쓴다.
- `.claude/workflows/blog-*.js`는 Workflow 도구 스크립트다(앵글 채굴, 리서치 수집, 재구성, 검수). 사용자가 워크플로 실행을 명시했을 때만 돌린다. `blog-slop-lint.mjs`와 `blog-structure-scan.mjs`는 LLM 호출이 없는 결정론 스크립트라 node로 직접 실행한다.
- 위임은 Agent 도구의 읽기 전용 에이전트(Explore)로 한다. 노트 수정은 주 세션이 직접 한다.
- 의미 검색은 `.mcp.json`의 qmd MCP로 한다. 절차는 `qmd` 스킬을 따른다.
