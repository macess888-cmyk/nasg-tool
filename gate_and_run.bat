@echo off
python -m nasg.pre_run_gate %1
if %errorlevel% neq 0 (
    echo Execution blocked by NASG
    exit /b 1
)

echo Running: %~2
call %~2