#!/usr/bin/env python3
# parse_qsd_checklist.py
# 讀取 QSD standard checklist.xls，產生索取文件清單 Markdown
# 根據 MEMORY.md 已知格式：xlrd + cp950 編碼

import xlrd
import os
import sys
from datetime import datetime

CHECKLIST_PATH = r"C:\D\MRS client-2014\MRS\AI training\Claude-QSD\1. QSD standard checklist.xls"
OUTPUT_PATH = r"C:\D\MRS client-2014\DKSH_OCD\OCD_QSD\QSD4603_Lee Road\05 QSD4603 Lee Road-202603\QSD-Step1-Document-Request-List.md"
SHEET_NAME = "QSD standard"

# 文件類型分類關鍵字
DOC_TYPE_MAP = [
    ("ISO 13485 certificate", ["ISO 13485", "certificate", "憑證", "證書"]),
    ("品質手冊", ["quality manual", "品質手冊", "QM"]),
    ("SOP 清單", ["SOP list", "SOP number", "SOP subject"]),
    ("Site Information Letter", ["site information", "basic site"]),
    ("廠房平面圖", ["plan layout", "layout", "平面圖"]),
    ("生產區域圖", ["production area", "diagram", "生產區域"]),
    ("主要設備清單", ["major equipment", "equipment list", "設備清單"]),
    ("製造流程圖", ["manufacturing flowchart", "flowchart", "流程圖"]),
    ("醫療器材檔案", ["medical device files", "device files", "醫療器材"]),
    ("SOP", ["SOP", "procedure", "作業程序", "操作規程"]),
    ("表單/記錄", ["form", "record", "表單", "記錄", "填寫"]),
    ("圖面/技術文件", ["drawing", "圖面", "技術規格", "specification"]),
    ("測試報告", ["test report", "測試報告", "驗收報告"]),
]

def classify_doc_type(text):
    if not text:
        return "其他"
    text_lower = text.lower()
    for doc_type, keywords in DOC_TYPE_MAP:
        for kw in keywords:
            if kw.lower() in text_lower:
                return doc_type
    return "其他"


def parse_checklist():
    if not os.path.isfile(CHECKLIST_PATH):
        print(f"ERROR: 找不到 checklist 檔案: {CHECKLIST_PATH}", file=sys.stderr)
        sys.exit(1)

    wb = xlrd.open_workbook(CHECKLIST_PATH, encoding_override='cp950')

    # 找工作表
    sheet = None
    for sh in wb.sheets():
        if sh.name.strip() == SHEET_NAME:
            sheet = sh
            break
    if sheet is None:
        print(f"ERROR: 找不到工作表 '{SHEET_NAME}'。可用工作表: {[s.name for s in wb.sheets()]}", file=sys.stderr)
        sys.exit(1)

    print(f"工作表: {sheet.name}, 總列數: {sheet.nrows}, 欄數: {sheet.ncols}")

    rows = []
    for i in range(sheet.nrows):
        row = [str(sheet.cell_value(i, j)).strip() if j < sheet.ncols else "" for j in range(max(sheet.ncols, 3))]
        rows.append(row)

    # 解析條款
    records = []
    parsed_count = 0
    current_section = ""
    current_section_num = ""

    # 核心文件 (Row 1–9, 條款 1.0~8.0)
    core_items = []
    sop_items = []

    for i, row in enumerate(rows):
        col0 = row[0].strip()
        col1 = row[1].strip() if len(row) > 1 else ""
        col2 = row[2].strip() if len(row) > 2 else ""

        # 跳過標題列 (Row 0)
        if i == 0:
            continue

        # 跳過空白行
        if not col0 and not col1:
            continue

        # Section 標題行（含 "Section" 字樣且 col1 為空或也是標題）
        if col0.lower().startswith("section") and not col1.replace("section", "").replace(" ", "").replace("0123456789", "").strip():
            current_section = col0
            current_section_num = col0
            continue

        # Module 標題行
        if "module" in col0.lower() or ("module" in col1.lower() and not col0):
            continue

        # 核心文件 (有條款編號如 1.0, 2.1, 2.2 ... 8.0)
        if col0 and col1:
            # 檢查是否為數字格式條款編號
            try:
                float(col0)
                is_numbered = True
            except ValueError:
                is_numbered = False

            if is_numbered:
                doc_type = classify_doc_type(col1)
                qty = "1 份"
                note = col2 if col2 else ""
                if "list" in col1.lower() or "清單" in col1:
                    qty = "1 份（清單格式）"
                core_items.append({
                    "clause": col0,
                    "doc_name": col1,
                    "doc_type": doc_type,
                    "qty": qty,
                    "note": note,
                    "section": "核心文件",
                })
                parsed_count += 1
                continue

        # Section 分組（col0 = "Section N" 格式）
        if col0.lower().startswith("section"):
            current_section = col0
            current_section_num = col0
            continue

        # ISO 13485 章節條款：col0 為章節號或空白，col1 為條款名稱
        if col1:
            clause_num = col0 if col0 else current_section_num
            doc_type = classify_doc_type(col1)
            note = col2 if col2 else ""
            qty = "N 份"
            if "sop" in doc_type.lower():
                qty = "相關 SOP 各 1 份"
            sop_items.append({
                "clause": clause_num,
                "doc_name": col1,
                "doc_type": doc_type,
                "qty": qty,
                "note": note,
                "section": "ISO 13485 SOP 要求",
            })
            parsed_count += 1

    all_records = core_items + sop_items
    return all_records, parsed_count


def generate_markdown(records):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = []
    lines.append("# QSD 索取文件清單")
    lines.append("")
    lines.append(f"**案件**：05 QSD4603 Lee Road-202603")
    lines.append(f"**產生日期**：{now}")
    lines.append(f"**Checklist 版本**：新版（不含第 11 項 ADR & Recall SOPs）")
    lines.append("")

    # 核心文件區塊
    core = [r for r in records if r["section"] == "核心文件"]
    sop = [r for r in records if r["section"] == "ISO 13485 SOP 要求"]

    lines.append("## 第一部分：核心文件（Core Documents）")
    lines.append("")
    lines.append("| 條款編號 | 文件名稱 | 文件類型 | 數量需求 | 備註 |")
    lines.append("|---------|---------|---------|---------|------|")
    for r in core:
        note = r["note"].replace("|", "｜")
        doc_name = r["doc_name"].replace("|", "｜")
        lines.append(f"| {r['clause']} | {doc_name} | {r['doc_type']} | {r['qty']} | {note} |")

    lines.append("")
    lines.append("## 第二部分：ISO 13485:2016 SOP 文件要求")
    lines.append("")
    lines.append("| 條款編號 | 文件名稱 | 文件類型 | 數量需求 | 備註 |")
    lines.append("|---------|---------|---------|---------|------|")
    for r in sop:
        note = r["note"].replace("|", "｜")
        doc_name = r["doc_name"].replace("|", "｜")
        lines.append(f"| {r['clause']} | {doc_name} | {r['doc_type']} | {r['qty']} | {note} |")

    lines.append("")
    lines.append("---")
    lines.append(f"**合計索取文件項目**：{len(records)} 項（核心文件 {len(core)} 項，SOP 文件要求 {len(sop)} 項）")
    lines.append("")
    lines.append("> 注意：此清單依據新版 QSD standard checklist 產生，不含第 11 項 ADR & Recall SOPs。")
    lines.append("> 產生者：QSD Document Collector Agent（Step 1）")

    return "\n".join(lines)


def main():
    print("=== QSD Document Collector — Step 1 ===")
    print(f"讀取 Checklist: {CHECKLIST_PATH}")

    records, parsed_count = parse_checklist()
    print(f"成功解析條款數: {parsed_count}")
    print(f"產生索取文件項目數: {len(records)}")

    md_content = generate_markdown(records)

    # 確保輸出目錄存在
    out_dir = os.path.dirname(OUTPUT_PATH)
    if not os.path.isdir(out_dir):
        print(f"ERROR: 輸出目錄不存在: {out_dir}", file=sys.stderr)
        sys.exit(1)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"輸出檔案: {OUTPUT_PATH}")
    print("=== 完成 ===")


if __name__ == "__main__":
    main()
