# SOP Renamer — Skills

## Skill 1: SOP Filename Parsing

**目的**：從檔名或 SOP 首頁/封面頁解析出三個欄位：SOP number、SOP subject、SOP version。

**識別常見命名慣例**：

| 原始模式 | 解析結果 |
|----------|----------|
| `QMS-001_Document Control_v2.1.pdf` | number=`QMS-001`, subject=`Document Control`, version=`v2.1` |
| `HR-SOP-005 Training Records Rev3.docx` | number=`HR-SOP-005`, subject=`Training Records`, version=`Rev3` |
| `SOP-IT-003_Access Management-V1.0.pdf` | number=`SOP-IT-003`, subject=`Access Management`, version=`V1.0` |
| `002_EquipmentCalibration_r4.xlsx` | number=`002`, subject=`EquipmentCalibration`, version=`r4` |

**解析規則**：
- SOP number：字母數字組合，常含連字號，通常為第一段
- SOP subject：描述性名稱，可能含空格或底線
- SOP version：以 `v`、`V`、`Rev`、`r`、`R` 前綴加數字，或 `vX.Y` 格式
- 任何欄位無法確認 → 標記 `⚠ NEEDS_REVIEW`，不猜測

**封面頁解析**：若檔名不足，Read 檔案前幾行，尋找含有 "SOP No"、"Document No"、
"Version"、"Revision" 等關鍵字的行。

---

## Skill 2: Batch File Operations

**目的**：使用 Python 批量另存新檔，輸出對照清單。

**Python 腳本模板**（寫入 `.claude/scripts/sop_rename.py` 後執行）：

```python
import shutil, os, json, sys

# 輸入：JSON list of {src, dst} pairs
pairs = json.load(open(sys.argv[1]))
results = []
for p in pairs:
    try:
        shutil.copy2(p['src'], p['dst'])
        results.append({'src': p['src'], 'dst': p['dst'], 'status': 'ok'})
    except Exception as e:
        results.append({'src': p['src'], 'dst': None, 'status': f'ERROR: {e}'})
        print(f"FAILED: {p['src']} — {e}", file=sys.stderr)
        sys.exit(1)  # 失敗立即停止，不繼續
print(json.dumps(results))
```

**規則**：
- 使用 `shutil.copy2`（保留 metadata），禁用 `shutil.move` 或 `os.rename`
- 任一複製失敗 → 立即停止整批操作（report_and_stop）
- 輸出 JSON 結果供後續步驟產生對照清單

---

## Skill 3: Naming Validation

**目的**：驗證輸出格式符合 `number@subject@version.ext`，偵測並標記異常。

**驗證檢核點**：
1. 恰好包含 2 個 `@` 字元
2. `@` 前後各欄位均非空字串
3. 副檔名與原始檔案一致（.pdf → .pdf，.docx → .docx）
4. 新檔名不含路徑分隔符號（`/`、`\`）或非法字元（`:`、`*`、`?`、`"`、`<`、`>`、`|`）

**自動旗標**：未通過任一檢核 → 該項目設為 `⚠ NEEDS_REVIEW`，不執行複製。

**輸出格式（Markdown 對照清單）**：

```markdown
| 原始檔名 | 新檔名 | 狀態 |
|----------|--------|------|
| QMS-001_Document Control_v2.1.pdf | QMS-001@Document Control@v2.1.pdf | ✓ |
| unknown_file.pdf | — | ⚠ NEEDS_REVIEW |
```

---

## NOT This Agent's Job

- **內容分析**：閱讀 SOP 內容判斷其合規性或完整性 → 交給 `qsd/compliance-checker`
- **清單比對**：比對 SOP 清單與主控台數據庫 → 交給 `qsd/list-comparator`
- **文件採集**：從多個來源蒐集 SOP 檔案 → 交給 `qsd/document-collector`
- **表格填寫**：填寫任何 QSD 評估或提交表格 → 交給 QSD 其他 worker
- **檔案轉換**：將 .docx 轉為 .pdf 或任何格式轉換 → 超出範圍
