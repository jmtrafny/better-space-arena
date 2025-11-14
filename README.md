# Battle Automata Engine

A theme-agnostic engine for simulating deterministic battles between customizable automata, inspired by the mobile game Space Arena.

## Project Status

🏗️ **Setup Complete** - Multi-agent development system ready

This repository contains a sophisticated multi-agent system designed to coordinate the development of the Battle Automata Engine through specialized AI agents.

## Quick Start

To begin building this project using the multi-agent system:

```bash
/orchestrator prompt.md
```

This will initiate a coordinated workflow through:
1. **Planning** - Project breakdown and task management
2. **Architecture** - System design and technical specifications
3. **Development** - Iterative feature implementation
4. **Testing** - Quality assurance and validation
5. **Documentation** - Comprehensive guides and references

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

## Multi-Agent System

This project uses specialized AI agents for development:

| Agent | Role | Purpose |
|-------|------|---------|
| **Orchestrator** | Master coordinator | Manages entire workflow |
| **Project Manager** | Coordination & planning | Breaks down tasks, tracks progress |
| **Architect** | System design | Creates architecture and specs |
| **Developer** | Implementation | Writes code and tests |
| **QA Tester** | Quality assurance | Tests and finds bugs |
| **Documentation** | Technical writing | Creates comprehensive docs |

See [HOW_TO_USE_MULTI_AGENT.md](HOW_TO_USE_MULTI_AGENT.md) for detailed usage instructions.

## Documentation

- **[prompt.md](prompt.md)** - Complete project requirements and specification
- **[HOW_TO_USE_MULTI_AGENT.md](HOW_TO_USE_MULTI_AGENT.md)** - Guide to using the multi-agent system
- **[.claude/commands/](.claude/commands/)** - Agent definitions

## Timeline

**Target:** Weekend project (2 days)

- **Day 1:** Core architecture and data structures
- **Day 2:** Combat simulation, polish, testing, docs

## Getting Started

### Prerequisites

- Claude Code with slash command support
- Git for version control
- Python 3.10+ (will be set up by agents)

### Initialize Project

```bash
# Start the multi-agent workflow
/orchestrator prompt.md
```

The orchestrator will:
1. Create project plan
2. Design architecture
3. Implement features
4. Test functionality
5. Generate documentation

### Manual Agent Usage

You can also invoke specific agents:

```bash
# Plan next steps
/project-manager Review progress and plan next iteration

# Design a system
/architect Design the combat simulation engine

# Implement a feature
/developer Implement component loading from JSON

# Test functionality
/qa-tester Test the battle simulation for determinism

# Create documentation
/documentation Write getting started guide
```

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

✅ Multi-agent system configured
⏳ Architecture design pending
⏳ Implementation pending
⏳ Testing pending
⏳ Documentation pending

**Ready to start development!** Run `/orchestrator prompt.md` to begin.

---

Built with ❤️ using Claude's multi-agent development system
