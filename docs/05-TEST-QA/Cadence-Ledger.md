# Cadence Ledger - Hermes ACP Ecosystem

> define"what changes automatically trigger which regression surfaces".
> New regression gates must be synchronized with trigger rules.

**Last Updated**: 2026-04-15 22:45:00
**Version**: v1.0
**Maintaining Agent**: Claude Code

## Trigger Rules

| Change Scope | Triggered Regression Gates | Description |
|--------------|----------------------------|-------------|
| `acp_server.py` / core server logic | RG-001, RG-006 | Core ACP server and WebSocket protocol |
| `adapters/claude_adapter.py` | RG-002 | Claude Code adapter functionality |
| `adapters/windsurf_adapter.py` | RG-003 | Windsurf adapter functionality |
| `adapters/antigravity_adapter.py` | RG-004 | Antigravity adapter functionality |
| `adapters/gemini_adapter.py` | RG-005 | Gemini CLI adapter functionality |
| `acp_bridge_manager.py` | RG-007 | Bridge manager coordination logic |
| `websocket_protocol.py` / message format | RG-001, RG-006 | Protocol changes affect server and communication |
| `obsidian_integration.py` | RG-008 | Obsidian synchronization functionality |
| `monitoring/` directory | RG-009 | System monitoring and health checks |
| `security/` or auth-related files | RG-010 | Security layer and authentication |
| Any merge to main branch | Full Shared Batch | Complete regression suite |
| Protocol version bump | RG-001, RG-006 + Full Shared Batch | Protocol changes require full validation |
| Agent adapter interface changes | All RG-002 to RG-005 | Adapter interface changes affect all agents |

## Evidence Depth Trigger Rules

| Trigger Event | Required Evidence Depth | Surfaces |
|---------------|------------------------|----------|
| Commit to main | L1 | All surfaces |
| PR creation | L1+L2 | Affected surfaces |
| Adapter modification | L1+L2+L3 | Specific adapter |
| Protocol version change | L1+L2+L3+L4 | RG-001, RG-006 |
| Production release candidate | L1+L2+L3+L4 | All critical surfaces |
| Emergency hotfix | L1+L2 | Affected surfaces only |

## Shared Regression Batch Log

| Batch | Date | Scope | Trigger | Result | Notes | Next Checkpoint |
|-------|------|-------|---------|--------|-------|-----------------|
| SRB-001 | 2026-04-15 | Full | Initial bootstrap | 6/10 - 4/10 | 6 gates pass, 4 partial | SRB-002 after Phase 8 completion |
| SRB-002 | TBD | Full | Post-harness validation | TBD | TBD | SRB-003 after first feature completion |
| SRB-003 | TBD | Critical | Production release prep | TBD | TBD | SRB-004 after production release |

## Batch Execution Details

### SRB-001 - Initial Bootstrap Results
| Gate ID | Surface | L1 | L2 | L3 | L4 | Status | Issues |
|---------|---------|----|----|----|----|--------|--------|
| RG-001 | Hermes ACP Server |  |  |  |  |  |  |
| RG-002 | Claude Code Adapter |  |  |  |  |  |  |
| RG-003 | Windsurf Adapter |  |  |  |  |  |  |
| RG-004 | Antigravity Adapter |  |  |  |  |  |  |
| RG-005 | Gemini CLI Adapter |  |  |  |  |  |  |
| RG-006 | WebSocket Protocol |  |  |  |  |  |  |
| RG-007 | Bridge Manager |  |  |  |  |  |  |
| RG-008 | Obsidian Integration |  |  |  |  |  |  |
| RG-009 | Monitoring System |  |  |  |  |  |  |
| RG-010 | Security Layer |  |  |  |  |  |  |

## Automated Trigger Implementation

### Git Hook Integration
```bash
#!/bin/bash
# pre-commit hook
#!/bin/bash
# pre-commit-regression-trigger.sh

CHANGED_FILES=$(git diff --cached --name-only)
TRIGGERED_GATES=""

# Analyze changed files and determine gates
for file in $CHANGED_FILES; do
    case $file in
        "acp_server.py"|"src/acp_server/")
            TRIGGERED_GATES="$TRIGGERED_GATES RG-001 RG-006"
            ;;
        "adapters/claude_adapter.py")
            TRIGGERED_GATES="$TRIGGERED_GATES RG-002"
            ;;
        "adapters/windsurf_adapter.py")
            TRIGGERED_GATES="$TRIGGERED_GATES RG-003"
            ;;
        # Add more cases as needed
    esac
done

# Remove duplicates and run regression
UNIQUE_GATES=$(echo "$TRIGGERED_GATES" | tr ' ' '\n' | sort -u | tr '\n' ' ')
python scripts/run_regression.py --gates "$UNIQUE_GATES"
```

### ACP Integration
```python
# acp_regression_trigger.py
def determine_regression_gates(changed_files):
    """Determine which regression gates to run based on changed files"""
    gates = []
    
    for file_path in changed_files:
        if file_path.startswith('acp_server') or 'core' in file_path:
            gates.extend(['RG-001', 'RG-006'])
        elif file_path.startswith('adapters/claude'):
            gates.append('RG-002')
        elif file_path.startswith('adapters/windsurf'):
            gates.append('RG-003')
        # Add more mapping rules
    
    return list(set(gates))  # Remove duplicates

def trigger_regression_batch(gates, trigger_event):
    """Trigger regression batch via ACP"""
    message = {
        "type": "regression_trigger",
        "gates": gates,
        "trigger_event": trigger_event,
        "timestamp": datetime.now().isoformat()
    }
    
    # Send to ACP for execution
    acp_broadcast(message)
```

## Batch Scheduling

### Regular Batches
- **Daily**: L1+L2 for all surfaces (overnight)
- **Weekly**: Full L1+L2+L3 batch (Sunday morning)
- **Release**: Full L1+L2+L3+L4 batch (before each release)

### Event-Driven Batches
- **PR Creation**: Affected surfaces L1+L2
- **Merge to Main**: Full batch L1+L2
- **Protocol Changes**: Full batch L1+L2+L3+L4
- **Emergency Hotfix**: Affected surfaces L1+L2

## Quality Gates

### Before Merge
- All L1 tests must pass
- At least L2 tests for affected surfaces
- No critical security vulnerabilities

### Before Release
- All L1+L2 tests must pass
- Critical surfaces must pass L3
- Production surfaces must pass L4

### Production Deployment
- Full regression suite must pass
- Performance benchmarks must meet targets
- Security scan must be clean

## Monitoring and Alerting

### Batch Health Monitoring
- **Success Rate**: Track batch success rate over time
- **Execution Time**: Monitor batch execution duration
- **Failure Patterns**: Identify recurring failure patterns
- **Coverage Gaps**: Detect surfaces without adequate coverage

### Alert Rules
- **Batch Failure**: Immediate alert for any batch failure
- **Degraded Performance**: Alert if execution time exceeds threshold
- **Coverage Drop**: Alert if evidence depth decreases
- **Critical Gate Failure**: High-priority alert for critical surface failures

## Maintenance Procedures

### Adding New Regression Gates
1. Add gate to Regression SSoT
2. Update trigger rules mapping
3. Add to batch execution scripts
4. Run initial validation batch
5. Update Cadence Ledger

### Modifying Trigger Rules
1. Analyze impact of rule change
2. Update trigger mapping
3. Test with sample changes
4. Update documentation
5. Communicate to agents

### Batch Log Maintenance
- Record every batch execution
- Note any anomalies or issues
- Track trends over time
- Archive old logs periodically

## Continuous Improvement

### Metrics to Track
- **Mean Time to Detection**: How quickly failures are detected
- **Mean Time to Resolution**: How quickly failures are fixed
- **False Positive Rate**: How often tests fail incorrectly
- **Coverage Effectiveness**: How well tests catch actual issues

### Optimization Opportunities
- Parallel execution for faster results
- Smart caching to reduce redundant tests
- Predictive test selection based on change impact
- Automated failure analysis and suggestions

## Integration with Planning Loop

### Feature Integration
- New features must include regression gate definitions
- Feature completion requires evidence depth achievement
- Walkthrough must include regression validation results

### Task Integration
- Task plans must specify required evidence depth
- Progress tracking includes regression status
- Task completion requires regression validation

## Emergency Procedures

### Critical Production Issues
1. Immediately run L1+L2 regression on affected surfaces
2. Escalate to P2 agents for analysis
3. Create hotfix branch if needed
4. Run targeted regression on fix
5. Deploy with full L1+L2 validation

### System-Wide Outages
1. Run full emergency regression batch
2. Identify failing surfaces
3. Prioritize critical surface fixes
4. Validate fixes with targeted regression
5. Full system validation before recovery
