# Multi-Agent Development System

A sophisticated multi-agent orchestration system for Claude Code, featuring parallel execution, multiple workflow patterns, and advanced coordination strategies.

> **Ready to use:** A clean, domain-agnostic multi-agent framework for any software development project.

## Overview

This repository provides a complete **multi-agent development framework** that allows you to:

- 🚀 **Execute agents in parallel** for 40-75% faster development
- 🎯 **Choose optimal workflow patterns** (Sequential, Parallel, Hybrid, Adaptive)
- 🤝 **Coordinate specialized agents** for complex projects
- 📊 **Track metrics** to optimize your workflow
- 🔄 **Synthesize results** from concurrent agent work

## Quick Start

### 1. Use the Enhanced Orchestrator

```bash
/orchestrator-v2 <your-requirements-file.md>
```

The orchestrator will:
1. Analyze your project characteristics
2. Recommend the best workflow pattern
3. Launch agents (in parallel when beneficial)
4. Synthesize results and manage human validation gates
5. Track time saved and quality metrics

### 2. Choose Your Workflow Pattern

| Pattern | Best For | Speed | Complexity | Time Savings |
|---------|----------|-------|------------|--------------|
| **Sequential** | Learning, high dependencies | ⭐⭐ | ⭐ Easy | Baseline |
| **Parallel** | Research, maximum speed | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ Complex | 60-75% |
| **Hybrid** | Most projects (RECOMMENDED) | ⭐⭐⭐⭐ | ⭐⭐⭐ Moderate | 40-50% |
| **Adaptive** | Experienced users | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ Very Complex | 50-60% |

**Not sure?** Start with **Hybrid** - it provides the best balance.

## Available Agents

### Core Agents

Located in `.claude/commands/`:

- **`orchestrator-v2.md`** - Enhanced orchestrator with parallel execution
- **`architect.md`** - System design and architecture
- **`developer.md`** - Code implementation
- **`qa-tester.md`** - Quality assurance and testing
- **`documentation.md`** - Technical writing
- **`project-manager.md`** - Planning and coordination

### Workflow Patterns

Located in `.claude/commands/patterns/`:

- **`sequential-workflow.md`** - Traditional waterfall approach
- **`parallel-workflow.md`** - Maximum concurrency
- **`hybrid-workflow.md`** - Sequential phases, parallel tasks
- **`adaptive-workflow.md`** - Dynamic per-phase optimization

### Coordinators

Located in `.claude/commands/coordinators/`:

- **`parallel-coordinator.md`** - Manages concurrent agents
- **`task-synthesizer.md`** - Merges parallel outputs

## Documentation

### Getting Started

- **`HOW_TO_USE_MULTI_AGENT.md`** - Complete usage guide
- **`docs/agentic-patterns/WHEN_TO_USE_WHAT.md`** - Pattern selection guide
- **`docs/agentic-patterns/PARALLEL_EXECUTION_GUIDE.md`** - Parallel execution details

### Advanced Topics

- **`docs/agentic-patterns/AGENTIC_PATTERNS.md`** - Comprehensive pattern guide

## Example Usage

### Sequential Pattern (Simple)

```bash
/orchestrator-v2 my-project-requirements.md
```

Select "Sequential" when prompted. Agents run one at a time.

### Hybrid Pattern (Recommended)

```bash
/orchestrator-v2 my-project-requirements.md
```

Select "Hybrid" when prompted. Sequential phases with parallel tasks:

```
Phase 1: Planning (Sequential)
    ↓
Phase 2: Architecture (PARALLEL)
    ├─→ Data Model Agent
    ├─→ API Design Agent
    └─→ Integration Agent
    ↓ [Synthesis]
    ↓ [Human Gate]
Phase 3: Development (PARALLEL)
    ├─→ Feature A Agent
    ├─→ Feature B Agent
    └─→ Feature C Agent
    ↓ [Integration]
```

### Parallel Pattern (Maximum Speed)

```bash
/orchestrator-v2 my-project-requirements.md
```

Select "Parallel" for maximum speed. All independent work runs concurrently.

## Workflow Patterns in Detail

### Sequential Pattern

**Best for:** Learning, highly coupled systems, simple projects

**How it works:** Agents run one at a time in waterfall fashion

**Time:** Baseline (100%)

### Parallel Pattern

**Best for:** Research, exploration, independent features

**How it works:** All agents run concurrently, then synthesize

**Time:** ~25-40% of sequential (60-75% faster)

### Hybrid Pattern (RECOMMENDED)

**Best for:** Most real-world projects

**How it works:** Sequential phases, parallel tasks within each phase

**Time:** ~50-60% of sequential (40-50% faster)

**Example:**
```
Sequential: 10 hours
Hybrid: 5-6 hours (save 4-5 hours)
Parallel: 2.5-4 hours (save 6-7.5 hours, but harder to manage)
```

### Adaptive Pattern

**Best for:** Experienced users wanting per-phase optimization

**How it works:** Chooses best strategy for each phase dynamically

**Time:** ~40-50% of sequential (50-60% faster)

## Human Validation Gates

The system includes human validation checkpoints:

```markdown
🚦 HUMAN VALIDATION REQUIRED

Phase: Architecture
Pattern Used: Hybrid
What Needs Approval: System design

Summary:
- Designed data model
- Defined API interfaces
- Created integration architecture

Deliverables:
- [Link to architecture doc]

To Proceed:
- ✅ Approved - continue
- 📝 Feedback - [adjustments needed]
- ❌ Rejected - [concerns]
```

## Metrics Tracking

The orchestrator tracks:

| Metric | Purpose |
|--------|---------|
| Time Saved | ROI of parallel execution |
| Synthesis Effort | Coordination overhead |
| Quality | Bug count, rework needed |
| Agent Failures | Reliability tracking |
| Pattern Switches | Pattern fit assessment |

## Customization

### Create Your Own Agent

1. Create a new file in `.claude/commands/`:

```bash
touch .claude/commands/my-custom-agent.md
```

2. Follow the template structure:

```markdown
---
description: Brief description of agent role
---

# Agent Name

You are a **[Role]** for [project type].

## Your Responsibilities

- Responsibility 1
- Responsibility 2

## Instructions

Step-by-step instructions for the agent...

## Output Format

Expected deliverables...
```

3. Invoke your custom agent:

```bash
/my-custom-agent <context>
```

### Create Your Own Workflow Pattern

1. Create a new file in `.claude/commands/patterns/`:

```bash
touch .claude/commands/patterns/my-pattern.md
```

2. Define the workflow structure
3. Reference it in your orchestrator calls

## Best Practices

### When to Use Parallel Execution

✅ **Good candidates for parallel:**
- Independent features
- Different architectural areas
- Separate test suites
- Different documentation types

❌ **Poor candidates for parallel:**
- Tightly coupled code
- Core engine/kernel
- Sequential algorithms
- Single coherent document

### Synthesis Tips

When merging parallel work:

1. Review all outputs thoroughly
2. Resolve conflicts with clear rationale
3. Document integration decisions
4. Test integrated result

### Human Gate Guidelines

Place validation gates at:
- Phase boundaries
- Before irreversible decisions
- After parallel synthesis
- Major deliverables

## Troubleshooting

### Issue: Parallel agents conflict

**Solution:** Use task-synthesizer or switch to hybrid/sequential pattern

### Issue: Synthesis takes too long

**Solution:** Reduce number of parallel agents or provide clearer specifications

### Issue: Pattern not working

**Solution:** Switch patterns mid-project (it's okay!)

## Contributing

This multi-agent system is designed to be extended. Contributions welcome:

1. New agent types
2. New workflow patterns
3. New coordinators
4. Documentation improvements
5. Example projects

## License

[Specify your license]

## Credits

Built using Claude Code's multi-agent capabilities with the Task tool for parallel execution.

---

**Ready to build something?**

```bash
/orchestrator-v2 your-project-requirements.md
```
