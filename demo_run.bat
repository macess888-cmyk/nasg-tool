@echo off
echo =========================
echo NASG DEMO RUN
echo =========================

echo.
echo [1] PASS case
run_nasg.bat examples\pass_case.json

echo.
echo [2] HOLD case
run_nasg.bat examples\test_case.json

echo.
echo [3] FAIL case
run_nasg.bat examples\prohibited_case.json

echo.
echo [4] Verify audit chain
python -m nasg.verify_audit

echo.
echo Demo complete