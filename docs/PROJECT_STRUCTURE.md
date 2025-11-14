# Battle Automata Engine - Project Structure & Build System

**Version:** 1.0
**Date:** 2025-11-13
**Status:** Architecture Specification
**Author:** Project Architect

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Directory Structure](#directory-structure)
3. [Package Configuration](#package-configuration)
4. [CLI Interface](#cli-interface)
5. [Data Organization](#data-organization)
6. [Build & Development](#build--development)
7. [Distribution](#distribution)
8. [Modding Support](#modding-support)
9. [Installation Instructions](#installation-instructions)

---

## Executive Summary

This document provides the complete project organization, build system, and deployment architecture for the Battle Automata Engine. The structure is designed to support:

- **Weekend MVP**: Fast initial development
- **Extensibility**: Easy to add themes, components, and features
- **Moddability**: Clear structure for community extensions
- **Professional quality**: Production-ready package structure
- **Cross-platform**: Windows, macOS, Linux support

### Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Package Manager** | pip + pyproject.toml | Modern Python standard (PEP 621) |
| **Build System** | setuptools | Widely supported, mature |
| **CLI Framework** | Click 8.x | Rich features, excellent UX |
| **Data Format** | YAML primary, JSON secondary | Human-readable configs, machine-readable serialization |
| **Validation** | Pydantic v2 | Type safety, automatic validation |
| **Testing** | pytest | Industry standard, rich plugin ecosystem |
| **Code Quality** | ruff + black + mypy | Fast, modern tooling |
| **Entry Point** | `battle-sim` command | Clear, memorable CLI name |

---

## Directory Structure

### Complete Project Layout

```
better-space-arena/
├── .github/                          # GitHub-specific files
│   └── workflows/
│       ├── ci.yml                    # CI/CD pipeline
│       └── publish.yml               # PyPI publishing workflow
│
├── .claude/                          # Multi-agent system (existing)
│   └── commands/                     # Agent definitions
│
├── src/                              # Source code (PUBLIC)
│   └── battle_automata/              # Main package
│       ├── __init__.py               # Package initialization
│       ├── __main__.py               # Entry point for python -m
│       │
│       ├── api/                      # PUBLIC API (import from here)
│       │   ├── __init__.py           # Export: initialize, Engine, Battle, Unit, etc.
│       │   ├── engine.py             # Engine facade
│       │   ├── components.py         # Component API
│       │   ├── units.py              # Unit API
│       │   ├── battles.py            # Battle API
│       │   └── themes.py             # Theme API
│       │
│       ├── core/                     # INTERNAL: Core engine
│       │   ├── __init__.py
│       │   ├── entity.py             # Entity/Component system
│       │   ├── world.py              # World container
│       │   ├── component.py          # Component base classes
│       │   ├── unit.py               # Unit assembly
│       │   ├── battle.py             # Battle orchestration
│       │   ├── simulation.py         # Simulation engine
│       │   └── registry.py           # Component registry
│       │
│       ├── mechanics/                # INTERNAL: Game mechanics
│       │   ├── __init__.py
│       │   ├── movement.py           # Movement system
│       │   ├── targeting.py          # Targeting system
│       │   ├── damage.py             # Damage calculations
│       │   ├── effects.py            # Status effects
│       │   └── ai.py                 # AI behaviors
│       │
│       ├── utils/                    # INTERNAL: Utilities
│       │   ├── __init__.py
│       │   ├── loader.py             # Data loading (YAML/JSON)
│       │   ├── validator.py          # Validation
│       │   ├── logger.py             # Event logging
│       │   ├── math.py               # Math utilities (Vector2D, etc.)
│       │   └── random.py             # Seeded RNG
│       │
│       ├── cli/                      # Command-line interface
│       │   ├── __init__.py
│       │   ├── main.py               # Main CLI entry point
│       │   ├── commands/             # CLI command groups
│       │   │   ├── __init__.py
│       │   │   ├── init.py           # Initialize project
│       │   │   ├── theme.py          # Theme management
│       │   │   ├── component.py      # Component operations
│       │   │   ├── unit.py           # Unit operations
│       │   │   ├── battle.py         # Battle simulation
│       │   │   └── config.py         # Configuration
│       │   └── output.py             # Output formatting
│       │
│       └── schemas/                  # JSON schemas
│           ├── __init__.py
│           ├── component.py          # Component schemas (Pydantic)
│           ├── unit.py               # Unit schemas
│           ├── battle.py             # Battle config schemas
│           └── theme.py              # Theme metadata schemas
│
├── data/                             # Game data (NOT in package)
│   ├── themes/                       # Theme directory
│   │   ├── space-ships/              # Default theme
│   │   │   ├── theme.yaml            # Theme metadata
│   │   │   ├── components/           # Component definitions
│   │   │   │   ├── weapons/
│   │   │   │   │   ├── laser_cannon_mk1.yaml
│   │   │   │   │   ├── laser_cannon_mk2.yaml
│   │   │   │   │   ├── missile_launcher.yaml
│   │   │   │   │   └── plasma_cannon.yaml
│   │   │   │   ├── armor/
│   │   │   │   │   ├── light_plating.yaml
│   │   │   │   │   ├── medium_plating.yaml
│   │   │   │   │   └── heavy_plating.yaml
│   │   │   │   ├── shields/
│   │   │   │   │   ├── basic_shield.yaml
│   │   │   │   │   └── advanced_shield.yaml
│   │   │   │   ├── engines/
│   │   │   │   │   ├── ion_engine.yaml
│   │   │   │   │   └── fusion_drive.yaml
│   │   │   │   └── power/
│   │   │   │       ├── fusion_reactor.yaml
│   │   │   │       └── solar_array.yaml
│   │   │   └── units/                # Preset units
│   │   │       ├── fighter.yaml
│   │   │       ├── bomber.yaml
│   │   │       ├── frigate.yaml
│   │   │       └── carrier.yaml
│   │   └── README.md                 # Theme creation guide
│   │
│   ├── battles/                      # Battle scenarios
│   │   ├── tutorial_01.yaml
│   │   ├── skirmish_01.yaml
│   │   └── campaign/
│   │       └── mission_01.yaml
│   │
│   └── config/                       # Configuration files
│       └── default.yaml              # Default battle settings
│
├── tests/                            # Test suite
│   ├── __init__.py
│   ├── conftest.py                   # Pytest configuration
│   │
│   ├── unit/                         # Unit tests (fast, isolated)
│   │   ├── __init__.py
│   │   ├── test_components.py
│   │   ├── test_units.py
│   │   ├── test_validation.py
│   │   ├── test_loader.py
│   │   └── test_math.py
│   │
│   ├── integration/                  # Integration tests
│   │   ├── __init__.py
│   │   ├── test_battle_flow.py
│   │   ├── test_theme_loading.py
│   │   └── test_cli.py
│   │
│   ├── e2e/                          # End-to-end tests
│   │   ├── __init__.py
│   │   ├── test_full_battle.py
│   │   └── test_determinism.py
│   │
│   └── fixtures/                     # Test data
│       ├── components/
│       ├── units/
│       └── battles/
│
├── docs/                             # Documentation
│   ├── INDEX.md                      # Documentation index
│   ├── ARCHITECTURE_SUMMARY.md       # Architecture overview
│   ├── ARCHITECTURE_DIAGRAMS.md      # Visual diagrams
│   ├── INTEGRATION_ARCHITECTURE.md   # Integration specs
│   ├── INTEGRATION_GUIDE.md          # Integration guide
│   ├── SIMULATION_ENGINE_ARCHITECTURE.md  # Simulation engine
│   ├── PROJECT_STRUCTURE.md          # This document
│   │
│   ├── user-guide/                   # User documentation
│   │   ├── getting-started.md
│   │   ├── cli-reference.md
│   │   ├── battle-configuration.md
│   │   └── examples.md
│   │
│   ├── developer-guide/              # Developer documentation
│   │   ├── api-reference.md
│   │   ├── extending-engine.md
│   │   ├── custom-mechanics.md
│   │   └── testing-guide.md
│   │
│   └── modding-guide/                # Modding documentation
│       ├── creating-themes.md
│       ├── component-schema.md
│       ├── unit-schema.md
│       └── examples.md
│
├── examples/                         # Example code
│   ├── README.md
│   ├── simple_battle.py              # Basic usage
│   ├── custom_component.py           # Creating components
│   ├── unit_builder.py               # Building units
│   ├── batch_simulation.py           # Running multiple battles
│   └── replay_viewer.py              # Replaying battles
│
├── scripts/                          # Development scripts
│   ├── setup_dev.sh                  # Setup dev environment
│   ├── validate_data.py              # Validate data files
│   ├── generate_docs.py              # Generate API docs
│   └── benchmark.py                  # Performance benchmarks
│
├── benchmarks/                       # Performance tests
│   ├── __init__.py
│   ├── bench_simulation.py
│   └── bench_loading.py
│
├── .gitignore                        # Git ignore rules
├── .editorconfig                     # Editor configuration
├── .pre-commit-config.yaml           # Pre-commit hooks
│
├── pyproject.toml                    # Package configuration (PEP 621)
├── setup.py                          # Setup script (for compatibility)
├── MANIFEST.in                       # Package manifest
│
├── requirements.txt                  # Production dependencies
├── requirements-dev.txt              # Development dependencies
│
├── Makefile                          # Development commands
├── README.md                         # Project README
├── LICENSE                           # License file
├── CHANGELOG.md                      # Version history
└── CONTRIBUTING.md                   # Contribution guidelines
```

### Directory Purposes

#### Source Code (`src/battle_automata/`)

| Directory | Access Level | Purpose |
|-----------|-------------|---------|
| `api/` | **PUBLIC** | Stable API for users to import |
| `core/` | **INTERNAL** | Core engine implementation |
| `mechanics/` | **INTERNAL** | Game mechanics systems |
| `utils/` | **INTERNAL** | Utility functions |
| `cli/` | **CLI** | Command-line interface |
| `schemas/` | **INTERNAL** | Pydantic validation schemas |

**Import Rules:**
```python
# GOOD: Import from public API
from battle_automata.api import Engine, Battle, Unit

# BAD: Don't import from internal modules
from battle_automata.core.entity import Entity  # Don't do this!
```

#### Data (`data/`)

| Directory | Purpose | Format |
|-----------|---------|--------|
| `themes/` | Theme definitions | YAML |
| `battles/` | Battle scenarios | YAML |
| `config/` | Configuration files | YAML |

**Note:** Data directory is NOT included in the Python package. Users create their own data directory when initializing projects.

#### Tests (`tests/`)

| Directory | Purpose | Speed |
|-----------|---------|-------|
| `unit/` | Unit tests | Fast (< 1s) |
| `integration/` | Integration tests | Medium (< 10s) |
| `e2e/` | End-to-end tests | Slow (> 10s) |
| `fixtures/` | Test data | N/A |

---

## Package Configuration

### pyproject.toml

Complete package configuration following PEP 621:

```toml
[build-system]
requires = ["setuptools>=65.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "battle-automata"
version = "0.1.0"
description = "A theme-agnostic engine for deterministic battle simulation between customizable automata"
readme = "README.md"
license = {text = "MIT"}
authors = [
    {name = "Battle Automata Team", email = "contact@example.com"}
]
maintainers = [
    {name = "Battle Automata Team", email = "contact@example.com"}
]
keywords = [
    "game",
    "simulation",
    "battle",
    "automata",
    "ecs",
    "strategy"
]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Intended Audience :: End Users/Desktop",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Games/Entertainment :: Simulation",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Typing :: Typed",
]
requires-python = ">=3.10"
dependencies = [
    "pydantic>=2.0.0,<3.0.0",
    "pyyaml>=6.0",
    "click>=8.0.0,<9.0.0",
    "rich>=13.0.0",
    "numpy>=1.24.0",
]

[project.optional-dependencies]
dev = [
    # Testing
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "pytest-xdist>=3.3.0",  # Parallel testing
    "pytest-benchmark>=4.0.0",

    # Code quality
    "ruff>=0.1.0",
    "black>=23.0.0",
    "mypy>=1.5.0",
    "isort>=5.12.0",

    # Development tools
    "pre-commit>=3.4.0",
    "ipython>=8.14.0",
    "ipdb>=0.13.13",
]
web = [
    "fastapi>=0.103.0",
    "uvicorn>=0.23.0",
]
docs = [
    "mkdocs>=1.5.0",
    "mkdocs-material>=9.2.0",
    "mkdocstrings[python]>=0.23.0",
]

[project.urls]
Homepage = "https://github.com/yourusername/better-space-arena"
Documentation = "https://better-space-arena.readthedocs.io"
Repository = "https://github.com/yourusername/better-space-arena"
"Bug Tracker" = "https://github.com/yourusername/better-space-arena/issues"

[project.scripts]
battle-sim = "battle_automata.cli.main:cli"

[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages.find]
where = ["src"]
include = ["battle_automata*"]
exclude = ["tests*", "docs*", "examples*"]

[tool.setuptools.package-data]
battle_automata = ["py.typed"]

# ============================================================================
# Development Tools Configuration
# ============================================================================

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_classes = "Test*"
python_functions = "test_*"
addopts = [
    "-v",
    "--strict-markers",
    "--tb=short",
    "--cov=battle_automata",
    "--cov-report=term-missing",
    "--cov-report=html",
]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: integration tests",
    "e2e: end-to-end tests",
]

[tool.coverage.run]
source = ["src"]
omit = [
    "*/tests/*",
    "*/test_*.py",
    "*/__main__.py",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
    "@abstractmethod",
]

[tool.black]
line-length = 100
target-version = ['py310']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
)/
'''

[tool.isort]
profile = "black"
line_length = 100
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
follow_imports = "normal"
strict_optional = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false

[tool.ruff]
line-length = 100
target-version = "py310"
select = [
    "E",  # pycodestyle errors
    "W",  # pycodestyle warnings
    "F",  # pyflakes
    "I",  # isort
    "C",  # flake8-comprehensions
    "B",  # flake8-bugbear
    "UP", # pyupgrade
]
ignore = [
    "E501",  # line too long (handled by black)
    "B008",  # do not perform function calls in argument defaults
    "C901",  # too complex
]

[tool.ruff.per-file-ignores]
"__init__.py" = ["F401"]  # Allow unused imports in __init__.py
```

### setup.py (Backward Compatibility)

Minimal setup.py for backward compatibility:

```python
#!/usr/bin/env python
"""
Setup script for backward compatibility.
Modern configuration is in pyproject.toml.
"""

from setuptools import setup

if __name__ == "__main__":
    setup()
```

### MANIFEST.in

Include non-Python files in distribution:

```text
include README.md
include LICENSE
include CHANGELOG.md
include requirements.txt
include requirements-dev.txt

recursive-include src/battle_automata py.typed
recursive-include docs *.md
recursive-include examples *.py
recursive-exclude tests *
recursive-exclude benchmarks *
recursive-exclude scripts *

global-exclude __pycache__
global-exclude *.py[co]
global-exclude .DS_Store
```

### requirements.txt

Production dependencies:

```text
pydantic>=2.0.0,<3.0.0
pyyaml>=6.0
click>=8.0.0,<9.0.0
rich>=13.0.0
numpy>=1.24.0
```

### requirements-dev.txt

Development dependencies:

```text
-r requirements.txt

# Testing
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-xdist>=3.3.0
pytest-benchmark>=4.0.0

# Code quality
ruff>=0.1.0
black>=23.0.0
mypy>=1.5.0
isort>=5.12.0

# Development tools
pre-commit>=3.4.0
ipython>=8.14.0
ipdb>=0.13.13
```

---

## CLI Interface

### Command Structure

```
battle-sim                          # Main command
├── init                            # Initialize project
│   ├── [--theme THEME]
│   └── [--directory DIR]
│
├── theme                           # Theme management
│   ├── list                        # List available themes
│   ├── info THEME                  # Show theme details
│   └── validate THEME              # Validate theme data
│
├── component                       # Component operations
│   ├── list [--theme THEME] [--type TYPE]
│   ├── show COMPONENT_ID [--theme THEME]
│   ├── validate FILE
│   └── create [--interactive] OUTPUT
│
├── unit                            # Unit operations
│   ├── list [--theme THEME]
│   ├── show UNIT_ID [--theme THEME]
│   ├── validate FILE
│   ├── create [--interactive] OUTPUT
│   └── info FILE                   # Show unit stats
│
├── battle                          # Battle simulation
│   ├── simulate UNIT1 UNIT2 [OPTIONS]
│   ├── replay RESULT_FILE
│   ├── tournament UNIT_PATTERN [OPTIONS]
│   └── analyze RESULT_FILE
│
└── config                          # Configuration
    ├── show                        # Show current config
    └── set KEY VALUE               # Set config value
```

### CLI Implementation

#### Main Entry Point (`src/battle_automata/cli/main.py`)

```python
"""
Main CLI entry point.
"""

import click
from rich.console import Console

from battle_automata import __version__
from battle_automata.cli.commands import (
    battle,
    component,
    config,
    init,
    theme,
    unit,
)

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="battle-sim")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.option("--quiet", "-q", is_flag=True, help="Suppress non-error output")
@click.pass_context
def cli(ctx: click.Context, verbose: bool, quiet: bool) -> None:
    """
    Battle Automata Engine - Deterministic battle simulation system.

    Create units from modular components, then simulate deterministic battles
    between automata. Supports multiple themes and custom components.
    """
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["quiet"] = quiet


# Register command groups
cli.add_command(init.init_cmd)
cli.add_command(theme.theme_group)
cli.add_command(component.component_group)
cli.add_command(unit.unit_group)
cli.add_command(battle.battle_group)
cli.add_command(config.config_group)


if __name__ == "__main__":
    cli()
```

#### Init Command (`src/battle_automata/cli/commands/init.py`)

```python
"""
Initialize a new Battle Automata project.
"""

import click
from pathlib import Path
from rich.console import Console

console = Console()


@click.command("init")
@click.option(
    "--theme",
    default="space-ships",
    help="Theme to initialize with",
    show_default=True,
)
@click.option(
    "--directory",
    "-d",
    type=click.Path(),
    default=".",
    help="Target directory",
    show_default=True,
)
def init_cmd(theme: str, directory: str) -> None:
    """
    Initialize a new Battle Automata project.

    Creates the necessary directory structure and copies
    example theme data.

    Examples:
        battle-sim init
        battle-sim init --theme mechs --directory ./my-project
    """
    target = Path(directory).resolve()

    console.print(f"[bold blue]Initializing Battle Automata project...[/]")
    console.print(f"Directory: {target}")
    console.print(f"Theme: {theme}")

    # Create directory structure
    directories = [
        target / "data" / "themes",
        target / "data" / "battles",
        target / "data" / "config",
        target / "results",
        target / "custom_components",
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        console.print(f"✓ Created {directory.relative_to(target)}")

    # Copy theme data
    # ... (implementation)

    console.print("[bold green]✓ Project initialized successfully![/]")
    console.print("\nNext steps:")
    console.print("  1. View available components: battle-sim component list")
    console.print("  2. Create a unit: battle-sim unit create my-unit.yaml")
    console.print("  3. Run a battle: battle-sim battle simulate unit1.yaml unit2.yaml")
```

#### Battle Command (`src/battle_automata/cli/commands/battle.py`)

```python
"""
Battle simulation commands.
"""

import click
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()


@click.group("battle")
def battle_group() -> None:
    """Battle simulation commands."""
    pass


@battle_group.command("simulate")
@click.argument("unit1", type=click.Path(exists=True))
@click.argument("unit2", type=click.Path(exists=True))
@click.option("--seed", type=int, help="Random seed for deterministic results")
@click.option("--max-turns", type=int, default=1000, help="Maximum simulation turns")
@click.option("--output", "-o", type=click.Path(), help="Save results to file")
@click.option("--verbose", "-v", is_flag=True, help="Show detailed battle log")
@click.option("--format", type=click.Choice(["text", "json", "yaml"]), default="text")
def simulate(
    unit1: str,
    unit2: str,
    seed: int | None,
    max_turns: int,
    output: str | None,
    verbose: bool,
    format: str,
) -> None:
    """
    Simulate a battle between two units.

    Examples:
        battle-sim battle simulate fighter.yaml bomber.yaml
        battle-sim battle simulate unit1.yaml unit2.yaml --seed 12345 -o result.json
    """
    from battle_automata.api import Engine, BattleConfig

    console.print(f"[bold blue]Starting battle simulation...[/]")
    console.print(f"Unit 1: {unit1}")
    console.print(f"Unit 2: {unit2}")

    if seed:
        console.print(f"Seed: {seed}")

    # Initialize engine
    engine = Engine()

    # Load units
    unit1_obj = engine.load_unit(Path(unit1))
    unit2_obj = engine.load_unit(Path(unit2))

    # Configure battle
    config = BattleConfig(
        seed=seed or 0,
        max_turns=max_turns,
    )

    # Run simulation
    with console.status("[bold green]Simulating battle..."):
        result = engine.simulate_battle(unit1_obj, unit2_obj, config)

    # Display results
    console.print("\n[bold green]Battle Complete![/]")
    console.print(f"Winner: {result.winner}")
    console.print(f"Duration: {result.duration:.1f}s ({result.turns} turns)")

    # Show statistics table
    stats_table = Table(title="Battle Statistics")
    stats_table.add_column("Metric", style="cyan")
    stats_table.add_column("Value", style="magenta")

    for key, value in result.statistics.items():
        stats_table.add_row(key, str(value))

    console.print(stats_table)

    # Save results
    if output:
        result.save(Path(output))
        console.print(f"\n✓ Results saved to {output}")


@battle_group.command("tournament")
@click.argument("unit_pattern")
@click.option("--rounds", type=int, default=1, help="Rounds per matchup")
@click.option("--seed-start", type=int, default=0, help="Starting seed")
@click.option("--output", "-o", type=click.Path(), help="Save results to file")
def tournament(
    unit_pattern: str,
    rounds: int,
    seed_start: int,
    output: str | None,
) -> None:
    """
    Run a round-robin tournament between units.

    Examples:
        battle-sim battle tournament "units/*.yaml" --rounds 5
    """
    # Implementation
    pass
```

### Command Examples

```bash
# Initialize a new project
battle-sim init --theme space-ships

# List available themes
battle-sim theme list

# List components
battle-sim component list --theme space-ships --type weapon

# Show component details
battle-sim component show laser_cannon_mk1 --theme space-ships

# Create a new unit interactively
battle-sim unit create fighter.yaml --interactive

# Validate a unit
battle-sim unit validate fighter.yaml

# Simulate a battle
battle-sim battle simulate fighter.yaml bomber.yaml --seed 12345

# Run a tournament
battle-sim battle tournament "units/*.yaml" --rounds 5 --output results.json

# Replay a battle
battle-sim battle replay results.json

# Analyze battle results
battle-sim battle analyze results.json
```

---

## Data Organization

### Theme Structure

Each theme is a self-contained directory:

```
data/themes/space-ships/
├── theme.yaml              # Theme metadata
├── components/             # Component library
│   ├── weapons/
│   ├── armor/
│   ├── shields/
│   ├── engines/
│   └── power/
└── units/                  # Preset units
    ├── fighter.yaml
    ├── bomber.yaml
    └── frigate.yaml
```

### Theme Metadata (`theme.yaml`)

```yaml
# Theme metadata
id: space-ships
name: "Space Ships"
version: "1.0.0"
description: >
  Sci-fi space combat theme featuring energy weapons, shields,
  and ion engines. Inspired by Space Arena.

author: "Battle Automata Team"
license: "MIT"

# Component categories
component_categories:
  - id: weapon
    name: "Weapons"
    types: [laser, missile, plasma, kinetic]

  - id: armor
    name: "Armor"
    types: [light, medium, heavy]

  - id: shield
    name: "Shields"
    types: [basic, advanced, reactive]

  - id: engine
    name: "Engines"
    types: [ion, fusion, antimatter]

  - id: power
    name: "Power Systems"
    types: [reactor, solar, battery]

# Resource types
resources:
  - id: power
    name: "Power"
    unit: "W"
    description: "Energy generation and consumption"

  - id: weight
    name: "Weight"
    unit: "kg"
    description: "Mass of components"

  - id: slots
    name: "Slots"
    unit: "slots"
    description: "Physical grid space"

# Default unit constraints
default_constraints:
  max_power: 1000
  max_weight: 5000
  max_slots: 100
  max_cost: 10000
```

### Component Schema

Components are defined in YAML:

```yaml
# data/themes/space-ships/components/weapons/laser_cannon_mk1.yaml
id: laser_cannon_mk1
name: "Laser Cannon Mk1"
type: offensive
category: weapon

description: >
  Basic energy weapon with good accuracy and fire rate.
  Effective against shields, less so against armor.

# Combat statistics
stats:
  damage: 50
  range: 100
  fire_rate: 1.0          # shots per second
  accuracy: 0.85
  projectile_speed: 200   # units/second

# Resource costs
resources:
  power_draw: 20          # watts consumed
  weight: 50              # kg
  slots: 1                # grid slots occupied
  cost: 100               # build cost

# Special properties
special:
  damage_type: energy
  armor_piercing: 0.3     # 30% armor penetration
  shield_bonus: 1.5       # 50% extra damage to shields

# Targeting behavior
targeting:
  arc: 90                 # degrees of firing arc
  preference: closest     # closest, weakest, strongest
  ignore_allies: true

# Visual/audio (optional, for future use)
visual:
  color: "#00FF00"
  effect: "laser_beam"
  sound: "laser_fire"

# Tags for categorization
tags:
  - energy_weapon
  - point_defense
  - anti_fighter

# Metadata
version: "1.0.0"
author: "Battle Automata Team"
```

### Unit Schema

Units are assemblies of components:

```yaml
# data/themes/space-ships/units/fighter.yaml
id: fighter_mk1
name: "Fighter Mk1"
theme: space-ships
class: fighter

description: >
  Fast and maneuverable light fighter. Excellent for hit-and-run
  tactics and anti-fighter roles.

# Grid layout
layout:
  type: grid
  size: [10, 10]          # 10x10 grid

# Resource budgets
resources:
  max_power: 100
  max_weight: 500
  max_slots: 20

# Component placements
components:
  # Weapons
  - id: laser_cannon_mk1
    position: [5, 2]
    facing: forward

  - id: laser_cannon_mk1
    position: [3, 2]
    facing: forward

  # Defense
  - id: light_armor_plate
    position: [5, 5]
    coverage:
      - [4, 4]
      - [5, 4]
      - [6, 4]
      - [4, 5]
      - [5, 5]
      - [6, 5]

  # Propulsion
  - id: ion_engine_mk1
    position: [5, 8]
    facing: rear

  - id: maneuvering_thruster
    position: [2, 5]
    facing: left

  - id: maneuvering_thruster
    position: [8, 5]
    facing: right

  # Power
  - id: fusion_reactor_small
    position: [5, 5]
    slot: core

# Initial state
initial_state:
  health: 100
  position: [0, 0]
  facing: 0
  velocity: [0, 0]

# AI behavior
ai:
  type: aggressive_fighter
  engagement_range: 150
  retreat_threshold: 30   # % health
  target_priority:
    - fighters
    - bombers
    - capitals

# Metadata
tags:
  - fighter
  - fast
  - anti_fighter

cost: 1500
build_time: 60
version: "1.0.0"
```

### Battle Configuration

```yaml
# data/battles/tutorial_01.yaml
name: "Tutorial: Basic Combat"
description: "Learn the basics of battle simulation"

# Battle configuration
config:
  seed: 12345
  max_turns: 1000
  max_duration: 100.0     # seconds
  time_step: 0.1          # seconds per turn

  # Arena
  arena:
    width: 1000
    height: 1000

  # Win conditions
  win_conditions:
    - elimination
    - timeout

  # Rules
  enable_fog_of_war: false
  enable_friendly_fire: false

# Units
units:
  - id: player_unit
    file: units/fighter.yaml
    team: 0
    position: [100, 500]
    facing: 0

  - id: enemy_unit
    file: units/bomber.yaml
    team: 1
    position: [900, 500]
    facing: 180

# Metadata
author: "Battle Automata Team"
difficulty: beginner
tags:
  - tutorial
  - 1v1
```

---

## Build & Development

### Makefile

Complete development workflow:

```makefile
.PHONY: help install install-dev test test-unit test-integration test-e2e \
        test-cov lint format typecheck clean build publish docs docs-serve \
        docker-build docker-run benchmark validate-data

# Default target
.DEFAULT_GOAL := help

# Colors
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
NC := \033[0m # No Color

help:  ## Show this help message
	@echo "$(BLUE)Battle Automata Engine - Development Commands$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

# ============================================================================
# Installation
# ============================================================================

install:  ## Install package in production mode
	pip install -e .

install-dev:  ## Install package with development dependencies
	pip install -e ".[dev,web,docs]"
	pre-commit install

# ============================================================================
# Testing
# ============================================================================

test:  ## Run all tests
	pytest

test-unit:  ## Run unit tests only
	pytest tests/unit -v

test-integration:  ## Run integration tests
	pytest tests/integration -v

test-e2e:  ## Run end-to-end tests
	pytest tests/e2e -v -m e2e

test-cov:  ## Run tests with coverage report
	pytest --cov --cov-report=html --cov-report=term

test-watch:  ## Run tests in watch mode
	pytest-watch -- -v

# ============================================================================
# Code Quality
# ============================================================================

lint:  ## Run linting checks
	@echo "$(BLUE)Running ruff...$(NC)"
	ruff check src tests
	@echo "$(BLUE)Running mypy...$(NC)"
	mypy src

format:  ## Format code with black and isort
	@echo "$(BLUE)Running black...$(NC)"
	black src tests examples
	@echo "$(BLUE)Running isort...$(NC)"
	isort src tests examples

format-check:  ## Check code formatting without making changes
	black --check src tests examples
	isort --check-only src tests examples

typecheck:  ## Run type checking
	mypy src

pre-commit:  ## Run pre-commit hooks on all files
	pre-commit run --all-files

# ============================================================================
# Build & Package
# ============================================================================

clean:  ## Remove build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build:  ## Build distribution packages
	python -m build

publish:  ## Publish to PyPI (requires credentials)
	python -m twine upload dist/*

publish-test:  ## Publish to TestPyPI
	python -m twine upload --repository testpypi dist/*

# ============================================================================
# Documentation
# ============================================================================

docs:  ## Generate documentation
	mkdocs build

docs-serve:  ## Serve documentation locally
	mkdocs serve

docs-deploy:  ## Deploy documentation to GitHub Pages
	mkdocs gh-deploy

# ============================================================================
# Docker
# ============================================================================

docker-build:  ## Build Docker image
	docker build -t battle-automata:latest .

docker-run:  ## Run Docker container
	docker run -it --rm -v $(PWD)/data:/app/data battle-automata:latest

docker-shell:  ## Open shell in Docker container
	docker run -it --rm -v $(PWD)/data:/app/data battle-automata:latest /bin/bash

# ============================================================================
# Development Tools
# ============================================================================

benchmark:  ## Run performance benchmarks
	pytest benchmarks/ --benchmark-only

validate-data:  ## Validate all data files
	python scripts/validate_data.py data/

init-project:  ## Initialize example project
	battle-sim init --directory ./example-project

# ============================================================================
# Development Server (Optional Web API)
# ============================================================================

server:  ## Start development server (requires web extras)
	uvicorn battle_automata.web.main:app --reload

# ============================================================================
# CI/CD Simulation
# ============================================================================

ci-lint:  ## Run CI linting checks
	ruff check src tests --exit-non-zero-on-fix
	black --check src tests
	isort --check-only src tests
	mypy src

ci-test:  ## Run CI tests
	pytest -v --cov --cov-report=xml --cov-report=term

ci-build:  ## Run CI build
	python -m build
	twine check dist/*

ci:  ## Run full CI pipeline locally
	@echo "$(BLUE)Running full CI pipeline...$(NC)"
	@$(MAKE) ci-lint
	@$(MAKE) ci-test
	@$(MAKE) ci-build
	@echo "$(GREEN)✓ CI pipeline passed!$(NC)"
```

### Pre-commit Configuration

`.pre-commit-config.yaml`:

```yaml
# See https://pre-commit.com for more information
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict
      - id: check-toml
      - id: debug-statements

  - repo: https://github.com/psf/black
    rev: 23.11.0
    hooks:
      - id: black
        language_version: python3.10

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: ["--profile", "black"]

  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.1
    hooks:
      - id: mypy
        additional_dependencies: [pydantic>=2.0, types-PyYAML]
        args: [--strict, --ignore-missing-imports]
```

### GitHub Actions CI/CD

`.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      - name: Install dependencies
        run: |
          pip install ruff black isort mypy
          pip install -e ".[dev]"

      - name: Run ruff
        run: ruff check src tests

      - name: Run black
        run: black --check src tests

      - name: Run isort
        run: isort --check-only src tests

      - name: Run mypy
        run: mypy src

  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ["3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          pip install -e ".[dev]"

      - name: Run tests
        run: |
          pytest -v --cov --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml

  integration:
    runs-on: ubuntu-latest
    needs: [lint, test]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      - name: Install dependencies
        run: pip install -e ".[dev]"

      - name: Run integration tests
        run: pytest tests/integration -v

      - name: Run end-to-end tests
        run: pytest tests/e2e -v -m e2e

  build:
    runs-on: ubuntu-latest
    needs: [lint, test, integration]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      - name: Install build dependencies
        run: pip install build twine

      - name: Build package
        run: python -m build

      - name: Check distribution
        run: twine check dist/*

      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: dist
          path: dist/
```

---

## Distribution

### PyPI Package

#### Package Structure

```
battle-automata-0.1.0/
├── setup.py
├── setup.cfg
├── pyproject.toml
├── README.md
├── LICENSE
├── MANIFEST.in
└── src/
    └── battle_automata/
        ├── __init__.py
        ├── py.typed
        └── ...
```

#### Version Management

Use `bump2version` for version management:

```bash
# Install
pip install bump2version

# Bump patch version (0.1.0 -> 0.1.1)
bump2version patch

# Bump minor version (0.1.0 -> 0.2.0)
bump2version minor

# Bump major version (0.1.0 -> 1.0.0)
bump2version major
```

`.bumpversion.cfg`:

```ini
[bumpversion]
current_version = 0.1.0
commit = True
tag = True

[bumpversion:file:pyproject.toml]
search = version = "{current_version}"
replace = version = "{new_version}"

[bumpversion:file:src/battle_automata/__init__.py]
search = __version__ = "{current_version}"
replace = __version__ = "{new_version}"
```

#### Publishing Workflow

```bash
# 1. Update version
bump2version patch

# 2. Clean previous builds
make clean

# 3. Build distribution
make build

# 4. Check distribution
twine check dist/*

# 5. Test on TestPyPI (optional)
make publish-test

# 6. Install and test locally
pip install -e .
battle-sim --version

# 7. Publish to PyPI
make publish
```

### Docker Distribution

`Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy package files
COPY pyproject.toml setup.py MANIFEST.in ./
COPY src/ src/
COPY README.md LICENSE ./

# Install package
RUN pip install --no-cache-dir -e .

# Create data directory
RUN mkdir -p /app/data

# Set up volume for user data
VOLUME /app/data

# Default command
ENTRYPOINT ["battle-sim"]
CMD ["--help"]
```

`docker-compose.yml`:

```yaml
version: '3.8'

services:
  battle-sim:
    build: .
    volumes:
      - ./data:/app/data
      - ./results:/app/results
    environment:
      - PYTHONUNBUFFERED=1
```

Usage:

```bash
# Build image
docker build -t battle-automata:latest .

# Run CLI
docker run -it --rm \
  -v $(pwd)/data:/app/data \
  battle-automata:latest init

# Run battle
docker run -it --rm \
  -v $(pwd)/data:/app/data \
  battle-automata:latest battle simulate data/units/fighter.yaml data/units/bomber.yaml
```

---

## Modding Support

### Modding Architecture

```
Custom Theme Structure:
my-custom-theme/
├── theme.yaml              # Theme metadata
├── components/             # Custom components
│   ├── weapons/
│   ├── armor/
│   └── ...
└── units/                  # Custom units
    └── ...

User Project Structure:
my-project/
├── data/
│   └── themes/
│       ├── space-ships/    # Built-in theme (read-only)
│       └── my-theme/       # Custom theme
├── custom_components/      # Custom Python components (advanced)
│   ├── __init__.py
│   └── plasma_weapon.py
└── results/                # Battle results
```

### Component Discovery

Components are discovered in this order:

1. **Built-in themes** (from package)
2. **User themes** (from `data/themes/`)
3. **Custom components** (from `custom_components/`)

### Creating Custom Themes

#### 1. Initialize Theme

```bash
battle-sim theme create my-theme --from space-ships
```

This creates:

```
data/themes/my-theme/
├── theme.yaml
├── components/
│   └── README.md
└── units/
    └── README.md
```

#### 2. Add Components

Create YAML files in `components/`:

```yaml
# data/themes/my-theme/components/weapons/custom_weapon.yaml
id: custom_plasma_cannon
name: "Custom Plasma Cannon"
type: offensive
category: weapon

stats:
  damage: 100
  range: 150
  fire_rate: 0.5
  accuracy: 0.9

resources:
  power_draw: 50
  weight: 100
  slots: 2
  cost: 500

special:
  damage_type: plasma
  splash_radius: 10
  heat_generation: 75
```

#### 3. Validate Theme

```bash
battle-sim theme validate my-theme
```

### Custom Python Components (Advanced)

For advanced users who want to add custom mechanics:

```python
# custom_components/plasma_weapon.py
from battle_automata.api import Component, ComponentRegistry

@ComponentRegistry.register('plasma_weapon')
class PlasmaWeapon(Component):
    """
    Custom plasma weapon with heat mechanics.
    """
    heat: int = 0
    max_heat: int = 100

    def on_fire(self, target):
        """Custom firing logic."""
        # Add heat
        self.heat += self.stats.get('heat_generation', 10)

        # Check overheat
        if self.heat >= self.max_heat:
            self.overheat()
            return False

        # Standard damage
        return super().on_fire(target)

    def on_tick(self, delta_time):
        """Cool down each tick."""
        cooling_rate = self.stats.get('cooling_rate', 5)
        self.heat = max(0, self.heat - cooling_rate * delta_time)

    def overheat(self):
        """Handle overheating."""
        self.heat = self.max_heat
        self.cooldown = 5.0  # Force 5 second cooldown
```

Load custom components:

```bash
# Add custom_components to Python path
export PYTHONPATH="${PYTHONPATH}:./custom_components"

# Run with custom components
battle-sim battle simulate unit1.yaml unit2.yaml
```

### Modding Documentation

See `docs/modding-guide/` for complete guides:

- `creating-themes.md` - Step-by-step theme creation
- `component-schema.md` - Complete component schema reference
- `unit-schema.md` - Complete unit schema reference
- `examples.md` - Example custom components

---

## Installation Instructions

### For End Users

#### From PyPI (Recommended)

```bash
# Install latest version
pip install battle-automata

# Verify installation
battle-sim --version

# Initialize a project
battle-sim init
```

#### From Source

```bash
# Clone repository
git clone https://github.com/yourusername/better-space-arena.git
cd better-space-arena

# Install
pip install -e .

# Verify
battle-sim --version
```

#### Using Docker

```bash
# Pull image
docker pull battle-automata:latest

# Run
docker run -it --rm \
  -v $(pwd)/data:/app/data \
  battle-automata:latest --help
```

### For Developers

#### Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/better-space-arena.git
cd better-space-arena

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
make install-dev

# Verify setup
make test
make lint
```

#### Development Workflow

```bash
# Run tests
make test

# Run tests with coverage
make test-cov

# Format code
make format

# Run linting
make lint

# Type checking
make typecheck

# Run all checks (as CI would)
make ci
```

### System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Python | 3.10 | 3.11+ |
| RAM | 512 MB | 1 GB+ |
| Disk Space | 100 MB | 500 MB+ |
| OS | Any | Linux/macOS/Windows |

### Troubleshooting

#### Common Issues

**Issue:** `battle-sim: command not found`

**Solution:**
```bash
# Ensure pip install location is in PATH
python -m pip install --user battle-automata
export PATH="$HOME/.local/bin:$PATH"  # Add to ~/.bashrc or ~/.zshrc
```

**Issue:** `ModuleNotFoundError: No module named 'battle_automata'`

**Solution:**
```bash
# Reinstall in development mode
pip install -e .
```

**Issue:** YAML parsing errors

**Solution:**
```bash
# Validate YAML syntax
battle-sim component validate components/my_component.yaml

# Check indentation (YAML is whitespace-sensitive)
```

---

## Summary

This document provides a complete specification for the Battle Automata Engine project structure and build system. The architecture supports:

- **Fast Development**: Clear structure, modern tooling
- **Quality Code**: Comprehensive testing, linting, type checking
- **Easy Distribution**: PyPI, Docker, source installation
- **Moddability**: Clear theme structure, plugin system
- **Professional Quality**: Production-ready package

### Next Steps for Implementation

1. **Create Directory Structure**
   ```bash
   mkdir -p src/battle_automata/{api,core,mechanics,utils,cli,schemas}
   mkdir -p tests/{unit,integration,e2e,fixtures}
   mkdir -p data/themes/space-ships/{components,units}
   mkdir -p docs/{user-guide,developer-guide,modding-guide}
   mkdir -p examples scripts benchmarks
   ```

2. **Set Up Package Files**
   - Copy `pyproject.toml` configuration
   - Create `setup.py` for compatibility
   - Add `MANIFEST.in` for package data
   - Create `Makefile` for development workflow

3. **Initialize Git**
   ```bash
   git init
   git add .
   git commit -m "Initial project structure"
   ```

4. **Set Up Development Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   make install-dev
   ```

5. **Start Implementation**
   - Begin with core data structures
   - Add API layer
   - Implement CLI commands
   - Write tests alongside code

This structure provides a solid foundation for the weekend MVP while supporting long-term growth and extensibility.

---

**Document Version:** 1.0
**Last Updated:** 2025-11-13
**Status:** Ready for Implementation
