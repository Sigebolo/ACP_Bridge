# Enhanced Sync: Reliable UI Focus & Precise Context Management

As requested, I will address the issue of "messy typing" into random files and solve the "too much history" problem by providing precise, context-rich notifications.

## User Review Required

> [!IMPORTANT]
> The history limit will be set to the last 100 items globally, but the API will now favor single-step lookups for new notifications. This ensures I only load what is necessary for the current review.

> [!WARNING]
> The RPA script will now perform a **Clear Input** action (Ctrl+A followed by Delete/Backspace) before typing. Ensure you don't have mission-critical text unsent in your chat input at that moment!

## Proposed Changes

### [Component] Bridge Server (Node.js)

#### [MODIFY] [server.js](file:///d:/Gemini/agent-hand/bridge/src/server.js)
-   **New Route**: `GET /antigravity/review-step/:id` — returns a single, specific action by ID.
-   **History Update**: Update `/antigravity/review-history` to accept a `limit` query param (default: 5).
-   **RPA Enrichment**: Generate a "Mission Briefing" message:
    ```
    [WINDSURF SYNC] Detected: {{event}} on {{file}}
    📡 Details: http://localhost:3000/antigravity/review-step/{{id}}
    🕒 History: http://localhost:3000/antigravity/review-history?limit=10
    👉 Action: Fetch details and perform Real-time Review.
    ```

### [Component] RPA Script

#### [MODIFY] [trigger-antigravity.ps1](file:///d:/Gemini/agent-hand/bridge/scripts/trigger-antigravity.ps1)
-   **Robust Focus**:
    1.  Focus "Antigravity" window.
    2.  Wait 1s.
    3.  Send `Ctrl+L` (Focus Chat).
    4.  Send `Ctrl+A` -> `BACKSPACE` (Clear potential debris).
    5.  Wait 300ms.
    6.  Paste & Send.
-   **Title Specificity**: Use a more rigid window title match if possible to avoid browser tabs.

## Open Questions

-   For the "1000 items" concern: Would you like the Bridge to persist these to a `reviews.log` file, or is keeping the most recent 100 in-memory enough for your current workflow?
-   Is **Ctrl+L** the confirmed shortcut for your chat input? If it varies, I can add a fallback key sequence.

## Verification Plan

### Automated Tests
-   Verify `GET /antigravity/review-step/:id` returns the expected JSON.
-   Verify `limit=5` correctly slices the history.

### Manual Verification
-   Trigger a `write` action and confirm the IDE window correctly gains focus, CLEARS the chat box, and inputs the full Mission Briefing.
