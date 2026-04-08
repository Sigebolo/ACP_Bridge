@echo off
echo ACP Bridge Status Check
echo ========================

cd /d "d:\Gemini\agent-hand\bridge"

echo.
echo Checking ACP Bridge Components...
echo.

echo 1. Checking ACP Configuration...
if exist "acp_agents_config.json" (
    echo [v] ACP Configuration: OK
) else (
    echo [x] ACP Configuration: Missing
)

echo.
echo 2. Checking ACP Bridge Manager...
if exist "acp_bridge_manager.py" (
    echo [v] ACP Bridge Manager: OK
) else (
    echo [x] ACP Bridge Manager: Missing
)

echo.
echo 3. Checking ACP Hook Handler...
if exist "acp_hook_handler.py" (
    echo [v] ACP Hook Handler: OK
) else (
    echo [x] ACP Hook Handler: Missing
)

echo.
echo 4. Checking Windsurf ACP Extension...
code --list-extensions | findstr "acp-client" >nul
if %errorlevel% == 0 (
    echo [v] Windsurf ACP Extension: Installed
) else (
    echo [x] Windsurf ACP Extension: Not installed
)

echo.
echo 5. Checking Gemini CLI...
npx @google/gemini-cli --version >nul 2>&1
if %errorlevel% == 0 (
    echo [v] Gemini CLI: Available
) else (
    echo [x] Gemini CLI: Not available
)

echo.
echo 6. Checking Claude Agent ACP...
if exist "d:/Gemini/agent-hand/claude-agent-acp/dist/index.js" (
    echo [v] Claude Agent ACP: Built
) else (
    echo [x] Claude Agent ACP: Not built
)

echo.
echo 7. Testing ACP Hook Handler...
python acp_hook_handler.py --event test --file "test.txt" >nul 2>&1
if %errorlevel% == 0 (
    echo [v] ACP Hook Handler: Working
) else (
    echo [x] ACP Hook Handler: Error
)

echo.
echo ========================
echo ACP Bridge Status Complete
echo ========================

pause
