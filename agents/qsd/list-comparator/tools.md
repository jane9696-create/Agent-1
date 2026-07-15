# List Comparator — Tools

## Primary Tools

| Tool | Purpose |
|------|---------|
| `Read` | 讀取重命名後 SOP 清單（來自 sop-renamer 的輸出）和原廠三份清單 |
| `Write` | 輸出差異摘要報告（Markdown）、比對腳本 |
| `Edit` | 更新記憶體（memory/MEMORY.md） |
| `Bash` | 執行 Python 比對腳本（openpyxl 讀寫 Excel）、worklog 打卡 |
| `Glob` | 尋找輸入檔案路徑（原廠清單 Excel/Word） |
| `Grep` | 在文字清單中搜尋特定 SOP 編號 |

## MCP Tools (Authorized)

| MCP 工具 | 用途 |
|----------|------|
| `workspace__bash` | 執行 Python 比對腳本（openpyxl 讀寫 Excel、差異標記寫入） |
| `desktop-commander` | 讀取 T:\ (Google Drive) 上的原廠清單檔案 |

> ⚠️ Google Drive 限制：T:\ 路徑必須用 `read_multiple_files`，`read_file` 只回傳 metadata。
> 詳見 `agents/protocols/rules/google-drive-read.md`

## Do NOT Use

- `Agent` — 只有 Manager 可派遣 agent；list-comparator 不派遣下游 agent

## Tool Usage Guidelines

- 使用 `Bash` 執行 Python 腳本（openpyxl）讀寫 Excel，不直接用 Claude 解析 Excel 二進位
- 比對邏輯寫入 `.claude/scripts/` 下的 `.py` 腳本，再用 `Bash` 執行
- 讀取輸入清單前，先用 `Glob` 確認檔案路徑正確
- worklog 打卡使用 `Bash` 呼叫 `scripts/_worklog_helper.py`
