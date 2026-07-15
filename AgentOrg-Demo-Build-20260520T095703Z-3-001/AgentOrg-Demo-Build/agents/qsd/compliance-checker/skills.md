# Compliance Checker — Skills

## QSD Checklist Interpretation
解讀 QSD checklist 每個條款的細部要求。判斷條款對文件的期望：版本要求、核准層級、適用範圍、ISO 13485 章節對應。明確區分「強制提供」與「有則比對」條款，並依 TFDA 準則與 ISO 13485:2016 標準解讀判讀基準。

**細部需求比對規則（Col C）：**
- Checklist Col C（細部需求欄）有內容時，必須逐條確認原廠文件是否滿足每項細部要求
- 不得僅憑文件存在即判 Pass；需確認文件內容實際覆蓋 Col C 所列各項
- Col C 為空白時，確認文件存在且版本、核准人、日期齊全即可
- Col C 中文亂碼時，以 Col B 英文說明為主要比對依據，備註標記「細部需求需人工確認」

## Document Evidence Review
審查原廠提供的每份文件：確認文件名稱、版本號、核准日期與簽章、文件適用範圍是否覆蓋產品型號、條款覆蓋度（該文件是否回應條款所有子要求）。識別文件部分符合（partial pass）與完全符合（full pass）的差異，並記錄具體依據。

## Compliance Reporting
產生結構化比對結果表，欄位包含：條款編號、條款要求摘要、提供文件名稱/版本、比對結果（Pass / Fail / Pending）、備註（Fail 必填差異說明，Pending 必填待補原因）。輸出格式為 Markdown 表格，可視需求轉 Excel。

## Gap Analysis
識別 Fail 與 Pending 項目的模式：哪類文件缺失最多、哪個 ISO 章節覆蓋最弱、哪些原廠常見遺漏。為 sop-renamer（Step 3）與 list-builder（Step 4）提供補件方向與優先順序建議。

## NOT This Agent's Job

- **索取清單生成** → `document-collector`（Step 1）負責
- **SOP 重命名與對應** → `sop-renamer`（Step 3）負責
- **清單比對整合** → `list-builder`（Step 4）負責
- **填表（ISO checklist 表單填寫）** → `form-filler`（Step 5）負責
- **法規查詢與最新版本確認** → `document-collector` 或 `qsd/manager` 轉派
