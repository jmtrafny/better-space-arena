---
description: Hybrid workflow pattern - sequential phases with parallel subtasks for optimal balance
---

# Hybrid Workflow Pattern

This workflow pattern provides the **best balance** between simplicity and speed. Phases run sequentially (for clear progression and human gates), but within each phase, parallelizable work runs concurrently.

## Pattern: Sequential Phases, Parallel Tasks

```
Phase 1: Planning (Sequential)
    ↓
Phase 2: Architecture (Parallel within phase)
    ├─→ [Data Model] ─┐
    ├─→ [Simulation]  ├─→ Synthesize → Architecture Doc
    └─→ [API Design]  ┘
    ↓ (Human Gate)
Phase 3: Development (Parallel within phase)
    ├─→ [Feature A] ─┐
    ├─→ [Feature B] ─┼─→ Integrate → Working Code
    └─→ [Feature C] ─┘
    ↓
Phase 4: Testing (Parallel within phase)
    ├─→ [Unit Tests] ─┐
    ├─→ [Integration] ├─→ Consolidate → Test Report
    └─→ [Determinism] ┘
    ↓ (Human Gate)
Phase 5: Documentation (Parallel within phase)
    └─→ Final Delivery
```

## When to Use This Pattern

✅ **Use when:**
- You want clear phase progression
- Human validation gates are important
- Some work within phases can parallelize
- You want a good speed/complexity trade-off

✅ **Best for:** Most real-world projects

## Project Context

$ARGUMENTS

## Hybrid Workflow Execution

### Phase 0: Initialization (Sequential)

**Orchestrator:**
- Read project requirements
- Present high-level understanding
- Initialize project structure
- Set expectations

**No parallelism needed:** Simple coordination phase.

### Phase 1: Planning (Sequential)

**Project Manager:**
- Break down requirements into tasks
- Create project plan
- Identify dependencies
- Estimate effort

**No parallelism needed:** Needs holistic view of project.

**HUMAN GATE:** Approve project plan

### Phase 2: Architecture (PARALLEL)

**Launch parallel architecture agents:**

Within this phase, we can parallelize different architecture areas:

```python
# Launch 3 architecture specialists in parallel:

Task(subagent_type="general-purpose",
     description="Design data architecture",
     prompt="""You are a data architecture specialist.

Design:
- Component schema (JSON structure, properties, validation)
- Unit schema (layout, slots, resources)
- Battle configuration schema
- Theme definition format

Deliverable: Complete data model with schemas and examples.
""")

Task(subagent_type="general-purpose",
     description="Design simulation architecture",
     prompt="""You are a simulation systems architect.

Design:
- Battle simulation algorithm (turn-based, time steps)
- Combat mechanics (movement, targeting, damage)
- Deterministic execution strategy
- Event logging for replay

Deliverable: Simulation engine architecture with algorithms.
""")

Task(subagent_type="general-purpose",
     description="Design integration architecture",
     prompt="""You are an integration architect.

Design:
- API interfaces between components
- CLI structure and commands
- Project directory layout
- Build and test infrastructure

Deliverable: Integration architecture and project structure.
""")
```

**Synthesize:** Merge three perspectives into unified architecture document.

**HUMAN GATE:** Approve architecture

### Phase 3: Development - Iteration 1 (PARALLEL)

**Strategy:** Core systems can be built in parallel, then integrated.

```python
# Launch parallel development agents for core systems:

Task(subagent_type="general-purpose",
     description="Implement component system",
     prompt="""Implement the component system per architecture.

Files to create:
- src/core/component.py
- tests/test_component.py

Features:
- Component class with properties
- Load from JSON
- Validation logic
- Type system

Include unit tests.
""")

Task(subagent_type="general-purpose",
     description="Implement data loader",
     prompt="""Implement data loading utilities.

Files to create:
- src/utils/loader.py
- src/utils/validator.py
- tests/test_loader.py

Features:
- JSON/YAML parsing
- Schema validation
- Error handling
- Theme loading

Include unit tests.
""")

Task(subagent_type="general-purpose",
     description="Create project structure",
     prompt="""Set up the project structure and infrastructure.

Create:
- Directory structure per architecture
- requirements.txt
- setup.py
- pytest configuration
- Example data files

Ensure everything is ready for development.
""")
```

**Integrate:** Merge code, resolve any conflicts, ensure everything works together.

**QA Test:** Run integration tests on combined code.

**HUMAN GATE:** Demo core systems working

### Phase 3: Development - Iteration 2 (PARALLEL)

**Strategy:** Build higher-level systems that depend on core.

```python
# Launch parallel development agents for simulation systems:

Task(subagent_type="general-purpose",
     description="Implement unit builder",
     prompt="""Implement the unit building system.

Files to create:
- src/core/unit.py
- tests/test_unit.py

Features:
- Unit class
- Component placement
- Resource validation
- Serialization

Use the component system already implemented.
""")

Task(subagent_type="general-purpose",
     description="Implement battle mechanics",
     prompt="""Implement battle mechanics systems.

Files to create:
- src/mechanics/movement.py
- src/mechanics/targeting.py
- src/mechanics/damage.py
- tests/test_mechanics.py

Features:
- Movement logic
- Targeting system
- Damage calculation
- Component destruction
""")

Task(subagent_type="general-purpose",
     description="Implement CLI",
     prompt="""Implement command-line interface.

Files to create:
- src/cli.py
- tests/test_cli.py

Features:
- Battle simulation command
- Unit validation command
- Example loading
- Output formatting
""")
```

**Integrate:** Combine with core systems, test integration.

**QA Test:** Full system testing.

**HUMAN GATE:** Demo battles working

### Phase 3: Development - Iteration 3 (PARALLEL)

**Strategy:** Final features and polish.

```python
# Launch parallel development agents for final features:

Task(subagent_type="general-purpose",
     description="Implement battle engine",
     prompt="""Implement the complete battle simulation engine.

Files to create:
- src/core/battle.py
- src/core/engine.py
- tests/test_battle.py

Features:
- Battle initialization
- Simulation loop
- Event logging
- Replay system
- Win condition detection

Integrate all mechanics.
""")

Task(subagent_type="general-purpose",
     description="Create theme content",
     prompt="""Create the space-ships theme with components.

Files to create:
- data/themes/space-ships/theme.yaml
- data/themes/space-ships/components/*.yaml (10-15 components)
- data/themes/space-ships/units/*.yaml (example units)

Create diverse, balanced components.
""")

Task(subagent_type="general-purpose",
     description="Create examples",
     prompt="""Create example scenarios and scripts.

Files to create:
- examples/simple_battle.py
- examples/custom_component.py
- examples/new_theme.py
- data/battles/example_*.json

Show how to use the system.
""")
```

**Integrate:** Final integration and polish.

**QA Test:** Comprehensive testing.

**HUMAN GATE:** Demo complete system

### Phase 4: Testing (PARALLEL)

**Strategy:** Different test areas can run concurrently.

```python
# Launch parallel QA agents:

Task(subagent_type="general-purpose",
     description="Test core systems",
     prompt="""Test component and unit systems.

Test:
- Component loading and validation
- Unit building and validation
- Resource constraints
- Error handling

Report all bugs found.
""")

Task(subagent_type="general-purpose",
     description="Test battle simulation",
     prompt="""Test battle simulation thoroughly.

Test:
- Combat mechanics
- Event logging
- Win conditions
- Edge cases

Report all bugs found.
""")

Task(subagent_type="general-purpose",
     description="Test determinism",
     prompt="""Test deterministic behavior.

Test:
- Same seed = same result
- Replay accuracy
- State consistency
- Float precision

Report any non-determinism.
""")

Task(subagent_type="general-purpose",
     description="Test usability",
     prompt="""Test user experience.

Test:
- CLI usability
- Error messages
- Documentation accuracy
- Example validity

Report UX issues.
""")
```

**Consolidate:** Merge bug reports, prioritize fixes.

**Developer:** Fix critical bugs (may parallelize bug fixes).

**QA Retest:** Verify fixes.

### Phase 5: Documentation (PARALLEL)

**Strategy:** Different doc types are independent.

```python
# Launch parallel documentation agents:

Task(subagent_type="general-purpose",
     description="Write getting started guide",
     prompt="""Create GETTING_STARTED.md.

Include:
- Installation
- Your first battle
- Understanding results
- Next steps

Make it beginner-friendly.
""")

Task(subagent_type="general-purpose",
     description="Write user guide",
     prompt="""Create USER_GUIDE.md.

Include:
- Core concepts
- Building units
- Configuring components
- Running battles
- Advanced features

Make it comprehensive.
""")

Task(subagent_type="general-purpose",
     description="Write API reference",
     prompt="""Create API_REFERENCE.md.

Document:
- All public classes
- All public methods
- Parameters and returns
- Usage examples

Make it complete.
""")

Task(subagent_type="general-purpose",
     description="Write developer guide",
     prompt="""Create DEVELOPER_GUIDE.md.

Include:
- Architecture overview
- Extending the engine
- Adding components
- Creating themes
- Contributing

Help future developers.
""")
```

**Organize:** Ensure consistency, cross-link docs, update README.

**HUMAN GATE:** Final approval

### Phase 6: Delivery (Sequential)

**Orchestrator:**
- Package deliverables
- Create summary report
- Present to stakeholder
- Celebrate! 🎉

## Advantages of Hybrid Pattern

✅ **Clear Progression:** Sequential phases are easy to follow
✅ **Speed Boost:** Parallelism where it helps most
✅ **Natural Gates:** Phase boundaries are validation points
✅ **Manageable Complexity:** Simpler than full parallel
✅ **Best Balance:** Good speed without overwhelming coordination

## Challenges of Hybrid Pattern

⚠️ **Coordination Still Needed:** Must synthesize parallel work
⚠️ **Integration Points:** Parallel code must merge cleanly
⚠️ **Optimal Split:** Need to identify what can parallelize

## Best Practices for Hybrid

### 1. Identify Parallelizable Work

Within each phase, ask:
- Can these tasks run independently?
- Do they share dependencies?
- Will integration be straightforward?

### 2. Keep Phases Sequential

Don't parallelize phases themselves:
- Architecture before implementation
- Implementation before testing
- Testing before documentation

### 3. Integrate Carefully

After parallel development:
- Review all code together
- Run integration tests
- Resolve conflicts thoughtfully
- Ensure cohesion

### 4. Use Human Gates Between Phases

Validate at phase boundaries:
- Architecture complete → approve before dev
- Features complete → demo before next iteration
- Testing complete → approve for docs

## When to Parallelize Within Phase

| Phase | Parallel Work | Sequential Work |
|-------|---------------|-----------------|
| Planning | ❌ None | ✅ All planning |
| Architecture | ✅ Different subsystems | ❌ Final synthesis |
| Development | ✅ Independent features | ❌ Integration |
| Testing | ✅ Different test areas | ❌ Bug fixing |
| Documentation | ✅ Different doc types | ❌ Final organization |

## Comparison with Other Patterns

| Aspect | Hybrid | Sequential | Parallel |
|--------|--------|------------|----------|
| Speed | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| Simplicity | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| Control | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Natural Gates | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Best for | Most projects | Simple projects | Research/exploration |

## Execution Template

For each phase:

1. **Assess Parallelizability**
   - What can run concurrently?
   - What must be sequential?

2. **Launch Parallel Work**
   - Use Task tool for concurrent agents
   - All in single message

3. **Synthesize/Integrate**
   - Merge parallel outputs
   - Resolve conflicts
   - Ensure coherence

4. **Validate**
   - Test integration
   - Human review if phase boundary

5. **Proceed to Next Phase**

## Recommended Usage

This is the **recommended pattern for the the project** because:

- Clear phase progression for learning
- Parallel speedup where it matters
- Natural human validation gates
- Manageable complexity
- Good balance of all factors

Start with this pattern, then experiment with full parallel or sequential if you want to compare.

---

**Ready to execute hybrid workflow?** This pattern provides the best balance for most projects.
