# Document Collector Memory Index

## 已知 Checklist 格式

### 1. QSD standard checklist.xls（目前預設）

| 屬性 | 值 |
|------|----|
| 路徑 | `C:\D\MRS client-2014\MRS\AI training\Claude-QSD\1. QSD standard checklist.xls` |
| 讀取方式 | `xlrd.open_workbook(path, encoding_override='cp950')` |
| 工作表 | `QSD standard`（index 0） |
| 總列數 | 87 |
| 欄數 | 3 |

**欄位對應：**

| 欄位 index | 意義 |
|-----------|------|
| Col 0 | 條款編號（如 `1.0`、`2.1`、`Section 1`） |
| Col 1 | 說明 / 文件名稱 |
| Col 2 | 補充需求（中文，可能空白） |

**資料結構：**

- Row 0：標題列（跳過）
- Row 1–9：核心文件 9 項（條款 1.0 ~ 8.0，含 2.1、2.2 子項）
- Row 10：空白（跳過）
- Row 11：Module 2 SOP 標題行（`module 2 SOP- Requirements (ISO 13485:2016)`）
- Row 12：空白（跳過）
- Row 13–86：ISO 13485 章節條款（Col 0 = Section N 分組標題，Col 1 = 條款全名）

**核心文件 9 項：**

| Row | 條款編號 | 文件名稱 |
|-----|---------|---------|
| 1 | 1.0 | ISO 13485:2016 certificate |
| 2 | 2.1 | Quality manual |
| 3 | 2.2 | SOP list (SOP number, SOP subject, version) |
| 4 | 3.0 | Basic site information letter |
| 5 | 4.0 | Plan layout |
| 6 | 5.0 | Production area diagram |
| 7 | 6.0 | Major equipment list |
| 8 | 7.0 | Manufacturing flowchart |
| 9 | 8.0 | Medical Device Files |

**注意：此 checklist 不含 ADR & Recall SOPs（舊版第 11 項），無需索取。**

**解析規則：**
- 條款編號欄為空白 + 說明欄非空 → 屬於上一個 Section 的子條款
- 條款編號欄值為 `Section N` → 章節分組標題，跳過不列入索件清單
- Col 2（補充需求）若有中文內容，加入備註欄

---

### 舊版格式備忘（已停用）

- 檔案：`QSD application Checklist-20240809.xlsx`
- 工作表：`TW_QSD standard`
- 格式：`.xlsx`（openpyxl 讀取）
- 核心文件：11 項（含第 11 項 ADR & Recall SOPs）
- **已停用，不再使用**

## Lesson Learned

- 2026-06-03：新版 checklist 為 `.xls`（非 `.xlsx`），必須用 `xlrd` + `encoding_override='cp950'`，否則中文欄位亂碼
- 2026-06-03：新版共 9 項核心文件，舊版 11 項，差異在於移除 ADR & Recall SOPs
