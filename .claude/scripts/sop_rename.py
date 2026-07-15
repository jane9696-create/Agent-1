#!/usr/bin/env python
# sop_rename.py — QSD Step3: Read PDF cover pages, extract subject & version, copy to renamed/
# Usage: python sop_rename.py

import os
import re
import shutil
import json

SRC_DIR = r"C:\D\MRS client-2014\DKSH_OCD\OCD_QSD\QSD4603_Lee Road\05 QSD4603 Lee Road-202603\Taiwan - QSD Lee Road"
DST_DIR = os.path.join(SRC_DIR, "renamed")
MANIFEST_PATH = r"C:\D\MRS client-2014\DKSH_OCD\OCD_QSD\QSD4603_Lee Road\05 QSD4603 Lee Road-202603\QSD-Step3-SOP-Rename-Manifest.md"

FILES = [
    "POL20026.pdf", "POL20173.pdf", "POL50079_docx.pdf", "POL50187.pdf",
    "PRO20125.pdf", "PRO20157.pdf", "PRO20215.pdf", "PRO20230.pdf", "PRO20727.pdf",
    "PRO50009_Rochester_Calibration_Process_docx.pdf", "PRO50025.pdf", "PRO50028.pdf",
    "PRO50093.pdf", "PRO50148.pdf", "PRO50314.pdf", "PRO50322.pdf", "PRO50331.pdf",
    "PRO50336_docx.pdf", "SOP20662.pdf", "SOP22549.pdf", "SOP22602.pdf", "SOP23908.pdf",
    "SOP24431_docx.pdf", "SOP25162_doc.pdf", "SOP26178.pdf", "SOP50158.pdf",
    "SOP51011.pdf", "SOP51070.pdf", "SOP51229.pdf", "SOP52727.pdf", "SOP53176.pdf",
    "SOP53365.pdf", "SPC20558_docx.pdf", "WKI52689.pdf", "WKI53682.pdf", "WKI54245.pdf"
]

def extract_sop_number(filename):
    """Extract SOP number from filename (e.g. SOP20662_docx.pdf -> SOP20662)"""
    base = os.path.splitext(filename)[0]
    # Remove suffixes like _docx, _doc
    base = re.sub(r'_(docx|doc)$', '', base, flags=re.IGNORECASE)
    # For PRO50009 which has extra text: PRO50009_Rochester_Calibration_Process_docx -> PRO50009
    m = re.match(r'^([A-Z]{2,5}\d{4,6})', base)
    if m:
        return m.group(1)
    return base

def clean_text(text):
    """Clean extracted PDF text"""
    # Remove null bytes and control chars
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    return text

def sanitize_filename_part(s):
    """Remove characters illegal in Windows filenames, collapse whitespace"""
    s = re.sub(r'[\\/:*?"<>|]', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def extract_from_pdf(filepath):
    """
    Try to extract subject and version from first 3 pages of PDF.
    Returns (subject, version) or (None, None)
    """
    try:
        import pdfplumber
        with pdfplumber.open(filepath) as pdf:
            pages_to_check = min(3, len(pdf.pages))
            all_text = ""
            for i in range(pages_to_check):
                page_text = pdf.pages[i].extract_text() or ""
                all_text += page_text + "\n"
            return parse_text_for_subject_version(all_text, filepath)
    except Exception as e1:
        pass

    try:
        import PyPDF2
        with open(filepath, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            pages_to_check = min(3, len(reader.pages))
            all_text = ""
            for i in range(pages_to_check):
                page_text = reader.pages[i].extract_text() or ""
                all_text += page_text + "\n"
            return parse_text_for_subject_version(all_text, filepath)
    except Exception as e2:
        pass

    return None, None

def parse_text_for_subject_version(raw_text, filepath=""):
    """Parse extracted text to find subject (title) and version."""
    text = clean_text(raw_text)
    lines = [l.strip() for l in text.splitlines() if l.strip()]

    subject = None
    version = None

    # --- Version patterns (search whole text) ---
    version_patterns = [
        r'\bRev(?:ision)?\.?\s*([A-Z0-9]+(?:\.[0-9]+)?)\b',
        r'\bRevision\s*:\s*([A-Z0-9]+(?:\.[0-9]+)?)',
        r'\bVersion\s*:?\s*([\d]+(?:\.[0-9]+)*)',
        r'\bv\s*([\d]+(?:\.[0-9]+)+)\b',
        r'\bV\s*([\d]+(?:\.[0-9]+)+)\b',
        r'\bRev\s+([A-Z])\b',
        r'Revision\s+([A-Z0-9]+)',
    ]
    for pat in version_patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            version = "Rev" + m.group(1) if re.match(r'^Rev', pat, re.IGNORECASE) and not m.group(1).startswith('Rev') else m.group(1)
            # Normalise
            raw_ver = m.group(0).strip()
            # Extract just the version token
            ver_m = re.search(r'(?:Rev(?:ision)?\.?\s*|Version\s*:?\s*|[vV]\s*)([\w.]+)', raw_ver, re.IGNORECASE)
            if ver_m:
                version = ver_m.group(0).strip()
                version = re.sub(r'\s+', '', version)  # no spaces
            break

    # --- Subject (title) patterns ---
    # Look for "Title:" or "Document Title:" label
    title_label_pat = re.compile(r'(?:Document\s+)?Title\s*:\s*(.+)', re.IGNORECASE)
    for line in lines:
        m = title_label_pat.search(line)
        if m:
            candidate = m.group(1).strip()
            if len(candidate) > 4:
                subject = sanitize_filename_part(candidate)
                break

    # If no labeled title, try "Name:" or "Procedure Name:"
    if not subject:
        name_pat = re.compile(r'(?:Procedure\s+)?Name\s*:\s*(.+)', re.IGNORECASE)
        for line in lines:
            m = name_pat.search(line)
            if m:
                candidate = m.group(1).strip()
                if len(candidate) > 4:
                    subject = sanitize_filename_part(candidate)
                    break

    # Heuristic: first long non-code line that looks like a title
    if not subject:
        sop_number_re = re.compile(r'^[A-Z]{2,5}\d{4,6}$')
        skip_words = re.compile(r'^(page|date|rev|version|effective|approved|author|department|classification|confidential|property|rights|reserved|printed|uncontrolled|copy|of|the|for|and|or|in|is|at|by|on|to|a|an)$', re.IGNORECASE)
        for line in lines[:40]:
            tokens = line.split()
            if len(tokens) < 2 or len(tokens) > 15:
                continue
            if sop_number_re.match(tokens[0]):
                continue
            # Skip lines that are mostly numbers/dates
            if re.match(r'^[\d\s\/\-\.]+$', line):
                continue
            # Skip lines with only stop words
            meaningful = [t for t in tokens if not skip_words.match(t)]
            if len(meaningful) < 2:
                continue
            # Skip lines that look like headers (all caps short tokens)
            if all(t.isupper() and len(t) <= 4 for t in tokens):
                continue
            # Looks like a reasonable title
            subject = sanitize_filename_part(line)
            if len(subject) > 5:
                break

    if subject:
        # Limit length
        subject = subject[:80]

    return subject, version


def process_all():
    os.makedirs(DST_DIR, exist_ok=True)
    results = []

    for fname in FILES:
        if fname.lower().startswith('zz'):
            continue
        src_path = os.path.join(SRC_DIR, fname)
        sop_number = extract_sop_number(fname)

        if not os.path.exists(src_path):
            results.append({
                "original": fname,
                "new_name": None,
                "status": "NEEDS_REVIEW",
                "reason": "FILE_NOT_FOUND"
            })
            continue

        subject, version = extract_from_pdf(src_path)

        if not subject or not version:
            reason_parts = []
            if not subject:
                reason_parts.append("subject未解析")
            if not version:
                reason_parts.append("version未解析")
            results.append({
                "original": fname,
                "new_name": None,
                "sop_number": sop_number,
                "raw_subject": subject,
                "raw_version": version,
                "status": "NEEDS_REVIEW",
                "reason": ", ".join(reason_parts)
            })
            continue

        # Validate
        new_base = f"{sop_number}@{subject}@{version}.pdf"
        # Check illegal chars
        illegal = re.search(r'[\\/:*?"<>|]', new_base.replace('@',''))
        if illegal:
            results.append({
                "original": fname,
                "new_name": new_base,
                "status": "NEEDS_REVIEW",
                "reason": f"非法字元: {illegal.group()}"
            })
            continue

        dst_path = os.path.join(DST_DIR, new_base)
        try:
            shutil.copy2(src_path, dst_path)
            results.append({
                "original": fname,
                "new_name": new_base,
                "status": "OK"
            })
        except Exception as e:
            results.append({
                "original": fname,
                "new_name": new_base,
                "status": "ERROR",
                "reason": str(e)
            })

    return results


def write_manifest(results):
    ok = [r for r in results if r['status'] == 'OK']
    needs_review = [r for r in results if r['status'] == 'NEEDS_REVIEW']
    errors = [r for r in results if r['status'] == 'ERROR']

    lines = [
        "# QSD Step3 SOP 重命名對照清單",
        "",
        f"**案件**：05 QSD4603 Lee Road-202603",
        f"**執行日期**：2026-06-24",
        f"**來源資料夾**：`C:\\D\\MRS client-2014\\DKSH_OCD\\OCD_QSD\\QSD4603_Lee Road\\05 QSD4603 Lee Road-202603\\Taiwan - QSD Lee Road`",
        f"**輸出資料夾**：`{DST_DIR}`",
        "",
        f"**摘要**：成功 {len(ok)} 份 | ⚠ NEEDS_REVIEW {len(needs_review)} 份 | ❌ 錯誤 {len(errors)} 份",
        "",
        "---",
        "",
        "## 對照清單",
        "",
        "| # | 原始檔名 | 新檔名 | 狀態 | 備註 |",
        "|---|----------|--------|------|------|",
    ]

    for i, r in enumerate(results, 1):
        orig = r['original']
        new = r.get('new_name') or '—'
        status = r['status']
        reason = r.get('reason', '')
        if status == 'OK':
            lines.append(f"| {i} | `{orig}` | `{new}` | ✓ | |")
        else:
            lines.append(f"| {i} | `{orig}` | {new} | ⚠ {status} | {reason} |")

    if needs_review:
        lines += [
            "",
            "---",
            "",
            "## NEEDS_REVIEW 詳情",
            "",
        ]
        for r in needs_review:
            lines.append(f"### `{r['original']}`")
            lines.append(f"- SOP Number: `{r.get('sop_number','—')}`")
            lines.append(f"- 解析 Subject: `{r.get('raw_subject','—')}`")
            lines.append(f"- 解析 Version: `{r.get('raw_version','—')}`")
            lines.append(f"- 原因: {r.get('reason','—')}")
            lines.append("")

    with open(MANIFEST_PATH, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    print(f"Manifest written: {MANIFEST_PATH}")


if __name__ == "__main__":
    print("Starting SOP rename process...")
    results = process_all()
    write_manifest(results)

    ok_count = sum(1 for r in results if r['status'] == 'OK')
    nr_count = sum(1 for r in results if r['status'] == 'NEEDS_REVIEW')
    err_count = sum(1 for r in results if r['status'] == 'ERROR')

    print(f"\n=== RESULTS ===")
    print(f"Total: {len(results)}")
    print(f"OK: {ok_count}")
    print(f"NEEDS_REVIEW: {nr_count}")
    print(f"ERROR: {err_count}")

    # Print NEEDS_REVIEW details
    for r in results:
        if r['status'] != 'OK':
            print(f"  [{r['status']}] {r['original']} -> reason: {r.get('reason','')}")
            if r.get('raw_subject') or r.get('raw_version'):
                print(f"    subject='{r.get('raw_subject')}' version='{r.get('raw_version')}'")

    # Print first 5 OK
    print("\n--- 前5項成功示例 ---")
    for r in results[:10]:
        if r['status'] == 'OK':
            print(f"  {r['original']} -> {r['new_name']}")

    print(json.dumps(results, ensure_ascii=False, indent=2))
