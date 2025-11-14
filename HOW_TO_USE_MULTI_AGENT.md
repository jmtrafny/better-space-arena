# How to Use the Multi-Agent System

This project uses a sophisticated multi-agent approach to coordinate development through specialized AI agents. Each agent has a specific role and expertise.

## Quick Start

### 1. Start the Project

To kick off the entire multi-agent workflow with advanced features:

```bash
/orchestrator-v2 your-requirements.md
```

This will:
- Read the project requirements from your requirements file
- Analyze project characteristics and recommend optimal workflow pattern
- Enable parallel agent execution for faster development (40-75% time savings)
- Coordinate all agents through the development lifecycle
- Pause at human validation gates for your approval
- Track metrics and synthesize results from concurrent work

**For simpler projects**, you can use the basic orchestrator:
```bash
/orchestrator your-requirements.md
```

### 2. Let the Agents Work

The orchestrator will automatically coordinate:
1. **Project Manager** - Creates detailed task breakdown
2. **Architect** - Designs system architecture
3. **Developer** - Implements features (can run in parallel)
4. **QA Tester** - Tests and validates
5. **Documentation** - Creates comprehensive docs

### 3. Approve at Gates

You'll be asked to approve at key milestones:
- ✋ Project plan approval
- ✋ Architecture design approval
- ✋ Feature demos
- ✋ Final delivery acceptance

## Available Agents

### `/orchestrator-v2 [requirements-file]`
**Enhanced coordinator** - Manages workflow with parallel execution, multiple patterns, and advanced coordination.

**Use when:**
- Starting any new project (RECOMMENDED)
- Want optimal workflow pattern selection
- Need parallel agent execution for speed
- Managing complex multi-phase work
- Want time savings and metrics tracking

**Features:**
- ✅ Parallel agent execution (40-75% faster)
- ✅ Multiple workflow patterns (Sequential, Parallel, Hybrid, Adaptive)
- ✅ Intelligent pattern recommendations
- ✅ Result synthesis from concurrent agents
- ✅ Human validation gates
- ✅ Metrics and time tracking

**Example:**
```bash
/orchestrator-v2 my-project-requirements.md
```

---

### `/orchestrator [requirements-file]`
**Basic coordinator** - Simple sequential workflow management.

**Use when:**
- Very simple projects
- Prefer straightforward sequential execution
- Learning the multi-agent system basics

**Example:**
```bash
/orchestrator my-requirements.md
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
/architect Design the database schema and API architecture
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
/developer Implement the user authentication system with JWT tokens
```

---

### `/qa-tester [what-to-test]`
**Quality assurance** - Tests features, finds bugs, validates functionality.

**Use when:**
- Need to test implementations
- Validate feature functionality
- Find bugs and edge cases
- Verify correct behavior

**Example:**
```bash
/qa-tester Test the payment processing for edge cases and correctness
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
# Start the entire project with enhanced orchestration
/orchestrator-v2 your-requirements.md
```

The orchestrator-v2 will guide you through:

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
/project-manager Break down the e-commerce checkout flow into tasks

# Design a specific system
/architect Design the authentication and authorization system

# Implement a feature
/developer Implement user registration with email verification

# Test a feature
/qa-tester Test the shopping cart logic

# Document something
/documentation Create API docs for the User service
```

## Workflow Patterns

Orchestrator-v2 supports multiple workflow patterns:

### Sequential Pattern
- **Best for:** Simple projects, high dependencies, learning
- **Speed:** Baseline
- **Complexity:** Low
- Agents work one at a time in order

### Parallel Pattern
- **Best for:** Research, independent tasks, maximum speed
- **Speed:** 60-75% faster
- **Complexity:** High
- Multiple agents work simultaneously

### Hybrid Pattern (RECOMMENDED)
- **Best for:** Most projects
- **Speed:** 40-50% faster
- **Complexity:** Moderate
- Sequential phases with parallel tasks within phases

### Adaptive Pattern
- **Best for:** Experienced users, complex projects
- **Speed:** 50-60% faster
- **Complexity:** Very high
- Dynamically chooses best strategy per phase

**Not sure?** Orchestrator-v2 will recommend the best pattern for your project.

## Tips for Success

### 1. Start with Orchestrator-v2

For new projects or major phases, always start with `/orchestrator-v2`. It will:
- Recommend the best workflow pattern for your project
- Enable parallel execution where beneficial
- Save 40-75% development time
- Manage the complete workflow for you

### 2. Be Specific in Requests

When invoking agents directly, provide clear context:

❌ Bad: `/developer build it`
✅ Good: `/developer Implement the user authentication according to the architecture, with JWT tokens and refresh tokens`

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
/documentation Document the authentication system now that it's implemented
```

## Multi-Agent Patterns

### Pattern 1: Feature Development

```bash
# 1. Plan the feature
/project-manager Plan implementation of user authentication system

# 2. Design the feature
/architect Design the authentication architecture with JWT

# 3. Implement
/developer Implement authentication per architecture

# 4. Test
/qa-tester Test authentication for security and edge cases

# 5. Document
/documentation Document the authentication API
```

### Pattern 2: Bug Fixing

```bash
# 1. Test to find bugs
/qa-tester Test the payment processing thoroughly

# 2. Fix bugs
/developer Fix the bugs found by QA

# 3. Retest
/qa-tester Verify the bug fixes
```

### Pattern 3: Refactoring

```bash
# 1. Plan refactor
/project-manager Plan refactoring of the data access layer

# 2. Design new approach
/architect Design improved data access architecture

# 3. Implement
/developer Refactor data access per new design

# 4. Test
/qa-tester Verify refactored system works correctly

# 5. Update docs
/documentation Update docs to reflect new approach
```

## Agent Coordination

Agents are designed to work together:

```
Orchestrator-v2
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
    ├── orchestrator.md          # Basic coordinator
    ├── orchestrator-v2.md       # Enhanced coordinator (RECOMMENDED)
    ├── project-manager.md       # Project management
    ├── architect.md             # System design
    ├── developer.md             # Implementation
    ├── qa-tester.md            # Quality assurance
    ├── documentation.md         # Technical writing
    ├── patterns/                # Workflow patterns
    │   ├── sequential-workflow.md
    │   ├── parallel-workflow.md
    │   ├── hybrid-workflow.md
    │   └── adaptive-workflow.md
    └── coordinators/            # Advanced coordination
        ├── parallel-coordinator.md
        └── task-synthesizer.md

docs/agentic-patterns/          # Multi-agent documentation
HOW_TO_USE_MULTI_AGENT.md      # This file
README.md                       # Overview
```

## Best Practices

1. **Use Orchestrator-v2**: Get parallel execution and optimal workflow patterns
2. **Trust the Process**: The multi-agent workflow is designed for quality
3. **Choose the Right Pattern**: Hybrid pattern works well for most projects
4. **Review Thoroughly**: Pay attention at validation gates
5. **Provide Feedback**: Clear feedback helps agents improve
6. **Test Often**: QA early and often prevents issues
7. **Leverage Parallelism**: Let multiple agents work concurrently when possible

## Getting Help

If you're unsure what to do:

```bash
/project-manager What is the current state of the project and what should we do next?
```

The Project Manager can always provide status and guidance.

---

## Let's Build! 🚀

To start building your project:

```bash
/orchestrator-v2 your-requirements.md
```

The agents will handle the rest, coordinating a professional development workflow from planning through delivery.
