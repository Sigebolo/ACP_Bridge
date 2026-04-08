@echo off
title ACP通讯监控器
echo ========================================
echo    ACP通讯监控器启动
echo ========================================
echo.
echo 这个监控器将实时显示与Gemini CLI的完整通讯过程
echo 所有消息都会记录到 acp_communication_log.txt
echo.
echo 按 Ctrl+C 可以停止监控
echo ========================================
echo.

cd /d "d:\Gemini\agent-hand\bridge"

echo 🚀 启动通讯监控器...
python acp_communication_monitor.py

echo.
echo ========================================
echo 监控器已停止
echo 查看通讯记录: acp_communication_log.txt
echo ========================================
pause
