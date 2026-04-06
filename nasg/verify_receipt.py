import hashlib
import json
import sys

def sha256_text(text):
    return hashlib.sha256(text.encode()).hexdigest()

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m nasg.verify_receipt receipt.json")
        return 1

    receipt_path = sys.argv[1]

    with open(receipt_path, "r") as f:
        outer = json.load(f)

    if "receipt_sha256" not in outer or "receipt" not in outer:
        print("FAIL: invalid receipt structure")
        return 1

    stored_hash = outer["receipt_sha256"]
    receipt = outer["receipt"]
    receipt_text = json.dumps(receipt, indent=2)
    computed_hash = sha256_text(receipt_text)

    if stored_hash != computed_hash:
        print("FAIL: receipt hash mismatch")
        print("Expected:", computed_hash)
        print("Found:   ", stored_hash)
        return 1

    print("PASS: receipt verified")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())