---
name: feedback-naming-convention
description: 無法從檔名解析的 SOP，應讀取 PDF 內容取得正確命名，不得使用 _NEEDS_MANUAL_REVIEW_ 前綴
metadata:
  type: feedback
---

命名規則：`檔案號碼@檔案名稱@版次.副檔名`

**Why:** 使用者明確指出 `_NEEDS_MANUAL_REVIEW_20119650` 的命名方式錯誤。加前綴會污染檔名，不符合 `號碼@名稱@版次` 格式要求。

**How to apply:**
- 若檔名缺少 `@` 格式（如 `20119650.pdf`），**必須讀取 PDF 第 1 頁**提取 Doc ID、Title、Version
- 取得資訊後依格式另存新檔：`DocID@Title@Version.pdf`
- 只有在讀取 PDF 後仍無法取得任一必要欄位時，才在 manifest 標記 `⚠ 待人工確認`，但副本仍以已知的部分命名（例如 `20119650@(UNKNOWN)@(UNKNOWN).pdf`），不加 `_NEEDS_MANUAL_REVIEW_` 前綴

---

## 2026-07-27 — 法文版 `_FR` 標記位置修正（QSD IBJB Step 3 客戶回饋）

**Why:** QSD IBJB 案 Step 3 產出 48 份重命名 SOP，其中 29 份法文版最初命名為
`number@subject@version_FR.pdf`（`_FR` 加在檔名最尾端、版本之後）。客戶回饋此格式不正確。

**Correct format:** `_FR` 應加在 **SOP subject 之後、第二個 `@` 之前**，而非加在檔名最尾端：

```
正確：SOP number@SOP subject_FR@SOP version.ext
錯誤：SOP number@SOP subject@SOP version_FR.ext
```

**How to apply:**
- 判斷文件內容語言為法文時，將 `_FR` 直接附加於 subject 欄位字串尾端（例如
  subject=`Service Client` → `Service Client_FR`），version 欄位維持乾淨、不含任何語言標記。
- 英文版（或無需語言標記的版本）維持標準 `number@subject@version.ext` 格式不變。
- 產生新檔名前，先在腦中/暫存變數組出完整字串再輸出，避免把 `_FR` 誤植到版本或副檔名前。
- 若下次審查案又遇到法文（或其他語言）版本需要標記，一律套用此規則，不再使用「標記加在檔名尾端」的舊格式。

---

## 2026-07-27 — 版本欄不得含 `Rev.` 文字前綴（QSD IBJB Step 3 客戶回饋）

**Why:** QSD IBJB 案 Step 3 產出的 48 份 SOP，版本欄原本統一格式化為 `Rev. 1`、
`Rev. 2`、`Rev. 3`（含文字前綴與空格）。客戶回饋版本欄不需要包含 `Rev.` 文字。

**Correct format:** 版本欄應只含阿拉伯數字，不含 `Rev.`、`Rev`、版次等文字前綴，
格式為 `number@subject[_FR]@數字.ext`：

```
正確：SOP number@SOP subject[_FR]@2.ext
錯誤：SOP number@SOP subject[_FR]@Rev. 2.ext
```

**How to apply:**
- 版本欄一律只寫出阿拉伯數字本身（如 `1`、`2`、`3`），不加任何文字前綴或空格。
- 若原始檔名或封面頁版次標示為 `Rev. 2`、`Rev2`、`第2版`、`版次二` 等含文字的格式，
  一律萃取其中的阿拉伯數字部分作為版本欄，其餘文字一律捨棄。
  （若版次以中文數字或羅馬數字表示且無法安全轉換為阿拉伯數字，維持標記 `⚠ NEEDS_REVIEW`，
  不得猜測轉換。）
- number、subject（含 `_FR` 標記）欄位不受此規則影響，維持既有規則不變。
- 若同一 SOP number 有多個版次（如 `SMQ-SOP-021` 的版次 1、2），去除 `Rev.` 文字後
  版本欄仍為不同數字，足以區分、不構成撞名；產生新檔名前應先做全批次的撞名檢查。
- 下次審查案的版本欄一律套用此「純數字」格式，不再使用「`Rev. X`」舊格式。

---

## 2026-08-11 — 原廠「補件」情境的處理方式（QSD IBJB Step 3，第二批 11 份英文 SOP）

**情境**：本案 Step 3 完成 48 份重命名後，原廠 IBJB 事後補件提供先前缺少的英文版 SOP
（15 份 PDF，其中 4 份與已處理檔案 md5 相同為純重複件，11 份為真正新文件）。

**How to apply（給下次遇到「補件」/「後續批次」情境的 sop-renamer 參考）**：
- **先做 md5／重複比對，非本 agent 職責時交給 Manager 判斷**：本案由 Manager 先核對 md5
  排除 4 份重複件，sop-renamer 只處理確認為新文件的部分，不自行臆測何者重複。
- **輸出到既有輸出資料夾，而非另開新資料夾**：補件的新檔案應 `shutil.copy2` 到與先前批次
  相同的 `output/step3_renamed_sops/`，讓輸出資料夾成為單一、累積、完整的集合，不因為
  補件而拆成多個資料夾。複製前務必先確認目的檔名是否已存在，若存在需停止並回報，
  不得覆蓋既有檔案（本案 11 份新檔名皆未與既有 48 份撞名，順利複製）。
- **對照清單（manifest）採「新增章節」而非重寫全文**：在既有 manifest 檔案中新增一個
  獨立章節記錄本批補件的對照結果，並更新檔首總計數字與統計摘要表格；不覆蓋、不刪除
  先前章節內容，維持完整歷史軌跡。
- **即使檔名看似能對應既有「缺件清單」，仍須逐份實際開啟 PDF 核對**：本案 11 份新檔案的
  數量剛好等於先前記錄「English SOP No. = Not available」的 11 份法文 SOP 缺件數，但不可
  僅憑數量或編號猜測配對關係。每份新 PDF 首頁均有「(Translate of XXX-SOP-YYY)」的
  自我標註可直接引用作為配對依據；若無此類標註，則需比對主題內容判斷對應關係，
  不得依編號規律（如「新編號比原編號多幾號」）猜測。
- **英文翻譯版命名不加 `_FR`**：翻譯版本身語言為英文，判斷語言後依標準格式
  `number@subject@version.pdf` 命名，不加任何語言標記；`_FR` 僅用於法文正本。
- **主題原文含 `/`（如 IVDR 法規編號 `2017/746`）時，依既有慣例改為 `-`**，因 `/` 為路徑
  分隔符號、不可出現於檔名，且本案先前處理法文正本 `CONCEPT-SOP-003`（RDIV 2017/746）
  時已建立此替換慣例，本次比照辦理維持一致性。
- **配對關係僅記錄於 sop-renamer 產出的對照表，不越界更新 Tier 2 清單**：確認某新英文檔
  對應哪份法文正本、是否使「Not available」缺件配齊，屬於 list-comparator／Manager 的
  下游工作範圍；sop-renamer 只需在自己的 manifest 中如實記錄配對依據，供下游引用，
  不自行修改 Tier 2 清單檔案（Scope Guard）。
