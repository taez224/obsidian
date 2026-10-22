# QMD MCP Server Setup

## Install

```bash
npm install -g @tobilu/qmd
qmd collection add ~/path/to/markdown --name myknowledge
qmd embed
```

## Configure MCP Client

**Claude Code** (`~/.claude/settings.json`):
```json
{
  "mcpServers": {
    "qmd": { "command": "qmd", "args": ["mcp"] }
  }
}
```

**Claude Desktop** (`~/Library/Application Support/Claude/claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "qmd": { "command": "qmd", "args": ["mcp"] }
  }
}
```

**OpenClaw** (`~/.openclaw/openclaw.json`):
```json
{
  "mcp": {
    "servers": {
      "qmd": { "command": "qmd", "args": ["mcp"] }
    }
  }
}
```

## HTTP Mode

```bash
qmd mcp --http              # Port 8181
qmd mcp --http --daemon     # Background
qmd mcp stop                # Stop daemon
```

## Tools

Read the connected MCP tools' input schemas before calling them. Those schemas are authoritative for tool names, parameters, and defaults; the example below is not a complete API reference. Follow the vault routing and collection scope in [SKILL.md](../SKILL.md).

- `query`: search with structured `searches` and retrieval `intent`; select collections with `collections`.
- `get`: read one source using its returned `file` path or `#docid` in the `file` parameter.
- `multi_get`: read multiple sources by `pattern`.
- `status`: inspect index health and available collections.

Example `query` input:

```json
{
  "searches": [
    { "type": "vec", "query": "노트 연결을 판단하는 기준은 무엇인가?" }
  ],
  "intent": "Obsidian 노트 사이의 의미 관계를 판단하는 기준을 찾는다.",
  "collections": ["PKM"],
  "limit": 10
}
```

## Troubleshooting

- **Not starting**: `which qmd`, `qmd mcp` manually
- **No results**: `qmd collection list`, `qmd embed`
- **Slow first search**: Normal, models loading (~3GB)
