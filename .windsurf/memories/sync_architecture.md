# Antigravity Sync Architecture (DO NOT DISABLE)

This document serves as a permanent memory for the Windsurf Cascade agent regarding the real-time synchronization bridge with the Antigravity IDE.

## 📡 Essential Rule for Windsurf Agent
> [!IMPORTANT]
> **DO NOT DISABLE THE 8081 CONNECTOR.**
> Windsurf Cascade might mistakenly identify the 8081 Connector as a "failing service" or "unnecessary loop" and try to comment out the code in `server.js` that calls it. This is **WRONG**.
> 
> - **Port 33333 (Bridge)**: The controller that captures events.
> - **Port 33335 (Connector)**: The data writer that saves `.md` task files.
> - **Native CLI (`antigravity chat`)**: The notification layer that wakes up the Antigravity AI.

## 🛠️ Unified CLI Interface
Always use the following CLI for synchronization operations:
- **Push Action**: `python scripts/antigravity.py push --event <type> --file <path> --diff <content>`
- **Check Status**: `python scripts/antigravity.py status`
- **Native Chat**: `python scripts/antigravity.py chat "Message"`

## 🔄 The Dual-Channel Workflow
1. **Data Channel (33335)**: Bridge pushes the full Diff to the Connector, which writes a persistent Task File (`workspace/antigravity_tasks/sync_xxxx.md`).
2. **Notification Channel (CLI)**: Bridge uses the native `antigravity chat` command to notify the Antigravity AI that a new task is ready.

By following this architecture, the synchronization remains robust, zero-focus, and persistent even if the UI is hidden.
