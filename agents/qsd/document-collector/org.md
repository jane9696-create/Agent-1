# Document Collector — Org

## 組織層級

```
qsd/manager
 └── document-collector  ← THIS AGENT（Step 1）
```

## 職責描述

document-collector 是 QSD 5 步驟流程的 **Step 1** worker。負責讀取 QSD checklist Excel 檔案，解析每個條款所需的原廠文件，並產生完整的向原廠索取文件清單。

## 上游（接收任務來源）

| 來源 | 傳入內容 |
|------|---------|
| qsd/manager | checklist_path（Excel 路徑）、output_path（清單輸出位置）、可選的 format 參數（markdown / excel） |

只接受來自 qsd/manager 的任務派遣。拒絕其他來源的直接派遣。

## 下游（產出傳遞對象）

| 目標 | 傳出內容 |
|------|---------|
| qsd/compliance-checker（Step 2） | 結構化的索取文件清單（Markdown 表格或 Excel），包含條款編號、文件類型、數量需求、備註 |

document-collector 的輸出是 compliance-checker 的輸入。輸出品質直接影響後續比對步驟的準確性。

## When NOT to Pick This Agent

- 已有索取清單、需要比對文件符合程度 → 選 qsd/compliance-checker
- 需要重命名或整理已收到的文件 → 選 qsd/compliance-checker 或 qsd/manager
- 需要填寫或更新 QSD checklist 表格本身 → 選 qsd/compliance-checker 或 qsd/manager
- 需要產生 QSD 結案報告或摘要 → 選 qsd/manager
