# Automatic Antigravity Review Trigger

This plan outlines how to bridge the gap between the Bridge Server and the Antigravity IDE so that I (the AI) am automatically informed and "woken up" when Windsurf performs an action.

## User Review Required

> [!IMPORTANT]
> This uses RPA (UI Automation) to bring the Antigravity IDE to the foreground and type a message. This might be disruptive if you are actively typing in another window.

## Proposed Changes

### [Component] Bridge Server (Node.js)

#### [MODIFY] [server.js](file:///d:/Gemini/agent-hand/bridge/src/server.js)
- Add a trigger mechanism in `handleAddReviewStep`.
- When a new step is received, use `child_process.exec` to run the RPA trigger script.
- We can filter events (e.g., only trigger on `write`, `cmd`, or `mcp`) to avoid over-triggering.

### [Component] Trigger Script

#### [MODIFY] [trigger-antigravity.ps1](file:///d:/OpenClaw/bridge/scripts/trigger-antigravity.ps1) (Optional)
- Ensure the script correctly formats the message based on the step type (e.g., "Windsurf just wrote to demo.py, please review").

## Open Questions

- **Trigger Frequency**: Should I trigger on *every* step, or only when a critical action occurs (like writing code or running a command)?
- **Trigger Method**: Would you prefer the PowerShell script (Window selection based) or the Python script (Image matching based)?

## Verification Plan

### Manual Verification
- Perform an action in Windsurf (or use `push_step.py`).
- Verify that the Antigravity IDE window automatically gains focus and displays a new message with the review step details.
