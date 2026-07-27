# Form Filler Memory Index

## 2026-07-27 — QSD IBJB Step5

- **模板格式陷阱**：form-E-Annex 2 標準模式模板實際可能是 `.odt`（非預設 .xlsx）。其表格結構為 1 個 table、7 個 grid 欄（非視覺欄數，因大量橫向 merge）：col0/col1=勾選框，col2=Article 編號（含 Section 標題列時整列 merge），col3+col4=ISO 13485 條款編號與名稱（merge 顯示為重複文字），col5=Procedure number（待填），col6=Version（待填）。Section 標題列（如「Section 2 Quality management system」）以 `cells[2].text.strip().startswith("Section")` 可辨識並跳過。
- **環境問題**：本 sandbox 初始只裝 `libreoffice-core`/`libreoffice-common`，未裝 `libreoffice-writer`/`libreoffice-calc`，導致 `soffice --headless --convert-to` 對任何檔案都回報「Error: source file could not be loaded」（含轉純文字檔），非常誤導（像是檔案損毀，其實是元件缺失）。修復：`apt-get update && apt-get install -y libreoffice-writer libreoffice-calc`。診斷方法：`dpkg -l | grep libreoffice`，若只有 core/common 沒有 writer/calc，就是此問題。
- **轉檔流程**：odt→docx（python-docx 編輯表格）→docx→odt（soffice），並務必再 odt→docx 做一次回轉驗證（round-trip check）確認表格列數/欄數/內容無損，再交付 .odt。
- **雙語 SOP 對應**：製造廠常見「法文原版 SOP + 既有英文翻譯版（不同編號前綴，如 QO-SMQ-SOP-XXX 或另編號 SMQ-SOP-02X）」並存，填 Procedure number 時建議兩者並列（法文正本編號 + 英譯版編號），優先引用英文版利於可讀性，若僅有法文版需標註「僅法文版」。
- **Yes/Partial/No 判定原則**：延用 compliance-checker（Step2）報告的內容驗證結果，但當 Step2 備註出現「假設」「未逐頁驗證」「依標題判」等推定性語言而非「已開啟內容確認」時，應下修為 Partial（避免因循 Step2 的樂觀推定），並在備註註明建議人工複核，以符合 form-filler 更嚴謹的可追溯性標準。
- **無版本文件（如 MDF）**：若文件本身確實無 Rev. 標示，如實填寫「版本未標示於文件」，不可臆測版本號。

## 2026-07-27 — 客戶回饋：Version 欄位格式（QSD IBJB Step5 修正）

- **Version 欄位應只含阿拉伯數字，不含 `Rev.` 文字前綴**。此為 QSD 團隊本次審查（`sop-renamer` 與 `form-filler`）一致採用的客戶偏好：客戶回饋 Step 5 表格 Version 欄的 `Rev. X` 格式與 Step 3 SOP 重命名版本欄修正不一致，應統一改為純數字 `X`。
- **後續填寫規範**：日後填寫 form-E-Annex 2 的 Version 欄時，應直接填入純數字（如 `3`、`1 / 2`），不要加 `Rev.` 前綴；同一格若引用多份 SOP 而有多個版本值，以 `/` 分隔各數字即可。
- **修正機械式處理方法**（供後續類似格式修正參考）：以 python-docx 開啟 docx 工作版本，對 Version 欄（表格 grid col index 6）每個儲存格段落的 run 文字套用正則 `Rev\.?\s*(\d+)`（case-insensitive）取代為捕獲群組 `\1`，可正確處理 `Rev. X`、`Rev.X`、`Rev X` 等變形及多個以 `/`（或 `+`）分隔的版本值；純解釋性文字（如「版本未標示於文件（原文無 Rev. 標示）」）因其後未直接接數字，此正則不會誤動，可安全略過，不需另外排除規則。修正後仍須走 docx→odt→docx 回轉驗證流程確認表格列數/欄數/內容無損且無 `Rev.` 殘留。

