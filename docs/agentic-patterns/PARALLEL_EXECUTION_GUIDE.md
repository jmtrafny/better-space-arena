# Parallel Execution Technical Guide

Complete guide for executing agents in parallel using Claude Code's Task tool.

## Core Concept

Launch multiple agents simultaneously for concurrent execution instead of waiting for each to complete sequentially.

**Sequential:** Agent 1 → Agent 2 → Agent 3 = 90 min
**Parallel:** Agents 1, 2, 3 (all at once) = 30 min

**Time Saved:** 67%!

## Critical Rule: Single Message

✅ **CORRECT - All Task calls in ONE message:**
```
Launching 3 agents in parallel:
[Task 1]
[Task 2]
[Task 3]
```

❌ **INCORRECT - Separate messages:**
```
Launching agent 1: [Task 1]
(wait)
Launching agent 2: [Task 2]
```

**Why?** Claude Code processes all tool calls in a single message concurrently.

## Task Tool Syntax

```
Task(
    subagent_type="general-purpose",
    description="Brief 3-5 word task description",
    prompt="Detailed multi-line instructions...",
    model="sonnet"  # Optional
)
```

## Example: Parallel Architecture Design

```
I'm launching 3 architecture specialists concurrently:

[Task for Data Model Architect]
[Task for Simulation Architect]
[Task for Integration Architect]

All will execute in parallel.
```

## Best Practices

### 1. Clear Scopes
Each agent needs:
- Specific focus (no overlap)
- Sufficient context
- Clear boundaries
- Defined deliverable

### 2. Synthesis Plan
Before launching:
- How will results merge?
- What if they conflict?
- Who synthesizes?

### 3. Error Handling
- Some agents may fail
- Plan for partial results
- Have fallback strategy

## Synthesis After Parallel Execution

Use `/task-synthesizer` or `/parallel-coordinator` to merge results:

1. Review all outputs
2. Identify commonalities
3. Resolve conflicts
4. Create unified deliverable
5. Document decisions

## When to Parallelize

✅ **Good candidates:**
- Independent modules
- Different test suites
- Separate documentation types
- Research tasks
- Exploration phases

❌ **Avoid parallelizing:**
- Tightly coupled code
- Sequential dependencies
- Core integration work
- Single coherent vision needed

## Metrics to Track

- Time saved vs sequential
- Synthesis overhead
- Conflict rate
- Integration issues
- Quality comparison

## Common Pitfalls

1. **Too many agents:** Diminishing returns after 4-5
2. **Insufficient context:** Agents lack needed information
3. **Overlapping scopes:** Duplicate work
4. **Poor synthesis:** Conflicts not resolved
5. **Integration ignored:** Parallel code doesn't merge

## Advanced: Nested Parallelism

Coordinators can launch parallel agents:

```
Orchestrator
  ├→ Parallel Coordinator (Research)
  │    ├→ Agent A
  │    ├→ Agent B
  │    └→ Agent C
  └→ Parallel Coordinator (Design)
       ├→ Agent D
       ├→ Agent E
       └→ Agent F
```

## Success Criteria

Parallel execution succeeds when:
- ✅ Time saved > synthesis overhead
- ✅ Quality maintained or improved
- ✅ Integration relatively smooth
- ✅ Learning value high

## Quick Reference

| Situation | Parallel? | Why |
|-----------|-----------|-----|
| Research phase | ✅ Yes | Independent exploration |
| Architecture design | ✅ Yes | Different subsystems |
| Core integration | ❌ No | Everything connects |
| Feature development | ✅ Maybe | If features independent |
| Testing | ✅ Yes | Different test areas |
| Bug fixing | ✅ Maybe | If bugs independent |
| Documentation | ✅ Yes | Different doc types |

See `.claude/commands/patterns/parallel-workflow.md` for complete pattern details.
