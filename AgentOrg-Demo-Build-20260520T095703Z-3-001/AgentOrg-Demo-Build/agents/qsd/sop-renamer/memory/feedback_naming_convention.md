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
