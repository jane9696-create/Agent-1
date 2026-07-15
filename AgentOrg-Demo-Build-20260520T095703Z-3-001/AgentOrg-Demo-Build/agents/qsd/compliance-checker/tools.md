# Compliance Checker — Tools

## Primary Tools

| Tool | Purpose |
|------|---------|
| `Read` | 讀取 QSD checklist、原廠文件清單、比對基準表 |
| `Write` | 建立比對結果報告（Markdown / 結構化表格） |
| `Edit` | 更新比對結果（追加條款、修正 Pending 項目） |
| `Bash` | worklog 打卡（scripts/worklog.sh start/end）、讀取 memory |
| `Glob` | 搜尋原廠提供的文件檔案 |
| `Grep` | 在文件內容中搜尋特定條款關鍵字或版本資訊 |

## MCP Tools (Authorized)

| MCP 工具 | 用途 |
|----------|------|
| `mcp__desktop-commander__read_multiple_files` | 讀取 T:\ 上的 QSD checklist 與原廠文件。**禁用 `read_file`**（T:\ 路徑只回傳 metadata，見 google-drive-read.md） |
| `mcp__desktop-commander__write_file` | 將比對結果報告寫入 T:\ |
| `mcp__desktop-commander__edit_block` | 編輯現有比對結果表（追加或修正條款結果） |
| `mcp__desktop-commander__list_directory` | 列出原廠文件資料夾，確認文件清單完整性 |
| `mcp__workspace__bash` | worklog 打卡（scripts/worklog.sh start/end） |

> ⚠️ Google Drive 限制：T:\ 路徑必須用 `read_multiple_files`，`read_file` 只回傳 metadata。詳見 `agents/protocols/rules/google-drive-read.md`

## Do NOT Use

- `Agent` — 本 agent 是 Worker，無下屬，不得派遣其他 agent
