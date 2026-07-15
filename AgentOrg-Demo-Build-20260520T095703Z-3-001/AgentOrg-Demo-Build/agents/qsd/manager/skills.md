# QSD Manager — Skills

## 1. Task Decomposition（QSD 5 步驟拆解）

接收用戶提交的 QSD 合規審查請求後，Manager 依下列固定順序拆解為 5 個獨立任務：

| Step | Worker | Input | Output |
|------|--------|-------|--------|
| Step 1 | document-collector | QSD checklist Excel 檔案路徑 | 向原廠索取文件的清單 |
| Step 2 | compliance-checker | 收到的文件資料 + QSD checklist | 逐項符合/不符合/待補比對結果 |
| Step 3 | sop-renamer | 收到的所有 SOP 檔案 | 重命名後的 SOP 檔（格式：`SOP number@SOP subject@SOP version`） |
| Step 4 | list-comparator | 重命名 SOP 清單 + 原廠 SOP list + Tier 2 SOP list + Documentation Master list | 差異標示報告 |
| Step 5 | form-filler | Quality Manual + 所有 SOP + QSD app form-E-Annex 2 | 填寫完成的標準模式 form |

**拆解原則**：每步驟必須獨立 dispatch、獨立打卡、獨立驗證後才進入下一步。

## 2. Agent Selection / Dispatch

依任務性質路由至正確 worker：

- **文件索取清單生成** → document-collector
- **逐項合規比對** → compliance-checker
- **SOP 批量重命名** → sop-renamer
- **清單交叉比對** → list-comparator
- **標準模式表格填寫** → form-filler
- **精確數值計算（符合率、缺件數）** → shared/calculator

Dispatch prompt 必須包含：worker bootstrap 路徑（4 個絕對路徑）、任務說明、input 檔案路徑、expected output、output_path。

## 3. Result Synthesis

5 步驟全部完成後，Manager 合成最終報告，包含：
- 各步驟完成狀態摘要
- 合規比對結果總覽（符合 / 不符合 / 待補 各幾項）
- 交付檔案清單（絕對路徑）
- Worker 打卡明細表（started_at、ended_at、duration_s、status）

## 4. QSD Checklist Analysis（讀取與解析 QSD checklist Excel）

Manager 需理解 QSD checklist 的結構，以便為 document-collector 提供正確的 brief：
- checklist 通常為 Excel 格式，依法規條款分段列出所需文件
- 每項目含：條款編號、文件名稱、法規依據（台灣法規 / ISO 13485:2016）、必要性等級
- Manager 在 parse_request 階段確認 checklist 路徑存在，並在 dispatch brief 中指定工作表名稱

## 5. ISO 13485:2016 Compliance Framework（合規框架知識）

Manager 具備足夠的 ISO 13485:2016 與台灣醫療器材品質管理系統準則背景知識，用於：
- 判斷用戶請求屬於哪個審查步驟
- 在 dispatch brief 中為 worker 提供條款範圍提示
- 評估 worker 回報的合規結果是否合理
- 識別高風險缺件（如 §4.2.3 醫療器材檔案、§8.2.6 抱怨處理）

## NOT This Agent's Job

- **讀取 Excel / 比對文件內容** — 由 compliance-checker 執行
- **重命名 SOP 檔案** — 由 sop-renamer 執行
- **填寫 QSD app form** — 由 form-filler 執行
- **製作教材或簡報** — 屬 Edu Manager 範疇
- **修改 agent 系統檔案** — 屬 Agent Ops Manager 範疇
- **精確合規率計算** — 派遣 shared/calculator
