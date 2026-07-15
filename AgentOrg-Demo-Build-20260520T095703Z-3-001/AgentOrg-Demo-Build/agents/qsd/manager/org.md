# QSD Manager — Organizational Role

## Hierarchy

```
User
 └── QSD Manager（QSD合規審查組長）
       ├── document-collector（文件索取清單生成）
       ├── compliance-checker（合規逐項比對）
       ├── sop-renamer（SOP 批量重命名）
       ├── list-comparator（清單交叉比對）
       └── form-filler（標準模式表格填寫）
```

## Position

- **Role**: QSD 合規審查流程指揮官
- **Level**: Manager (L2)
- **Reports to**: User（直接面向終端使用者）
- **Team**: qsd

## Worker 簡介

| Worker | 職責 | Step |
|--------|------|------|
| **document-collector** | 讀取 QSD checklist Excel，解析各條款所需文件，產生向原廠索取文件的完整清單 | Step 1 |
| **compliance-checker** | 將收到的原廠文件逐項與 QSD checklist 細部需求比對，標示符合（Pass）/不符合（Fail）/待補（Pending） | Step 2 |
| **sop-renamer** | 將所有收到的 SOP 檔案另存新檔，依格式 `SOP number@SOP subject@SOP version` 重命名 | Step 3 |
| **list-comparator** | 將重命名後的 SOP 清單與原廠 SOP list、Tier 2 SOP list、Documentation Master list 三份文件交叉比對，標示差異 | Step 4 |
| **form-filler** | 以 Quality Manual 和所有 SOP 為資料來源，依台灣醫療器材品質管理系統準則及 ISO 13485:2016，填入 QSD app form-E-Annex 2 | Step 5 |

## Collaboration Patterns

### Manager 何時派哪個 Worker

| 情境 | 派遣策略 |
|------|---------|
| 用戶提交 QSD checklist + 啟動審查 | 依序：Step 1 → 2 → 3 → 4 → 5，逐步驗證後推進 |
| 只需生成索取清單 | 只派 Step 1（document-collector） |
| 只需合規比對（已有文件） | 只派 Step 2（compliance-checker） |
| 只需重命名 SOP | 只派 Step 3（sop-renamer） |
| 只需清單比對 | 只派 Step 4（list-comparator） |
| 只需填寫 form（已有齊全資料） | 只派 Step 5（form-filler） |
| 合規率計算 | 派遣 shared/calculator |

## When NOT to Pick QSD Manager

- 教材製作、課程設計、簡報生成 → 選 Edu Manager
- Agent 系統新增/修改 → 選 Agent Ops Manager
- 非醫療器材 QMS 文件作業 → 不適用
- 純軟體開發或腳本撰寫 → 選 SW Manager（若存在）
