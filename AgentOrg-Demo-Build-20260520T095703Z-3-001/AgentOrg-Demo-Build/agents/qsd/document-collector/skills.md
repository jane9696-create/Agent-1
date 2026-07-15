# Document Collector — Skills

## QSD Checklist Parsing

解析 QSD checklist Excel 檔案的能力：

- 使用 Python + openpyxl（.xlsx）或 xlrd（.xls）讀取 Excel 內容
- 識別條款結構：條款編號欄、條款名稱欄、要求說明欄、文件類型欄
- 處理合併儲存格（merged cells）、多工作表（multi-sheet）的 checklist 格式
- 辨識空白行、說明行、分隔行，與實際條款行的差異
- 對欄位標題進行模糊比對（如「文件編號」≈「Doc. No.」≈「条款编号」），提升相容性

## Document Classification

對 QSD 條款所需文件進行分類標準化：

| 文件類型 | 典型關鍵字 |
|---------|---------|
| 品質手冊 | Quality Manual、品質手冊、QM |
| SOP / 作業程序 | SOP、Procedure、作業程序、操作規程 |
| 表單 / 記錄 | Form、Record、表單、記錄、填寫 |
| 圖面 / 技術文件 | Drawing、圖面、技術規格、Specification |
| 測試報告 | Test Report、測試報告、驗收報告 |
| 其他 | 無法歸類的文件，保留原始描述並標記「其他」 |

分類規則：
- 依條款說明文字中的關鍵字進行匹配
- 一個條款可能需要多種文件類型（分拆為多筆記錄）
- 無法確定類型時，填入「其他」並在備註欄保留原文

## Request List Generation

產生結構化的索取文件清單：

輸出格式（Markdown 表格）：
```
| 條款編號 | 文件類型 | 數量需求 | 備註 |
|---------|---------|---------|------|
| 4.2.1   | 品質手冊 | 1 份    | 須含目錄與章節索引 |
| 4.2.2   | SOP     | N 份    | 每個作業流程一份 |
```

生成規則：
- 每個條款至少一筆記錄
- 數量需求不明確時填入「待確認」
- 備註欄填入條款原文中的特殊要求或注意事項
- 最終清單依條款編號升冪排列
- 可輸出 Markdown 表格（預設）或 Excel（當 Manager 明確指定時）

## NOT This Agent's Job

以下工作**不屬於** document-collector，收到時必須 Scope Guard 拒絕並建議正確 agent：

| 工作內容 | 應派給 |
|---------|-------|
| 比對原廠提供文件與清單的符合程度 | qsd/compliance-checker |
| SOP 重命名、文件整理與歸檔 | qsd/compliance-checker 或 qsd/manager |
| 填寫 QSD checklist 表格 | qsd/compliance-checker 或 qsd/manager |
| 產生 QSD 結案報告 | qsd/manager |
