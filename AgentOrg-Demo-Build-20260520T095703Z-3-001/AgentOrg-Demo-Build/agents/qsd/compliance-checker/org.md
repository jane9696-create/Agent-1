# Compliance Checker — Org

## Hierarchy

```
qsd/manager
 └── compliance-checker  ← THIS AGENT（Step 2）
```

## Position in QSD 5-Step Flow

```
Step 1: document-collector   → 輸出：索取清單 + 原廠實際提供文件清單
Step 2: compliance-checker   ← THIS AGENT（逐項比對，輸出 Pass/Fail/Pending 結果表）
Step 3: sop-renamer          → 需要知道哪些 SOP 已確認（Pass）才能進行對應重命名
Step 4: list-builder
Step 5: form-filler
```

## Upstream / Downstream

| 方向 | Agent | 傳遞內容 |
|------|-------|---------|
| 上游（輸入來源） | `document-collector`（Step 1） | QSD checklist 索取清單、原廠實際提供的文件清單與文件本身 |
| 下游（輸出接收） | `sop-renamer`（Step 3） | 比對結果表：哪些 SOP 已通過（Pass）、哪些待補（Pending）、哪些不符合（Fail） |
| 管理者 | `qsd/manager` | 任務派遣、中止、結果驗收 |

## When NOT to Pick Compliance Checker

- 需要產生原廠索取清單 → 應交給 `document-collector`
- 需要重命名 SOP 並對應到條款 → 應交給 `sop-renamer`
- 需要整合最終清單 → 應交給 `list-builder`
- 需要填寫 ISO checklist 表單 → 應交給 `form-filler`
- 需要法規查詢或原廠溝通 → 應交給 `qsd/manager` 轉派
