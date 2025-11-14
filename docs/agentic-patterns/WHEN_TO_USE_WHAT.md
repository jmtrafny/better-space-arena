# When to Use What - Quick Decision Guide

Fast reference for choosing the right workflow pattern for your needs.

## TL;DR Recommendations

| Your Situation | Use This Pattern | Why |
|----------------|------------------|-----|
| First time using multi-agent | **Sequential** | Learn the basics without complexity |
| Weekend project, want speed | **Hybrid** | Best balance for this project |
| Research/exploration phase | **Parallel** | Get diverse perspectives fast |
| Experienced, want optimal | **Adaptive** | Choose best per phase |
| Need simplicity | **Sequential** | Clearest progression |
| Time is critical | **Parallel** or **Hybrid** | Maximum speed |

## Decision Tree

```
START: What's most important?

├─ "I want to learn multi-agent basics"
│  └─> **Sequential** → Then try Hybrid

├─ "I want to build fast and learn advanced patterns"
│  └─> **Hybrid** (recommended for this project)

├─ "I want maximum speed"
│  ├─ "Tasks are independent" → **Parallel**
│  └─ "Mixed dependencies" → **Hybrid**

├─ "I want optimal strategy per phase"
│  ├─ "I'm experienced" → **Adaptive**
│  └─ "I'm new" → **Hybrid** first, then Adaptive

└─ "I want simplicity"
   └─> **Sequential**
```

## Quick Assessment Questions

Answer these 5 questions to find your pattern:

### 1. Experience Level?
- **Never used multi-agent:** Sequential → 2 points
- **Some experience:** Hybrid → 4 points
- **Experienced:** Any → 5 points

### 2. Time Constraints?
- **Plenty of time:** Sequential → 2 points
- **Weekend timeline:** Hybrid → 4 points
- **Very tight:** Parallel → 5 points

### 3. Learning Goals?
- **Understand basics:** Sequential → 3 points
- **Learn advanced coordination:** Hybrid/Parallel → 5 points
- **Master all patterns:** Adaptive → 5 points

### 4. Comfort with Complexity?
- **Prefer simple:** Sequential → 2 points
- **OK with moderate:** Hybrid → 4 points
- **Embrace complexity:** Parallel/Adaptive → 5 points

### 5. Project Characteristics?
- **High dependencies:** Sequential → 2 points
- **Mixed:** Hybrid → 4 points
- **Very modular:** Parallel → 5 points

**Scoring:**
- **10-15 points:** Sequential
- **16-20 points:** Hybrid (recommended)
- **21-25 points:** Parallel or Adaptive

## Pattern by Project Phase

Different patterns work better for different phases:

| Phase | Best Pattern | Why |
|-------|--------------|-----|
| **Planning** | Sequential | Needs holistic view |
| **Architecture** | Parallel or Hybrid | Different subsystems independent |
| **Core Development** | Parallel | Modular systems |
| **Integration** | Sequential | Everything connects |
| **Feature Development** | Hybrid | Some features independent |
| **Testing** | Parallel | Different test suites |
| **Bug Fixing** | Hybrid | Some bugs independent |
| **Documentation** | Parallel | Different doc types |

💡 **Tip:** Adaptive pattern uses these insights per phase!

## Pattern by Team/User Type

### Solo Developer, First Project
**Recommended:** Sequential → Hybrid

**Rationale:**
- Learn basics with Sequential
- Graduate to Hybrid for speed
- Manageable complexity alone

### Solo Developer, Experienced
**Recommended:** Hybrid or Adaptive

**Rationale:**
- You can handle coordination
- Time savings are significant
- Learning value is high

### Learning Focus
**Recommended:** Try all patterns!

**Rationale:**
- Run project multiple times
- Compare results
- Maximum learning
- Build intuition

### Professional Reference Project
**Recommended:** Adaptive

**Rationale:**
- Shows sophisticated understanding
- Demonstrates decision-making skills
- Portfolio piece
- Most impressive

## Pattern by Project Constraints

### Constraint: Time (Weekend Project)
**Best:** Hybrid or Parallel
- Hybrid: 40-60% faster than sequential
- Parallel: 50-75% faster but harder
- **Recommendation:** Hybrid

### Constraint: Complexity Tolerance
**Best:** Sequential or Hybrid
- Sequential: Simplest
- Hybrid: Manageable complexity
- **Recommendation:** Sequential if new, Hybrid if experienced

### Constraint: Learning Goals
**Best:** All patterns (try each)
- Run project multiple times
- Compare and contrast
- **Recommendation:** Sequential → Hybrid → Parallel → Adaptive

### Constraint: Quality Over Speed
**Best:** Sequential or Adaptive
- Sequential: Thorough, single vision
- Adaptive: Choose quality-first per phase
- **Recommendation:** Sequential for safety

## Common Scenarios

### Scenario 1: "I've never used Claude Code's multi-agent features"

**Answer:** **Sequential**

**Path:**
1. Start with Sequential pattern
2. Run through entire project
3. Document what you learn
4. Next project: Try Hybrid

**Why:** Learn to walk before you run. Understanding sequential flow is foundational.

---

### Scenario 2: "I want to finish this weekend project fast"

**Answer:** **Hybrid**

**Path:**
1. Use Hybrid pattern from start
2. Parallel for Architecture, Development, Testing, Docs
3. Sequential for Planning, Integration
4. ~40% time savings

**Why:** Best speed/complexity trade-off for weekend timeline.

---

### Scenario 3: "I want to learn everything about agentic workflows"

**Answer:** **Try all patterns**

**Path:**
1. Run project with Sequential (baseline)
2. Run again with Hybrid (compare)
3. Run specific phases with Parallel
4. Run full project with Adaptive
5. Document learnings

**Why:** Maximum learning comes from comparison.

---

### Scenario 4: "I need this for my portfolio/resume"

**Answer:** **Adaptive**

**Path:**
1. Use Adaptive pattern
2. Document decision-making process
3. Track metrics and learnings
4. Show sophisticated understanding

**Why:** Demonstrates advanced skills and judgment.

---

### Scenario 5: "I just want something that works"

**Answer:** **Hybrid**

**Path:**
1. Use Hybrid pattern
2. Don't overthink it
3. Follow the workflow
4. Deliver working project

**Why:** Safest bet for success with good speed.

## Red Flags by Pattern

### Don't Use Sequential If:
- ❌ Time is very constrained
- ❌ You're experienced with agents
- ❌ Tasks are clearly independent
- ❌ You want to learn advanced patterns

### Don't Use Parallel If:
- ❌ First time with multi-agent
- ❌ Tasks have high dependencies
- ❌ Integration is complex
- ❌ You're not ready for synthesis challenges

### Don't Use Hybrid If:
- ❌ You want maximum simplicity (use Sequential)
- ❌ You want maximum speed (use Parallel)
- ❌ You want to learn basics (start with Sequential)

### Don't Use Adaptive If:
- ❌ First time with multi-agent
- ❌ Don't want decision overhead
- ❌ Prefer consistency (same pattern throughout)
- ❌ Not ready for complexity

## Switching Patterns Mid-Project

**It's OK to switch!** If your pattern isn't working:

### Sequential → Hybrid
**When:** Sequential is too slow
**How:** Start parallelizing within phases

### Hybrid → Sequential
**When:** Synthesis overhead too high
**How:** Stop parallelizing, go phase-by-phase

### Parallel → Hybrid
**When:** Too many conflicts, integration issues
**How:** Reduce parallelism, stay sequential for complex phases

### Any → Adaptive
**When:** Want to optimize each phase differently
**How:** Start analyzing context per phase

## Quick Reference Table

| If You Value... | Use Pattern | Trade-Off |
|-----------------|-------------|-----------|
| Simplicity | Sequential | Speed |
| Speed | Parallel | Complexity |
| Balance | Hybrid | Some synthesis needed |
| Optimization | Adaptive | Decision overhead |
| Learning | All patterns | Time investment |
| Reliability | Sequential or Hybrid | May be slower |
| Efficiency | Parallel or Hybrid | More coordination |
| Flexibility | Adaptive | Requires experience |

## Final Recommendations

### General Guidance:

**Recommended for most projects:** **Hybrid Pattern**

**Why:**
- ✅ Good balance of speed and complexity
- ✅ Most projects have some parallelizable work
- ✅ Not too complex for newcomers
- ✅ Great learning value
- ✅ Natural validation gates at phase boundaries
- ✅ Good success rate across different project types

**Alternative:** Sequential if this is your first multi-agent project ever.

---

### For Learning Agentic Workflows:

**Recommended Path:**
1. **Sequential** (Day 1): Understand basics
2. **Hybrid** (Day 2): See speed benefits
3. **Parallel** (Day 3): Experience full parallelism
4. **Adaptive** (Day 4): Master context-driven decisions

---

### For Professional Portfolio:

**Recommended:** **Adaptive** with comprehensive documentation

**Include:**
- Decision analysis per phase
- Metrics tracked
- Learnings documented
- Trade-offs explained
- Comparison with other patterns

---

## Still Not Sure?

### Default Choice: **Hybrid**

When in doubt, Hybrid is the safest bet because:
- Works well for most projects
- Significant speed boost
- Not overwhelming
- Clear structure
- Good learning value
- High success rate

### Get Started:

```bash
/orchestrator-v2 prompt.md
```

Then choose Hybrid when prompted. The orchestrator will guide you through!

---

## Need Help Deciding?

Ask yourself:
1. **What's my primary goal?** (Learn / Build fast / Both)
2. **Am I comfortable with complexity?** (Yes / No / Somewhat)
3. **How much time do I have?** (Lots / Weekend / Tight)

Then look up your answers in this guide.

Still stuck? **Go with Hybrid.** You can't go wrong.

Happy orchestrating! 🎯
