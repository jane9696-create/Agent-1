# SOP Renamer Memory Index

## Purpose
此檔案儲存 sop-renamer agent 在歷次任務中學到的命名模式與解析規則，
供後續任務的 check_memory 步驟載入，提升解析準確率。

## Learned Naming Patterns
<!-- sop-renamer 在任務執行後自動更新此區塊 -->

## Resolved Edge Cases

- `20119650.pdf`（QSD50750 Millipore 2026）：檔名僅含編號，讀取 PDF 第 1 頁取得 Title=`DOCUMENT MANAGEMENT AT MERCK LIVINGSTON`、Version=`39.0`，正確命名為 `20119650@DOCUMENT MANAGEMENT AT MERCK LIVINGSTON@39.0.pdf`

## Feedback Rules

- [[feedback-naming-convention]] — 禁用 `_NEEDS_MANUAL_REVIEW_` 前綴；無法從檔名解析時必須讀取 PDF 內容，見 `feedback_naming_convention.md`

## Known Unresolvable Patterns
<!-- 記錄曾被標記 NEEDS_REVIEW 的命名模式，避免重複嘗試解析 -->

## Last Updated
<!-- ISO 8601 timestamp, updated after each run -->
