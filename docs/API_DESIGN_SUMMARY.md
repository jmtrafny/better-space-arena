# Battle Automata Engine - API Design Summary

**Quick Reference Guide**

---

## Overview

The Battle Automata Engine API provides a clean, type-safe interface for building units from components and simulating deterministic battles. This document summarizes the key APIs.

---

## Quick Start

### 1. Simple Battle

```python
from battle_automata.api import Engine

engine = Engine()
engine.load_theme("space-ships")

result = engine.quick_battle(
    "fighter.yaml",
    "tank.yaml",
    seed=12345
)

print(f"Winner: {result.winner}")
```

### 2. Build Custom Unit

```python
unit = (engine.create_unit("Fighter", "space-ships")
    .with_layout(10, 10)
    .with_resources(power=100, weight=500)
    .add_component("laser_cannon", (5, 2))
    .add_component("engine", (5, 8))
    .build())
```

### 3. Step-by-Step Battle

```python
battle = Battle.from_files("unit1.yaml", "unit2.yaml")

for step in battle.simulate_step_by_step():
    print(f"Turn {step.turn}: {len(step.events)} events")
    if step.is_finished:
        break
```

---

## Core APIs

### Engine (Facade)

**Main entry point for all operations**

```python
class Engine:
    def load_theme(theme_name: str) -> int
    def create_unit(name: str, theme: str) -> UnitBuilder
    def load_unit(file_path: str) -> Unit
    def create_battle(*units: Unit, **config) -> Battle
    def quick_battle(unit1: str, unit2: str, **config) -> BattleResult
```

**Example:**
```python
engine = Engine(data_directory="./data")
engine.load_theme("space-ships")
result = engine.quick_battle("fighter.yaml", "tank.yaml")
```

---

### ComponentRegistry

**Load and manage components**

```python
class ComponentRegistry:
    def load_theme(theme_name: str) -> int
    def load_from_directory(directory: Path) -> int
    def get(component_id: str) -> Component
    def filter(category=None, tags=None, min_stat=None) -> List[Component]
    def register(component: Component) -> None
```

**Example:**
```python
registry = ComponentRegistry()
registry.load_theme("space-ships")

laser = registry.get("laser_cannon_mk1")
weapons = registry.filter(category="offensive")
heavy = registry.filter(min_stat={"damage": 50})
```

---

### Component

**Component definition with validation**

```python
class Component(BaseModel):
    name: str
    id: str
    category: ComponentCategory
    stats: Dict[str, Any]
    resources: Dict[str, int]
    special: Dict[str, Any]
    tags: List[str]

    @classmethod
    def from_file(file_path: str) -> Component
    def get_stat(stat_name: str, default=None) -> Any
    def has_tag(tag: str) -> bool
```

**Example:**
```python
laser = Component.from_file("laser_cannon.yaml")
damage = laser.get_stat("damage", 0)
is_energy = laser.has_tag("energy_weapon")
```

---

### UnitBuilder

**Fluent interface for building units**

```python
class UnitBuilder:
    def with_layout(width: int, height: int) -> UnitBuilder
    def with_resources(power=None, weight=None, slots=None) -> UnitBuilder
    def add_component(component_id: str, position: Tuple, facing=0) -> UnitBuilder
    def validate() -> UnitBuilder
    def build() -> Unit
    def save(file_path: str) -> None
```

**Example:**
```python
unit = (UnitBuilder("Fighter", "space-ships")
    .with_layout(10, 10)
    .with_resources(power=100, weight=500, slots=20)
    .add_component("laser_cannon", (5, 2), facing=0)
    .add_component("armor_plate", (5, 5))
    .add_component("engine", (5, 8), facing=180)
    .validate()
    .build())
```

---

### Unit

**Combat unit composed of components**

```python
class Unit(BaseModel):
    name: str
    theme: str
    layout_size: Tuple[int, int]
    components: List[ComponentPlacement]
    max_power: int
    max_weight: int
    max_slots: int

    @classmethod
    def from_file(file_path: str) -> Unit
    def add_component(component, position, facing=0) -> Unit
    def get_resource_usage() -> Dict[str, int]
    def validate() -> ValidationResult
```

**Example:**
```python
unit = Unit.from_file("fighter.yaml")
usage = unit.get_resource_usage()
print(f"Power: {usage['power']}/{unit.max_power}")
```

---

### Battle

**Battle simulation**

```python
class Battle:
    def __init__(*units: Unit, config: BattleConfig = None)

    @classmethod
    def from_files(*unit_files: str, config=None) -> Battle

    def simulate() -> BattleResult
    def simulate_step_by_step() -> Iterator[BattleStep]
    def get_state() -> BattleState
    def reset() -> None
```

**Example:**
```python
# Quick battle
battle = Battle(unit1, unit2)
result = battle.simulate()

# From files
battle = Battle.from_files("fighter.yaml", "tank.yaml")

# Step-by-step
for step in battle.simulate_step_by_step():
    visualize(step.state)
```

---

### BattleConfig

**Battle simulation parameters**

```python
@dataclass
class BattleConfig:
    seed: int = 42
    max_turns: int = 1000
    max_time: float = 100.0
    time_step: float = 0.1
    battlefield: Battlefield = Battlefield()
    win_conditions: List[WinCondition] = None
    enable_fog_of_war: bool = False
    enable_friendly_fire: bool = False
```

**Example:**
```python
config = BattleConfig(
    seed=12345,
    max_turns=500,
    time_step=0.05,
    battlefield=Battlefield(width=200, height=200)
)

battle = Battle(unit1, unit2, config=config)
```

---

### BattleResult

**Battle outcome and statistics**

```python
@dataclass
class BattleResult:
    winner: Optional[str]
    duration: float
    turns: int
    events: List[Event]
    final_state: Dict[str, Any]
    statistics: Dict[str, Any]

    def save(file_path: str) -> None
    def get_events_by_type(event_type: str) -> List[Event]
    def get_damage_dealt(unit_id: str) -> int
```

**Example:**
```python
result = battle.simulate()
print(f"Winner: {result.winner}")
print(f"Duration: {result.duration}s in {result.turns} turns")

# Analysis
hits = result.get_events_by_type("attack_hit")
damage = result.get_damage_dealt("fighter")

# Save
result.save("battle_result.json")
```

---

### BattleReplay

**Replay battle from events**

```python
class BattleReplay:
    def __init__(result: BattleResult)

    @classmethod
    def from_file(file_path: str) -> BattleReplay

    def reset() -> None
    def step_forward() -> Optional[Event]
    def step_to_turn(turn: int) -> List[Event]
    def __iter__() -> Iterator[Event]
```

**Example:**
```python
replay = BattleReplay.from_file("battle.json")

for event in replay:
    print(f"[{event.turn}] {event.type}: {event.data}")
```

---

## CLI Commands

### Simulate Battle

```bash
battle-sim battle simulate UNIT1 UNIT2 [OPTIONS]

# Examples
battle-sim battle simulate fighter.yaml tank.yaml --seed 12345
battle-sim battle simulate u1.yaml u2.yaml --output result.json --verbose
```

### Component Management

```bash
# List components
battle-sim component list --theme space-ships --type offensive

# Show component
battle-sim component show laser_cannon_mk1

# Create component
battle-sim component create weapon.yaml --interactive

# Validate component
battle-sim component validate weapon.yaml
```

### Unit Management

```bash
# List units
battle-sim unit list --theme space-ships

# Show unit
battle-sim unit show fighter.yaml

# Create unit
battle-sim unit create fighter.yaml --interactive

# Validate unit
battle-sim unit validate fighter.yaml
```

### Theme Management

```bash
# List themes
battle-sim theme list

# Show theme info
battle-sim theme info space-ships

# Validate theme
battle-sim theme validate ./data/themes/space-ships
```

### Battle Analysis

```bash
# Replay battle
battle-sim battle replay result.json

# Analyze battle
battle-sim battle analyze result.json

# Run tournament
battle-sim battle tournament u1.yaml u2.yaml u3.yaml
```

---

## Extension Points

### Custom Components

```python
# Register custom component type
from battle_automata.api import ComponentRegistry

registry = ComponentRegistry()
registry.register_type("custom_weapon", CustomWeaponClass)
```

### Plugin Hooks

```python
# Hook into engine events
from battle_automata.api import PluginRegistry

@PluginRegistry.register_hook("on_damage_dealt")
def log_damage(event):
    print(f"Damage: {event.data['amount']}")
```

### Custom AI

```python
# Define custom AI behavior
from battle_automata.api import AIBehavior

class AggressiveAI(AIBehavior):
    def decide_movement(self, unit, state):
        # Custom logic
        return (velocity_x, velocity_y)

unit.set_ai(AggressiveAI())
```

### Custom Themes

```bash
# Directory structure
data/themes/my-theme/
  theme.yaml
  components/
    weapon1.yaml
    weapon2.yaml
  units/
    unit1.yaml
```

---

## Error Handling

### Exception Hierarchy

```python
BattleAutomataError           # Base
├── ValidationError           # Data validation
├── ComponentError           # Component issues
│   └── ComponentNotFoundError
├── UnitError                # Unit building
├── BattleError              # Simulation
└── ThemeError               # Theme loading
    └── ThemeNotFoundError
```

### Error Handling Example

```python
from battle_automata.api import (
    Engine,
    ValidationError,
    ComponentNotFoundError
)

try:
    engine = Engine()
    engine.load_theme("space-ships")

    unit = (engine.create_unit("Fighter", "space-ships")
        .add_component("laser_cannon", (5, 2))
        .validate()
        .build())

except ValidationError as e:
    print(f"Validation failed: {e.message}")
    print(f"  Field: {e.field}")
    print(f"  Details: {e.details}")

except ComponentNotFoundError as e:
    print(f"Component not found: {e}")

except Exception as e:
    print(f"Unexpected error: {e}")
```

---

## Common Patterns

### Pattern 1: Load and Battle

```python
from battle_automata.api import Engine

engine = Engine()
engine.load_theme("space-ships")

result = engine.quick_battle(
    "fighter.yaml",
    "tank.yaml",
    seed=12345
)
```

### Pattern 2: Build and Test

```python
# Build unit
unit = (engine.create_unit("Test", "space-ships")
    .with_layout(10, 10)
    .with_resources(power=100, weight=500)
    .add_component("laser_cannon", (5, 2))
    .add_component("engine", (5, 8))
    .build())

# Test against preset
enemy = engine.load_unit("tank.yaml")
battle = engine.create_battle(unit, enemy, seed=42)
result = battle.simulate()
```

### Pattern 3: Component Discovery

```python
registry = engine.components

# Find all heavy weapons
heavy = registry.filter(
    category="offensive",
    min_stat={"damage": 50}
)

# Find energy weapons
energy = registry.filter(tags=["energy_weapon"])

# Find anti-fighter weapons
anti_fighter = registry.filter(tags=["anti_fighter"])
```

### Pattern 4: Battle Analysis

```python
result = battle.simulate()

# Damage statistics
for unit_id in ["unit1", "unit2"]:
    damage = result.get_damage_dealt(unit_id)
    print(f"{unit_id} dealt {damage} damage")

# Hit rate
hits = result.get_events_by_type("attack_hit")
misses = result.get_events_by_type("attack_miss")
rate = len(hits) / (len(hits) + len(misses))
print(f"Hit rate: {rate:.1%}")

# Event timeline
for event in result.events:
    print(f"[{event.turn}] {event.type}")
```

### Pattern 5: Tournament

```python
units = [
    engine.load_unit("fighter.yaml"),
    engine.load_unit("tank.yaml"),
    engine.load_unit("bomber.yaml")
]

# Round-robin tournament
results = {}
for i, u1 in enumerate(units):
    for u2 in units[i+1:]:
        battle = engine.create_battle(u1, u2, seed=42)
        result = battle.simulate()
        results[f"{u1.name} vs {u2.name}"] = result.winner

# Tally wins
wins = {}
for winner in results.values():
    wins[winner] = wins.get(winner, 0) + 1

print("Standings:", wins)
```

---

## Type Safety

All APIs include full type hints:

```python
from typing import List, Optional, Dict, Any, Tuple
from pathlib import Path

def load_components(
    theme: str,
    directory: Optional[Path] = None
) -> Dict[str, Component]:
    """Load components with full type safety."""
    ...

def create_battle(
    unit1: Unit,
    unit2: Unit,
    seed: Optional[int] = None
) -> Battle:
    """Type-checked battle creation."""
    ...
```

IDE autocomplete and type checking work perfectly:

```python
# IDE knows all available methods
engine.  # <-- shows load_theme, create_unit, etc.

# Type checking catches errors
unit: Unit = engine.load_unit("fighter.yaml")
result: BattleResult = battle.simulate()  # Checked at dev time
```

---

## Best Practices

### 1. Always Use the Facade

```python
# Good: Use Engine facade
from battle_automata.api import Engine
engine = Engine()

# Avoid: Importing internals
from battle_automata.core.battle import BattleImpl  # Don't do this
```

### 2. Validate Early

```python
# Validate during building
unit = (builder
    .add_component("laser", (5, 2))
    .validate()  # Validate here
    .add_component("armor", (5, 5))
    .validate()  # And here
    .build())
```

### 3. Handle Errors Gracefully

```python
# Get validation result without raising
result = builder.get_validation_result()
if not result.valid:
    for error in result.errors:
        print(f"Error: {error}")
    # Fix issues
else:
    unit = builder.build()
```

### 4. Use Type Hints

```python
from battle_automata.api import Unit, Battle, BattleResult

def run_battle(unit1: Unit, unit2: Unit) -> BattleResult:
    battle: Battle = Battle(unit1, unit2)
    return battle.simulate()
```

### 5. Save Results

```python
# Save for analysis later
result = battle.simulate()
result.save("battle_result.json")

# Load and analyze
replay = BattleReplay.from_file("battle_result.json")
```

---

## Configuration

### Engine Configuration

```yaml
# .battle-sim.yaml
data_directory: "./data"
default_theme: "space-ships"

simulation:
  default_seed: null
  time_step: 0.1
  max_duration: 300.0

output:
  format: "json"
  verbose: false
```

### Environment Variables

```bash
export BATTLE_SIM_DATA_DIR="./data"
export BATTLE_SIM_THEME="space-ships"
export BATTLE_SIM_SEED="12345"
```

---

## Performance Tips

1. **Cache Components**: Load theme once, reuse registry
2. **Reuse Battles**: Reset instead of recreating
3. **Lazy Load**: Only load themes when needed
4. **Parallel Battles**: Use multiprocessing for tournaments

```python
# Good: Load once
engine = Engine()
engine.load_theme("space-ships")
# ... run many battles

# Avoid: Reloading
for _ in range(100):
    engine = Engine()  # Don't do this
    engine.load_theme("space-ships")
```

---

## Next Steps

1. **Read Full API Design**: See `API_DESIGN.md` for complete specification
2. **Try Examples**: Run code from usage examples section
3. **Build Custom Unit**: Use UnitBuilder to create your own units
4. **Create Theme**: Build a custom theme with your own components

---

## Quick Reference Card

| Task | API Call |
|------|----------|
| Initialize | `Engine()` |
| Load theme | `engine.load_theme("space-ships")` |
| Get component | `engine.components.get("laser_cannon")` |
| Build unit | `engine.create_unit("Name", "theme")` |
| Load unit | `engine.load_unit("unit.yaml")` |
| Quick battle | `engine.quick_battle("u1.yaml", "u2.yaml")` |
| Create battle | `Battle(unit1, unit2, seed=42)` |
| Simulate | `battle.simulate()` |
| Step-by-step | `battle.simulate_step_by_step()` |
| Replay | `BattleReplay.from_file("result.json")` |

---

**Full Documentation**: See `API_DESIGN.md` for complete API specification with all method signatures, parameters, and detailed examples.
