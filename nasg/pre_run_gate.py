import json
import sys
from nasg.validator import evaluate

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m nasg.pre_run_gate input.json")
        return 1

    with open(sys.argv[1], "r") as f:
        data = json.load(f)

    decision, reason = evaluate(data)

    print("Decision:", decision)
    print("Reason:", reason)

    if decision != "PASS":
        print("BLOCK: execution not allowed")
        return 1

    print("ALLOW: execution allowed")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())