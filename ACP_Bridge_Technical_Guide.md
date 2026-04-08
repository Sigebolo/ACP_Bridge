# ACP Bridge Technical Guide - Agent Self-Installation Protocol

## Bootstrap Section (Agent Self-Installation)

### Agent Auto-Configuration Instructions

When an Agent first reads this document, it must execute the following bootstrap procedure to establish ACP communication:

#### 1. Required Bootstrap Command
```bash
python D:/Gemini/agent-hand/bridge/acp_server_clean.py --install
```

This command will:
- Create `acp_agents_config.json` with proper Agent configurations
- Generate `config/hooks.json` for Windsurf integration
- Set up necessary directories for communication
- Install diagnostic tools

#### 2. Post-Installation Verification
After bootstrap execution, verify installation by running:
```bash
python D:/Gemini/agent-hand/bridge/diagnose_acp.py
```

Expected output should show:
```
[ACP Diag] OK: d:/Gemini/agent-hand/bridge/acp_agents_config.json
[ACP Diag] OK: d:/Gemini/agent-hand/bridge/config/hooks.json
[ACP Diag] OK: d:/Gemini/agent-hand/bridge/logs
[ACP Diag] OK: d:/Gemini/agent-hand/bridge/windsurf_notifications
[ACP Diag] OK: d:/Gemini/agent-hand/bridge/gemini_responses
[ACP Diag] All systems ready!
```

---

## ACP Architecture Overview

### Communication Flow
```
Agent (Gemini CLI) <-> ACP Protocol <-> Bridge Server <-> Windsurf (Cascade)
```

### Key Components

#### 1. ACP Agents Configuration (`acp_agents_config.json`)
Defines available agents and their capabilities:
```json
{
  "agents": [
    {
      "name": "Gemini CLI",
      "command": ["cmd", "/c", "npx @google/gemini-cli --experimental-acp"],
      "capabilities": ["file_access", "terminal", "tools", "streaming"]
    }
  ],
  "defaultAgent": "Gemini CLI"
}
```

#### 2. Windsurf Hooks Configuration (`config/hooks.json`)
Defines how Windsurf events are captured and forwarded:
```json
{
  "hooks": {
    "post_read_code": [...],
    "post_write_code": [...],
    "post_run_command": [...],
    "post_mcp_tool_use": [...],
    "post_cascade_response": [...]
  }
}
```

#### 3. Input Hooks (Agent -> Windsurf)
Endpoints for agents to send messages back to Windsurf:
- `/api/gemini/message` - General messages
- `/api/gemini/review` - Code reviews
- `/api/gemini/suggestion` - Suggestions

---

## Self-Healing Toolkit

### Diagnostic Script (`diagnose_acp.py`)
Automated system health check that verifies:
- Configuration file existence
- Directory structure
- Agent availability
- Communication readiness

### Common Issues & Solutions

#### Issue: Agent cannot connect
**Solution**: Run diagnostic script
```bash
python diagnose_acp.py
```

#### Issue: Hooks not working
**Solution**: Re-run bootstrap
```bash
python acp_server_clean.py --install
```

#### Issue: Missing directories
**Solution**: Bootstrap creates required directories automatically

---

## Agent Activation Protocol

### Step 1: Self-Installation
Agent must execute bootstrap command upon first activation.

### Step 2: Verification
Run diagnostic to ensure all systems operational.

### Step 3: Communication Test
Agent should send a test message to verify bidirectional communication.

### Step 4: Operational Mode
Once verified, agent can engage in full ACP communication.

---

## Integration Points

### For Windsurf
- Monitor `windsurf_notifications/` directory for incoming messages
- Process JSON files with agent responses
- Display notifications in IDE interface

### For Agents
- Use ACP protocol for standardized communication
- Send messages via input hook endpoints
- Monitor for Windsurf events via hooks

---

## Security Considerations

- All communication uses local filesystem (no network exposure)
- Agent capabilities are explicitly defined in configuration
- Diagnostic tools help detect configuration issues

---

## Troubleshooting

### Bootstrap Fails
1. Check Python installation
2. Verify file permissions
3. Ensure directory structure exists

### Communication Issues
1. Run diagnostic script
2. Check configuration files
3. Verify agent process status

### Hook Issues
1. Verify hook paths in configuration
2. Check Python script execution permissions
3. Test individual hook commands

---

**Status: READY FOR AGENT ACTIVATION**

This guide provides complete self-installation instructions for any Agent to establish ACP communication with Windsurf.
