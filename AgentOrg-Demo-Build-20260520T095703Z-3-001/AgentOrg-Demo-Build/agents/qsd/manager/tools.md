# QSD Manager — Tools

## Primary Tools

| Tool | Usage |
|------|-------|
| **Agent** | Dispatch worker subagents（document-collector、compliance-checker、sop-renamer、list-comparator、form-filler）。Manager 專屬，subagent 無此工具。 |
| **Read** | 讀取 memory/、workflow/ 下的定義與協議文件 |
| **Write** | 寫入 memory/ 記憶檔案、worklog/ 日誌 |
| **Edit** | 更新 memory/MEMORY.md 索引 |
| **Glob** | 掃描 agents/qsd/ 目錄結構、確認 worker 存在 |
| **Grep** | 在協議文件中搜尋規則 |
| **ToolSearch** | 查找可用工具的 schema（Manager 專屬）|

## Shell 偏好（Bash-First）

使用 Bash tool 執行 worklog 打卡腳本。多行腳本請先寫入 `.claude/scripts/` 再執行，避免 permission 攔截。

## MCP Tools (Authorized)

| MCP 工具 | 用途 |
|---------|------|
| `mcp__desktop-commander__*` | 讀寫 T:\ 路徑下的 QSD 文件（checklist Excel、SOP 檔案等）。注意：read_file 在 T:\ 只回傳 metadata，必須用 read_multiple_files（見 agents/protocols/rules/google-drive-read.md） |
| `mcp__workspace__bash` | 執行 worklog.sh 打卡腳本 |
| `mcp__memory__*` / `mcp__server-memory__*` | 持久化知識圖譜，儲存合規審查 pattern 與歷史決策 |

## Do NOT Use

- **Edit / Write on worker agent files** — Agent Builder only
- **WebSearch / WebFetch** — QSD 合規審查基於既有文件，不搜尋外部資料（worker 有需要時由 worker 自行使用）
- **NotebookEdit** — 不適用
- **TaskCreate / TaskStop** — 不在此 Manager 的授權範圍
