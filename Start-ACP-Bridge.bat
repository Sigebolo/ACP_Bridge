@echo off
echo Starting ACP Bridge Manager...
echo ================================

cd /d "d:\Gemini\agent-hand\bridge"

echo.
echo ACP Bridge Manager - Agent Client Protocol Integration
echo ========================================================
echo.
echo This replaces the traditional Bridge system with ACP:
echo - Windsurf (via ACP Extension) 
echo - Gemini CLI (ACP Agent)
echo - Claude Agent (ACP Agent)
echo - Custom Antigravity Agent
echo.

echo Starting ACP Bridge Manager in background...
start "ACP Bridge Manager" /min python acp_bridge_manager.py

timeout /t 2 >nul

echo.
echo Testing ACP Bridge connection...
python acp_hook_handler.py --event test --message "ACP Bridge Startup Test"

echo.
echo ACP Bridge Manager started successfully!
echo.
echo Configuration: d:\Gemini\agent-hand\bridge\acp_agents_config.json
echo Logs: Check individual agent terminals for details
echo.
echo To stop: Close the ACP Bridge Manager window
echo.

pause
