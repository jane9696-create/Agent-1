#!/usr/bin/env python3
"""
QSD IBJB Step3 命名格式修正腳本 — 客戶回饋 (2026-07-27)

問題：先前 Step3 產出的法文版 SOP 命名把 `_FR` 加在檔名最尾端
      (number@subject@version_FR.pdf)，客戶回饋此格式不正確。

正確格式：`_FR` 應加在 subject 欄位之後、第二個 @ 之前
      (number@subject_FR@version.pdf)

方法（依 tools.md 規範，禁用 os.rename/shutil.move 直接改名）：
  1. 用 shutil.copy2 在同一資料夾內複製出修正後檔名的副本（保留 metadata）。
  2. 驗證副本存在且檔案大小與原檔一致後，才刪除舊（錯誤命名）副本。
  3. 全程只操作 Step3 輸出的「重命名副本」，不觸碰任何上游原始 SOP 來源檔案。

輸出：JSON 對照清單 (old_name -> new_name, status)，供人工/manifest 更新使用。
"""
import shutil
import os
import json
import sys

TARGET_DIR = "/tmp/claude-0/-home-user-Agent-1/b9895f9d-c4b9-5cc0-a006-560cdaea9f43/scratchpad/qsd_ibjb/output/step3_renamed_sops"

def parse_and_fix(filename):
    root, ext = os.path.splitext(filename)
    parts = root.split("@")
    if len(parts) != 3:
        return None, "⚠ NEEDS_REVIEW (not exactly 2 '@')"
    number, subject, version = parts
    if version.endswith("_FR"):
        new_version = version[:-3]
        new_subject = subject + "_FR"
        new_name = f"{number}@{new_subject}@{new_version}{ext}"
        return new_name, "fixed"
    else:
        return filename, "unchanged"

def main():
    entries = sorted(os.listdir(TARGET_DIR))
    files = [f for f in entries if os.path.isfile(os.path.join(TARGET_DIR, f))]

    results = []
    # Pass 1: compute mapping, detect collisions before touching anything
    mapping = []
    seen_new_names = set()
    for f in files:
        new_name, status = parse_and_fix(f)
        if new_name is None:
            results.append({"old": f, "new": None, "status": status})
            continue
        if new_name in seen_new_names or (new_name != f and new_name in files):
            results.append({"old": f, "new": new_name, "status": "⚠ COLLISION"})
            continue
        seen_new_names.add(new_name)
        mapping.append((f, new_name, status))

    # Pass 2: execute copy2 + verify + remove old, only for status == fixed
    for old_name, new_name, status in mapping:
        old_path = os.path.join(TARGET_DIR, old_name)
        if status == "unchanged":
            results.append({"old": old_name, "new": new_name, "status": "unchanged"})
            continue

        new_path = os.path.join(TARGET_DIR, new_name)
        try:
            old_size = os.path.getsize(old_path)
            shutil.copy2(old_path, new_path)
            new_size = os.path.getsize(new_path)
            if new_size != old_size:
                results.append({"old": old_name, "new": new_name, "status": f"⚠ SIZE_MISMATCH old={old_size} new={new_size}"})
                continue
            # verified copy ok -> remove the old, wrongly-named duplicate
            os.remove(old_path)
            results.append({"old": old_name, "new": new_name, "status": "fixed"})
        except Exception as e:
            results.append({"old": old_name, "new": new_name, "status": f"⚠ ERROR: {e}"})
            print(f"FAILED: {old_name} -> {new_name}: {e}", file=sys.stderr)

    print(json.dumps(results, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
