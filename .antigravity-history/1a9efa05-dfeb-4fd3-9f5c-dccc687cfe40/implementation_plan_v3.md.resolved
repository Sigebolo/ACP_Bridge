# Phase 3: Agentic Task Delivery (Robust Synchronization)

To solve the issues of "typing into the wrong IDE" and "flaky UI automation," I am transitioning the system to use the **Antigravity Connector API**.

## User Review Required

> [!IMPORTANT]
> This change moves the "source of truth" from a chat message to a **Markdown Task File** in your workspace. I will now "receive" actions as formal tasks that I can read with my tools, making the review far more precise.

> [!TIP]
> The RPA will be significantly simplified. It will no longer "type the diff"—it will simply focus the Antigravity window and say: `[Windsurf Sync] New action detected. Read workspace/antigravity_tasks/review_xxxx.md`.

## Proposed Changes

### [Component] Bridge Server (Node.js)

#### [MODIFY] [server.js](file:///d:/Gemini/agent-hand/bridge/src/server.js)
-   **Method**: `triggerAntigravityTask(step)`
    -   Uses `axios` to `POST` to `http://localhost:8081/tasks`.
    -   Payload includes: `title: "Windsurf Review: ${step.file}"`, `description: step.diff`, `type: "review"`.
-   **Trigger Flow**:
    1.  Push to `reviewStream`.
    2.  Push to **Connector (8081)**.
    3.  Trigger **Minimal RPA** (Just a focus ping).

### [Component] RPA Script

#### [MODIFY] [trigger-antigravity.ps1](file:///d:/Gemini/agent-hand/bridge/scripts/trigger-antigravity.ps1)
-   **Specific Targeting**: Change the filter to `Get-Process -Name "Antigravity"`. This explicitly avoids Windsurf (which likely has its own process name).
-   **Minimal Message**: Reduce the payload to a single-line notification to avoid typing lag/errors.

## Open Questions

-   Is port **8081** confirmed to be available and running your `antigravity-connector.js`?
-   Would you like the MD task files to be automatically deleted after I finish reviewing them to keep your workspace clean?

## Verification Plan

### Automated Tests
-   Verify `axios.post` to 8081 returns `200 OK`.
-   Verify a new `.md` file appears in `workspace/antigravity_tasks/`.

### Manual Verification
-   Trigger a Windsurf action.
-   Confirm focus moves to **Antigravity.exe** (and NOT Windsurf).
-   Confirm a simple message arrives and the task file is generated.
