import hashlib
import json
import os

RECEIPTS_DIR = "receipts"

def sha256_text(text):
    return hashlib.sha256(text.encode()).hexdigest()

def export_receipt(data, decision, reason, observer_result):
    os.makedirs(RECEIPTS_DIR, exist_ok=True)

    milestone = data.get("milestone", "unknown_milestone")
    safe_name = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in milestone)
    receipt_path = os.path.join(RECEIPTS_DIR, f"{safe_name}.json")

    receipt = {
        "milestone": milestone,
        "decision": decision,
        "reason": reason,
        "observer": observer_result["observer"],
        "posture": observer_result["posture"],
        "notes": observer_result["notes"],
        "input": data
    }

    receipt_text = json.dumps(receipt, indent=2)
    receipt_hash = sha256_text(receipt_text)

    final_output = {
        "receipt_sha256": receipt_hash,
        "receipt": receipt
    }

    with open(receipt_path, "w") as f:
        json.dump(final_output, f, indent=2)

    return receipt_path, receipt_hash