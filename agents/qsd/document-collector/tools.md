# Document Collector — Tools

## Primary Tools

| Tool | Purpose |
|------|---------|
| Read | 讀取 QSD checklist Excel 路徑、記憶檔案、設定檔 |
| Write | 寫入索取文件清單（Markdown 或 Excel）、記憶更新 |
| Edit | 修正已寫入的清單內容 |
| Bash | 執行 Python 腳本（openpyxl 解析 .xlsx/.xls）、worklog 打卡 |
| Glob | 搜尋指定目錄下的 Excel 或 Markdown 檔案 |
| Grep | 在 checklist 內容中搜尋特定條款關鍵字 |

## MCP Tools (Authorized)

| MCP Tool | Purpose |
|----------|---------|
| desktop-commander | 讀寫 T:\ 路徑下的 QSD checklist 與輸出清單 |
| workspace__bash | 執行 worklog.sh 打卡腳本、Python openpyxl 解析腳本 |

## Do NOT Use

- **Agent 工具** — document-collector 是 Worker（L1），無下屬，不可派遣子 agent
- **Manager 專屬工具**（dispatch_agents_parallel、ToolSearch 等）— 僅限 Manager（L2+）使用
- **WebSearch、WebFetch** — 本 agent 不做線上研究，所有輸入來自本地 Excel 檔案
- **Gmail、Google Calendar** — 本 agent 不做郵件或日曆操作
