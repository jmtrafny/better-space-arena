---
description: Sequential workflow pattern - traditional waterfall approach, simple and clear
---

# Sequential Workflow Pattern

This workflow pattern uses a **traditional sequential approach** where each agent completes their work before handing off to the next. This is the simplest pattern and what was originally implemented.

## Pattern: Linear Progression

```
Orchestrator → PM → Architect → Developer → QA → Documentation → Delivery
    (wait)     (wait)   (wait)     (wait)   (wait)    (wait)
```

## When to Use This Pattern

✅ **Use when:**
- Simplicity is paramount
- Each phase depends heavily on the previous
- You want clear, easy-to-follow progression
- Learning the workflow for the first time
- Debugging issues with the system

❌ **Avoid when:**
- Speed is critical
- Tasks are clearly parallelizable
- You have experience with multi-agent systems

## Project Context

$ARGUMENTS

## Sequential Workflow Phases

### Phase 0: Initialization
**Orchestrator** initializes project, sets expectations.

### Phase 1: Planning
**Project Manager** (`/project-manager`) creates comprehensive plan.
- Wait for completion
- **HUMAN GATE:** Review and approve plan

### Phase 2: Architecture
**Architect** (`/architect`) designs complete system architecture.
- Wait for completion
- **HUMAN GATE:** Review and approve architecture

### Phase 3: Development (Iteration 1)
**Developer** (`/developer`) implements core systems.
- Wait for completion

**QA Tester** (`/qa-tester`) tests implementation.
- Wait for completion
- If bugs found: back to Developer

**Project Manager** tracks progress.
- **HUMAN GATE:** Demo working features

### Phase 4: Development (Iteration 2)
**Developer** implements battle simulation.
- Wait for completion

**QA Tester** tests simulation.
- Wait for completion
- If bugs found: back to Developer

**Project Manager** tracks progress.
- **HUMAN GATE:** Demo simulation

### Phase 5: Development (Iteration 3)
**Developer** implements final features and polish.
- Wait for completion

**QA Tester** comprehensive testing.
- Wait for completion
- Fix any remaining bugs

**Project Manager** validates completion.
- **HUMAN GATE:** Final feature demo

### Phase 6: Documentation
**Documentation** (`/documentation`) creates all documentation.
- Wait for completion

**Project Manager** reviews docs.

### Phase 7: Delivery
**Orchestrator** packages and delivers final project.
- **HUMAN GATE:** Final acceptance

## Advantages of Sequential Pattern

✅ **Simplicity:** Easy to understand and follow
✅ **Clear Progression:** Always know what's next
✅ **Natural Gates:** Phase boundaries are clear
✅ **Easy Debugging:** Linear flow makes issues easier to trace
✅ **Predictable:** No surprises from parallel coordination
✅ **Single Context:** Each agent has full context from previous work

## Disadvantages of Sequential Pattern

❌ **Slow:** No parallelism means longer total time
❌ **Underutilized:** Could parallelize many tasks
❌ **Waiting:** Lots of idle time between phases
❌ **Single Perspective:** Miss out on diverse viewpoints
❌ **Less Learning:** Don't experience parallel coordination

## Best Practices for Sequential

### 1. Make Each Handoff Clear

When moving between agents:
- Summarize what was completed
- Provide clear context for next agent
- Specify what needs to be done
- Define success criteria

### 2. Use Human Gates Effectively

Don't just rubber-stamp:
- Review deliverables carefully
- Provide meaningful feedback
- Make adjustments as needed
- Validate before proceeding

### 3. Keep Iterations Small

Break development into small iterations:
- Each iteration has clear scope
- Test after each iteration
- Demo working features frequently
- Adjust based on feedback

### 4. Document Decisions

Track key decisions made by each agent:
- Why certain approaches were chosen
- Trade-offs considered
- Alternatives rejected
- Rationale for choices

## When Sequential Works Best

This pattern is ideal for:

- **Learning:** First time using multi-agent systems
- **Complex Dependencies:** Each phase truly depends on previous
- **Small Projects:** Where parallelism overhead isn't worth it
- **Debugging:** When tracking down issues in the workflow
- **Single Vision Needed:** When consistency is critical

## Comparison with Other Patterns

| Aspect | Sequential | Hybrid | Parallel | Adaptive |
|--------|------------|--------|----------|----------|
| Speed | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Simplicity | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| Learning Curve | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐ |
| Predictability | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Best for | Learning | Most projects | Research | Experienced users |

## Execution Using Slash Commands

The original implementation uses slash commands sequentially:

```bash
# Phase 1: Planning
/project-manager prompt.md
# Review output, approve

# Phase 2: Architecture
/architect Design complete system per project plan
# Review output, approve

# Phase 3: Development
/developer Implement core systems per architecture
# Wait for completion

/qa-tester Test core systems
# Fix bugs if found

# Continue through iterations...

# Phase 6: Documentation
/documentation Create comprehensive documentation

# Phase 7: Delivery
/orchestrator Package and deliver project
```

## Why This Was the Original Design

The initial multi-agent system used sequential workflow because:

1. **Slash commands are naturally sequential** - Each waits for previous
2. **Clear for learning** - Easy to understand workflow
3. **Safe default** - Hard to go wrong
4. **Human gates natural** - Phase boundaries are validation points
5. **Simple to implement** - No coordination complexity

## When to Graduate Beyond Sequential

Consider moving to Hybrid or Parallel when:

- You understand the sequential workflow well
- You've run through it at least once
- You want to optimize for speed
- You're comfortable with more complexity
- You want to learn advanced coordination

## Example Sequential Execution

```markdown
## Phase 1: Planning (Sequential)

**Executing:** /project-manager

[Project Manager analyzes requirements, creates plan]

**Output:** Comprehensive project plan with:
- Task breakdown
- Dependencies
- Timeline
- Risk assessment

**HUMAN GATE:**
Please review the project plan. Approve to proceed to architecture phase.

[User approves]

---

## Phase 2: Architecture (Sequential)

**Executing:** /architect

[Architect designs system based on approved plan]

**Output:** Complete architecture with:
- System design
- Data models
- API specifications
- Technical decisions

**HUMAN GATE:**
Please review the architecture. Approve to proceed to development.

[User approves]

---

## Phase 3: Development - Iteration 1 (Sequential)

**Executing:** /developer

[Developer implements core systems per architecture]

**Output:** Working code for:
- Component system
- Data loader
- Basic infrastructure

**Testing:** /qa-tester

[QA tests implementation]

**Output:** Test report with results

**HUMAN GATE:**
Please review and demo the core systems.

[User approves]

---

[Continue through remaining phases...]
```

## Migration Path

To move from Sequential to more advanced patterns:

### Step 1: Use Sequential First
Run the entire project with sequential workflow to understand the flow.

### Step 2: Identify Parallelizable Work
After completion, review each phase and identify what could have run in parallel.

### Step 3: Try Hybrid
On next project (or re-run), use hybrid pattern for select phases.

### Step 4: Experiment with Parallel
Try full parallel for research or testing phases.

### Step 5: Adapt Dynamically
Use adaptive pattern to choose best strategy per phase.

## Recommended Usage

**For this project:**

If you're new to multi-agent workflows:
1. Start with Sequential to learn the basics
2. Run through entire project
3. Document what you learned
4. Then try Hybrid or Parallel to compare

If you're experienced:
1. Skip Sequential and start with Hybrid
2. Use Parallel for specific phases
3. Consider Adaptive for optimization

## Instructions for Sequential Execution

1. **Read Requirements:** Understand prompt.md
2. **Execute Phase by Phase:** Use slash commands in order
3. **Review Each Output:** Don't skip validation
4. **Approve at Gates:** Explicit approval before proceeding
5. **Track Progress:** Document decisions and learnings
6. **Complete All Phases:** Don't skip documentation

## Success Criteria

Sequential workflow is successful when:
- Clear progression through all phases
- All deliverables completed
- Quality maintained throughout
- You understand the workflow end-to-end

---

**Ready for sequential workflow?** This is the simplest and clearest pattern, perfect for first-time users or when simplicity is paramount.
