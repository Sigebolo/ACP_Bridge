@echo off
chcp 65001 >nul
title ACP Communication Monitor
echo ========================================
echo    ACP Communication Monitor
echo ========================================
echo.
echo This monitor will show real-time communication with Gemini CLI
echo All messages will be saved to acp_communication_log.txt
echo.
echo Press Ctrl+C to stop monitoring
echo ========================================
echo.

cd /d "d:\Gemini\agent-hand\bridge"

echo Starting ACP Communication Monitor...
python acp_communication_monitor.py

echo.
echo ========================================
echo Monitor stopped
echo Check communication log: acp_communication_log.txt
echo ========================================
pause
