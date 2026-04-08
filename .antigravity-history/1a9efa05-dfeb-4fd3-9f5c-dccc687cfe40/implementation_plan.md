# Real-time Windsurf to Antigravity Synchronization Bridge

This plan outlines the steps to implement a real-time synchronization bridge that captures Windsurf Cascade actions (hooks) and pushes them to Antigravity for live review via a Server-Sent Events (SSE) stream.

## User Review Required

> [!IMPORTANT]
> The current bridge is implemented in Node.js, while the user's provided snippets suggested Python (FastAPI). This plan implements the SSE and POST endpoints in the existing Node.js `BridgeServer` to maintain consistency with the current codebase.

> [!WARNING]
> Windsurf Cascade Hooks must be manually configured in Windsurf's `settings.json` or `.windsurf/hooks.json`.

## Proposed Changes

### [Component] Bridge Server (Node.js)

#### [MODIFY] [server.js](file:///d:/Gemini/agent-hand/bridge/src/server.js)
- Add `POST /antigravity/review-step` to receive events from Windsurf.
- Add `GET /antigravity/live-review` to provide an SSE stream for Antigravity.
- Integrate with `NotificationService` to emit and listen for `review_step` events.

### [Component] Scripts & Config

#### [NEW] [push_step.py](file:///d:/Gemini/agent-hand/bridge/scripts/push_step.py)
- A lightweight Python script that Windsurf will execute after every action to POST data to the Bridge server.

#### [NEW] [hooks.json](file:///d:/Gemini/agent-hand/bridge/config/hooks.json)
- Example configuration for Windsurf Cascade Hooks.

## Open Questions

- Should we store the review steps in a persistent database (e.g., `data/reviews.json`) or only keep them in memory for the live stream? (Currently proposing in-memory + event emission for simplicity).
- Do we need a feedback loop where Antigravity can "block" Windsurf? The user mentioned this, but it requires Windsurf to wait for a response, which hooks might not support synchronously in the way described.

## Verification Plan

### Automated Tests
- Use `curl` to POST a dummy step to `/antigravity/review-step`.
- Use `curl` or a browser to connect to `/antigravity/live-review` and verify the dummy step appears in the stream.

### Manual Verification
- Configure Windsurf with the new hooks.
- Perform an action in Windsurf (e.g., read a file).
- Check the `bridge` logs and SSE stream output to confirm the event was captured.
