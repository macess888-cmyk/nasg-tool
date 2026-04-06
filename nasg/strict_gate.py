ALLOWED_CLAIM_CLASSES = ["E", "M", "I", "D", "X"]
ALLOWED_SUPPORT_LAYERS = ["empirical", "model", "interpretive", "deployment"]

def check_strict_requirements(data):
    if "present_state_proof" not in data:
        return "FAIL", "missing present_state_proof"

    if not isinstance(data["present_state_proof"], str) or not data["present_state_proof"].strip():
        return "FAIL", "present_state_proof must be a non-empty string"

    if "falsifier" not in data:
        return "FAIL", "missing falsifier"

    if not isinstance(data["falsifier"], str) or not data["falsifier"].strip():
        return "FAIL", "falsifier must be a non-empty string"

    if "claims" not in data:
        return "FAIL", "missing claims"

    if not isinstance(data["claims"], list) or len(data["claims"]) == 0:
        return "FAIL", "claims must be a non-empty list"

    for i, claim in enumerate(data["claims"]):
        if not isinstance(claim, dict):
            return "FAIL", f"claim {i} must be an object"

        if "text" not in claim:
            return "FAIL", f"claim {i} missing text"

        if not isinstance(claim["text"], str) or not claim["text"].strip():
            return "FAIL", f"claim {i} text must be a non-empty string"

        if "class" not in claim:
            return "FAIL", f"claim {i} missing class"

        if claim["class"] not in ALLOWED_CLAIM_CLASSES:
            return "FAIL", f"claim {i} has invalid class: {claim['class']}"

        if claim["class"] == "X":
            return "FAIL", f"claim {i} is prohibited extension"

        if "support_layer" not in claim:
            return "FAIL", f"claim {i} missing support_layer"

        if claim["support_layer"] not in ALLOWED_SUPPORT_LAYERS:
            return "FAIL", f"claim {i} has invalid support_layer: {claim['support_layer']}"

    return "PASS", "strict requirements satisfied"