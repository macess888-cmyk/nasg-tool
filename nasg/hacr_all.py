def observe(data, decision, reason):
    notes = []

    milestone = data.get("milestone", "")
    empirical = data.get("empirical", "")
    interpretive = data.get("interpretive", "")
    human_risk = data.get("human_risk", "")
    rollback = data.get("rollback", "")

    notes.append(f"milestone={milestone}")
    notes.append(f"decision={decision}")
    notes.append(f"reason={reason}")

    if empirical != "PASS":
        notes.append("signal=present_state_proof_incomplete")

    if interpretive == "EXPANDED":
        notes.append("signal=interpretive_scope_exceeds_safe_boundary")

    if human_risk in ["ELEVATED", "HIGH"]:
        notes.append("signal=human_proximity_risk_active")

    if rollback in ["PARTIAL", "NONE"]:
        notes.append("signal=rollback_boundary_not_fully_closed")

    if decision == "PASS":
        posture = "OBSERVE"
    elif decision == "HOLD":
        posture = "HOLD"
    else:
        posture = "FAIL_CLOSED"

    return {
        "observer": "HACR-ALL",
        "posture": posture,
        "notes": notes
    }