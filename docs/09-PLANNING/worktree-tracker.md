# Worktree Tracker

> Track all active worktrees for multi-agent parallel development.
> Updated every time a worktree is created, modified, or removed.

**Last Updated**: 2026-04-15 22:55:00
**Version**: v1.0
**Maintaining Agent**: Claude Code

## Active Worktrees

| Worktree | Agent | Task | Branch | Created | Status | Last Activity | Notes |
|----------|-------|------|--------|---------|--------|---------------|-------|
| agent/TASK-001/claude | Claude Code | TASK-001 | feature/TASK-001-claude | 2026-04-15 | In Progress | 2026-04-15 22:55 | Harness bootstrap Phase 7-11 |
| agent/TASK-004/windsurf | Windsurf | TASK-004 | feature/TASK-004-windsurf | 2026-04-10 | In Progress | 2026-04-15 22:30 | Obsidian Integration v2 |

## Worktree Naming Convention

### Format: `agent/{TASK-ID}/{agent-name}`

**Components**:
- `agent/`: Fixed prefix for all agent worktrees
- `{TASK-ID}`: Task identifier from Feature SSoT
- `{agent-name}`: Agent name (claude, windsurf, gemini, antigravity)

### Examples
- `agent/TASK-001/claude` - Claude Code working on TASK-001
- `agent/TASK-002/windsurf` - Windsurf working on TASK-002
- `agent/TASK-003/gemini` - Gemini CLI working on TASK-003
- `agent/HOTFIX-001/claude` - Claude Code working on emergency fix

## Branch Naming Convention

### Format: `feature/{TASK-ID}-{agent-name}`

**Special Prefixes**:
- `feature/` - Standard feature development
- `hotfix/` - Emergency fixes
- `refactor/` - Refactoring tasks
- `experiment/` - Experimental features

### Examples
- `feature/TASK-001-claude` - Claude Code feature branch
- `hotfix/HOTFIX-001-windsurf` - Windsurf hotfix branch
- `refactor/REF-001-gemini` - Gemini CLI refactor branch

## Worktree Creation Process

### 1. Pre-Creation Checks
```bash
# Ensure main branch is clean
git status
# Should show "working tree clean"

# Check existing worktrees
git worktree list
# Verify no naming conflicts
```

### 2. Create Worktree
```bash
# Standard feature worktree
git worktree add agent/TASK-001/claude -b feature/TASK-001-claude

# Emergency fix worktree
git worktree add agent/HOTFIX-001/windsurf -b hotfix/HOTFIX-001-windsurf

# Experimental worktree
git worktree add agent/EXP-001/gemini -b experiment/EXP-001-gemini
```

### 3. Configure Worktree
```bash
cd agent/TASK-001/claude

# Set agent-specific git config
git config user.name "Claude Code Agent"
git config user.email "claude@agent.local"

# Create task directory structure
mkdir -p docs/09-PLANNING/TASKS/TASK-001
```

## Worktree Management Rules

### When Worktrees Are Required
- Multi-file implementation or refactoring
- Tasks spanning multiple iterations
- Regression or harness semantic changes
- When main workspace has uncommitted changes

### When Worktrees Are Optional
- Read-only analysis tasks
- Minor documentation updates
- User explicitly requests direct modification
- Continuing existing work in current workspace

### Worktree Cleanup Rules
- **Must Clean**: After successful merge to main
- **Must Clean**: After task cancellation
- **Can Keep**: Only with explicit reason in progress.md
- **Maximum Lifetime**: 14 days (except for long-running experiments)

## Multi-Agent Coordination

### Parallel Development Rules
1. **Task Isolation**: Each agent works only in their designated worktree
2. **Shared Resource Coordination**: Coordinate through ACP for shared files
3. **Merge Order**: Determined by task priority and dependencies
4. **Conflict Resolution**: High-priority agent takes precedence

### Resource Sharing Protocol
```python
# ACP resource sharing message
{
    "type": "resource_request",
    "agent": "claude",
    "resource": "adapters/base_adapter.py",
    "operation": "modify",
    "duration": "30 minutes",
    "priority": "P2"
}
```

### Conflict Resolution
- **Simple Conflicts**: Auto-resolve by higher priority agent
- **Complex Conflicts**: Human intervention required
- **Shared Files**: Sequential access through ACP locking
- **Protocol Changes**: Requires all P2 agents approval

## Worktree Status Tracking

### Status Values
- **Creating**: Worktree being created
- **Active**: Worktree in use
- **Paused**: Worktree temporarily paused
- **Merging**: Worktree being merged
- **Cleaning**: Worktree being cleaned up
- **Completed**: Worktree successfully merged and cleaned
- **Failed**: Worktree creation or merge failed

### Activity Types
- **Created**: New worktree created
- **Committed**: Changes committed to worktree
- **Pushed**: Branch pushed to remote
- **Merged**: Branch merged to main
- **Cleaned**: Worktree removed
- **Conflict**: Merge conflict encountered

## Worktree Health Monitoring

### Daily Health Check
```bash
#!/bin/bash
# daily-worktree-health-check.sh

echo "=== Worktree Health Check ==="
echo "Active worktrees:"
git worktree list

echo -e "\n\nStale worktrees (no activity 7+ days):"
find agent/ -maxdepth 3 -type d -mtime +7 -exec ls -la {} \;

echo -e "\n\nUnmerged branches:"
git branch --no-merged main

echo -e "\n\nWorktree sizes:"
du -sh agent/*/* 2>/dev/null || echo "No active worktrees"
```

### Automated Cleanup
```bash
#!/bin/bash
# automated-worktree-cleanup.sh

# Clean up completed worktrees (merged branches)
for worktree in $(find agent/ -maxdepth 2 -type d); do
    if [ -f "$worktree/.git" ]; then
        branch=$(git --git-dir="$worktree/.git" rev-parse --abbrev-ref HEAD)
        if git merge-base --is-ancestor origin/main "$branch" 2>/dev/null; then
            echo "Cleaning up completed worktree: $worktree"
            git worktree remove "$worktree"
            git branch -d "$branch"
        fi
    fi
done

# Clean up stale worktrees (14+ days old)
find agent/ -maxdepth 3 -type d -mtime +14 -exec rm -rf {} \; 2>/dev/null
```

## Worktree Templates and Scripts

### Worktree Creation Script
```bash
#!/bin/bash
# create-agent-worktree.sh

TASK_ID=$1
AGENT_NAME=$2
TASK_TYPE=${3:-"feature"}

if [ -z "$TASK_ID" ] || [ -z "$AGENT_NAME" ]; then
    echo "Usage: $0 <TASK_ID> <AGENT_NAME> [TASK_TYPE]"
    exit 1
fi

WORKTREE_PATH="agent/$TASK_ID/$AGENT_NAME"
BRANCH_NAME="$TASK_TYPE/$TASK_ID-$AGENT_NAME"

echo "Creating worktree: $WORKTREE_PATH"
echo "Branch: $BRANCH_NAME"

# Create worktree
git worktree add "$WORKTREE_PATH" -b "$BRANCH_NAME"

# Configure worktree
cd "$WORKTREE_PATH"
git config user.name "$AGENT_NAME Agent"
git config user.email "$AGENT_NAME@agent.local"

# Create task directory if it doesn't exist
TASK_DIR="docs/09-PLANNING/TASKS/$TASK_ID"
mkdir -p "$TASK_DIR"

echo "Worktree created successfully: $WORKTREE_PATH"
```

### Worktree Status Script
```bash
#!/bin/bash
# worktree-status.sh

echo "=== Agent Worktree Status ==="
echo

for worktree in $(find agent/ -maxdepth 2 -type d -name ".git"); do
    worktree_dir=$(dirname "$worktree")
    worktree_name=$(basename "$worktree_dir")
    agent_name=$(basename $(dirname "$worktree_dir"))
    
    cd "$worktree_dir"
    branch=$(git rev-parse --abbrev-ref HEAD)
    status=$(git status --porcelain)
    commits_behind=$(git rev-list --count HEAD..origin/main 2>/dev/null || echo "0")
    
    echo "Agent: $agent_name"
    echo "Worktree: $worktree_name"
    echo "Branch: $branch"
    echo "Status: $([ -z "$status" ] && echo "Clean" || echo "Dirty")"
    echo "Behind main: $commits_behind commits"
    echo "Last activity: $(stat -c %y "$worktree")"
    echo "---"
    
    cd - > /dev/null
done
```

## Worktree Integration with Planning Loop

### Task Plan Integration
Every task plan must specify:
- **Worktree Required**: Yes/No
- **Worktree Path**: `agent/{TASK-ID}/{agent-name}`
- **Branch Name**: `feature/{TASK-ID}-{agent-name}`
- **Cleanup Timeline**: When worktree should be cleaned

### Progress Tracking Integration
Progress updates must include:
- **Worktree Status**: Current state of worktree
- **Branch Status**: Clean/dirty/merged
- **Conflict Status**: Any merge conflicts
- **Cleanup Plan**: When and how worktree will be cleaned

### Feature SSoT Integration
Feature SSoT tracks:
- **Active Worktrees**: Number and status of active worktrees
- **Agent Utilization**: Which agents are using worktrees
- **Worktree Lifetime**: How long worktrees remain active
- **Cleanup Efficiency**: How quickly worktrees are cleaned

## Troubleshooting

### Common Issues
1. **Worktree Creation Fails**: Check for naming conflicts
2. **Branch Already Exists**: Use different branch name or clean up existing
3. **Merge Conflicts**: Use conflict resolution protocol
4. **Worktree Won't Remove**: Check for uncommitted changes

### Recovery Procedures
```bash
# Force remove corrupted worktree
git worktree prune
rm -rf agent/TASK-001/claude

# Recover lost worktree
git worktree add agent/TASK-001/claude feature/TASK-001-claude

# Check worktree consistency
git worktree list --porcelain
```

## Best Practices

### Worktree Management
1. **Clean Up Promptly**: Remove worktrees immediately after merge
2. **Monitor Activity**: Regularly check for stale worktrees
3. **Coordinate Access**: Use ACP for shared resource access
4. **Document Exceptions**: Record reasons for keeping worktrees

### Agent Coordination
1. **Respect Boundaries**: Work only in assigned worktrees
2. **Communicate Intentions**: Use ACP to announce plans
3. **Handle Conflicts Gracefully**: Follow conflict resolution protocol
4. **Share Learnings**: Document worktree-specific learnings

### Performance Optimization
1. **Limit Concurrent Worktrees**: Maximum 5 per agent
2. **Monitor Disk Usage**: Clean up large files promptly
3. **Optimize Git Operations**: Use git worktree prune regularly
4. **Batch Operations**: Group similar worktree operations

---

**Last Updated**: 2026-04-15 22:55:00
**Maintaining Agent**: Claude Code
**Active Worktrees**: 2
**Total Worktrees Created**: 7
**Average Worktree Lifetime**: 3.2 days
