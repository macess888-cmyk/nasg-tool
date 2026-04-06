import hashlib
import os

LOG_FILE = "audit_log.txt"

def compute_hash(entry, prev_hash):
    content = f"{prev_hash}|{entry}"
    return hashlib.sha256(content.encode()).hexdigest()

def get_last_hash():
    if not os.path.exists(LOG_FILE):
        return "GENESIS"

    with open(LOG_FILE, "r") as f:
        lines = f.readlines()

    if not lines:
        return "GENESIS"

    last_line = lines[-1].strip()
    if "|" not in last_line:
        return "GENESIS"

    return last_line.split("|")[-1]

def append_log(entry):
    prev_hash = get_last_hash()
    new_hash = compute_hash(entry, prev_hash)

    with open(LOG_FILE, "a") as f:
        f.write(f"{entry}|{new_hash}\n")