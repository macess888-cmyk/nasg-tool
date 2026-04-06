import json
import sys
from nasg.hacr_all import observe
from nasg.strict_gate import check_strict_requirements
from nasg.audit_chain import append_log
from nasg.receipt_export import export_receipt

REQUIRED_FIELDS = [
    "milestone",
    "empirical",
    "interpretive",
    "human_risk",
    "rollback"
]

VALID_VALUES = {
    "empirical": ["PASS", "PARTIAL", "FAIL", "INSUFFICIENT"],
    "interpretive": ["RESTRICTED", "EXPANDED", "INSUFFICIENT"],
    "human_risk": ["LOW", "ELEVATED", "HIGH", "INSUFFICIENT"],
    "rollback": ["DEFINED", "PARTIAL", "NONE", "INSUFFICIENT"]
}

def evaluate(data):
    for field in REQUIRED_FIELDS:
        if field not in data:
            return "FAIL", f"missing field: {field}"

    for key, allowed in VALID_VALUES.items():
        if data[key] not in allowed:
            return "FAIL", f"invalid value for {key}: {data[key]}"

    strict_status, strict_reason = check_strict_requirements(data)
    if strict_status != "PASS":
        return "FAIL", strict_reason

    if data["rollback"] == "NONE":
        return "FAIL", "no rollback defined"

    if (
        data["empirical"] == "INSUFFICIENT" or
        data["interpretive"] == "INSUFFICIENT" or
        data["human_risk"] == "INSUFFICIENT" or
        data["rollback"] == "INSUFFICIENT"
    ):
        return "HOLD", "insufficient evidence at boundary"

    if data["empirical"] != "PASS":
        return "HOLD", "empirical not fully validated"

    if data["human_risk"] == "HIGH":
        return "HOLD", "human risk too high"

    return "PASS", "all conditions satisfied"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m nasg.validator input.json")
        sys.exit(1)

    with open(sys.argv[1], "r") as f:
        data = json.load(f)

    decision, reason = evaluate(data)
    observer_result = observe(data, decision, reason)

    print("Decision:", decision)
    print("Reason:", reason)
    print("Observer:", observer_result["observer"])
    print("Posture:", observer_result["posture"])
    print("Notes:")
    for note in observer_result["notes"]:
        print("-", note)

    entry = f"{data['milestone']} | {decision} | {reason} | {observer_result['posture']}"
    append_log(entry)

    receipt_path, receipt_hash = export_receipt(data, decision, reason, observer_result)
    print("Receipt:", receipt_path)
    print("Receipt SHA256:", receipt_hash)