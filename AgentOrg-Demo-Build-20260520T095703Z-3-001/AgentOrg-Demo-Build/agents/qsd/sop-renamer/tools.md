# SOP Renamer — Tools

## Primary Tools

| Tool | Purpose |
|------|---------|
| `Read` | 讀取 SOP 檔案封面頁以解析編號、主題、版本 |
| `Write` | 寫入重命名對照清單（Markdown 格式） |
| `Bash` | 執行 Python 重命名腳本、worklog 打卡（scripts/worklog.sh start/end） |
| `Glob` | 掃描資料夾，列出所有 .pdf / .docx / .xlsx / .pptx 檔案 |

## MCP Tools (Authorized)

| MCP 工具 | 用途 |
|----------|------|
| `workspace__bash` | 執行 Python 批量重命名腳本（shutil.copy2），處理大批檔案 |
| `mcp__desktop-commander__read_multiple_files` | 讀取 T:\ (Google Drive) 上的 SOP 檔案封面內容。**禁用 `read_file`**（僅回傳 metadata） |
| `mcp__desktop-commander__list_directory` | 列出 T:\ 上的資料夾結構，確認 SOP 檔案清單 |

> ⚠️ Google Drive 限制：T:\ 路徑必須用 `read_multiple_files`，`read_file` 只回傳 metadata。
> 詳見 `agents/protocols/rules/google-drive-read.md`

## Do NOT Use

- `Agent` — 只有 Manager 派遣 agent；sop-renamer 不可自行派遣子 agent
- `Edit` — 不修改任何 SOP 檔案內容；Edit 工具僅用於修改文本，不適用於二進制檔案操作

## Tool Usage Guidelines

- 優先從檔名解析命名元素；如檔名不足，再用 Read 讀取封面頁
- Python 腳本統一使用 `shutil.copy2` 另存副本，不使用 `os.rename` 或 `shutil.move`
- Bash 僅用於執行腳本和 worklog 打卡，不直接操作檔案系統複製
- 輸出對照清單使用 Write 工具寫入 Markdown，不使用 Bash echo
