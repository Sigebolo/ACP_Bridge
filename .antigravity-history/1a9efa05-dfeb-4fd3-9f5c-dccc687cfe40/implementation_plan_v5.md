# Phase 5: Port Migration (Reliability & Stability)

To resolve persistent "Port Occupied" (EADDRINUSE) issues that caused the Bridge to crash and miss sync events, I am migrating the entire system to a unique high-port range (33333+).

## User Review Required

> [!IMPORTANT]
> **Hook URL Change**: After this change, any external tools or Windsurf settings pointing to `localhost:3000` **must** be updated to `localhost:33333`. I will update the internal scripts automatically.

> [!TIP]
> This move to "private range" ports ensures that common development tools (like React on 3000 or proxy servers on 8081) won't crash our bridge in the future.

## Proposed Changes

### [Component] Bridge Server (Node.js)

#### [MODIFY] [server.js](file:///d:/Gemini/agent-hand/bridge/src/server.js)
-   **Port HTTP**: `33333`
-   **Port WS**: `33334`

### [Component] Antigravity Connector (8081 -> 33335)

#### [MODIFY] [antigravity-connector.js](file:///d:/Gemini/agent-hand/bridge/scripts/antigravity-connector.js)
-   **Local Port**: `33335`
-   **Bridge URL**: `http://localhost:33333`

### [Component] Sync Scripts & CLI

#### [MODIFY] [antigravity.py](file:///d:/Gemini/agent-hand/bridge/scripts/antigravity.py)
#### [MODIFY] [push_step.py](file:///d:/Gemini/agent-hand/bridge/scripts/push_step.py)
#### [MODIFY] [.windsurf/memories/sync_architecture.md](file:///d:/Gemini/agent-hand/bridge/.windsurf/memories/sync_architecture.md)
-   Update all references from `3000/8081` to `33333/33335`.

## Open Questions

-   Are you okay with using the **33333** range, or would you prefer a different specific range (e.g., 50000+)?

## Verification Plan

### Automated Tests
-   Verify `python scripts/antigravity.py status` returns Success for the new ports.
-   Force-kill and restart, confirm no `EADDRINUSE` errors occur.

### Manual Verification
-   Trigger a Windsurf action and confirm it reaches the Bridge on `33333`.
