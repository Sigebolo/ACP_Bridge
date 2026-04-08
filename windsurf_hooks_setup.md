# Windsurf Hooks Setup Guide

## Current Status

### 1. Hook Configuration Files Ready
- `config/hooks.json` - Contains all 5 hook configurations
- `test_hooks.py` - Working hook handler for testing

### 2. Required Windsurf Settings

To enable hooks in Windsurf, add the following to your `settings.json`:

```json
{
  "windsurf.cascade.hooks": {
    "onWrite": "python d:/Gemini/agent-hand/bridge/acp_hook_handler.py --event write --file ${file} --diff ${diff}",
    "onRead": "python d:/Gemini/agent-hand/bridge/acp_hook_handler.py --event read --file ${file} --content ${content}",
    "onCommand": "python d:/Gemini/agent-hand/bridge/acp_hook_handler.py --event cmd --command ${command} --output ${output}",
    "onMcpTool": "python d:/Gemini/agent-hand/bridge/acp_hook_handler.py --event mcp --tool ${tool} --result ${result}",
    "onResponse": "python d:/Gemini/agent-hand/bridge/acp_hook_handler.py --event response --reasoning ${reasoning}"
  }
}
```

### 3. Hook Event Types

| Hook | Trigger | Command |
|------|---------|---------|
| `post_read_code` | File read | `--event read` |
| `post_write_code` | File write | `--event write` |
| `post_run_command` | Command execution | `--event cmd` |
| `post_mcp_tool_use` | MCP tool use | `--event mcp` |
| `post_cascade_response` | Cascade response | `--event response` |

### 4. Testing Hooks

Test individual hooks:
```bash
# Test file write hook
python test_hooks.py --event write --file example.py --diff "+ new line"

# Test command hook  
python test_hooks.py --event cmd --command "npm test" --output "Tests passed"

# Test response hook
python test_hooks.py --event response --reasoning "I analyzed the code and found..."
```

### 5. Current Issues

- `acp_bridge_manager.py` has syntax errors (line 449)
- Need to fix before using production hooks
- `test_hooks.py` works as temporary replacement

### 6. Next Steps

1. Fix `acp_bridge_manager.py` syntax errors
2. Configure Windsurf `settings.json` with hooks
3. Test bidirectional communication
4. Verify Gemini CLI receives Windsurf events
