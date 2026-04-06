# NASG — Neuro-Admissibility & Scaling Gate

Deterministic, fail-closed verification for admissibility and invariant preservation.

---

## What this is

NASG provides:

- strict admissibility checks (no internal authority)
- invariant enforcement (Fisher + scale conjugation)
- deterministic offline verification (no runtime execution)
- explicit PASS / FAIL outcomes
- receipt-based audit trail

This is an execution-layer verifier, not a modeling or prediction system.

---

## Core properties

- fail-closed (no silent success)
- deterministic (same input → same output)
- offline (no dependency on runtime pipelines)
- externally referenced invariants (no self-certification)

---

## Appendix B.8 verifier

This repository includes a minimal deterministic offline verifier aligned to Appendix B.8.

### Run PASS reference

```bat
python -c "import json; from nasg_appendix_b8_verifier import verify_spec; print(verify_spec(json.load(open('pass_case.json'))).to_json())" > receipts\reference_receipt.json