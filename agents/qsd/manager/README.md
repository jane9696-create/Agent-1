# QSD Manager

## 用途

QSD Manager 是 QSD（Quality System Documentation）標準模式合規性審查流程的指揮官。它協調 5 個 worker agent 完成醫療器材製造商文件的完整合規審查，確保文件符合：

- 台灣醫療器材品質管理系統準則
- ISO 13485:2016（醫療器材品質管理系統國際標準）

QSD Manager 不親自執行任何文件操作——它負責分派、協調、驗證、綜合。

## 觸發條件（Trigger Conditions）

使用 `/mrs-qsd-standard` 或直接描述以下需求時觸發：

- QSD 標準模式合規性審查
- 醫療器材品質管理系統文件稽核
- ISO 13485:2016 合規文件審查
- QSD checklist 比對作業
- SOP 批量重命名（`SOP number@SOP subject@SOP version` 格式）
- QSD app form-E-Annex 2 填寫

## 輸入需求（Required Inputs）

全流程審查需要以下文件：

| 步驟 | 必要輸入 |
|------|---------|
| Step 1 | QSD checklist Excel 檔案路徑 |
| Step 2 | 原廠提供的文件資料（路徑或資料夾）|
| Step 3 | 原始 SOP 檔案資料夾路徑 |
| Step 4 | 重命名後 SOP 清單 + 原廠 SOP list + Tier 2 SOP list + Documentation Master list |
| Step 5 | Quality Manual + 所有 SOP + QSD app form-E-Annex 2 空白模板 |

若只執行單一步驟，只需提供對應步驟的輸入。

## 輸出產物（Deliverables）

| 步驟 | Worker | 輸出 |
|------|--------|------|
| Step 1 | document-collector | 向原廠索取文件的完整清單（Markdown / Excel） |
| Step 2 | compliance-checker | 逐項比對結果表（Pass / Fail / Pending 標示） |
| Step 3 | sop-renamer | 重命名後的 SOP 檔案（格式：`SOP number@SOP subject@SOP version`） |
| Step 4 | list-comparator | 四份清單交叉比對差異報告 |
| Step 5 | form-filler | 填寫完成的 QSD app form-E-Annex 2 |

最終交付還包含：合規總覽報告、所有 worker 打卡明細表。

## 注意事項

- 5 步驟必須**依序執行**，前步驗證通過後才進入下步
- 缺少必要 input 文件時，Manager 會暫停並請求用戶提供
- 所有產出檔案寫入 `output/qsd/{task_id}/`
