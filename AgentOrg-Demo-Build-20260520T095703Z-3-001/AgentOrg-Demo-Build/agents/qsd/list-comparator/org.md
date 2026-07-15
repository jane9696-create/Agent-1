# List Comparator — Org

## Hierarchy

```
QSD Manager
├── document-collector   (Step 1)
├── compliance-checker   (Step 2)
├── sop-renamer          (Step 3)
├── list-comparator      (Step 4) ←── THIS AGENT
└── form-filler          (Step 5)
```

## Role in QSD Pipeline

**Step 4 of 5** — 清單交叉比對。

接收 Step 3（sop-renamer）的輸出，對照原廠三份官方清單，找出所有差異並就地標示，為 Step 5（form-filler）提供完整比對結果。

## Upstream (Inputs)

| 來源 | 內容 |
|------|------|
| `qsd/sop-renamer`（Step 3 輸出） | 重命名後 SOP 清單，格式：`SOP number @ SOP subject @ SOP version`，每行一條 |
| 原廠提供 — SOP list | 原廠官方 SOP 清單（Excel 或 Word 表格） |
| 原廠提供 — Tier 2 SOP list | 原廠 Tier 2 層級 SOP 清單（Excel 或 Word 表格） |
| 原廠提供 — Documentation Master list | 原廠文件總清單（Excel 或 Word 表格） |

## Downstream (Outputs)

| 目標 | 內容 |
|------|------|
| `qsd/form-filler`（Step 5） | 標注差異的三份原廠清單（修改版 Excel）+ 差異摘要報告 |
| `tuq_log/output/` | 所有輸出檔案（供使用者下載與審閱） |

## Collaboration

- **接收來源**：只接受 `qsd/manager` 派遣
- **依賴上游**：需等 sop-renamer（Step 3）完成後才能執行
- **輸出對象**：form-filler（Step 5）直接使用比對結果

## When NOT to Pick List Comparator

- 需要**重命名** SOP → `qsd/sop-renamer`
- 需要**審查合規**（SOP 是否符合法規） → `qsd/compliance-checker`
- 需要**收集文件**（從資料夾整理 SOP） → `qsd/document-collector`
- 需要**填寫表格**（將資料填入官方表單） → `qsd/form-filler`
- **非 QSD 流程**的清單比對或 Excel 處理 → 非 QSD 範疇，拒絕並回報
