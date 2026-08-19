# Form Filler Memory Index

## 2026-07-27 — QSD IBJB Step5

- **模板格式陷阱**：form-E-Annex 2 標準模式模板實際可能是 `.odt`（非預設 .xlsx）。其表格結構為 1 個 table、7 個 grid 欄（非視覺欄數，因大量橫向 merge）：col0/col1=勾選框，col2=Article 編號（含 Section 標題列時整列 merge），col3+col4=ISO 13485 條款編號與名稱（merge 顯示為重複文字），col5=Procedure number（待填），col6=Version（待填）。Section 標題列（如「Section 2 Quality management system」）以 `cells[2].text.strip().startswith("Section")` 可辨識並跳過。
- **環境問題**：本 sandbox 初始只裝 `libreoffice-core`/`libreoffice-common`，未裝 `libreoffice-writer`/`libreoffice-calc`，導致 `soffice --headless --convert-to` 對任何檔案都回報「Error: source file could not be loaded」（含轉純文字檔），非常誤導（像是檔案損毀，其實是元件缺失）。修復：`apt-get update && apt-get install -y libreoffice-writer libreoffice-calc`。診斷方法：`dpkg -l | grep libreoffice`，若只有 core/common 沒有 writer/calc，就是此問題。
- **轉檔流程**：odt→docx（python-docx 編輯表格）→docx→odt（soffice），並務必再 odt→docx 做一次回轉驗證（round-trip check）確認表格列數/欄數/內容無損，再交付 .odt。
- **雙語 SOP 對應**：製造廠常見「法文原版 SOP + 既有英文翻譯版（不同編號前綴，如 QO-SMQ-SOP-XXX 或另編號 SMQ-SOP-02X）」並存，填 Procedure number 時建議兩者並列（法文正本編號 + 英譯版編號），優先引用英文版利於可讀性，若僅有法文版需標註「僅法文版」。
- **Yes/Partial/No 判定原則**：延用 compliance-checker（Step2）報告的內容驗證結果，但當 Step2 備註出現「假設」「未逐頁驗證」「依標題判」等推定性語言而非「已開啟內容確認」時，應下修為 Partial（避免因循 Step2 的樂觀推定），並在備註註明建議人工複核，以符合 form-filler 更嚴謹的可追溯性標準。
- **無版本文件（如 MDF）**：若文件本身確實無 Rev. 標示，如實填寫「版本未標示於文件」，不可臆測版本號。

## 2026-08-11 — QSD IBJB Step5 追補：原廠補件英文SOP的引用更新

- **任務性質辨識**：本次任務是「已填妥表格因上游文件補件而需局部更新引用」，非重新填表或重新審查。執行前應先明確任務邊界（僅新增英文版引用，不變動判定），並在完成後以逐格 diff（python-docx 讀取兩版本表格，比對每列每欄 text）量化驗證「只改了預期的欄位」，而非僅憑肉眼檢查或信任自己的編輯清單。本次以 diff 統計「25 列 × 2 欄 = 50 格差異，其餘 0 差異」作為越權防呆的具體證據，此方法可複用於未來任何「局部修訂已交付表格」的任務。
- **不可僅憑上游 agent（如 sop-renamer）的配對記錄就直接改表**：即使收到的配對關係已註明「經開啟 PDF 內容確認 (Translate of X) 自我標註，非猜測」，form-filler 仍應自行重新開啟每一份新文件核閱，原因：(1) 上游 agent 的「確認」可能只驗證了標題自我標註，未必核對章節結構與內容深度是否足以支持原本的 Yes/Partial 判定；(2) 版本號、章節編號等細節仍可能與表格原引用的法文版有出入，需 form-filler 自己核對後才能安全更新欄位。本次以 `pypdf` 全文擷取這 11 份英文版 PDF，逐份核對標題頁自我標註、Table of Contents 章節編號與表格原引用的 §X.Y 是否一致，確認無誤後才動筆修改。
- **雙語 SOP 引用格式（法文正本 + 新到英文版）之欄位聯動機制**：Procedure number 欄（col5）與 Version 欄（col6）在 python-docx 表格中常以「段落（paragraph）」為單位一一對應——col5 某段落內以「/」或「+」分隔的多個文件代碼，其版次會依「相同順序」出現在 col6 對應段落的「/」分隔數字列表中（即使 col5 該段落內另含與代碼無關的「/」，如中文說明文字「訂單/需求審查」或章節「§7.3 / §7.6」，也不影響——因為版次列表的項目數與「實際文件代碼數」而非「/」出現次數對應，須以代碼 regex 辨識而非單純按「/」切割字串）。新增一份英文版引用時，需：(1) 在 col5 對應段落中，緊接在該法文代碼後插入 " / {英文代碼} (EN)"；(2) 在 col6 對應段落的版次列表中，於相同位置插入同一版次數字（因原廠提供的翻譯版版次與法文正本版次一致）。特殊情況：若 col5 是單一段落但内含以「+」分隔的兩個邏輯子句（如 "CODE-A §X + CODE-B (FR)/CODE-C (EN) 說明"），col6 可能仍以「兩個段落」分別對應「+」前後兩個子句（而非以 col5 段落數對應）——編輯前務必先以 `paragraphs` 屬性逐一印出 col5/col6 的段落列表核對，不可假設兩欄段落數必然相等。
- **移除「僅法文版」備註的替代寫法**：原「（FR，僅法文版）」統一改為「（FR）」+ 新增「(EN)」代碼，並視版面簡潔需要加註「（原廠已補件提供英文版）」，非強制每處都加、但同一份文件於同一列多次出現時應至少註記一次，避免重複贅述。
- **診斷 PDF 文字工具**：本次環境 `pdftotext`（poppler-utils）未安裝，但 Python `pypdf` 套件可用（`PyPDF2` 不可用），可直接 `pypdf.PdfReader(path).pages[i].extract_text()` 逐頁擷取，足以完成核閱工作，無需額外安裝套件或使用 pdf skill 的完整流程。

## 2026-07-27 — 客戶回饋：Version 欄位格式（QSD IBJB Step5 修正）

- **Version 欄位應只含阿拉伯數字，不含 `Rev.` 文字前綴**。此為 QSD 團隊本次審查（`sop-renamer` 與 `form-filler`）一致採用的客戶偏好：客戶回饋 Step 5 表格 Version 欄的 `Rev. X` 格式與 Step 3 SOP 重命名版本欄修正不一致，應統一改為純數字 `X`。
- **後續填寫規範**：日後填寫 form-E-Annex 2 的 Version 欄時，應直接填入純數字（如 `3`、`1 / 2`），不要加 `Rev.` 前綴；同一格若引用多份 SOP 而有多個版本值，以 `/` 分隔各數字即可。
- **修正機械式處理方法**（供後續類似格式修正參考）：以 python-docx 開啟 docx 工作版本，對 Version 欄（表格 grid col index 6）每個儲存格段落的 run 文字套用正則 `Rev\.?\s*(\d+)`（case-insensitive）取代為捕獲群組 `\1`，可正確處理 `Rev. X`、`Rev.X`、`Rev X` 等變形及多個以 `/`（或 `+`）分隔的版本值；純解釋性文字（如「版本未標示於文件（原文無 Rev. 標示）」）因其後未直接接數字，此正則不會誤動，可安全略過，不需另外排除規則。修正後仍須走 docx→odt→docx 回轉驗證流程確認表格列數/欄數/內容無損且無 `Rev.` 殘留。

