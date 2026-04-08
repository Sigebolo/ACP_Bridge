@echo off
echo Starting OpenClaw Bridge Service...

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

REM Check if dependencies are installed
if not exist "node_modules" (
    echo Installing dependencies...
    npm install
    if %errorlevel% neq 0 (
        echo Error: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Create necessary directories
if not exist "data" mkdir data
if not exist "artifacts" mkdir artifacts
if not exist "logs" mkdir logs
if not exist "workspace" mkdir workspace
if not exist "workspace\google-cli" mkdir workspace\google-cli
if not exist "workspace\windsurf" mkdir workspace\windsurf

REM Set environment variables
set NODE_ENV=development
set PORT=3000
set WS_PORT=3001

REM Start the server
echo Starting server on port %PORT%...
echo WebSocket server on port %WS_PORT%...
echo.
echo Press Ctrl+C to stop the server
echo.

npm start
