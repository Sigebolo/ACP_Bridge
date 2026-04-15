# [Wave/Feature Name] Walkthrough

---
title: "[Wave/Feature Name] Walkthrough"
task_id: "TASK-[ID]"
agent: "[Agent Name]"
start_date: "[YYYY-MM-DD]"
completion_date: "[YYYY-MM-DD]"
evidence_depth: "[L1-L4]"
related_ssoT: "[Feature SSoT entry link]"
---

## Overview

**One-sentence summary**: [What this wave/feature accomplished in one sentence]

**Agent**: [Primary executing agent]
**Duration**: [Start date] to [Completion date]
**Complexity**: [Low/Medium/High]

## Change Scope

### Modified Modules/Packages
- [Module 1]: [Brief description of changes]
- [Module 2]: [Brief description of changes]
- [Module 3]: [Brief description of changes]

### Added Files
- `path/to/new/file1.py`: [Purpose]
- `path/to/new/file2.js`: [Purpose]
- `docs/xx-xxx/new-doc.md`: [Purpose]

### Deleted Files
- `path/to/removed/file.py`: [Reason for removal]
- `docs/xx-xxx/old-doc.md`: [Reason for removal]

### Configuration Changes
- `config/file.json`: [Changed parameters]
- `.env.example`: [Updated environment variables]

## Key Decisions

| Decision | Choice | Reason | Alternatives Considered |
|----------|--------|--------|--------------------------|
| [Decision 1] | [What was chosen] | [Why this choice] | [What was not chosen and why] |
| [Decision 2] | [What was chosen] | [Why this choice] | [What was not chosen and why] |
| [Decision 3] | [What was chosen] | [Why this choice] | [What was not chosen and why] |

### Technical Architecture Decisions
- **Architecture Change**: [Description of any architectural changes]
- **Protocol Changes**: [Any changes to WebSocket protocol or message formats]
- **Agent Coordination**: [Changes to how agents coordinate]
- **Data Flow**: [Changes to data flow patterns]

### Agent Collaboration Decisions
- **Agent Assignment**: [Why specific agents were chosen]
- **Coordination Pattern**: [How agents worked together]
- **Communication Protocol**: [ACP message patterns used]
- **Conflict Resolution**: [How conflicts were resolved]

## Validation Results

### Evidence Depth Achievement
- **L1 (Unit Tests)**: [Status] - [Coverage percentage]% - [Test count]
- **L2 (Integration)**: [Status] - [Integration scenarios tested]
- **L3 (Live Environment)**: [Status] - [Live test results]
- **L4 (Production Smoke)**: [Status] - [Production validation]

### Test Results
```bash
# Commands run and results
python -m pytest tests/unit/test_new_feature.py -v
# Output: X passed, Y failed

python scripts/integration_test.sh
# Output: Integration tests: PASSED

python scripts/live_environment_test.py
# Output: Live validation: PASSED
```

### Regression Validation
- **Regression Gates Executed**: [List of RG-XXX gates]
- **Results**: [X/Y passed, Z failed]
- **Reference**: [Link to Regression SSoT results]
- **Performance Impact**: [Performance metrics before/after]

### Agent-Specific Validation
- **Hermes ACP Server**: [Validation results]
- **Claude Code Adapter**: [Validation results]
- **Windsurf Adapter**: [Validation results]
- **Gemini CLI Adapter**: [Validation results]
- **Antigravity Adapter**: [Validation results]

## Residual Items

### High Priority (P1)
- [ ] [Issue 1]: [Description] - [Target resolution date]
- [ ] [Issue 2]: [Description] - [Target resolution date]

### Medium Priority (P2)
- [ ] [Issue 3]: [Description] - [Target resolution date]
- [ ] [Issue 4]: [Description] - [Target resolution date]

### Low Priority (P3)
- [ ] [Issue 5]: [Description] - [Target resolution date]

### Technical Debt
- [ ] [Debt 1]: [Description] - [Impact]
- [ ] [Debt 2]: [Description] - [Impact]

**If no residual items**: "No residual items identified"

## Knowledge Accumulation

### Reusable Patterns
1. **Pattern Name**: [Description]
   - **When to Use**: [Applicable scenarios]
   - **Implementation**: [Key implementation details]
   - **Caveats**: [Important considerations]

2. **Pattern Name**: [Description]
   - **When to Use**: [Applicable scenarios]
   - **Implementation**: [Key implementation details]
   - **Caveats**: [Important considerations]

### Agent Coordination Learnings
- **What Worked**: [Coordination patterns that succeeded]
- **What Didn't Work**: [Coordination challenges encountered]
- **Improvements**: [Suggestions for better coordination]

### Technical Learnings
- **Performance Insights**: [Performance learnings]
- **Security Considerations**: [Security-related learnings]
- **Scalability Observations**: [Scalability-related insights]

## Related Documentation

### Planning Documents
- **Task Plan**: `docs/09-PLANNING/TASKS/[TASK-ID]/task_plan.md`
- **Findings**: `docs/09-PLANNING/TASKS/[TASK-ID]/findings.md`
- **Progress**: `docs/09-PLANNING/TASKS/[TASK-ID]/progress.md`

### SSoT References
- **Feature SSoT**: `docs/09-PLANNING/Hermes-ACP-Feature-SSoT.md#[F-ID]`
- **Regression SSoT**: `docs/05-TEST-QA/Regression-SSoT.md#[RG-ID]`

### Reference Standards
- **Engineering Standard**: `docs/11-REFERENCE/engineering-standard.md`
- **Testing Standard**: `docs/11-REFERENCE/testing-standard.md`
- **Walkthrough Standard**: `docs/11-REFERENCE/walkthrough-standard.md`

### Code References
- **Main Commit**: [Commit hash] - [Commit message]
- **Pull Request**: [PR number] - [PR title]
- **Branch**: [Branch name]

## Impact Assessment

### System Impact
- **Performance**: [Performance impact assessment]
- **Stability**: [Stability impact assessment]
- **Scalability**: [Scalability impact assessment]
- **Security**: [Security impact assessment]

### Agent Impact
- **Hermes**: [Impact on Hermes ACP Server]
- **Claude Code**: [Impact on Claude Code adapter]
- **Windsurf**: [Impact on Windsurf adapter]
- **Gemini CLI**: [Impact on Gemini CLI adapter]
- **Antigravity**: [Impact on Antigravity adapter]

### User Impact
- **End User**: [Impact on end users]
- **Developer**: [Impact on developers]
- **Operations**: [Impact on operations]

## Next Steps

### Immediate (1-2 days)
- [ ] [Task 1]: [Description]
- [ ] [Task 2]: [Description]

### Short Term (1-2 weeks)
- [ ] [Task 3]: [Description]
- [ ] [Task 4]: [Description]

### Long Term (1+ months)
- [ ] [Task 5]: [Description]
- [ ] [Task 6]: [Description]

## Quality Metrics

### Code Quality
- **Test Coverage**: [Percentage]%
- **Code Complexity**: [Complexity metric]
- **Documentation Coverage**: [Percentage]%
- **Security Score**: [Security assessment score]

### Process Quality
- **Planning Adherence**: [Adherence to original plan]
- **Timeline Accuracy**: [Planned vs actual duration]
- **Collaboration Efficiency**: [Agent coordination efficiency]
- **Knowledge Transfer**: [Effectiveness of knowledge capture]

## Review and Approval

### Technical Review
- **Reviewer**: [Agent name]
- **Date**: [Review date]
- **Status**: [Approved/Needs revision/Rejected]
- **Comments**: [Review comments]

### Quality Review
- **Reviewer**: [Agent name]
- **Date**: [Review date]
- **Status**: [Approved/Needs revision/Rejected]
- **Comments**: [Review comments]

### Security Review
- **Reviewer**: [Agent name]
- **Date**: [Review date]
- **Status**: [Approved/Needs revision/Rejected]
- **Comments**: [Review comments]

---

## Appendix

### A. Command History
```bash
# Key commands executed during this wave
git log --oneline --grep="[TASK-ID]"
git diff --stat [commit-range]
python scripts/deploy_validation.sh
```

### B. Configuration Changes
```diff
# Key configuration changes
- old_setting=value
+ new_setting=value
```

### C. Performance Benchmarks
| Metric | Before | After | Change |
|--------|--------|-------|--------|
| [Metric 1] | [Value] | [Value] | [Delta] |
| [Metric 2] | [Value] | [Value] | [Delta] |

### D. Error Log Summary
- **Total Errors**: [Number]
- **Critical Errors**: [Number]
- **Warnings**: [Number]
- **Most Common Error**: [Error description]

---
**Document Status**: [Draft/Review/Approved/Final]
**Last Updated**: [YYYY-MM-DD HH:MM] by [Agent name]
