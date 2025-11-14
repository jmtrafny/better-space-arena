## Agentic Patterns - Complete Guide

This guide explains the four multi-agent workflow patterns available in this project, when to use them, and what you'll learn from each.

## Overview

An **agentic pattern** is a strategy for coordinating multiple AI agents to accomplish complex tasks. Different patterns make different trade-offs between simplicity, speed, and coordination overhead.

### The Four Patterns

| Pattern | Best For | Speed | Complexity | Learning Value |
|---------|----------|-------|------------|----------------|
| **Sequential** | First-timers, high dependencies | ⭐⭐ | ⭐ | ⭐⭐⭐ |
| **Parallel** | Research, independent tasks | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Hybrid** | Most projects | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Adaptive** | Experienced users | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## Pattern 1: Sequential Workflow

### Concept

Traditional waterfall approach where each agent completes before the next begins.

```
Orchestrator → PM → Architect → Developer → QA → Documentation → Delivery
    (wait)     (wait)   (wait)     (wait)   (wait)    (wait)
```

### When to Use

✅ **Use Sequential when:**
- First time using multi-agent systems
- Each phase heavily depends on previous
- Need simple, clear progression
- Learning the workflow
- Debugging issues

### Example Flow

```markdown
1. /project-manager prompt.md
   [Wait for completion, review plan]
   ✅ Approve

2. /architect Design system per approved plan
   [Wait for completion, review architecture]
   ✅ Approve

3. /developer Implement core systems per architecture
   [Wait for completion]

4. /qa-tester Test implementation
   [Wait for completion, fix bugs if found]
   ✅ Demo

5. Continue through all phases...
```

### Advantages

- ⭐⭐⭐⭐⭐ **Simplicity:** Easy to understand
- ⭐⭐⭐⭐⭐ **Predictability:** Know what's next
- ⭐⭐⭐⭐⭐ **Clear Gates:** Natural validation points
- ⭐⭐⭐⭐ **Single Context:** Full context from previous work

### Disadvantages

- ❌ **Slow:** No parallelism, ~50-100% longer
- ❌ **Idle Time:** Lots of waiting
- ❌ **Single View:** Miss diverse perspectives

### Key Learning

**What you'll learn:**
- How agents hand off work
- How context flows through workflow
- How to validate at gates
- Basics of agent coordination

**Professional Value:**
Understanding sequential workflow is foundational. Most real projects have some sequential dependencies, so this pattern teaches you to identify them.

---

## Pattern 2: Parallel Workflow

### Concept

Maximum parallelism - launch multiple agents concurrently, then synthesize results.

```
Orchestrator
     ├─→ [Agent 1] ─┐
     ├─→ [Agent 2] ─┤
     ├─→ [Agent 3] ─┼─→ Synthesize → Next Phase
     └─→ [Agent N] ─┘
```

### When to Use

✅ **Use Parallel when:**
- Tasks are truly independent
- Speed is critical
- Research/exploration phase
- Want diverse perspectives
- Can synthesize multiple views

### Example Flow

```markdown
## Phase 2: Architecture (Parallel)

Launching 4 architecture agents in parallel:

Task(description="Design data models",
     prompt="Design user, product, order schemas...")

Task(description="Design business logic",
     prompt="Design order processing algorithm...")

Task(description="Design APIs",
     prompt="Design public interfaces...")

Task(description="Design deployment",
     prompt="Design project structure, CLI...")

[All 4 execute concurrently]

Synthesize into unified architecture document.
```

### Advantages

- ⭐⭐⭐⭐⭐ **Speed:** Massive time savings (50-75%)
- ⭐⭐⭐⭐⭐ **Diversity:** Multiple perspectives
- ⭐⭐⭐⭐ **Robustness:** If one fails, others may succeed
- ⭐⭐⭐⭐ **Coverage:** Broad exploration

### Disadvantages

- ❌ **Synthesis Overhead:** Merging results takes effort
- ❌ **Potential Conflicts:** May propose incompatible solutions
- ❌ **Integration Complexity:** Parallel code can be tricky to merge
- ❌ **Cost:** More agents = more API calls

### Key Learning

**What you'll learn:**
- Using Task tool for parallel execution
- Synthesizing diverse outputs
- Resolving conflicts between agents
- Managing coordination overhead

**Professional Value:**
Parallel execution is crucial for modern AI systems. Learning to coordinate multiple LLM calls and synthesize results is a highly valuable skill for AI-powered applications.

### Technical Details

**Launching Agents in Parallel:**

Must use **single message** with multiple `Task` tool calls:

```python
# CORRECT: All in one message
Task(...Agent 1...)
Task(...Agent 2...)
Task(...Agent 3...)

# INCORRECT: Separate messages
Task(...Agent 1...)
# then later:
Task(...Agent 2...)
```

**Why?** Claude Code processes all Tool calls in a single message concurrently.

---

## Pattern 3: Hybrid Workflow

### Concept

Best of both worlds: sequential phases for clear progression, parallel execution within phases for speed.

```
Phase 1: Planning (Sequential)
    ↓
Phase 2: Architecture (Parallel within phase)
    ├─→ [Data Model] ─┐
    ├─→ [Simulation]  ├─→ Synthesize
    └─→ [API Design]  ┘
    ↓ (Human Gate)
Phase 3: Development (Parallel within phase)
    ├─→ [Feature A] ─┐
    ├─→ [Feature B] ─┼─→ Integrate
    └─→ [Feature C] ─┘
    ↓
...
```

### When to Use

✅ **Use Hybrid when:**
- Most typical projects (RECOMMENDED)
- Want clear phase progression
- Some work within phases can parallelize
- Want good speed without overwhelming complexity
- Balanced priorities

### Example Flow

```markdown
## Phase 1: Planning (Sequential)
/project-manager Create comprehensive plan
✅ Human approval

## Phase 2: Architecture (PARALLEL)
Launch 3 parallel architecture agents:
- Data Model specialist
- Simulation specialist
- Integration specialist

Synthesize into unified architecture.
✅ Human approval

## Phase 3: Dev Iteration 1 (PARALLEL)
Launch 3 parallel developers:
- Component system
- Data loader
- Project infrastructure

Integrate code, test integration.

QA tests (sequential after dev).
✅ Human demo

## Phase 4: Dev Iteration 2 (PARALLEL)
[Continue similar pattern...]
```

### Advantages

- ⭐⭐⭐⭐ **Speed:** 40-60% time savings
- ⭐⭐⭐⭐ **Clear Progression:** Sequential phases easy to follow
- ⭐⭐⭐⭐⭐ **Natural Gates:** Phase boundaries for validation
- ⭐⭐⭐ **Manageable Complexity:** Simpler than full parallel
- ⭐⭐⭐⭐⭐ **Best Balance:** Optimal for most projects

### Disadvantages

- ⚠️ **Some Synthesis:** Still need to merge parallel work
- ⚠️ **Integration Points:** Parallel code must merge cleanly
- ⚠️ **Planning Needed:** Must identify what can parallelize

### Key Learning

**What you'll learn:**
- When to parallelize vs stay sequential
- Phase boundaries as validation gates
- Integration strategies for parallel work
- Balancing speed and simplicity

**Professional Value:**
This is the most practical pattern for real-world projects. You'll learn to identify when parallelism helps vs when it adds overhead - a critical judgment skill.

---

## Pattern 4: Adaptive Workflow

### Concept

Dynamically choose the best strategy for each phase based on context analysis.

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

### When to Use

✅ **Use Adaptive when:**
- Experienced with other patterns
- Want optimal strategy per phase
- Learning and experimentation goals
- Willing to analyze each phase
- Variable project characteristics

### Example Flow

```markdown
## Phase 1: Planning

Context Analysis:
- Task Independence: Low (need holistic view)
- Integration: N/A
- Context: Large
- Score: 5 → SEQUENTIAL

Execute: /project-manager

Retrospective: Sequential was right choice.

---

## Phase 2: Architecture

Context Analysis:
- Task Independence: High (different subsystems)
- Integration: Medium (need synthesis)
- Context: Medium
- Score: 12 → HYBRID

Execute: Parallel arch agents, synthesize.

Retrospective: Saved 45 min, synthesis took 15 min.
Net gain: 30 min. Good choice!

---

## Phase 3: Core Development

Context Analysis:
- Task Independence: Very high
- Integration: Low (clear interfaces)
- Context: Small
- Score: 15 → PARALLEL

Execute: 4 parallel developers, integrate.

Retrospective: Saved 1 hour, smooth integration.
Excellent choice!

---

[Adapt strategy for each subsequent phase...]
```

### Advantages

- ⭐⭐⭐⭐⭐ **Optimized:** Best strategy per phase
- ⭐⭐⭐⭐⭐ **Learning:** Understand what works where
- ⭐⭐⭐⭐⭐ **Flexible:** Adapt to changing needs
- ⭐⭐⭐⭐ **Sophisticated:** Advanced coordination

### Disadvantages

- ❌ **Decision Overhead:** Must analyze each phase
- ❌ **Requires Experience:** Need good judgment
- ❌ **Variable Consistency:** Different phases use different patterns
- ❌ **Most Complex:** Hardest to execute well

### Key Learning

**What you'll learn:**
- Context-aware decision making
- Trade-off analysis for patterns
- When each pattern shines
- Building intuition for coordination

**Professional Value:**
This teaches meta-skills: how to choose the right tool for the job. In professional settings, you'll need to make these judgment calls constantly. This pattern builds that intuition.

### Decision Framework

For each phase, score these criteria (1-3):

| Criteria | Low (1) | Medium (2) | High (3) |
|----------|---------|------------|----------|
| Task Independence | Sequential dependencies | Some shared context | Fully independent |
| Integration Complexity | Hard to merge | Moderate merging | Easy integration |
| Context Size | Needs full context | Manageable chunks | Small focused context |
| Time Pressure | Quality > speed | Balanced | Speed critical |
| Convergence Need | Single vision needed | Balanced | Multiple views OK |

**Total Score:**
- **5-8:** Sequential
- **9-12:** Hybrid
- **13-15:** Parallel

---

## Pattern Comparison

### Speed Comparison

Estimated time for typical phase:

| Phase | Sequential | Parallel | Hybrid | Adaptive |
|-------|------------|----------|--------|----------|
| Planning | 30 min | 30 min | 30 min | 30 min |
| Architecture | 90 min | 30 min | 45 min | Variable |
| Core Dev | 120 min | 45 min | 60 min | Variable |
| Complex Module | 90 min | 90 min* | 90 min | Variable |
| Testing | 60 min | 20 min | 30 min | Variable |
| Documentation | 60 min | 25 min | 35 min | Variable |
| **TOTAL** | **450 min** | **240 min** | **290 min** | **~280 min** |

*Some phases can't be parallelized effectively

### Complexity Comparison

| Aspect | Sequential | Parallel | Hybrid | Adaptive |
|--------|------------|----------|--------|----------|
| Understanding | ⭐ Easy | ⭐⭐⭐ Hard | ⭐⭐ Moderate | ⭐⭐⭐⭐ Very Hard |
| Execution | ⭐ Easy | ⭐⭐⭐ Hard | ⭐⭐ Moderate | ⭐⭐⭐⭐ Very Hard |
| Debugging | ⭐ Easy | ⭐⭐⭐⭐ Very Hard | ⭐⭐ Moderate | ⭐⭐⭐ Hard |
| Predictability | ⭐ Very High | ⭐⭐⭐ Moderate | ⭐⭐ High | ⭐⭐⭐ Moderate |

### Learning Value Comparison

| What You Learn | Sequential | Parallel | Hybrid | Adaptive |
|----------------|------------|----------|--------|----------|
| Basic coordination | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Parallel execution | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Synthesis skills | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Decision making | ⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Trade-off analysis | ⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## Recommended Learning Path

### Path 1: Thorough Learning (Recommended)

1. **Week 1: Sequential**
   - Run entire project with sequential workflow
   - Focus on understanding agent handoffs
   - Note where you waited for completions
   - Document learnings

2. **Week 2: Hybrid**
   - Re-run project with hybrid pattern
   - Compare time to sequential
   - Note synthesis challenges
   - Compare quality of outputs

3. **Week 3: Parallel**
   - Try full parallel for specific phases
   - Experience coordination complexity
   - Practice synthesis skills
   - Compare results

4. **Week 4: Adaptive**
   - Use adaptive pattern
   - Make conscious decisions per phase
   - Track metrics
   - Build intuition

### Path 2: Fast Track

1. **Start with Hybrid** (recommended for this project)
2. **Document what works and what doesn't**
3. **Try Parallel for one phase** (e.g., testing)
4. **Compare and learn**

### Path 3: Experimental

1. **Try all patterns in parallel** (meta!)
   - Run project 4 times with different patterns
   - Compare results side-by-side
   - Comprehensive learning
   - Most time-intensive but most educational

---

## Common Questions

### Q: Which pattern should I use for my project?

**A:** **Hybrid is recommended** for most projects because:
- Good balance between speed and complexity
- Clear learning value
- Significant speed boost without overwhelming complexity
- Natural validation gates at phase boundaries

### Q: Can I switch patterns mid-project?

**A:** **Yes!** It's perfectly fine to switch if a pattern isn't working. Document why you switched - that's valuable learning.

### Q: What if agents conflict in parallel execution?

**A:** This is normal and expected. Use the Task Synthesizer to:
1. Analyze all outputs
2. Identify conflicts
3. Resolve through reasoned choices
4. Document decisions

See COORDINATION_STRATEGIES.md for details.

### Q: Is parallel always faster?

**A:** No. Consider:
- **Synthesis overhead:** Time to merge results
- **Task dependencies:** Some things must be sequential
- **Integration complexity:** Parallel code may be harder to merge
- **Diminishing returns:** Beyond 4-5 agents, coordination dominates

### Q: How do I know if I'm ready for Adaptive?

**A:** Try Adaptive when:
- You've used Sequential and Hybrid
- You understand trade-offs
- You can analyze task independence
- You're comfortable with complexity

---

## Metrics to Track

For learning purposes, track these for each pattern:

### Time Metrics
- Total project time
- Time per phase
- Time saved vs sequential baseline
- Synthesis/integration time

### Quality Metrics
- Bug count
- Rework needed
- Output quality (subjective rating)
- Integration issues

### Learning Metrics
- "Aha moments" count
- Unexpected challenges
- Skills developed
- Would-use-again rating

### Example Tracking

```markdown
## Pattern: Hybrid

**Time:**
- Total: 12 hours
- Saved vs Sequential: ~4 hours
- Synthesis overhead: ~1.5 hours
- Net savings: ~2.5 hours

**Quality:**
- Bugs found: 8 (similar to sequential)
- Rework: Minimal
- Output quality: 4/5
- Integration issues: 2 (easily resolved)

**Learning:**
- "Aha moments": 3
  - Parallel architecture saved huge time
  - Synthesis is an art
  - Integration planning upfront pays off
- Challenges:
  - First synthesis took longer than expected
  - Integration required good specs
- Skills: Parallel coordination, synthesis, integration
- Would use again: ⭐⭐⭐⭐⭐ Definitely!
```

---

## Professional Applications

### How This Applies to Your Work

While you can't use autonomous coding agents professionally (per your constraints), these patterns teach transferable skills:

**1. Team Coordination**
- Sequential: Waterfall project management
- Parallel: Concurrent team workstreams
- Hybrid: Agile sprints with parallel work
- Adaptive: Context-driven team management

**2. AI System Design**
- Parallel: Multiple LLM calls for diverse perspectives
- Synthesis: Combining AI outputs
- Coordination: Orchestrating AI workflows
- Trade-offs: When to parallelize vs centralize

**3. System Architecture**
- Identifying parallelizable work
- Managing dependencies
- Integration strategies
- Context-aware decisions

**4. Code Review**
- Multiple reviewers (parallel)
- Synthesizing feedback
- Resolving conflicts
- Iterative refinement

### Discussion Topics for Work

Safe topics using learnings from this project:

- "Different coordination patterns for different project phases"
- "Trade-offs between parallel work and integration overhead"
- "Synthesis strategies for diverse inputs"
- "Context-aware decision making in project management"
- "Managing dependencies in concurrent workstreams"

---

## Next Steps

1. **Choose your pattern** based on goals:
   - Learning: Sequential → Hybrid → Parallel → Adaptive
   - Speed: Hybrid or Parallel
   - Safety: Sequential or Hybrid

2. **Read pattern-specific guide:**
   - `.claude/commands/patterns/[pattern]-workflow.md`

3. **Start orchestration:**
   - `/orchestrator-v2 prompt.md`

4. **Track learnings:**
   - Use LESSONS_LEARNED_TEMPLATE.md

5. **Experiment:**
   - Try different patterns
   - Compare results
   - Build intuition

Happy orchestrating! 🚀
