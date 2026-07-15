# SOP Renamer — Org

## Hierarchy

```
QSD Manager
├── document-collector   (Step 1: 採集原始 SOP 檔案)
├── compliance-checker   (Step 2: 合規審查)
├── sop-renamer          ←── THIS AGENT (Step 3: 批量重命名另存)
├── list-comparator      (Step 4: 與主控台清單比對)
└── [Step 5 worker TBD]  (Step 5: 後續處理)
```

## Collaboration

### Upstream — compliance-checker → sop-renamer

`compliance-checker` 完成合規審查後，將通過審查的 SOP 資料夾路徑傳遞給 `sop-renamer`。
`sop-renamer` 接收此資料夾路徑作為輸入，對其中所有 SOP 檔案執行重命名（另存副本）。

### sop-renamer → Downstream — list-comparator

`sop-renamer` 完成後，輸出：
1. **重命名副本資料夾路徑** — 含所有新命名檔案
2. **對照清單（Markdown）** — 原始檔名 → 新檔名 逐行對照，含 `⚠ NEEDS_REVIEW` 標記

`list-comparator` 以此對照清單為基礎，執行 Step 4 的清單比對工作。

### QSD Manager → sop-renamer

Manager 直接派遣 `sop-renamer`，傳入：
- `input_folder`：包含 SOP 檔案的資料夾路徑
- `output_folder`（可選）：另存新檔的目標位置（預設：input_folder 同層的 `renamed/` 子目錄）

## When NOT to Pick sop-renamer

| 情境 | 應選擇的 Agent |
|------|---------------|
| 需要判斷 SOP 內容是否合規 | `qsd/compliance-checker` |
| 需要比對 SOP 清單與資料庫 | `qsd/list-comparator` |
| 需要從多個位置蒐集 SOP 檔案 | `qsd/document-collector` |
| 需要填寫 QSD 提交表格 | QSD 其他 worker |
| 需要轉換檔案格式（pdf → docx 等） | 超出 QSD 範圍 |
| 已是標準格式，只需驗證命名 | 僅用 Naming Validation skill，不需 sop-renamer 全流程 |
