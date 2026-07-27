import os
import re
import sys
import json
import shutil

FOLDER = "/tmp/claude-0/-home-user-Agent-1/b9895f9d-c4b9-5cc0-a006-560cdaea9f43/scratchpad/qsd_ibjb/output/step3_renamed_sops"

MODE = sys.argv[1] if len(sys.argv) > 1 else "dryrun"  # dryrun | apply

def parse(filename):
    name, ext = os.path.splitext(filename)
    parts = name.split("@")
    if len(parts) != 3:
        return None, f"unexpected @ count ({len(parts)})"
    number, subject, version = parts
    # extract arabic digits from version field (e.g. "Rev. 2" -> "2")
    m = re.search(r"(\d+)", version)
    if not m:
        return None, f"no digit found in version field '{version}'"
    digits = m.group(1)
    new_name = f"{number}@{subject}@{digits}{ext}"
    return new_name, None

def main():
    files = sorted(os.listdir(FOLDER))
    mapping = []
    errors = []
    for f in files:
        full = os.path.join(FOLDER, f)
        if not os.path.isfile(full):
            continue
        new_name, err = parse(f)
        if err:
            errors.append({"old": f, "error": err})
            continue
        mapping.append({"old": f, "new": new_name})

    # collision check among new names
    new_names = [m["new"] for m in mapping]
    dupes = set([n for n in new_names if new_names.count(n) > 1])

    print(f"Total files: {len(files)}")
    print(f"Parsed OK: {len(mapping)}")
    print(f"Parse errors: {len(errors)}")
    if errors:
        for e in errors:
            print(f"  ERROR: {e['old']} -> {e['error']}")
    if dupes:
        print(f"COLLISIONS DETECTED: {dupes}")
    else:
        print("No collisions among new filenames.")

    print("\n--- Mapping (old -> new) ---")
    for m in mapping:
        print(f"{m['old']}  ->  {m['new']}")

    if MODE == "apply":
        if errors or dupes:
            print("\nABORT: errors or collisions present, will not apply.", file=sys.stderr)
            sys.exit(1)
        results = []
        for m in mapping:
            src = os.path.join(FOLDER, m["old"])
            dst = os.path.join(FOLDER, m["new"])
            if src == dst:
                results.append({"old": m["old"], "new": m["new"], "status": "skip-same"})
                continue
            shutil.copy2(src, dst)
            src_size = os.path.getsize(src)
            dst_size = os.path.getsize(dst)
            if src_size != dst_size:
                print(f"SIZE MISMATCH: {m['old']} ({src_size}) vs {m['new']} ({dst_size})", file=sys.stderr)
                sys.exit(1)
            results.append({"old": m["old"], "new": m["new"], "status": "copied", "size": dst_size})
        # after all copies verified, delete old files
        for r in results:
            if r["status"] == "copied":
                old_path = os.path.join(FOLDER, r["old"])
                os.remove(old_path)
                r["old_deleted"] = True
        print("\n--- APPLY RESULTS ---")
        print(json.dumps(results, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
