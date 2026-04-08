@echo off
chcp 65001 >nul
REM ============================================================
REM Antigravity RPA Dialog Trigger for OpenClaw-Atom
REM Usage: trigger-antigravity.bat ["Your message here"]
REM ============================================================

set "PROMPT=%~1"
if "%PROMPT%"=="" set "PROMPT=Bridge上有新的任务，请检查 workspace\antigravity_tasks 目录并开始处理。"

echo [Antigravity Trigger] Message: %PROMPT%

python "%~dp0trigger_antigravity.py" "%PROMPT%"
