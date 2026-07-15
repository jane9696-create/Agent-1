# List Comparator — Skills

## Multi-list Cross-comparison

同時比對多份清單，識別三種差異類型：
- **我方有，原廠清單無**：重命名清單中存在，但原廠清單中找不到對應 SOP 編號
- **原廠清單有，我方未收**：原廠清單中存在，但重命名清單中找不到對應 SOP 編號
- **版本差異**：SOP 編號匹配，但版本號不一致（如 v1.0 vs v2.0）

三份清單（SOP list、Tier 2 SOP list、Documentation Master list）分別獨立比對，各自產出差異集合。

## SOP ID Normalization

比對前執行正規化，確保格式差異不被誤判為缺漏：
- 全部轉大寫（`QSD-001` = `qsd-001`）
- 去除前後多餘空格（`QSD-001 ` = `QSD-001`）
- 統一連字號（全角「－」→ 半形「-」）
- 移除多餘內部空格（`QSD - 001` → `QSD-001`）

正規化後建立映射表（normalized_id → original_row），再執行集合比對。

## Excel Annotation

使用 openpyxl 在 Excel 儲存格加入差異標記：
- **我方有，原廠無**：在原廠清單對應列加黃色背景（PatternFill）並寫備註「未列入清單」
- **原廠有，我方未收**：在原廠清單對應列加橘色背景並寫備註「我方未收到此 SOP」
- **版本差異**：在版本欄加紅色背景並寫備註「版本不符：我方 {ver_ours} / 原廠 {ver_theirs}」
- 未比中（原廠清單獨有）的新列附加至工作表末尾，標示來源

## Discrepancy Reporting

產生結構化差異摘要報告（Markdown），包含：
- 執行日期、輸入檔案清單、比對參數
- 各份清單的差異統計（三種類型各自條目數）
- 逐條差異清單（SOP 編號、差異類型、版本資訊）
- 總計：我方多 N 筆 / 原廠多 M 筆 / 版本差異 K 筆

## NOT This Agent's Job

- **SOP 重命名** → `qsd/sop-renamer`（Step 3）
- **合規審查** → `qsd/compliance-checker`（Step 2）
- **文件收集** → `qsd/document-collector`（Step 1）
- **表格填寫** → `qsd/form-filler`（Step 5）
- **Excel 表格以外的文件格式解析（PDF 圖片）** → 需人工介入或 OCR 工具
