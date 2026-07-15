# Form Filler — Org

## Hierarchy

```
QSD Manager
├── document-collector   (Step 1: 生成索取清單)
├── compliance-checker   (Step 3: 合規逐項比對)
├── sop-renamer          (Step 4: SOP 重命名)
├── list-comparator      (Step 4: 清單比對)
└── form-filler          (Step 5: 表格填寫) ←── THIS AGENT

Shared Services:
└── shared/calculator    (精確數值計算)
```

## Role in QSD 5-Step Flow

| 步驟 | Agent | 輸出 |
|------|-------|------|
| Step 1 | document-collector | 索取清單（TFDA 所需文件清單） |
| Step 2 | （人工）| 收集 Quality Manual + SOP 文件 |
| Step 3 | compliance-checker | 合規比對報告 |
| Step 4 | sop-renamer + list-comparator | 重命名後的 SOP 清單；清單差異報告 |
| **Step 5** | **form-filler** | **填寫完成的 form-E-Annex 2 + 缺件清單** |

## Upstream Inputs

form-filler 接收以下輸入，由 Manager 或上游 worker 提供：

1. **Quality Manual**（品質手冊）— .docx 格式，含 ISO 13485 各章節對應說明
2. **所有 SOP 文件** — .docx 格式，由 document-collector 索取、Step 2 人工收集
3. **list-comparator 輸出**（可選）— SOP 清單確認報告，用於驗證文件完整性
4. **form-E-Annex 2 空白模板** — .xlsx 格式，QSD app 標準模式表格

## Downstream Outputs（最終交付物）

form-filler 是 QSD 流程的**最終交付官**，產出：

1. **填寫完成的 form-E-Annex 2** — .xlsx 或 Markdown 表格，包含所有 ISO 13485 條款的文件對應
2. **缺件清單** — 標示無對應文件的條款，供客戶補件參考
3. **填寫摘要** — 完成率統計（條款總數、Yes/Partial/No 各多少條）

## Collaboration

- **接收自**：QSD Manager（派遣）、上游 workers（文件輸入）
- **回報給**：QSD Manager（交付最終成果）
- **不直接協作**：其他 QSD worker（各 worker 獨立，由 Manager 協調）

## When NOT to Pick Form Filler

- 需要**生成 TFDA 索取文件清單** → 應交給 `qsd/document-collector`
- 需要**執行合規比對**（逐條比對現有文件是否符合法規）→ 應交給 `qsd/compliance-checker`
- 需要**重命名 SOP 文件** → 應交給 `qsd/sop-renamer`
- 需要**比對新舊文件清單差異** → 應交給 `qsd/list-comparator`
- 需要**修改或撰寫 Quality Manual** → 超出 QSD 範圍，需人工處理
- 尚未完成文件收集（Step 2 未完成）→ 缺少輸入文件，無法執行
