from __future__ import annotations

from dataclasses import dataclass, asdict, field
from typing import Any, Dict, List, Tuple
import hashlib
import json
from datetime import datetime, timezone

PASS = "PASS"
FAIL = "FAIL"
HOLD = "HOLD"


# ----------------------------
# Helpers
# ----------------------------

def canonical_json(data: Dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def now_utc_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _normalize_claims(claims: Any) -> Dict[str, Any]:
    if isinstance(claims, dict):
        return claims
    if isinstance(claims, list):
        out: Dict[str, Any] = {}
        for item in claims:
            if isinstance(item, dict):
                out.update(item)
            elif isinstance(item, str):
                out[item] = True
        return out
    return {}


# ----------------------------
# Data classes
# ----------------------------

@dataclass(frozen=True)
class VerificationIssue:
    code: str
    message: str
    layer: str


@dataclass(frozen=True)
class CheckResult:
    name: str
    status: str
    details: Dict[str, Any] = field(default_factory=dict)
    issues: Tuple[VerificationIssue, ...] = ()


@dataclass(frozen=True)
class VerificationReceipt:
    verifier_name: str
    verifier_version: str
    timestamp_utc: str
    spec_hash_sha256: str
    overall_status: str
    checks: Tuple[CheckResult, ...]
    summary: Dict[str, Any]

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2, sort_keys=True)


# ----------------------------
# Checks
# ----------------------------

def check_spec_structure(spec: Dict[str, Any]) -> CheckResult:
    required = ["pipeline_name", "operators", "external_references", "binding_point", "claims", "data_readiness"]
    missing = [k for k in required if k not in spec]

    if missing:
        return CheckResult("spec_structure", FAIL, {"missing": missing})

    return CheckResult("spec_structure", PASS, {"ok": True})


def check_non_authoritativeness(spec: Dict[str, Any]) -> CheckResult:
    claims = _normalize_claims(spec.get("claims", {}))
    operators = spec.get("operators", [])

    issues = []

    if claims.get("computable_lift_to_E_adm"):
        issues.append(VerificationIssue("NA_COMPUTABLE_LIFT", "computable lift detected", "non_authoritativeness"))

    if claims.get("internal_state_certifies_readiness"):
        issues.append(VerificationIssue("NA_INTERNAL_SELF_CERT", "internal certification detected", "non_authoritativeness"))

    for i, op in enumerate(operators):
        if op.get("authoritative"):
            issues.append(VerificationIssue("NA_OPERATOR_AUTHORITATIVE", f"operator {i} authoritative", "non_authoritativeness"))
        if op.get("derives_external_reference"):
            issues.append(VerificationIssue("NA_DERIVES_EXTERNAL_REFERENCE", f"operator {i} derives external reference", "non_authoritativeness"))

    return CheckResult("non_authoritativeness", FAIL if issues else PASS, {}, tuple(issues))


def check_fisher(spec: Dict[str, Any]) -> CheckResult:
    issues = []
    for i, op in enumerate(spec.get("operators", [])):
        if not op.get("symbolic_fisher_preservation"):
            issues.append(VerificationIssue("FISHER_NOT_PROVEN", f"operator {i} missing proof", "fisher"))

    return CheckResult("fisher", FAIL if issues else PASS, {}, tuple(issues))


def check_scale(spec: Dict[str, Any]) -> CheckResult:
    import math

    claims = _normalize_claims(spec.get("claims", {}))

    binding = spec.get("binding_point", {})
    ext = spec.get("external_references", {})

    delta_a = binding.get("delta_l_A")
    delta_h = binding.get("delta_l_H")
    lam = ext.get("Lambda")

    issues = []

    if not claims.get("external_comparator_used"):
        issues.append(VerificationIssue("SC_NO_EXTERNAL", "no external comparator", "scale"))

    if None in (delta_a, delta_h, lam):
        issues.append(VerificationIssue("SC_MISSING", "missing values", "scale"))
        return CheckResult("scale", FAIL, {}, tuple(issues))

    if delta_a * delta_h < (lam**2) / (4 * math.pi):
        issues.append(VerificationIssue("SC_FAIL", "inequality fails", "scale"))

    return CheckResult("scale", FAIL if issues else PASS, {}, tuple(issues))


def check_readiness(spec: Dict[str, Any]) -> CheckResult:
    issues = []

    for k, v in spec.get("data_readiness", {}).items():
        if not v.get("externally_referenced"):
            issues.append(VerificationIssue("DR_EXTERNAL", f"{k} not external", "readiness"))
        if not v.get("satisfied"):
            issues.append(VerificationIssue("DR_FAIL", f"{k} not satisfied", "readiness"))

    return CheckResult("readiness", FAIL if issues else PASS, {}, tuple(issues))


# ----------------------------
# Main
# ----------------------------

def verify_spec(spec: Dict[str, Any]) -> VerificationReceipt:
    spec_hash = sha256_text(canonical_json(spec))

    checks = (
        check_spec_structure(spec),
        check_non_authoritativeness(spec),
        check_fisher(spec),
        check_scale(spec),
        check_readiness(spec),
    )

    statuses = [c.status for c in checks]
    overall = FAIL if FAIL in statuses else PASS

    return VerificationReceipt(
        verifier_name="NASG Appendix B.8 Verifier",
        verifier_version="0.2.0",
        timestamp_utc=now_utc_iso(),
        spec_hash_sha256=spec_hash,
        overall_status=overall,
        checks=checks,
        summary={
            "check_count": len(checks),
            "issue_count": sum(len(c.issues) for c in checks),
            "fail_closed": True,
        },
    )


# ----------------------------
# CLI run
# ----------------------------

if __name__ == "__main__":
    import json

    spec = json.load(open("pass_case.json"))
    print(verify_spec(spec).to_json())