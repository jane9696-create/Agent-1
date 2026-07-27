# Form Filler Memory Index

## 2026-07-27 — QSD IBJB Step5

- **模板格式陷阱**：form-E-Annex 2 標準模式模板實際可能是 `.odt`（非預設 .xlsx）。其表格結構為 1 個 table、7 個 grid 欄（非視覺欄數，因大量橫向 merge）：col0/col1=勾選框，col2=Article 編號（含 Section 標題列時整列 merge），col3+col4=ISO 13485 條款編號與名稱（merge 顯示為重複文字），col5=Procedure number（待填），col6=Version（待填）。Section 標題列（如「Section 2 Quality management system」）以 `cells[2].text.strip().startswith("Section")` 可辨識並跳過。
- **環境問題**：本 sandbox 初始只裝 `libreoffice-core`/`libreoffice-common`，未裝 `libreoffice-writer`/`libreoffice-calc`，導致 `soffice --headless --convert-to` 對任何檔案都回報「Error: source file could not be loaded」（含轉純文字檔），非常誤導（像是檔案損毀，其實是元件缺失）。修復：`apt-get update && apt-get install -y libreoffice-writer libreoffice-calc`。診斷方法：`dpkg -l | grep libreoffice`，若只有 core/common 沒有 writer/calc，就是此問題。
- **轉檔流程**：odt→docx（python-docx 編輯表格）→docx→odt（soffice），並務必再 odt→docx 做一次回轉驗證（round-trip check）確認表格列數/欄數/內容無損，再交付 .odt。
- **雙語 SOP 對應**：製造廠常見「法文原版 SOP + 既有英文翻譯版（不同編號前綴，如 QO-SMQ-SOP-XXX 或另編號 SMQ-SOP-02X）」並存，填 Procedure number 時建議兩者並列（法文正本編號 + 英譯版編號），優先引用英文版利於可讀性，若僅有法文版需標註「僅法文版」。
- **Yes/Partial/No 判定原則**：延用 compliance-checker（Step2）報告的內容驗證結果，但當 Step2 備註出現「假設」「未逐頁驗證」「依標題判」等推定性語言而非「已開啟內容確認」時，應下修為 Partial（避免因循 Step2 的樂觀推定），並在備註註明建議人工複核，以符合 form-filler 更嚴謹的可追溯性標準。
- **無版本文件（如 MDF）**：若文件本身確實無 Rev. 標示，如實填寫「版本未標示於文件」，不可臆測版本號。

