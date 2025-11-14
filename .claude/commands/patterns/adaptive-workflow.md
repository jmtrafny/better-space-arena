---
description: Adaptive workflow pattern - dynamically chooses optimal strategy based on context
---

# Adaptive Workflow Pattern

This workflow pattern **intelligently adapts** based on the current context, choosing between sequential, parallel, or hybrid approaches depending on what's most appropriate for each phase.

## Pattern: Context-Aware Adaptation

```
Orchestrator (Analyzes context)
     ↓
Decision: What strategy for this phase?
     ├─→ High independence → Parallel
     ├─→ High interdependence → Sequential
     └─→ Mixed → Hybrid
     ↓
Execute chosen strategy
     ↓
Learn & adapt for next phase
```

## When to Use This Pattern

✅ **Use when:**
- Project has varying complexity across phases
- You want optimal strategy for each phase
- You're willing to make phase-by-phase decisions
- You want to learn what works best

✅ **Best for:** Experienced users, learning/experimentation

## Project Context

$ARGUMENTS

## Adaptive Decision Framework

### Decision Criteria

For each phase, evaluate:

#### 1. Task Independence
- **High (score: 3):** Tasks completely independent → **Parallel**
- **Medium (score: 2):** Some shared context → **Hybrid**
- **Low (score: 1):** Strong dependencies → **Sequential**

#### 2. Integration Complexity
- **Low (score: 3):** Easy to merge → **Parallel**
- **Medium (score: 2):** Moderate integration → **Hybrid**
- **High (score: 1):** Complex merging → **Sequential**

#### 3. Context Size
- **Small (score: 3):** Fits in prompt → **Parallel**
- **Medium (score: 2):** Manageable chunks → **Hybrid**
- **Large (score: 1):** Needs full context → **Sequential**

#### 4. Time Pressure
- **High (score: 3):** Speed critical → **Parallel**
- **Medium (score: 2):** Balanced → **Hybrid**
- **Low (score: 1):** Quality > speed → **Sequential**

#### 5. Convergence Need
- **Low (score: 3):** Multiple views OK → **Parallel**
- **Medium (score: 2):** Balanced → **Hybrid**
- **High (score: 1):** Need single vision → **Sequential**

### Decision Matrix

| Total Score | Strategy | Rationale |
|-------------|----------|-----------|
| 13-15 | **Parallel** | High independence, low integration cost |
| 9-12 | **Hybrid** | Mixed characteristics, balanced approach |
| 5-8 | **Sequential** | High dependencies, single coherent view needed |

## Adaptive Workflow Execution

### Phase 0: Initialization

**Analysis:**
- Task Independence: N/A (single task)
- Integration: N/A
- Context: Small
- Time: Low pressure
- Convergence: High (need single plan)

**Decision: SEQUENTIAL** (1 orchestrator task)

### Phase 1: Project Planning

**Analysis:**
- Task Independence: Low (1) - needs holistic view
- Integration: N/A
- Context: Large (1) - full requirements
- Time: Medium (2)
- Convergence: High (1) - need single plan

**Score: 5 → SEQUENTIAL**

**Execution:**
```
/project-manager Create comprehensive project plan
```

### Phase 2: Architecture Design

**Analysis:**
- Task Independence: High (3) - different subsystems
- Integration: Medium (2) - need unified design
- Context: Medium (2) - architecture constraints
- Time: High (3) - want multiple perspectives
- Convergence: Medium (2) - synthesize views

**Score: 12 → HYBRID**

**Execution:**
```python
# Launch 3 parallel architecture agents, then synthesize

Task 1: Data model architecture
Task 2: Simulation engine architecture
Task 3: Integration architecture

→ Synthesize into unified architecture document
```

### Phase 3: Core Development

**Analysis:**
- Task Independence: High (3) - separate modules
- Integration: Low (3) - clear interfaces
- Context: Small (3) - specific features
- Time: High (3) - want speed
- Convergence: Low (3) - modular OK

**Score: 15 → PARALLEL**

**Execution:**
```python
# Full parallel development of core systems

Task 1: Implement component system
Task 2: Implement data loader
Task 3: Implement validation
Task 4: Set up project structure

→ Integrate all modules
```

### Phase 4: Battle Engine Development

**Analysis:**
- Task Independence: Low (1) - core simulation loop
- Integration: High (1) - everything connects
- Context: Large (1) - needs full system understanding
- Time: Medium (2)
- Convergence: High (1) - single coherent engine

**Score: 6 → SEQUENTIAL**

**Execution:**
```
/developer Implement battle engine integrating all systems
```

### Phase 5: Testing

**Analysis:**
- Task Independence: High (3) - different test suites
- Integration: Low (3) - test reports merge easily
- Context: Medium (2) - specific areas
- Time: High (3) - want broad coverage fast
- Convergence: Low (3) - multiple reports OK

**Score: 14 → PARALLEL**

**Execution:**
```python
# Parallel testing across different areas

Task 1: Test core systems
Task 2: Test battle simulation
Task 3: Test determinism
Task 4: Test performance

→ Consolidate test reports
```

### Phase 6: Bug Fixing

**Analysis:**
- Task Independence: Medium (2) - some shared code
- Integration: Medium (2) - need conflict resolution
- Context: Small (3) - specific bugs
- Time: High (3) - fix fast
- Convergence: Medium (2) - merge fixes

**Score: 12 → HYBRID**

**Execution:**
```python
# Parallel fixes for independent bugs, sequential for related

Parallel: [Bug 1 in component system], [Bug 2 in CLI], [Bug 3 in data loader]
Sequential: [Bug 4 & 5 in battle engine - related]

→ Integrate and retest
```

### Phase 7: Documentation

**Analysis:**
- Task Independence: High (3) - different docs
- Integration: Medium (2) - need consistency
- Context: Medium (2) - system knowledge
- Time: High (3) - want complete docs fast
- Convergence: Medium (2) - unified style

**Score: 12 → HYBRID**

**Execution:**
```python
# Parallel doc creation, then organize

Task 1: Getting started guide
Task 2: API reference
Task 3: User guide
Task 4: Developer guide

→ Organize, cross-link, ensure consistency
```

## Adaptive Strategy Template

For each phase:

```markdown
## Phase N: [Phase Name]

### Context Analysis

**Task Independence:** [High/Medium/Low] (score)
- Reasoning: [Why?]

**Integration Complexity:** [Low/Medium/High] (score)
- Reasoning: [Why?]

**Context Size:** [Small/Medium/Large] (score)
- Reasoning: [Why?]

**Time Pressure:** [High/Medium/Low] (score)
- Reasoning: [Why?]

**Convergence Need:** [Low/Medium/High] (score)
- Reasoning: [Why?]

**Total Score:** [Sum]

### Strategy Decision

**Chosen Strategy:** [Sequential/Hybrid/Parallel]

**Rationale:** [Why this strategy fits the context]

### Execution Plan

[Specific execution approach using chosen strategy]

### Validation

[How to validate this phase]

### Learnings

[After phase completes, note what worked well and what didn't]
```

## Advantages of Adaptive Pattern

✅ **Optimized:** Each phase uses best strategy
✅ **Learning:** Understand what works where
✅ **Flexible:** Adapt to changing needs
✅ **Sophisticated:** Shows advanced understanding
✅ **Contextual:** Decisions based on reality, not dogma

## Challenges of Adaptive Pattern

⚠️ **Decision Overhead:** Need to analyze each phase
⚠️ **Requires Experience:** Need to make good choices
⚠️ **Variable Consistency:** Different phases use different patterns
⚠️ **More Complex:** Hardest pattern to execute

## Best Practices for Adaptive

### 1. Explicit Analysis

Always document your reasoning:
- Why you chose a particular strategy
- What factors were most important
- What alternatives you considered

### 2. Learn and Adjust

Track outcomes:
- Did the strategy work well?
- What would you do differently?
- Apply learnings to future phases

### 3. Default to Hybrid

When in doubt, use hybrid:
- Safe middle ground
- Good balance
- Hard to go wrong

### 4. Consider Constraints

Factor in real-world limits:
- API rate limits
- Token costs
- Time available
- Complexity tolerance

## Decision Shortcuts

### Fast Heuristics

**Use Parallel when:**
- Research/exploration phase
- Independent test suites
- Separate documentation types
- "Embarrassingly parallel" work

**Use Sequential when:**
- Core algorithm design
- Complex integration
- Need single coherent vision
- Learning new system

**Use Hybrid when:**
- Typical development work
- Balanced characteristics
- Unsure which is best

## Example: Adaptive Phase Transition

```markdown
## Phase 2 Complete: Architecture Design

**Strategy Used:** Hybrid
- 3 parallel architecture agents
- Synthesized into unified design

**Outcome:** ✅ Success
- Good diversity of ideas
- Synthesis took 10 minutes
- Final architecture is strong

**Learning:** Parallel architecture worked well. Consider full parallel for similar phases.

---

## Phase 3: Core Development

### Context Analysis

**Task Independence:** High (3)
- Component system, data loader, and CLI are separate modules
- Clear interfaces defined in architecture
- Minimal shared code

**Integration Complexity:** Low (3)
- Well-defined interfaces
- Each module has clear boundaries
- Integration should be straightforward

**Context Size:** Small (3)
- Each module is focused
- Architecture provides clear specifications
- Agents don't need full system context

**Time Pressure:** High (3)
- Weekend project, need speed
- Parallel will save significant time
- Can test integration separately

**Convergence Need:** Low (3)
- Modular design is fine
- Synthesis is just integration, not reconciliation
- Different coding styles OK if interfaces match

**Total Score:** 15

### Strategy Decision

**Chosen Strategy:** PARALLEL

**Rationale:** Perfect candidate for parallelism:
- Maximum independence
- Minimal integration complexity
- Speed boost will be significant
- Low risk

### Execution Plan

Launch 4 development agents in parallel:
1. Component system implementation
2. Data loader implementation
3. Validation utilities
4. Project structure & CLI skeleton

Then: Integrate, test, demo.
```

## Metrics to Track

For each phase, record:

| Phase | Strategy | Score | Time Saved | Quality | Issues | Notes |
|-------|----------|-------|------------|---------|--------|-------|
| Planning | Sequential | 5 | Baseline | ✅ | None | Clear plan |
| Architecture | Hybrid | 12 | ~30 min | ✅ | Minor conflicts | Good diversity |
| Core Dev | Parallel | 15 | ~1 hour | ✅ | Integration smooth | Perfect fit |
| Engine Dev | Sequential | 6 | N/A | ✅ | None | Needed coherence |
| Testing | Parallel | 14 | ~45 min | ✅ | None | Great coverage |

## Comparison with Other Patterns

| Aspect | Adaptive | Sequential | Parallel | Hybrid |
|--------|----------|------------|----------|--------|
| Optimization | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Simplicity | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| Learning Value | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Flexibility | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| Requires Experience | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐ | ⭐⭐ |

## Recommended Approach

1. **Start with Hybrid** for the project
2. **Switch to Adaptive** when you understand the patterns
3. **Document your decisions** and learnings
4. **Compare outcomes** across patterns

## Instructions for Using Adaptive Pattern

1. **At Each Phase:**
   - Analyze context using framework
   - Calculate score
   - Choose strategy
   - Document reasoning

2. **Execute Chosen Strategy:**
   - Follow pattern instructions
   - Track time and quality
   - Note issues

3. **Review After Phase:**
   - Did strategy work well?
   - What would you change?
   - Update strategy if needed

4. **Learn and Improve:**
   - Build intuition
   - Refine decision criteria
   - Share learnings

---

**Ready for adaptive workflow?** This pattern requires the most sophistication but provides the best learning experience and optimal results for each phase.
