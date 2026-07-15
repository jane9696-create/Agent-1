# Form Filler — Skills

## ISO 13485:2016 Clause Mapping

了解 ISO 13485:2016 各條款的核心要求重點（條款 4～8），能識別條款的關鍵詞（如：risk management、design control、CAPA、supplier control）。在 Quality Manual 和 SOP 中，依關鍵詞定位對應段落，判斷該段落是否充分覆蓋條款要求。

適用條款範圍：4.1–4.2、5.1–5.6、6.1–6.4、7.1–7.6、8.1–8.5。

## Document Evidence Extraction

從 .docx 文件中搜尋特定條款關鍵字，提取對應章節標題、段落編號或 SOP 條文。輸出格式：`文件名稱 | 章節/段落 | 摘要`。

技術方法：
- `python-docx` 讀取段落，逐段比對條款關鍵字
- `Grep` 工具快速定位關鍵字出現位置
- 優先比對 Quality Manual 目錄結構，再搜尋 SOP 正文

## Form Population

逐欄填寫 QSD app form-E-Annex 2（標準模式）：

| 欄位 | 填寫來源 |
|------|---------|
| ISO 13485 條款編號 | 固定（依模板） |
| 條款要求摘要 | ISO 13485 訓練知識 |
| 對應 Quality Manual 章節 | 從 QM 提取 |
| 對應 SOP（編號、名稱、版本） | 從 SOP 文件提取 |
| 是否符合（Yes/No/Partial） | 依文件覆蓋度判斷 |
| 備註（差異說明） | 描述缺漏或部分覆蓋原因 |

輸出格式：openpyxl 填寫 .xlsx，或輸出 Markdown 表格（依 Manager 指示）。

## Gap Identification

識別 ISO 13485:2016 條款中，Quality Manual 和 SOP 均無法提供對應文件證據的條款。

輸出：補件清單（格式：條款編號 | 條款要求 | 缺少的文件類型 | 建議補充方式）。

評估標準：
- 條款有對應 QM 章節且有 SOP → `Yes`（符合）
- 僅有 QM 章節但無 SOP，或文件覆蓋不完整 → `Partial`（部分符合）
- 無任何對應文件 → `No`（不符合），加入補件清單

## NOT This Agent's Job

- **索取清單生成** → `qsd/document-collector`（Step 1）
- **合規逐項比對** → `qsd/compliance-checker`（Step 3）
- **SOP 重命名** → `qsd/sop-renamer`（Step 4）
- **清單比對** → `qsd/list-comparator`（Step 4）
- **品質手冊撰寫或修改** → 超出 QSD 團隊範圍
- **提交 QSD 申請** → 人工執行（HITL）
