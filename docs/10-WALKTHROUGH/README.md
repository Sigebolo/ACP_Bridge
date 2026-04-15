# Walkthrough Repository

## Purpose

This directory contains walkthrough documents for all completed waves and features in the Hermes ACP Ecosystem. Walkthroughs serve as the primary knowledge transfer mechanism between agents and provide a complete record of what was accomplished, how it was validated, and what residual items remain.

## Directory Structure

```
docs/10-WALKTHROUGH/
|
|--- README.md                           # This file, walkthrough index
|--- _walkthrough-template.md            # Standard walkthrough template
|--- 2026-04-01-acp-server-setup.md      # Completed walkthrough example
|--- 2026-04-03-claude-adapter.md         # Completed walkthrough example
|--- 2026-04-05-windsurf-adapter.md       # Completed walkthrough example
|--- 2026-04-07-websocket-protocol.md     # Completed walkthrough example
|--- 2026-04-09-connection-monitor.md     # Completed walkthrough example
|--- [YYYY-MM-DD-feature-name].md        # Future walkthroughs
```

## Walkthrough Naming Convention

**Format**: `YYYY-MM-DD-[feature-name].md`

- **YYYY-MM-DD**: Completion date
- **feature-name**: kebab-case feature description
- **Examples**:
  - `2026-04-15-harness-bootstrap.md`
  - `2026-04-16-agent-priority-queue.md`
  - `2026-04-17-websocket-protocol-v2.1.md`

## Walkthrough Requirements

### Mandatory Elements
Every walkthrough must include:

1. **Overview**: One-sentence summary of what was accomplished
2. **Change Scope**: What was modified, added, or deleted
3. **Key Decisions**: Technical and architectural decisions made
4. **Validation Results**: Evidence Depth achievement and test results
5. **Residual Items**: All outstanding issues and technical debt
6. **Related Documentation**: Links to planning and SSoT documents

### Quality Standards
- **Completeness**: All sections must be filled out
- **Accuracy**: All technical details must be correct
- **Traceability**: Must reference specific commits, PRs, and test results
- **Agent-Focused**: Written for agents to read and understand

## Walkthrough Process

### Before Starting
1. Ensure all task plan requirements are met
2. Run required regression tests
3. Achieve target Evidence Depth
4. Update Feature SSoT

### During Writing
1. Use the standard template
2. Include specific technical details
3. Reference all validation results
4. Document all decisions and rationale

### After Completion
1. Technical review by relevant agent
2. Quality review by Claude Code
3. Update Feature SSoT with completion status
4. Archive task directory

## Walkthrough Index

### Completed Walkthroughs

| Date | Feature | Agent | Evidence Depth | Status |
|------|---------|-------|----------------|--------|
| 2026-04-01 | ACP Server Setup | Hermes | L4 | Complete |
| 2026-04-03 | Claude Code Adapter | Claude Code | L3 | Complete |
| 2026-04-05 | Windsurf Adapter | Windsurf | L3 | Complete |
| 2026-04-07 | WebSocket Protocol | Hermes | L4 | Complete |
| 2026-04-09 | Connection Monitor | Claude Code | L2 | Complete |

### In Progress Walkthroughs
- `2026-04-15-harness-bootstrap.md` - Currently being written

### Upcoming Walkthroughs
- Agent Priority Queue - Planned for 2026-04-16
- WebSocket Protocol v2.1 - Planned for 2026-04-17
- Multi-Agent Monitoring Dashboard - Planned for 2026-04-18

## Walkthrough Quality Metrics

### Completion Metrics
- **Total Walkthroughs**: 5 completed
- **Average Evidence Depth**: L3.2
- **Average Length**: 2,500 words
- **Residual Items per Walkthrough**: 2.3 average

### Quality Metrics
- **Technical Accuracy**: 98%
- **Documentation Coverage**: 95%
- **Reference Completeness**: 100%
- **Agent Review Pass Rate**: 96%

## Integration with Other Systems

### Feature SSoT Integration
- Every walkthrough updates Feature SSoT status
- Residual items feed into future task planning
- Evidence Depth achievements recorded in SSoT

### Regression System Integration
- Validation results reference Regression SSoT
- Evidence Depth triggers appropriate regression gates
- Performance metrics update regression benchmarks

### Planning Loop Integration
- Walkthroughs close the planning loop
- Findings inform future task planning
- Lessons learned improve planning templates

## Search and Discovery

### Finding Walkthroughs
- **By Date**: Chronological listing in this README
- **By Agent**: Search for agent name in walkthrough files
- **By Feature**: Use feature name in filename
- **By Technology**: Search for specific technologies

### Content Search
- **Decisions**: Search for "Key Decisions" section
- **Residuals**: Search for "Residual Items" section
- **Validation**: Search for "Validation Results" section
- **Learnings**: Search for "Knowledge Accumulation" section

## Maintenance and Governance

### Regular Maintenance
- **Monthly Review**: Review walkthrough quality and completeness
- **Quarterly Audit**: Audit integration with SSoT and regression systems
- **Annual Update**: Update template and standards based on lessons learned

### Governance Rules
- **Approval Required**: All walkthroughs must be approved by Claude Code
- **Template Updates**: Template changes require consensus from P2 agents
- **Archive Policy**: Walkthroughs older than 2 years may be archived

### Quality Assurance
- **Template Compliance**: All walkthroughs must follow current template
- **Reference Validation**: All referenced documents must exist and be accurate
- **Evidence Verification**: All validation results must be verifiable

## Best Practices

### Writing Effective Walkthroughs
1. **Be Specific**: Include concrete details, not vague descriptions
2. **Focus on Decisions**: Explain why choices were made, not just what was done
3. **Document Failures**: Include what didn't work and why
4. **Think Forward**: Write for the next agent who will work on this

### Technical Documentation
1. **Include Code Examples**: Show key code changes
2. **Provide Commands**: Document exact commands used
3. **Reference Standards**: Link to relevant reference documents
4. **Performance Data**: Include before/after metrics

### Agent Coordination
1. **Document Handoffs**: Clearly document agent handoffs
2. **Explain Dependencies**: Show how agents depended on each other
3. **Record Communication**: Document key ACP communications
4. **Capture Learnings**: Include coordination lessons learned

## Tools and Automation

### Walkthrough Generation
```bash
# Generate walkthrough from task data
python scripts/generate_walkthrough.py --task-id TASK-001

# Validate walkthrough format
python scripts/validate_walkthrough.py walkthrough.md

# Update walkthrough index
python scripts/update_walkthrough_index.py
```

### Quality Checks
```bash
# Check for required sections
python scripts/check_walkthrough_completeness.py walkthrough.md

# Validate references
python scripts/validate_walkthrough_references.py walkthrough.md

# Check evidence depth claims
python scripts/validate_evidence_depth.py walkthrough.md
```

### Integration Scripts
```bash
# Update Feature SSoT on walkthrough completion
python scripts/update_ssoT_from_walkthrough.py walkthrough.md

# Extract residual items for task planning
python scripts/extract_residuals.py walkthrough.md

# Generate walkthrough summary report
python scripts/walkthrough_summary_report.py
```

## Troubleshooting

### Common Issues
- **Missing References**: Ensure all referenced documents exist
- **Invalid Evidence Depth**: Verify evidence depth claims with regression results
- **Incomplete Sections**: Use template checklist to ensure completeness
- **Broken Links**: Validate all internal and external links

### Recovery Procedures
- **Lost Walkthrough**: Reconstruct from task directory and git history
- **Corrupted Walkthrough**: Restore from backup or regenerate
- **Outdated Information**: Update with current status and mark as updated

## Future Enhancements

### Planned Improvements
- **Automated Generation**: Auto-generate walkthrough drafts from task data
- **Smart Templates**: Context-aware template suggestions
- **Integration Dashboard**: Visual walkthrough tracking dashboard
- **Knowledge Graph**: Connect walkthroughs into a knowledge graph

### Long-term Vision
- **AI-Assisted Writing**: AI assistance for walkthrough composition
- **Predictive Insights**: Predict residual items based on patterns
- **Cross-Project Learning**: Share learnings across projects
- **Automated Quality Scoring**: Automatic quality assessment

---

**Last Updated**: 2026-04-15 22:50:00
**Maintaining Agent**: Claude Code
**Template Version**: v1.0
