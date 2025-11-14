# Battle Automata Engine

A theme-agnostic engine for simulating deterministic battles between customizable automata, inspired by the mobile game Space Arena.

## Project Status

🏗️ **Enhanced Multi-Agent System** - Advanced workflow patterns ready

This repository contains an **advanced multi-agent system** with:
- 🚀 **Parallel Agent Execution** - Launch concurrent agents for speed
- 🎯 **Multiple Workflow Patterns** - Sequential, Parallel, Hybrid, Adaptive
- 🤝 **Specialized Coordinators** - Synthesis and integration experts
- 📚 **Comprehensive Documentation** - Complete learning resources

**NEW in V2:** Parallel execution using Task tool for 40-75% faster development!

## Quick Start

### Recommended: Enhanced Orchestrator V2

```bash
/orchestrator-v2 prompt.md
```

The enhanced orchestrator will:
1. Help you **choose the best workflow pattern** for your needs
2. **Launch agents in parallel** when beneficial for speed
3. **Synthesize results** from concurrent work
4. **Adapt strategy** based on each phase's needs
5. **Track metrics** to show you what works best

### Choose Your Workflow Pattern

| Pattern | Best For | Speed | Complexity |
|---------|----------|-------|------------|
| **Sequential** | Learning basics | ⭐⭐ | ⭐ Easy |
| **Parallel** | Maximum speed | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ Complex |
| **Hybrid** | Most projects (RECOMMENDED) | ⭐⭐⭐⭐ | ⭐⭐⭐ Moderate |
| **Adaptive** | Experienced users | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ Very Complex |

**Not sure?** The orchestrator will help you decide!

See [docs/agentic-patterns/WHEN_TO_USE_WHAT.md](docs/agentic-patterns/WHEN_TO_USE_WHAT.md) for guidance.

## What Gets Built

The multi-agent system will create:

### Core Engine
- **Component System** - Modular building blocks for units
- **Unit Builder** - Assemble units from components
- **Battle Simulator** - Deterministic combat simulation
- **Event Logger** - Complete battle history for replay

### Features
- Theme-agnostic architecture (space ships, mechs, armies, etc.)
- Data-driven configuration (JSON/YAML)
- Deterministic, reproducible battles
- CLI tool for running simulations
- Comprehensive test suite

### Deliverables
- Working simulation engine
- Example theme with components
- Command-line interface
- Complete documentation
- Test scenarios

## Project Vision

Build combat units from modular components, then watch them battle autonomously in deterministic simulations. The system is designed to support multiple themes:
- 🚀 Space ships (inspired by Space Arena)
- 🤖 Mech robots (Pacific Rim style)
- ⚓ Naval fleets
- ⚔️ Fantasy armies
- 🎨 Custom themes

## Multi-Agent System V2

### Core Agents

| Agent | Role | Execution |
|-------|------|-----------|
| **Orchestrator V2** | Master coordinator with pattern selection | Sequential |
| **Project Manager** | Planning & coordination | Sequential |
| **Architect** | System design | Can run in parallel (3+ specialists) |
| **Developer** | Implementation | Can run in parallel (per feature) |
| **QA Tester** | Quality assurance | Can run in parallel (per test area) |
| **Documentation** | Technical writing | Can run in parallel (per doc type) |

### Coordinators (NEW!)

| Coordinator | Purpose |
|-------------|---------|
| **Parallel Coordinator** | Launches and manages concurrent agents |
| **Task Synthesizer** | Merges outputs from parallel agents |

### Workflow Patterns

| Pattern | Description | Files |
|---------|-------------|-------|
| **Sequential** | Traditional waterfall | `.claude/commands/patterns/sequential-workflow.md` |
| **Parallel** | Maximum concurrency | `.claude/commands/patterns/parallel-workflow.md` |
| **Hybrid** | Sequential phases, parallel tasks | `.claude/commands/patterns/hybrid-workflow.md` |
| **Adaptive** | Context-driven strategy per phase | `.claude/commands/patterns/adaptive-workflow.md` |

## Documentation

### Getting Started
- **[prompt.md](prompt.md)** - Complete project requirements
- **[HOW_TO_USE_MULTI_AGENT.md](HOW_TO_USE_MULTI_AGENT.md)** - Multi-agent usage guide

### Learning Resources
- **[docs/agentic-patterns/AGENTIC_PATTERNS.md](docs/agentic-patterns/AGENTIC_PATTERNS.md)** - Complete pattern guide
- **[docs/agentic-patterns/WHEN_TO_USE_WHAT.md](docs/agentic-patterns/WHEN_TO_USE_WHAT.md)** - Decision framework
- **[docs/agentic-patterns/PARALLEL_EXECUTION_GUIDE.md](docs/agentic-patterns/PARALLEL_EXECUTION_GUIDE.md)** - Technical guide
- **[docs/agentic-patterns/LESSONS_LEARNED_TEMPLATE.md](docs/agentic-patterns/LESSONS_LEARNED_TEMPLATE.md)** - Track your learnings

### Agent Definitions
- **[.claude/commands/](.claude/commands/)** - Core agents
- **[.claude/commands/patterns/](.claude/commands/patterns/)** - Workflow patterns
- **[.claude/commands/coordinators/](.claude/commands/coordinators/)** - Parallel coordinators

## Timeline

**Target:** Weekend project (2 days)

- **Day 1:** Core architecture and data structures
- **Day 2:** Combat simulation, polish, testing, docs

## Getting Started

### Prerequisites

- Claude Code with slash command support
- Git for version control
- Python 3.10+ (will be set up by agents)

### Initialize Project (V2 Enhanced)

```bash
# Recommended: Start with enhanced orchestrator
/orchestrator-v2 prompt.md
```

The V2 orchestrator offers:
- Pattern selection guidance
- Parallel agent execution
- Time savings metrics
- Adaptive strategies

**Or use a specific pattern:**
```bash
/hybrid-workflow prompt.md    # Recommended for this project
/parallel-workflow prompt.md  # Maximum speed
/sequential-workflow prompt.md  # Learning basics
/adaptive-workflow prompt.md  # Advanced users
```

### Learning Value

This project is designed as a **learning laboratory** for agentic workflows:

**You'll learn:**
- ✅ How to coordinate multiple AI agents
- ✅ When to use parallel vs sequential execution
- ✅ How to synthesize diverse agent outputs
- ✅ Trade-offs between different patterns
- ✅ Real-world agent coordination strategies

**Professional Applications:**
- Team coordination patterns
- Multi-LLM system design
- Parallel workflow optimization
- Context-aware decision making

Even if you can't use autonomous agents at work, these **coordination principles transfer** to team management, system architecture, and AI system design.

## Architecture Overview

```
battle-automata-engine/
├── src/              # Core engine code
│   ├── core/        # Component, Unit, Battle classes
│   ├── mechanics/   # Combat, movement, targeting
│   └── utils/       # Loading, validation, logging
├── data/            # Game data (components, units, battles)
│   └── themes/      # Theme definitions
├── tests/           # Test suite
├── docs/            # Documentation
└── examples/        # Usage examples
```

## Key Concepts

### Components
Modular parts that make up units:
- **Offensive**: Weapons, turrets
- **Defensive**: Armor, shields
- **Mobility**: Engines, thrusters
- **Support**: Power, sensors

### Units
Assemblies of components with:
- Layout and positioning
- Resource constraints
- Validation rules

### Battles
Deterministic simulations featuring:
- Turn-based with time steps
- Positional combat
- Component damage
- Complete event logging

## Development Workflow

The multi-agent system follows this workflow:

```
Orchestrator → Project Manager → Architect → Developer ↔ QA Tester → Documentation
                      ↓                                        ↓              ↓
                Human Gates                              Human Gates    Human Gate
```

Human validation is requested at key milestones for approval and feedback.

## Contributing

This project is developed through the multi-agent system. To contribute:

1. Review the [prompt.md](prompt.md) requirements
2. Use the appropriate agent for your task
3. Follow the workflow and validation gates
4. Ensure tests pass before moving forward

## Inspiration

Inspired by **Space Arena** - a mobile game where players build spaceships from modular components and watch them fight autonomously in deterministic battles.

The core concept: design → build → simulate → iterate.

## License

To be determined (will be set by project owner)

## Status

✅ **Enhanced multi-agent system V2 complete!**
- ✅ 4 workflow patterns implemented
- ✅ Parallel execution with Task tool
- ✅ Specialized coordinators ready
- ✅ Comprehensive documentation
- ⏳ Architecture design pending
- ⏳ Implementation pending
- ⏳ Testing pending
- ⏳ Engine documentation pending

**Ready to start development!** Run `/orchestrator-v2 prompt.md` to begin.

## What Makes This Special

This isn't just a game engine project - it's an **advanced multi-agent coordination system** that demonstrates:

1. **Parallel Agent Execution** - True concurrent AI agent coordination
2. **Multiple Workflow Patterns** - 4 different strategies to choose from
3. **Synthesis & Integration** - Combining diverse agent outputs
4. **Learning Laboratory** - Experiment and compare approaches
5. **Professional Transferable Skills** - Coordination patterns for work

**Time Savings:** 40-75% faster than sequential approaches!

---

Built with ❤️ using Claude's enhanced multi-agent development system V2

**Contributing:** This is a learning project. Feel free to fork, experiment with different patterns, and share your learnings!
