# NASG — Neuro-Admissibility & Scaling Gate

Boundary-first governance tool for neural simulation, brain-inspired AI, and neurotechnology research.

## What it does

- Enforces admissibility before scaling
- Requires present-state proof and falsifiers
- Blocks prohibited semantic expansion
- Adds HACR-All observational signals
- Produces tamper-evident audit logs
- Exports signed decision receipts
- Blocks execution unless PASS

## Structure

nasg/
- validator.py
- hacr_all.py
- strict_gate.py
- claim_register.py
- audit_chain.py
- verify_audit.py
- pre_run_gate.py
- receipt_export.py
- verify_receipt.py

examples/
- pass_case.json
- test_case.json
- prohibited_case.json

## Usage

Run evaluation:

run_nasg.bat examples\pass_case.json

Verify audit chain:

python -m nasg.verify_audit

Verify receipt:

python -m nasg.verify_receipt receipts\<file>.json

Gate execution:

gate_and_run.bat examples\pass_case.json "echo SAFE RUN"

## Decision Outputs

- PASS → allowed to scale / execute
- HOLD → insufficient or partial validation
- FAIL → structural violation

## Core Rule

No present-state proof → no scaling.