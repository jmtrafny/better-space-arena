# Integration Architecture Summary
## Battle Automata Engine

**Quick Reference Guide**

---

## Architecture at a Glance

### System Overview

```
┌────────────────────────────────────────────────────────┐
│                   USER INTERFACES                      │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐  │
│  │     CLI      │  │   Web API    │  │  Python SDK │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬──────┘  │
└─────────┼──────────────────┼─────────────────┼─────────┘
          │                  │                 │
┌─────────┴──────────────────┴─────────────────┴─────────┐
│                    PUBLIC API LAYER                     │
│  Component API │ Unit API │ Battle API │ Theme API      │
└─────────────────────────────┬───────────────────────────┘
                              │
┌─────────────────────────────┴───────────────────────────┐
│                    CORE ENGINE LAYER                     │
│  Component System │ Unit Builder │ Battle Orchestrator  │
└─────────────────────────────┬───────────────────────────┘
                              │
┌─────────────────────────────┴───────────────────────────┐
│                   MECHANICS LAYER                        │
│  Movement │ Targeting │ Damage │ Effects │ Physics      │
└─────────────────────────────┬───────────────────────────┘
                              │
┌─────────────────────────────┴───────────────────────────┐
│                   UTILITIES LAYER                        │
│  Loader │ Validator │ Logger │ Serializer │ RNG         │
└──────────────────────────────────────────────────────────┘
```

---

## Public API Quick Reference

### Component API

```python
from battle_automata.api import Component, ComponentRegistry

# Load component
component = Component.from_file("laser_cannon.yaml")

# Use registry
registry = ComponentRegistry()
registry.load_from_directory("data/themes/space-ships/components")
laser = registry.get("laser_cannon_mk1")
```

### Unit API

```python
from battle_automata.api import Unit, UnitBuilder

# Load unit
unit = Unit.from_file("fighter.yaml")

# Build unit programmatically
unit = (UnitBuilder("Fighter", "space-ships")
    .with_layout((10, 10))
    .with_resources(power=100, weight=500, slots=10)
    .add_component("laser_cannon", (5, 2), "forward")
    .add_component("engine", (5, 8), "rear")
    .build())
```

### Battle API

```python
from battle_automata.api import Battle, BattleConfig

# Create battle
battle = Battle(unit1, unit2, config=BattleConfig(seed=12345))

# Simulate
result = battle.simulate()

# Access results
print(f"Winner: {result.winner}")
print(f"Duration: {result.duration}s")
```

### Engine API (Facade)

```python
from battle_automata.api import initialize, get_engine

# Initialize once
engine = initialize(data_directory="./data")

# Use everywhere
engine = get_engine()
result = engine.simulate_battle("fighter.yaml", "tank.yaml", seed=12345)
```

---

## CLI Command Reference

### Essential Commands

```bash
# Initialize project
battle-sim init --theme space-ships

# List components
battle-sim component list --type offensive

# Create unit
battle-sim unit create --theme space-ships fighter.yaml

# Simulate battle
battle-sim battle simulate fighter.yaml tank.yaml --seed 12345

# Run tournament
battle-sim battle tournament unit1.yaml unit2.yaml unit3.yaml
```

### Command Structure

```
battle-sim
├── init                    # Project initialization
├── theme                   # Theme management
│   ├── list
│   ├── info <theme>
│   └── validate <path>
├── component               # Component operations
│   ├── list [--type]
│   ├── show <id>
│   ├── create <output>
│   └── validate <file>
├── unit                    # Unit operations
│   ├── list [--theme]
│   ├── show <id>
│   ├── create <output>
│   ├── validate <file>
│   └── export <file>
├── battle                  # Battle simulation
│   ├── simulate <u1> <u2>
│   ├── tournament <units>
│   ├── replay <log>
│   └── analyze <log>
└── server                  # Development server
    └── start
```

---

## Project Structure Quick Reference

```
better-space-arena/
│
├── src/battle_automata/           # Source code
│   ├── api/                       # Public API (IMPORT FROM HERE)
│   │   ├── component.py
│   │   ├── unit.py
│   │   ├── battle.py
│   │   ├── theme.py
│   │   └── engine.py
│   ├── core/                      # Core implementation (INTERNAL)
│   ├── mechanics/                 # Game mechanics (INTERNAL)
│   ├── utils/                     # Utilities (INTERNAL)
│   ├── cli/                       # CLI implementation
│   └── schemas/                   # JSON schemas
│
├── data/                          # Game data
│   ├── config/                    # Engine configuration
│   └── themes/                    # Theme directory
│       └── space-ships/           # Example theme
│           ├── theme.yaml
│           ├── components/        # Component definitions
│           │   ├── offensive/
│           │   ├── defensive/
│           │   ├── mobility/
│           │   └── support/
│           └── units/             # Preset units
│
├── tests/                         # Test suite
│   ├── unit/                      # Unit tests
│   ├── integration/               # Integration tests
│   ├── e2e/                       # End-to-end tests
│   └── fixtures/                  # Test data
│
├── docs/                          # Documentation
│   ├── INTEGRATION_ARCHITECTURE.md
│   ├── user-guide/
│   ├── developer-guide/
│   └── api/
│
└── examples/                      # Example code
```

---

## Module Dependencies

### Allowed Imports

```python
# ✅ External code - Use PUBLIC API
from battle_automata.api import Engine, Unit, Battle, Component

# ✅ Internal modules - Import from same layer or below
# In core/unit.py
from battle_automata.core.component import ComponentImpl
from battle_automata.utils.validator import validate_schema

# ✅ Type hints only
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from battle_automata.core.battle import BattleEngine
```

### Forbidden Imports

```python
# ❌ External code - Don't skip API layer
from battle_automata.core.battle import BattleEngine

# ❌ Circular dependencies
# In core/component.py importing from core/unit.py
# when core/unit.py imports from core/component.py

# ❌ Upward dependencies
# In utils/ importing from core/
```

### Dependency Hierarchy

```
CLI/Web → API → Core → Mechanics → Utils
           ↓      ↓       ↓          ↓
        Theme → Utils   Utils      stdlib
```

---

## Data Format Examples

### Component Definition (YAML)

```yaml
id: laser_cannon_mk1
name: "Laser Cannon Mk1"
type: offensive
category: weapon

stats:
  damage: 50
  range: 100
  fire_rate: 1.0
  accuracy: 0.85

resources:
  power_draw: 20
  weight: 50
  slots: 1

special:
  damage_type: energy
  armor_piercing: 0.3
```

### Unit Definition (YAML)

```yaml
id: fighter_mk1
name: "Fighter Mk1"
theme: space-ships

layout:
  size: [10, 10]

components:
  - component_id: laser_cannon_mk1
    position: [5, 2]
    facing: forward

  - component_id: engine_basic
    position: [5, 8]
    facing: rear

resources:
  power: 100
  weight_limit: 500
  slot_limit: 10
```

---

## Build Commands

### Development

```bash
# Install for development
make install-dev

# Run tests
make test
make test-cov        # With coverage
make test-watch      # Watch mode

# Code quality
make lint            # Check code
make format          # Format code
make typecheck       # Type checking
```

### Build & Deploy

```bash
# Build package
make build

# Run locally
pip install -e .
battle-sim --version

# Docker
make docker-build
make docker-run
```

---

## Testing Strategy

### Test Types

| Type | Location | Purpose | Command |
|------|----------|---------|---------|
| Unit | `tests/unit/` | Test individual functions | `make test-unit` |
| Integration | `tests/integration/` | Test module interactions | `make test-integration` |
| E2E | `tests/e2e/` | Test complete workflows | `make test-e2e` |

### Key Test Areas

1. **Determinism**: Same seed = same result
2. **Validation**: Invalid data rejected
3. **API Contracts**: Public API stability
4. **Performance**: Simulation speed benchmarks
5. **CLI**: Command functionality

---

## Configuration

### Engine Configuration

```yaml
# data/config/engine.yaml

engine:
  version: "0.1.0"
  data_directory: "./data"

simulation:
  default_seed: null
  time_step: 0.1
  max_duration: 300.0

themes:
  active: "space-ships"
  directory: "./data/themes"
```

### Development Configuration

```python
# pyproject.toml

[project]
name = "battle-automata"
version = "0.1.0"
requires-python = ">=3.10"

dependencies = [
    "pydantic>=2.0.0",
    "pyyaml>=6.0",
    "click>=8.1.0",
    "rich>=13.0.0",
]

[project.scripts]
battle-sim = "battle_automata.cli.main:cli"
```

---

## Extension Points

### How to Extend

1. **New Component Types**
   - Add component definition YAML
   - No code changes needed

2. **New Themes**
   - Create theme directory
   - Add components and units
   - Update theme.yaml metadata

3. **Custom Mechanics**
   - Extend mechanics module
   - Register via plugin system

4. **Custom CLI Commands**
   - Add command in `cli/commands/`
   - Register in `cli/main.py`

5. **Web API Endpoints**
   - Add route in `web/routes/`
   - Register in `web/app.py`

---

## Performance Guidelines

### Best Practices

1. **Cache Components**: Load once, reuse
2. **Lazy Load Themes**: Load on-demand
3. **Parallel Battles**: Use multiprocessing for tournaments
4. **Profiling**: Enable profiling in development

### Optimization Targets

- Component loading: < 10ms per component
- Unit validation: < 50ms per unit
- Battle simulation: > 100 turns/second
- API response time: < 100ms

---

## Error Handling

### Exception Hierarchy

```python
BattleAutomataError                 # Base exception
├── ValidationError                 # Data validation
├── ComponentError                  # Component issues
├── UnitError                       # Unit building/validation
├── BattleError                     # Simulation errors
└── ThemeError                      # Theme loading/validation
```

### Error Response Format

```python
{
    "error": "ValidationError",
    "message": "Invalid component configuration",
    "details": {
        "field": "stats.damage",
        "issue": "Must be non-negative"
    }
}
```

---

## Development Workflow

### Quick Start

```bash
# 1. Clone and setup
git clone <repo>
cd better-space-arena
make install-dev

# 2. Run tests
make test

# 3. Make changes
# ... edit code ...

# 4. Check quality
make lint format

# 5. Run tests again
make test-cov

# 6. Try it out
battle-sim battle simulate \
  data/themes/space-ships/units/fighter.yaml \
  data/themes/space-ships/units/tank.yaml
```

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/new-mechanic

# Make changes, commit
git add .
git commit -m "Add new targeting mechanic"

# Push and create PR
git push origin feature/new-mechanic
```

---

## Resources

### Documentation

- Full Architecture: [`INTEGRATION_ARCHITECTURE.md`](/home/user/better-space-arena/docs/INTEGRATION_ARCHITECTURE.md)
- User Guide: `docs/user-guide/`
- Developer Guide: `docs/developer-guide/`
- API Reference: `docs/api/`

### Key Files

- Main API: `src/battle_automata/api/`
- CLI Entry: `src/battle_automata/cli/main.py`
- Build Config: `pyproject.toml`
- Make Commands: `Makefile`

---

## Quick Decision Matrix

### When to use what?

| Use Case | Tool/Pattern |
|----------|-------------|
| Use engine in Python | Import from `battle_automata.api` |
| Run battle from terminal | `battle-sim battle simulate` |
| Create new component | Edit YAML, or `battle-sim component create` |
| Build unit | `battle-sim unit create --interactive` |
| Test changes | `make test` |
| Deploy | `make build && make publish` |
| Extend mechanics | Subclass in `mechanics/` module |
| Add CLI command | Add to `cli/commands/` |

---

## Version Compatibility

| Version | Python | Features |
|---------|--------|----------|
| 0.1.x | 3.10+ | Core engine, CLI, basic themes |
| 0.2.x | 3.10+ | Web API, advanced mechanics |
| 1.0.x | 3.10+ | Stable API, production ready |

### API Stability Promise

- **Major version**: Breaking changes allowed
- **Minor version**: New features, backward compatible
- **Patch version**: Bug fixes only

---

## Support and Contributing

### Getting Help

1. Check documentation
2. Search issues on GitHub
3. Ask in discussions
4. Create issue if bug

### Contributing

1. Read `CONTRIBUTING.md`
2. Fork repository
3. Create feature branch
4. Submit pull request
5. Wait for review

---

**Document Version**: 1.0
**Last Updated**: 2025-11-14
**Full Architecture**: See [`INTEGRATION_ARCHITECTURE.md`](/home/user/better-space-arena/docs/INTEGRATION_ARCHITECTURE.md)