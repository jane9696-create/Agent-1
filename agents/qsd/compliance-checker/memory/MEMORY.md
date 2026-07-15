# Compliance Checker Memory Index

## 預設 Checklist（比對基準）

| 項目 | 值 |
|------|-----|
| 路徑 | `C:\D\MRS client-2014\MRS\AI training\Claude-QSD\1. QSD standard checklist.xls` |
| 工作表 | `QSD standard`（index 0） |
| 讀取方式 | `xlrd.open_workbook(path, encoding_override='cp950')` |
| 欄位 | Col 0 = 條款編號 / Col 1 = 文件名稱 / Col 2 = 細部需求 |
| 更新日期 | 2026-06-03 |

---

## Part A：核心文件 9 項 — 細部需求對照表

Step 2 比對時，**必須逐條核查原廠文件是否滿足以下細部需求**，不得僅憑文件存在判 Pass。

| 條款 | 文件名稱 | 細部需求（Col C） |
|------|---------|-----------------|
| 1.0 | ISO 13485:2016 certificate | ISO scope 是否包含申請品項 |
| 2.1 | Quality manual | （無細部需求，確認版本、核准人、日期齊全即可） |
| 2.2 | SOP list | 須為**英文**；項目4提供的所有 SOP 均需列於 SOP list 中 |
| 3.0 | Basic site information letter | 須包含以下所有資訊：①名稱、②地址、③經緯度、④電子郵件、⑤負責人、⑥電話、⑦傳真、⑧成立年份、⑨員工人數；並說明：⑩自前次取得QSD製造許可以來原製造廠是否有任何變更、⑪製造廠於本申請案是否已提供最新有效版本之品質手冊/文件總覽表/品質系統程序文件、⑫台灣代理商的名稱及地址、⑬授權代理商執行QSD申請、⑭授權台灣代理商在發生產品有嚴重不良反應或產品回收事件時執行 |
| 4.0 | Plan layout | 至少標示：大門、倉庫、進料、出貨、生產製造、包裝、檢驗、人員辦公室 |
| 5.0 | Production area diagram | 須標示製造作業區域內之：配置、人員動線、原物料動線、成品動線 |
| 6.0 | Major equipment list | 須將**生產製造設備**與**檢驗設備**分開列示 |
| 7.0 | Manufacturing flowchart | 依申請品項分類；若委託滅菌作業，須附受託廠 ISO 13485 證書 |
| 8.0 | Medical Device Files | 依醫療器材品質管理系統準則第11條要求，須含：「醫療器材概述、預期用途或目的及標示」、「產品規格」、「製造、包裝、儲存、搬運及運銷之規格、程序」、「量測及監管程序」、「必要之安裝要求」、「必要之服務要求」；原廠需提供申請範圍內所有醫療器材檔案之資料及程序 |

**注意：本 checklist 不含 ADR & Recall SOPs 獨立文件要求；ADR/Recall 授權聲明已整合於 3.0 Basic site info letter 細部需求第⑭項。**

---

## Part B：Module 2 SOP 比對範圍（ISO 13485:2016）

以下章節各需有對應 Tier 2 SOP（Col C 均為空白，確認 SOP 存在且版本有效即可）：

**Section 1 — 4. Quality management system**
4.1 / 4.2.1 / 4.2.2 / 4.2.3 / 4.2.4 / 4.2.5

**Section 2 — 5. Management responsibility**
5.1 / 5.2 / 5.3 / 5.4.1 / 5.4.2 / 5.5.1 / 5.5.2 / 5.5.3 / 5.6.1 / 5.6.2 / 5.6.3

**Section 3 — 6. Resource management**
6.1 / 6.2 / 6.3 / 6.4.1 / 6.4.2

**Section 4 — 7. Product realization**
7.1 / 7.2.1 / 7.2.2 / 7.2.3 / 7.3.1–7.3.10 / 7.4.1–7.4.3 / 7.5.1–7.5.11 / 7.6

**Section 5 — 8. Measurement, analysis and improvement**
8.1 / 8.2.1–8.2.6 / 8.3.1–8.3.4 / 8.4 / 8.5.1–8.5.3

---

## 比對判斷規則

| 結果 | 條件 |
|------|------|
| **Pass** | 文件存在且所有細部需求均已滿足 |
| **Pending** | 文件存在但細部需求部分未確認，或需人工核實 |
| **Fail** | 文件缺失，或文件存在但明確未滿足細部需求 |
| **N/A** | QM 明確聲明不適用（如安裝、維修、滅菌等活動） |

---

## 已知用戶偏好

- ADR & Recall SOPs：不列為獨立比對項目（已整合於 3.0 Basic site info letter）
- 報告語言：繁體中文
- 輸出格式：Markdown 表格

## Lesson Learned

- 2026-06-03：換用新版 checklist（9 項核心文件），細部需求從 Col C 實際讀取
- 2026-06-03：3.0 Basic site info letter 的細部需求第⑭項包含 ADR/Recall 授權確認，不另立獨立項目
- 2026-06-03：2.2 SOP list 須為英文，且需涵蓋實際提供的所有 Tier 2 SOP
