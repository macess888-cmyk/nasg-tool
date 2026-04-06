import hashlib
import os
import sys

LOG_FILE = "audit_log.txt"

def compute_hash(entry, prev_hash):
    content = f"{prev_hash}|{entry}"
    return hashlib.sha256(content.encode()).hexdigest()

def verify_log():
    if not os.path.exists(LOG_FILE):
        print("FAIL: audit_log.txt not found")
        return 1

    with open(LOG_FILE, "r") as f:
        lines = [line.rstrip("\n") for line in f if line.strip()]

    prev_hash = "GENESIS"

    for i, line in enumerate(lines, start=1):
        parts = line.split("|")
        if len(parts) < 2:
            print(f"FAIL: line {i} malformed")
            return 1

        stored_hash = parts[-1].strip()
        entry = "|".join(parts[:-1]).strip()
        expected_hash = compute_hash(entry, prev_hash)

        if stored_hash != expected_hash:
            print(f"FAIL: line {i} hash mismatch")
            print(f"Expected: {expected_hash}")
            print(f"Found:    {stored_hash}")
            return 1

        prev_hash = stored_hash

    print("PASS: audit chain verified")
    return 0

if __name__ == "__main__":
    sys.exit(verify_log())