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
