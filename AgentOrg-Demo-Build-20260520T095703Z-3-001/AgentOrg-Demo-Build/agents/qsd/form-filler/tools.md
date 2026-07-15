# Form Filler — Tools

## Primary Tools

| Tool | Purpose |
|------|---------|
| `Read` | 讀取 Quality Manual（.docx）、SOP 文件（.docx）、form-E-Annex 2 模板（.xlsx） |
| `Write` | 輸出填寫完成的表格（Markdown 格式）、缺件清單、執行摘要 |
| `Bash` | 執行 Python 腳本（讀取 docx/xlsx、填寫 Excel）；worklog 打卡 |
| `Grep` | 在 Quality Manual 和 SOP 文件中搜尋特定 ISO 13485 條款關鍵字 |
| `Glob` | 掃描工作目錄中所有 SOP 文件（.docx）和 Quality Manual |

## MCP Tools (Authorized)

| MCP 工具 | 用途 |
|----------|------|
| `mcp__workspace__bash` | 執行 Python 腳本讀取 .docx（python-docx）、.xlsx（openpyxl）；worklog 打卡 |
| `mcp__desktop-commander__read_multiple_files` | 讀取位於 T:\ (Google Drive) 的文件（Quality Manual、SOP、模板）|
| `mcp__desktop-commander__list_directory` | 列出輸入目錄中的所有 SOP 文件 |

> ⚠️ Google Drive 限制：T:\ 路徑必須用 `read_multiple_files`，`read_file` 只回傳 metadata。詳見 `agents/protocols/rules/google-drive-read.md`

## Do NOT Use

- `Agent` — only Manager dispatches agents
- `WebSearch` / `WebFetch` — 只用提供的文件，不查網路。ISO 13485 條款知識來自訓練，文件證據必須來自提供的 Quality Manual 和 SOP
- `Edit` — form-filler 不修改其他 agent 的檔案

## Tool Usage Guidelines

- 先用 `Glob` 掃描所有輸入 .docx 文件，再逐一 `Read` 或用 Python 提取段落
- 用 `Grep` 快速定位條款關鍵字後，再精讀具體段落
- 使用 Python（python-docx、openpyxl）處理 .docx 和 .xlsx 格式的讀寫
- `Write` 輸出到 `tuq_log/output/` 或 Manager 指定目錄
