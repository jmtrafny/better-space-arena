---
description: Parallel workflow pattern - maximize speed through concurrent agent execution
---

# Parallel Workflow Pattern

This workflow pattern demonstrates **maximum parallelism** using the Task tool to launch multiple agents concurrently. This is the fastest approach but requires careful coordination.

## Pattern: Fork-Join Parallelism

```
Orchestrator
     ├─→ [Agent 1] ─┐
     ├─→ [Agent 2] ─┤
     ├─→ [Agent 3] ─┼─→ Synthesize → Next Phase
     └─→ [Agent N] ─┘
```

## When to Use This Pattern

✅ **Use when:**
- Tasks are independent and can run concurrently
- Speed is critical
- Tasks don't depend on each other's outputs
- You can synthesize multiple perspectives

❌ **Avoid when:**
- Tasks have sequential dependencies
- Coordination overhead outweighs speed gains
- You need one canonical answer (not multiple perspectives)
- Context is too large for multiple agents

## Project Context

$ARGUMENTS

## Parallel Workflow Phases

### Phase 1: Parallel Research & Analysis

**Launch concurrent research agents:**

Use the Task tool to launch multiple agents in a **single message**:

```python
# In one message, launch all research agents:
Task(subagent_type="general-purpose",
     description="Research Space Arena mechanics",
     prompt="Research Space Arena gameplay mechanics, combat systems, and component design...")

Task(subagent_type="general-purpose",
     description="Research similar games",
     prompt="Research similar games: Gratuitous Space Battles, From the Depths, etc...")

Task(subagent_type="general-purpose",
     description="Research Python simulation libraries",
     prompt="Research Python libraries for game simulation, physics, and deterministic systems...")

Task(subagent_type="general-purpose",
     description="Analyze component-based architectures",
     prompt="Research component-based entity systems, ECS patterns, and modular design...")
```

**Then synthesize:** Combine findings into comprehensive research report.

### Phase 2: Parallel Architecture Design

**Launch specialized architecture agents:**

```python
# Launch 4 architecture sub-agents in parallel:
Task(subagent_type="general-purpose",
     description="Design data models",
     prompt="You are an architect specializing in data modeling. Design the complete data schema for components, units, and battles...")

Task(subagent_type="general-purpose",
     description="Design simulation engine",
     prompt="You are an architect specializing in simulation systems. Design the battle simulation algorithm, turn processing, and deterministic execution...")

Task(subagent_type="general-purpose",
     description="Design API interfaces",
     prompt="You are an architect specializing in API design. Design the public APIs for the engine, including interfaces for all major systems...")

Task(subagent_type="general-purpose",
     description="Design deployment architecture",
     prompt="You are an architect specializing in deployment. Design the project structure, build system, CLI interface, and distribution...")
```

**Then synthesize:** Merge into unified architecture document.

**HUMAN GATE:** Present synthesized architecture.

### Phase 3: Parallel Feature Development

**Launch feature teams concurrently:**

```python
# Launch parallel development agents:
Task(subagent_type="general-purpose",
     description="Implement component system",
     prompt="Implement the component system per architecture: Component class, loading from JSON, validation, type system...")

Task(subagent_type="general-purpose",
     description="Implement unit builder",
     prompt="Implement the unit building system: Unit class, component placement, resource constraints, validation...")

Task(subagent_type="general-purpose",
     description="Implement battle simulator",
     prompt="Implement the battle simulation engine: Battle initialization, turn processing, event logging...")

Task(subagent_type="general-purpose",
     description="Implement data loader",
     prompt="Implement data loading utilities: JSON/YAML parsing, schema validation, theme loading...")
```

**Then integrate:** Merge code, resolve conflicts, ensure cohesion.

### Phase 4: Parallel Testing

**Launch testing agents across different areas:**

```python
# Launch parallel QA agents:
Task(subagent_type="general-purpose",
     description="Test component system",
     prompt="Test the component system thoroughly: loading, validation, edge cases, error handling...")

Task(subagent_type="general-purpose",
     description="Test combat mechanics",
     prompt="Test battle simulation: movement, targeting, damage, win conditions...")

Task(subagent_type="general-purpose",
     description="Test determinism",
     prompt="Test deterministic behavior: same seeds produce same results, replay accuracy...")

Task(subagent_type="general-purpose",
     description="Test performance",
     prompt="Test performance: battle speed, memory usage, large unit handling...")
```

**Then consolidate:** Create unified bug report and test summary.

### Phase 5: Parallel Documentation

**Launch documentation agents for different audiences:**

```python
# Launch parallel documentation agents:
Task(subagent_type="general-purpose",
     description="Write user guide",
     prompt="Create comprehensive user guide: getting started, building units, running battles...")

Task(subagent_type="general-purpose",
     description="Write API reference",
     prompt="Create complete API reference documentation for all public interfaces...")

Task(subagent_type="general-purpose",
     description="Create examples",
     prompt="Create working examples: simple battles, custom components, new themes...")

Task(subagent_type="general-purpose",
     description="Write developer guide",
     prompt="Create developer guide: architecture overview, extending the engine, contributing...")
```

**Then organize:** Structure docs, ensure consistency, cross-link.

## Coordination Strategy

### 1. Launch in Parallel

Use **single message with multiple Task calls**:

```markdown
I'm launching 4 architecture agents in parallel to design different aspects of the system:

[Task 1: Data Model Design]
[Task 2: Simulation Engine Design]
[Task 3: API Design]
[Task 4: Deployment Architecture]

All agents will work concurrently. I'll synthesize their outputs when complete.
```

### 2. Wait for All Completions

Each Task tool call will return when its agent completes. Process all results.

### 3. Synthesize Results

Combine outputs into coherent whole:
- Identify overlaps and conflicts
- Merge compatible approaches
- Resolve contradictions
- Create unified deliverable

### 4. Validate & Proceed

Present synthesized result at human gate, then continue to next phase.

## Advantages of This Pattern

✅ **Speed:** Massive time savings through parallelism
✅ **Diversity:** Multiple perspectives and approaches
✅ **Robustness:** If one agent struggles, others may succeed
✅ **Coverage:** Broad exploration of solution space
✅ **Learning:** See different approaches to same problem

## Challenges of This Pattern

⚠️ **Coordination Overhead:** Synthesis takes effort
⚠️ **Potential Conflicts:** Agents may propose incompatible solutions
⚠️ **Context Management:** Agents don't see each other's work
⚠️ **Integration Complexity:** Merging parallel work can be tricky
⚠️ **Cost:** More agents = more API calls

## Best Practices

### 1. Clear Agent Prompts

Each parallel agent needs:
- **Specific scope:** "Design ONLY the data model"
- **Context:** Relevant architecture constraints
- **Format:** Expected output structure
- **Boundaries:** What NOT to include

### 2. Synthesis Phase

After parallel execution:
- Review all outputs thoroughly
- Identify commonalities
- Resolve conflicts through reasoned choice
- Create coherent unified result
- Document synthesis decisions

### 3. Human Validation

Always pause for human review:
- Present synthesized result
- Explain key decisions made during synthesis
- Highlight areas of agent disagreement
- Get approval before proceeding

### 4. Fault Tolerance

Plan for agent failures:
- Some agents may not complete successfully
- Synthesis should handle partial results
- Have fallback strategies
- Don't block entire workflow on one agent

## Example: Parallel Architecture Phase

```markdown
## Phase 2: Parallel Architecture Design

I'm launching 4 specialized architecture agents to design different aspects concurrently:

**Agent 1: Data Model Architecture**
Scope: Design component, unit, and battle data schemas
Focus: JSON structures, validation rules, relationships

**Agent 2: Simulation Engine Architecture**
Scope: Design battle simulation algorithm and mechanics
Focus: Turn processing, deterministic execution, event logging

**Agent 3: API Design**
Scope: Design public interfaces for all major systems
Focus: Function signatures, contracts, extension points

**Agent 4: Deployment Architecture**
Scope: Design project structure and distribution
Focus: Directory layout, CLI, build system, packaging

[Launches all 4 agents in parallel using Task tool]

... agents execute concurrently ...

**Synthesis:**
All agents have completed. Synthesizing outputs:

1. Data Model (Agent 1): Proposes JSON schema with validation
2. Simulation (Agent 2): Proposes turn-based with 0.1s steps
3. API (Agent 3): Proposes class-based with clear interfaces
4. Deployment (Agent 4): Proposes Python package with CLI

**Unified Architecture:**
[Creates single coherent architecture document merging all designs]

**HUMAN GATE:** Please review the synthesized architecture.
```

## Metrics to Track

When using this pattern, track:

- **Time Saved:** Compare to sequential execution
- **Synthesis Effort:** How long to merge results?
- **Conflict Rate:** How often do agents disagree?
- **Quality:** Is parallel result better/worse than sequential?
- **Cost:** Total tokens/API calls vs sequential

## When This Pattern Shines

This pattern works best for:

✨ **Exploration Phase:** Research and discovery
✨ **Design Phase:** Multiple architectural approaches
✨ **Testing Phase:** Independent test suites
✨ **Documentation Phase:** Different doc types
✨ **Code Review:** Multiple reviewers simultaneously

## Instructions for Using This Pattern

1. **Identify Parallelizable Work**
   - Break phase into independent tasks
   - Ensure tasks don't depend on each other
   - Define clear scope for each

2. **Prepare Agent Prompts**
   - Write specific, focused prompts
   - Include necessary context
   - Define expected outputs

3. **Launch in Parallel**
   - Use single message
   - Multiple Task tool calls
   - All agents start simultaneously

4. **Monitor Progress**
   - Agents return when complete
   - Review each output
   - Note any failures

5. **Synthesize Results**
   - Combine outputs coherently
   - Resolve conflicts
   - Create unified deliverable

6. **Validate & Continue**
   - Human review and approval
   - Proceed to next phase

## Comparison with Other Patterns

| Aspect | Parallel | Sequential | Hybrid |
|--------|----------|------------|--------|
| Speed | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐ |
| Simplicity | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Coordination | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Diversity | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| Cost | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |

## Next Steps

After completing a phase with this pattern:
1. Review synthesis quality
2. Track metrics
3. Decide if pattern worked well
4. Consider switching patterns if needed

Remember: **Parallel is not always better.** Use when the benefits outweigh the coordination overhead.

---

**Ready to execute parallel workflow?** The orchestrator will coordinate all parallel agents and synthesize their results.
