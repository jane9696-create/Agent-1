# QSD Manager Memory Index

## 預設 Checklist 路徑

| 項目 | 值 |
|------|-----|
| 路徑 | `C:\D\MRS client-2014\MRS\AI training\Claude-QSD\1. QSD standard checklist.xls` |
| 工作表 | `QSD standard` |
| 格式 | `.xls`（xlrd + encoding cp950） |
| 更新日期 | 2026-06-03 |

> 每次新案件啟動 Step 1 時，若用戶未另行指定 checklist 路徑，預設使用上述路徑。

## Checklist 版本說明

- **新版（目前預設）**：`1. QSD standard checklist.xls`
  - 核心文件：9 項（1.0, 2.1, 2.2, 3.0–8.0）
  - **不含** ADR & Recall SOPs（舊版第 11 項已移除）
  - Module 2 SOP 章節：ISO 13485:2016 完整章節

- **舊版（已停用）**：`QSD application Checklist-20240809.xlsx`（工作表：TW_QSD standard）
  - 核心文件：11 項（含第 11 項 ADR & Recall SOPs）
  - 不再使用

## 已知用戶偏好

- 第 11 項（ADR & Recall SOPs）：依用戶指示排除比對（舊版已存在此項；新版 checklist 已不含此項）
- 觸發語：「執行 [專案名] QSD standard合規審查」即可啟動全流程

## Lesson Learned

- 2026-06-03：用戶更換 checklist 至新版 `.xls`，格式從 `.xlsx` 改為 `.xls`，需注意 xlrd 讀取與 cp950 編碼
