# Architecture Deliverable - Project Structure & Build System
## Battle Automata Engine

**Date:** 2025-11-13
**Architect:** Project Organization Specialist
**Status:** Complete - Ready for Implementation

---

## Executive Summary

A complete project structure, build system, and deployment architecture has been designed for the Battle Automata Engine. This deliverable provides all necessary specifications to begin implementation immediately.

### What's Delivered

1. **Complete Directory Structure** - 100+ directories and files specified
2. **Package Configuration** - Full `pyproject.toml` with all dependencies
3. **CLI Interface** - Complete command hierarchy with 20+ commands
4. **Data Organization** - Theme structure and data schemas
5. **Build System** - Makefile with development workflow
6. **Distribution** - PyPI and Docker deployment strategies
7. **Modding Support** - Plugin architecture and extension mechanisms

---

## Key Design Decisions

| Aspect | Decision | Rationale |
|--------|----------|-----------|
| **Python Version** | 3.10+ | Modern features, excellent type hints |
| **Package Structure** | src-layout | Best practice for importable packages |
| **CLI Framework** | Click 8.x | Rich features, great UX |
| **Data Format** | YAML primary | Human-readable configurations |
| **Validation** | Pydantic v2 | Type safety, automatic validation |
| **Testing** | pytest | Industry standard |
| **Code Quality** | ruff + black + mypy | Fast, modern tooling |
| **Build Tool** | setuptools | Mature, widely supported |
| **Entry Point** | `battle-sim` | Clear, memorable CLI name |

---

## Directory Structure Overview

```
better-space-arena/
├── src/battle_automata/          # Source code
│   ├── api/                       # PUBLIC API
│   ├── core/                      # Core engine (internal)
│   ├── mechanics/                 # Game mechanics (internal)
│   ├── utils/                     # Utilities (internal)
│   ├── cli/                       # Command-line interface
│   └── schemas/                   # Pydantic schemas
│
├── data/                          # Game data (not in package)
│   ├── themes/                    # Theme definitions
│   ├── battles/                   # Battle scenarios
│   └── config/                    # Configuration files
│
├── tests/                         # Test suite
│   ├── unit/                      # Fast unit tests
│   ├── integration/               # Integration tests
│   └── e2e/                       # End-to-end tests
│
├── docs/                          # Documentation
│   ├── user-guide/
│   ├── developer-guide/
│   └── modding-guide/
│
├── examples/                      # Example code
├── scripts/                       # Development scripts
├── benchmarks/                    # Performance tests
│
├── pyproject.toml                 # Package configuration
├── Makefile                       # Development commands
└── README.md                      # Project README
```

---

## CLI Command Structure

```
battle-sim
├── init                           # Initialize project
├── theme                          # Theme management
│   ├── list
│   ├── info
│   └── validate
├── component                      # Component operations
│   ├── list
│   ├── show
│   ├── validate
│   └── create
├── unit                           # Unit operations
│   ├── list
│   ├── show
│   ├── validate
│   ├── create
│   └── info
├── battle                         # Battle simulation
│   ├── simulate
│   ├── replay
│   ├── tournament
│   └── analyze
└── config                         # Configuration
    ├── show
    └── set
```

### Example Usage

```bash
# Initialize a new project
battle-sim init --theme space-ships

# List available components
battle-sim component list --theme space-ships --type weapon

# Create a unit
battle-sim unit create fighter.yaml --interactive

# Simulate a battle
battle-sim battle simulate fighter.yaml bomber.yaml --seed 12345

# Run a tournament
battle-sim battle tournament "units/*.yaml" --rounds 5
```

---

## Package Configuration Highlights

### pyproject.toml

**Core Dependencies:**
- `pydantic>=2.0.0` - Data validation
- `pyyaml>=6.0` - YAML parsing
- `click>=8.0.0` - CLI framework
- `rich>=13.0.0` - Terminal output
- `numpy>=1.24.0` - Numerical operations

**Development Tools:**
- `pytest` - Testing framework
- `ruff` - Fast linting
- `black` - Code formatting
- `mypy` - Type checking
- `pre-commit` - Git hooks

**Optional Extras:**
- `[dev]` - Development dependencies
- `[web]` - Web API (FastAPI)
- `[docs]` - Documentation tools

---

## Data Organization

### Theme Structure

```
data/themes/space-ships/
├── theme.yaml                     # Theme metadata
├── components/                    # Component library
│   ├── weapons/
│   │   ├── laser_cannon_mk1.yaml
│   │   ├── missile_launcher.yaml
│   │   └── plasma_cannon.yaml
│   ├── armor/
│   ├── shields/
│   ├── engines/
│   └── power/
└── units/                         # Preset units
    ├── fighter.yaml
    ├── bomber.yaml
    └── frigate.yaml
```

### Component Schema Example

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
  cost: 100

special:
  damage_type: energy
  armor_piercing: 0.3
  shield_bonus: 1.5
```

---

## Build & Development Workflow

### Makefile Commands

```bash
# Installation
make install          # Install for production
make install-dev      # Install with dev dependencies

# Testing
make test            # Run all tests
make test-unit       # Unit tests only
make test-cov        # With coverage report

# Code Quality
make lint            # Run linting checks
make format          # Auto-format code
make typecheck       # Type checking

# Build & Package
make clean           # Remove build artifacts
make build           # Build distribution
make publish         # Publish to PyPI

# Documentation
make docs            # Generate docs
make docs-serve      # Serve docs locally

# Docker
make docker-build    # Build Docker image
make docker-run      # Run container

# CI Simulation
make ci              # Run full CI pipeline locally
```

### Development Setup

```bash
# 1. Clone repository
git clone https://github.com/yourusername/better-space-arena.git
cd better-space-arena

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install development dependencies
make install-dev

# 4. Verify setup
make test
make lint

# 5. Start developing!
```

---

## Distribution Strategies

### 1. PyPI Distribution

```bash
# Build package
make build

# Publish to PyPI
make publish

# Users install with:
pip install battle-automata
```

### 2. Docker Distribution

```bash
# Build image
docker build -t battle-automata:latest .

# Run
docker run -it --rm \
  -v $(pwd)/data:/app/data \
  battle-automata:latest init
```

### 3. Source Installation

```bash
# Clone and install
git clone <repo>
cd better-space-arena
pip install -e .
```

---

## Modding Support

### Custom Theme Structure

```
my-custom-theme/
├── theme.yaml              # Theme metadata
├── components/             # Custom components
│   ├── weapons/
│   ├── armor/
│   └── ...
└── units/                  # Custom units
```

### Creating Custom Themes

```bash
# 1. Create theme from template
battle-sim theme create my-theme --from space-ships

# 2. Add custom components (YAML files)
# Edit: data/themes/my-theme/components/weapons/custom_weapon.yaml

# 3. Validate theme
battle-sim theme validate my-theme

# 4. Use in battles
battle-sim battle simulate \
  --theme my-theme \
  unit1.yaml unit2.yaml
```

### Advanced: Custom Python Components

```python
# custom_components/plasma_weapon.py
from battle_automata.api import Component, ComponentRegistry

@ComponentRegistry.register('plasma_weapon')
class PlasmaWeapon(Component):
    """Custom weapon with heat mechanics."""

    def on_fire(self, target):
        # Custom firing logic
        pass
```

---

## Testing Strategy

### Test Pyramid

```
        /\
       /  \      e2e tests (few, slow)
      /    \
     /------\    integration tests (medium)
    /        \
   /----------\  unit tests (many, fast)
  /______________\
```

### Test Structure

```
tests/
├── unit/                          # Fast, isolated tests
│   ├── test_components.py
│   ├── test_units.py
│   └── test_validation.py
│
├── integration/                   # Module interaction tests
│   ├── test_battle_flow.py
│   └── test_theme_loading.py
│
└── e2e/                          # Complete workflow tests
    ├── test_full_battle.py
    └── test_determinism.py
```

### Running Tests

```bash
# All tests
make test

# Unit tests only (fast)
make test-unit

# With coverage
make test-cov

# Specific test file
pytest tests/unit/test_components.py -v

# Specific test
pytest tests/unit/test_components.py::test_component_validation -v
```

---

## Documentation Structure

```
docs/
├── INDEX.md                       # Documentation index
├── PROJECT_STRUCTURE.md           # This deliverable
├── ARCHITECTURE_SUMMARY.md        # Architecture overview
├── INTEGRATION_GUIDE.md           # Integration guide
│
├── user-guide/                    # For end users
│   ├── getting-started.md
│   ├── cli-reference.md
│   └── examples.md
│
├── developer-guide/               # For contributors
│   ├── api-reference.md
│   ├── extending-engine.md
│   └── testing-guide.md
│
└── modding-guide/                 # For modders
    ├── creating-themes.md
    ├── component-schema.md
    └── unit-schema.md
```

---

## CI/CD Pipeline

### GitHub Actions Workflow

```yaml
Jobs:
1. Lint
   - ruff check
   - black --check
   - isort --check
   - mypy

2. Test (Matrix)
   - OS: Ubuntu, macOS, Windows
   - Python: 3.10, 3.11, 3.12
   - Run pytest with coverage

3. Integration
   - Integration tests
   - End-to-end tests

4. Build
   - Build distribution
   - Check with twine
   - Upload artifacts
```

---

## Installation Instructions

### For End Users

```bash
# From PyPI
pip install battle-automata

# Verify installation
battle-sim --version

# Initialize project
battle-sim init
```

### For Developers

```bash
# Clone repository
git clone <repo>
cd better-space-arena

# Install development environment
make install-dev

# Run tests
make test
```

---

## Quick Start Guide

### 1. Install

```bash
pip install battle-automata
```

### 2. Initialize Project

```bash
battle-sim init --theme space-ships
cd my-project
```

### 3. Explore Components

```bash
battle-sim component list --theme space-ships
battle-sim component show laser_cannon_mk1
```

### 4. Create a Unit

```bash
battle-sim unit create my-fighter.yaml --interactive
```

### 5. Run a Battle

```bash
battle-sim battle simulate \
  data/themes/space-ships/units/fighter.yaml \
  data/themes/space-ships/units/bomber.yaml \
  --seed 12345
```

---

## Success Criteria

This architecture meets all project requirements:

- ✅ **Weekend MVP Ready**: Clear structure, minimal setup
- ✅ **Theme-Agnostic**: Easy to add new themes
- ✅ **Data-Driven**: Components and units in YAML
- ✅ **Modding Support**: Plugin architecture ready
- ✅ **CLI Tool**: Complete command structure
- ✅ **Professional Quality**: Production-ready package
- ✅ **Well Tested**: Comprehensive test structure
- ✅ **Well Documented**: Complete documentation structure
- ✅ **Cross-Platform**: Windows, macOS, Linux support
- ✅ **Easy to Extend**: Clear API boundaries

---

## Files Delivered

1. **PROJECT_STRUCTURE.md** (60KB)
   - Complete directory structure
   - Package configuration
   - CLI interface specification
   - Data organization
   - Build system
   - Distribution strategies
   - Modding support
   - Installation instructions

2. **ARCHITECTURE_DELIVERABLE.md** (This file)
   - Executive summary
   - Quick reference
   - Key decisions
   - Getting started guide

---

## Next Steps for Implementation

### Phase 1: Project Setup (30 minutes)

```bash
# 1. Create directory structure
mkdir -p src/battle_automata/{api,core,mechanics,utils,cli,schemas}
mkdir -p tests/{unit,integration,e2e,fixtures}
mkdir -p data/themes/space-ships/{components,units}
mkdir -p docs/{user-guide,developer-guide,modding-guide}

# 2. Copy configuration files
# - pyproject.toml
# - Makefile
# - .gitignore
# - .pre-commit-config.yaml

# 3. Initialize git
git init
git add .
git commit -m "Initial project structure"

# 4. Set up development environment
python -m venv venv
source venv/bin/activate
make install-dev
```

### Phase 2: Core Implementation (Day 1)

1. **Data Structures** (2 hours)
   - `src/battle_automata/utils/math.py` - Vector2D, Position
   - `src/battle_automata/core/entity.py` - Entity, World
   - `src/battle_automata/schemas/component.py` - Component schemas

2. **Data Loading** (2 hours)
   - `src/battle_automata/utils/loader.py` - YAML/JSON loading
   - `src/battle_automata/utils/validator.py` - Validation
   - `src/battle_automata/core/registry.py` - Component registry

3. **API Layer** (2 hours)
   - `src/battle_automata/api/engine.py` - Engine facade
   - `src/battle_automata/api/components.py` - Component API
   - `src/battle_automata/api/units.py` - Unit API

4. **Tests** (2 hours)
   - Write tests alongside implementation
   - Aim for 80%+ coverage

### Phase 3: Battle System (Day 2)

1. **Simulation Engine** (3 hours)
   - `src/battle_automata/core/simulation.py`
   - `src/battle_automata/mechanics/movement.py`
   - `src/battle_automata/mechanics/targeting.py`
   - `src/battle_automata/mechanics/damage.py`

2. **CLI Commands** (2 hours)
   - `src/battle_automata/cli/main.py`
   - `src/battle_automata/cli/commands/*.py`

3. **Example Data** (1 hour)
   - Create space-ships theme
   - 10+ components
   - 5+ preset units

4. **Integration Tests** (2 hours)
   - End-to-end battle simulation
   - Determinism validation
   - CLI testing

### Phase 4: Polish & Documentation (Ongoing)

1. **Documentation**
   - User guide
   - Developer guide
   - API reference

2. **Examples**
   - Simple battle script
   - Custom component example
   - Unit builder example

3. **Package**
   - Build distribution
   - Test installation
   - Publish to PyPI (if ready)

---

## Resources & References

### Documentation Files

- `PROJECT_STRUCTURE.md` - This complete specification
- `ARCHITECTURE_SUMMARY.md` - Architecture overview
- `INTEGRATION_ARCHITECTURE.md` - Integration details
- `SIMULATION_ENGINE_ARCHITECTURE.md` - Simulation engine design

### External Resources

- [PEP 621](https://peps.python.org/pep-0621/) - pyproject.toml specification
- [Click Documentation](https://click.palletsprojects.com/) - CLI framework
- [Pydantic Documentation](https://docs.pydantic.dev/) - Validation
- [pytest Documentation](https://docs.pytest.org/) - Testing

---

## Support & Contact

For questions or clarifications:

1. Review the detailed documentation in `docs/PROJECT_STRUCTURE.md`
2. Check the architecture diagrams in `docs/ARCHITECTURE_DIAGRAMS.md`
3. Refer to integration guide in `docs/INTEGRATION_GUIDE.md`
4. Contact the architecture team for specific questions

---

**Deliverable Status:** ✅ Complete
**Review Status:** ⏳ Awaiting Review
**Implementation Status:** 🟢 Ready to Begin

**Architect:** Project Organization Specialist
**Date:** 2025-11-13
**Version:** 1.0

---

This architecture provides a complete, production-ready foundation for the Battle Automata Engine. All specifications are detailed enough to begin implementation immediately with confidence.

**Ready to build an awesome battle simulation engine!** 🚀
