ALLOWED_CLAIM_CLASSES = ["E", "M", "I", "D", "X"]

def check_claims(data):
    claims = data.get("claims", [])

    if not isinstance(claims, list):
        return "FAIL", "claims must be a list"

    for i, claim in enumerate(claims):
        if not isinstance(claim, dict):
            return "FAIL", f"claim {i} must be an object"

        if "text" not in claim:
            return "FAIL", f"claim {i} missing text"

        if "class" not in claim:
            return "FAIL", f"claim {i} missing class"

        if claim["class"] not in ALLOWED_CLAIM_CLASSES:
            return "FAIL", f"claim {i} has invalid class: {claim['class']}"

        if claim["class"] == "X":
            return "FAIL", f"claim {i} is prohibited extension"

    return "PASS", "claims valid"