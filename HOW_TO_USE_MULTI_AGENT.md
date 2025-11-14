# How to Use the Multi-Agent System

This project uses a sophisticated multi-agent approach to coordinate development through specialized AI agents. Each agent has a specific role and expertise.

## Quick Start

### 1. Start the Project

To kick off the entire multi-agent workflow:

```bash
/orchestrator prompt.md
```

This will:
- Read the project requirements from `prompt.md`
- Initialize the project workflow
- Coordinate all agents through the development lifecycle
- Pause at human validation gates for your approval

### 2. Let the Agents Work

The orchestrator will automatically coordinate:
1. **Project Manager** - Creates detailed task breakdown
2. **Architect** - Designs system architecture
3. **Developer** - Implements features
4. **QA Tester** - Tests and validates
5. **Documentation** - Creates comprehensive docs

### 3. Approve at Gates

You'll be asked to approve at key milestones:
- ✋ Project plan approval
- ✋ Architecture design approval
- ✋ Feature demos
- ✋ Final delivery acceptance

## Available Agents

### `/orchestrator [context]`
**Master coordinator** - Manages the entire workflow from start to finish.

**Use when:**
- Starting a new project
- Need coordination across all phases
- Managing complex multi-phase work

**Example:**
```bash
/orchestrator prompt.md
```

---

### `/project-manager [context]`
**Project management** - Breaks down tasks, tracks progress, coordinates agents.

**Use when:**
- Need task breakdown and planning
- Tracking project progress
- Coordinating between agents
- Managing dependencies

**Example:**
```bash
/project-manager Review current progress and plan next iteration
```

---

### `/architect [requirements]`
**System design** - Creates architecture, data models, APIs, technical specs.

**Use when:**
- Need system architecture design
- Defining data models and schemas
- Planning technical approach
- Making technology decisions

**Example:**
```bash
/architect Design the component system and battle simulation architecture
```

---

### `/developer [task]`
**Implementation** - Writes code, implements features, creates tests.

**Use when:**
- Need to implement specific features
- Writing code based on architecture
- Creating working software
- Building tests

**Example:**
```bash
/developer Implement the component loading system from JSON files
```

---

### `/qa-tester [what-to-test]`
**Quality assurance** - Tests features, finds bugs, validates functionality.

**Use when:**
- Need to test implementations
- Validate feature functionality
- Find bugs and edge cases
- Verify deterministic behavior

**Example:**
```bash
/qa-tester Test the battle simulation for determinism and correctness
```

---

### `/documentation [what-to-document]`
**Technical writing** - Creates docs, guides, examples, API references.

**Use when:**
- Need user documentation
- Creating developer guides
- Writing API references
- Building example galleries

**Example:**
```bash
/documentation Create getting started guide and API reference
```

## Typical Workflow

### Full Project Workflow

```bash
# Start the entire project
/orchestrator prompt.md
```

The orchestrator will guide you through:

1. **Planning Phase**
   - PM creates project plan
   - You approve the plan

2. **Architecture Phase**
   - Architect designs the system
   - You approve the architecture

3. **Development Phase (Iterative)**
   - Developer implements features
   - QA tests each feature
   - You approve working demos
   - Repeat for each iteration

4. **Documentation Phase**
   - Documentation agent creates all docs

5. **Delivery**
   - Final review and acceptance

### Using Individual Agents

You can also invoke agents directly for specific tasks:

```bash
# Get a project plan
/project-manager Break down the battle simulation into tasks

# Design a specific system
/architect Design the damage calculation system

# Implement a feature
/developer Implement unit loading from YAML files

# Test a feature
/qa-tester Test the component validation logic

# Document something
/documentation Create API docs for the Battle class
```

## Tips for Success

### 1. Start with the Orchestrator

For new projects or major phases, always start with `/orchestrator`. It will manage the workflow for you.

### 2. Be Specific in Requests

When invoking agents directly, provide clear context:

❌ Bad: `/developer build it`
✅ Good: `/developer Implement the Movement class according to the architecture, with grid-based positioning`

### 3. Use PM for Coordination

If you're unsure what to do next, ask the Project Manager:

```bash
/project-manager What should we work on next?
```

### 4. Don't Skip Testing

Always run QA after development:

```bash
/developer Implement feature X
# After implementation completes:
/qa-tester Test feature X
```

### 5. Document as You Go

Don't wait until the end to document:

```bash
/documentation Document the component system now that it's implemented
```

## Multi-Agent Patterns

### Pattern 1: Feature Development

```bash
# 1. Plan the feature
/project-manager Plan implementation of weapon targeting system

# 2. Design the feature
/architect Design the targeting system architecture

# 3. Implement
/developer Implement targeting system per architecture

# 4. Test
/qa-tester Test targeting system for correctness and edge cases

# 5. Document
/documentation Document the targeting system API
```

### Pattern 2: Bug Fixing

```bash
# 1. Test to find bugs
/qa-tester Test the combat simulation thoroughly

# 2. Fix bugs
/developer Fix the bugs found by QA

# 3. Retest
/qa-tester Verify the bug fixes
```

### Pattern 3: Refactoring

```bash
# 1. Plan refactor
/project-manager Plan refactoring of the data loading system

# 2. Design new approach
/architect Design improved data loading architecture

# 3. Implement
/developer Refactor data loading per new design

# 4. Test
/qa-tester Verify refactored system works correctly

# 5. Update docs
/documentation Update docs to reflect new approach
```

## Agent Coordination

Agents are designed to work together:

```
Orchestrator
    ↓
Project Manager ←→ All agents (coordination)
    ↓
Architect
    ↓
Developer ←→ QA Tester (feedback loop)
    ↓
Documentation
```

The Project Manager acts as the hub, coordinating handoffs between specialized agents.

## Human Validation Gates

The system will pause and request your input at critical points:

```
🚦 HUMAN VALIDATION REQUIRED

Phase: Architecture Design
What Needs Approval: System architecture and data models

[Summary of what was designed]

Please review and provide:
- ✅ Approved - continue as planned
- 📝 Feedback - [what to change]
- ❌ Rejected - [major concerns]
```

Always review these carefully and provide clear feedback.

## Troubleshooting

### Agent Seems Confused?

Provide more context:
```bash
/agent-name Here's the context: [explain situation]
```

### Need to Reset Direction?

Go back to Project Manager:
```bash
/project-manager Reset: we need to change direction. Here's what we want instead: [explain]
```

### Something Not Working?

Run QA to identify issues:
```bash
/qa-tester Do a comprehensive test of [system/feature] and identify all issues
```

## File Structure

The multi-agent system uses this structure:

```
.claude/
└── commands/
    ├── orchestrator.md      # Master coordinator
    ├── project-manager.md   # Project management
    ├── architect.md         # System design
    ├── developer.md         # Implementation
    ├── qa-tester.md        # Quality assurance
    └── documentation.md     # Technical writing

prompt.md                    # Project requirements (input)
HOW_TO_USE_MULTI_AGENT.md  # This file
```

## Best Practices

1. **Trust the Process**: The multi-agent workflow is designed for quality
2. **Be Patient**: Let each agent complete their work
3. **Review Thoroughly**: Pay attention at validation gates
4. **Provide Feedback**: Clear feedback helps agents improve
5. **Iterate**: It's okay to go back and refine
6. **Document Decisions**: Agents will track key decisions
7. **Test Often**: QA early and often prevents issues

## Getting Help

If you're unsure what to do:

```bash
/project-manager What is the current state of the project and what should we do next?
```

The Project Manager can always provide status and guidance.

---

## Let's Build! 🚀

To start building the Battle Automata Engine:

```bash
/orchestrator prompt.md
```

The agents will handle the rest, coordinating a professional development workflow from planning through delivery.

Good luck with your weekend project!
