# Battle Automata Engine - Public API Design

**Version:** 1.0
**Date:** 2025-11-13
**Status:** Design Specification
**Author:** System Architect

---

## Table of Contents

1. [Overview](#overview)
2. [Design Principles](#design-principles)
3. [Component System API](#component-system-api)
4. [Unit Builder API](#unit-builder-api)
5. [Battle Simulation API](#battle-simulation-api)
6. [Data Loading API](#data-loading-api)
7. [Extension Points](#extension-points)
8. [CLI Interface](#cli-interface)
9. [Error Handling](#error-handling)
10. [Type Definitions](#type-definitions)
11. [Usage Examples](#usage-examples)

---

## Overview

### Purpose

This document specifies the **public API** for the Battle Automata Engine. The API provides a clean, intuitive interface for:

- Loading and managing components
- Building units from components
- Simulating battles
- Extending the engine with custom content
- Command-line interaction

### API Philosophy

The Battle Automata Engine API follows these core principles:

1. **Simplicity First**: Common tasks should be simple
2. **Progressive Disclosure**: Advanced features available when needed
3. **Type Safety**: Full type hints for IDE support
4. **Fail Fast**: Clear errors at the earliest possible point
5. **Consistency**: Similar operations use similar patterns
6. **Documentation**: Every public API has comprehensive docstrings

### API Layers

```
┌─────────────────────────────────────────────────────────┐
│                    CLIENT CODE                          │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                 PUBLIC API LAYER                        │
│  battle_automata.api.*                                  │
│  - Engine (Facade)                                      │
│  - Component, ComponentRegistry                         │
│  - Unit, UnitBuilder                                    │
│  - Battle, BattleConfig, BattleResult                   │
│  - ThemeLoader                                          │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│               INTERNAL IMPLEMENTATION                   │
│  battle_automata.core.*                                 │
│  battle_automata.mechanics.*                            │
│  battle_automata.utils.*                                │
│  (NOT FOR DIRECT USE)                                   │
└─────────────────────────────────────────────────────────┘
```

---

## Design Principles

### 1. Single Import Point

All public APIs accessible from `battle_automata.api`:

```python
# Good: Single import
from battle_automata.api import Engine, Unit, Battle, Component

# Avoid: Importing from internal modules
from battle_automata.core.unit import UnitImpl  # Internal, do not use
```

### 2. Fluent Interfaces

Builder pattern for complex construction:

```python
# Chainable methods for readability
unit = (UnitBuilder("Fighter", theme="space-ships")
    .with_layout(10, 10)
    .with_resources(power=100, weight=500, slots=20)
    .add_component("laser_cannon", position=(5, 2))
    .add_component("engine", position=(5, 8))
    .build())
```

### 3. Sensible Defaults

Common use cases work with minimal configuration:

```python
# Minimal configuration
battle = Battle(unit1, unit2)
result = battle.simulate()

# Advanced configuration when needed
battle = Battle(
    unit1, unit2,
    config=BattleConfig(
        seed=12345,
        battlefield=Battlefield(width=200, height=200),
        time_step=0.05
    )
)
```

### 4. Type Safety

Full type hints on all public APIs:

```python
from typing import List, Optional, Dict, Any
from pathlib import Path

def load_components(
    theme: str,
    directory: Optional[Path] = None
) -> Dict[str, Component]:
    """
    Load all components for a theme.

    Args:
        theme: Theme name (e.g., "space-ships")
        directory: Optional custom directory path

    Returns:
        Dictionary mapping component IDs to Component instances

    Raises:
        ThemeNotFoundError: If theme does not exist
        ValidationError: If component data is invalid
    """
    ...
```

### 5. Clear Error Messages

Errors include context and suggestions:

```python
# Bad error
ValidationError("Invalid component")

# Good error
ValidationError(
    "Component 'laser_cannon_mk1' requires power generator, "
    "but none present in unit. Add a component with type 'power_generator' "
    "to satisfy this requirement."
)
```

---

## Component System API

### Component Class

The base component interface:

```python
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from enum import Enum

class ComponentCategory(str, Enum):
    """Component category types."""
    OFFENSIVE = "offensive"
    DEFENSIVE = "defensive"
    MOBILITY = "mobility"
    SUPPORT = "support"

class Component(BaseModel):
    """
    A game component that can be attached to units.

    Components are loaded from YAML/JSON data files and represent
    modular parts that can be assembled into units.

    Example:
        >>> component = Component.from_file("data/components/laser.yaml")
        >>> print(component.name)
        "Laser Cannon Mk1"
    """

    # Identification
    name: str = Field(..., min_length=1, max_length=100)
    id: str = Field(..., regex=r'^[a-z0-9_]+$')
    category: ComponentCategory
    description: Optional[str] = None

    # Stats (category-dependent)
    stats: Dict[str, Any] = Field(default_factory=dict)

    # Resource costs
    resources: Dict[str, int] = Field(default_factory=dict)

    # Special properties
    special: Dict[str, Any] = Field(default_factory=dict)

    # Tags for filtering
    tags: List[str] = Field(default_factory=list)

    class Config:
        use_enum_values = True

    @classmethod
    def from_file(cls, file_path: str) -> 'Component':
        """
        Load component from YAML or JSON file.

        Args:
            file_path: Path to component definition file

        Returns:
            Component instance

        Raises:
            FileNotFoundError: If file does not exist
            ValidationError: If component data is invalid

        Example:
            >>> laser = Component.from_file("laser_cannon.yaml")
        """
        ...

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Component':
        """
        Create component from dictionary.

        Args:
            data: Component data dictionary

        Returns:
            Component instance

        Raises:
            ValidationError: If data is invalid
        """
        ...

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert component to dictionary.

        Returns:
            Component data as dictionary
        """
        ...

    def get_stat(self, stat_name: str, default: Any = None) -> Any:
        """
        Get a component stat value.

        Args:
            stat_name: Name of the stat (e.g., "damage")
            default: Default value if stat not found

        Returns:
            Stat value or default

        Example:
            >>> damage = laser.get_stat("damage", 0)
        """
        ...

    def get_resource_cost(self, resource: str) -> int:
        """
        Get resource cost.

        Args:
            resource: Resource name (e.g., "power_draw")

        Returns:
            Resource cost (0 if not specified)
        """
        ...

    def has_tag(self, tag: str) -> bool:
        """
        Check if component has a tag.

        Args:
            tag: Tag to check

        Returns:
            True if component has the tag
        """
        ...
```

### ComponentRegistry

Registry for discovering and loading components:

```python
from typing import Dict, List, Optional, Type
from pathlib import Path

class ComponentRegistry:
    """
    Registry for component definitions.

    The registry provides centralized access to all components
    and supports loading from themes and custom sources.

    Example:
        >>> registry = ComponentRegistry()
        >>> registry.load_theme("space-ships")
        >>> laser = registry.get("laser_cannon_mk1")
        >>> all_weapons = registry.filter(category="offensive")
    """

    def __init__(self, data_directory: Optional[Path] = None):
        """
        Initialize component registry.

        Args:
            data_directory: Root data directory (defaults to ./data)
        """
        ...

    def load_theme(self, theme_name: str) -> int:
        """
        Load all components from a theme.

        Args:
            theme_name: Name of theme (e.g., "space-ships")

        Returns:
            Number of components loaded

        Raises:
            ThemeNotFoundError: If theme does not exist

        Example:
            >>> registry.load_theme("space-ships")
            15  # Loaded 15 components
        """
        ...

    def load_from_directory(self, directory: Path) -> int:
        """
        Load components from a directory.

        Recursively scans directory for YAML/JSON component files.

        Args:
            directory: Directory to scan

        Returns:
            Number of components loaded
        """
        ...

    def load_from_file(self, file_path: Path) -> Component:
        """
        Load a single component file.

        Args:
            file_path: Path to component file

        Returns:
            Loaded component

        Raises:
            ValidationError: If component is invalid
        """
        ...

    def register(self, component: Component) -> None:
        """
        Register a component instance.

        Allows programmatic component creation.

        Args:
            component: Component to register

        Example:
            >>> custom = Component(id="custom_laser", ...)
            >>> registry.register(custom)
        """
        ...

    def get(self, component_id: str) -> Optional[Component]:
        """
        Get component by ID.

        Args:
            component_id: Component identifier

        Returns:
            Component or None if not found

        Example:
            >>> laser = registry.get("laser_cannon_mk1")
        """
        ...

    def get_or_raise(self, component_id: str) -> Component:
        """
        Get component by ID or raise error.

        Args:
            component_id: Component identifier

        Returns:
            Component instance

        Raises:
            ComponentNotFoundError: If component does not exist
        """
        ...

    def filter(
        self,
        category: Optional[ComponentCategory] = None,
        tags: Optional[List[str]] = None,
        min_stat: Optional[Dict[str, int]] = None
    ) -> List[Component]:
        """
        Filter components by criteria.

        Args:
            category: Filter by category
            tags: Filter by tags (must have all)
            min_stat: Minimum stat values

        Returns:
            List of matching components

        Example:
            >>> weapons = registry.filter(category="offensive")
            >>> lasers = registry.filter(tags=["energy_weapon"])
            >>> heavy = registry.filter(min_stat={"damage": 50})
        """
        ...

    def list_ids(self) -> List[str]:
        """
        Get list of all component IDs.

        Returns:
            List of component IDs
        """
        ...

    def count(self) -> int:
        """
        Get number of registered components.

        Returns:
            Component count
        """
        ...

    def clear(self) -> None:
        """Clear all registered components."""
        ...
```

---

## Unit Builder API

### Unit Class

The unit entity:

```python
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass

@dataclass
class ComponentPlacement:
    """
    A component placed on a unit.

    Attributes:
        component: The component instance
        position: Grid position (x, y)
        facing: Direction in degrees (0 = forward)
    """
    component: Component
    position: Tuple[int, int]
    facing: float = 0.0

class Unit(BaseModel):
    """
    A combat unit composed of components.

    Units are built from components and validated against
    resource constraints and placement rules.

    Example:
        >>> unit = Unit.from_file("fighter.yaml")
        >>> unit.add_component(laser, position=(5, 2))
    """

    # Identification
    name: str
    id: Optional[str] = None
    theme: str
    description: Optional[str] = None

    # Layout
    layout_size: Tuple[int, int] = (10, 10)

    # Components
    components: List[ComponentPlacement] = Field(default_factory=list)

    # Resource budget
    max_power: int = 100
    max_weight: int = 500
    max_slots: int = 20

    @classmethod
    def from_file(cls, file_path: str) -> 'Unit':
        """
        Load unit from YAML/JSON file.

        Args:
            file_path: Path to unit definition

        Returns:
            Unit instance

        Raises:
            FileNotFoundError: If file not found
            ValidationError: If unit data invalid
        """
        ...

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Unit':
        """Create unit from dictionary."""
        ...

    def to_dict(self) -> Dict[str, Any]:
        """Convert unit to dictionary."""
        ...

    def add_component(
        self,
        component: Component,
        position: Tuple[int, int],
        facing: float = 0.0
    ) -> 'Unit':
        """
        Add component to unit.

        Args:
            component: Component to add
            position: Grid position (x, y)
            facing: Direction in degrees

        Returns:
            Self for chaining

        Raises:
            ValidationError: If placement invalid
        """
        ...

    def remove_component(self, index: int) -> Component:
        """Remove component by index."""
        ...

    def get_resource_usage(self) -> Dict[str, int]:
        """
        Calculate current resource usage.

        Returns:
            Dictionary with power, weight, slots used
        """
        ...

    def validate(self) -> 'ValidationResult':
        """
        Validate unit configuration.

        Returns:
            ValidationResult with errors/warnings
        """
        ...
```

### UnitBuilder

Fluent interface for building units:

```python
from typing import Optional, Tuple

class UnitBuilder:
    """
    Fluent builder for constructing units.

    Provides a chainable interface for assembling units from
    components with validation at each step.

    Example:
        >>> unit = (UnitBuilder("Fighter", theme="space-ships")
        ...     .with_layout(10, 10)
        ...     .with_resources(power=100, weight=500)
        ...     .add_component("laser_cannon", (5, 2))
        ...     .add_component("engine", (5, 8))
        ...     .validate()
        ...     .build())
    """

    def __init__(
        self,
        name: str,
        theme: str,
        registry: Optional[ComponentRegistry] = None
    ):
        """
        Initialize unit builder.

        Args:
            name: Unit name
            theme: Theme name
            registry: Component registry (uses global if None)
        """
        ...

    def with_layout(self, width: int, height: int) -> 'UnitBuilder':
        """
        Set unit layout grid size.

        Args:
            width: Grid width
            height: Grid height

        Returns:
            Self for chaining
        """
        ...

    def with_resources(
        self,
        power: Optional[int] = None,
        weight: Optional[int] = None,
        slots: Optional[int] = None
    ) -> 'UnitBuilder':
        """
        Set resource budgets.

        Args:
            power: Maximum power budget
            weight: Maximum weight limit
            slots: Maximum slot capacity

        Returns:
            Self for chaining
        """
        ...

    def add_component(
        self,
        component_id: str,
        position: Tuple[int, int],
        facing: float = 0.0
    ) -> 'UnitBuilder':
        """
        Add component by ID.

        Looks up component in registry and adds to unit.

        Args:
            component_id: Component identifier
            position: Grid position (x, y)
            facing: Direction in degrees (0 = forward)

        Returns:
            Self for chaining

        Raises:
            ComponentNotFoundError: If component not in registry
            ValidationError: If placement invalid

        Example:
            >>> builder.add_component("laser_cannon", (5, 2), facing=0)
        """
        ...

    def add_component_instance(
        self,
        component: Component,
        position: Tuple[int, int],
        facing: float = 0.0
    ) -> 'UnitBuilder':
        """
        Add component instance.

        Args:
            component: Component to add
            position: Grid position
            facing: Direction in degrees

        Returns:
            Self for chaining
        """
        ...

    def remove_component_at(
        self,
        position: Tuple[int, int]
    ) -> 'UnitBuilder':
        """
        Remove component at position.

        Args:
            position: Grid position

        Returns:
            Self for chaining
        """
        ...

    def validate(self) -> 'UnitBuilder':
        """
        Validate current configuration.

        Checks resource budgets, dependencies, and placement rules.
        Raises exception if validation fails.

        Returns:
            Self for chaining

        Raises:
            ValidationError: If unit is invalid
        """
        ...

    def get_validation_result(self) -> 'ValidationResult':
        """
        Get validation result without raising.

        Returns:
            ValidationResult with errors and warnings
        """
        ...

    def build(self) -> Unit:
        """
        Build the final unit.

        Performs final validation and returns unit instance.

        Returns:
            Constructed unit

        Raises:
            ValidationError: If unit is invalid
        """
        ...

    def save(self, file_path: str) -> None:
        """
        Build and save unit to file.

        Args:
            file_path: Output file path (.yaml or .json)
        """
        ...
```

---

## Battle Simulation API

### BattleConfig

Configuration for battle simulation:

```python
from typing import List, Optional
from dataclasses import dataclass
from enum import Enum

class WinCondition(str, Enum):
    """Win condition types."""
    ELIMINATION = "elimination"  # Last team standing
    TIMEOUT = "timeout"           # Time/turn limit
    OBJECTIVE = "objective"       # Custom objective

@dataclass
class Battlefield:
    """
    Battlefield dimensions and properties.

    Attributes:
        width: Battlefield width
        height: Battlefield height
    """
    width: float = 1000.0
    height: float = 1000.0

@dataclass
class BattleConfig:
    """
    Configuration for battle simulation.

    Defines all parameters for running a battle.

    Example:
        >>> config = BattleConfig(
        ...     seed=12345,
        ...     max_turns=1000,
        ...     time_step=0.1
        ... )
    """

    # Random seed for determinism
    seed: int = 42

    # Time limits
    max_turns: int = 1000
    max_time: float = 100.0  # seconds
    time_step: float = 0.1   # seconds per turn

    # Battlefield
    battlefield: Battlefield = Battlefield()

    # Win conditions
    win_conditions: List[WinCondition] = None

    # Simulation options
    enable_fog_of_war: bool = False
    enable_friendly_fire: bool = False

    def __post_init__(self):
        if self.win_conditions is None:
            self.win_conditions = [WinCondition.ELIMINATION]
```

### Battle

Main battle simulation interface:

```python
from typing import List, Optional, Iterator

class Battle:
    """
    A battle between units.

    Manages the complete battle simulation lifecycle from
    initialization through execution to results.

    Example:
        >>> battle = Battle(unit1, unit2)
        >>> result = battle.simulate()
        >>> print(f"Winner: {result.winner}")
    """

    def __init__(
        self,
        *units: Unit,
        config: Optional[BattleConfig] = None
    ):
        """
        Initialize battle.

        Args:
            *units: Units to fight (2+ units)
            config: Battle configuration (default if None)

        Raises:
            ValueError: If less than 2 units provided

        Example:
            >>> battle = Battle(unit1, unit2)
            >>> battle = Battle(u1, u2, u3, config=custom_config)
        """
        ...

    @classmethod
    def from_files(
        cls,
        *unit_files: str,
        config: Optional[BattleConfig] = None
    ) -> 'Battle':
        """
        Create battle from unit files.

        Args:
            *unit_files: Paths to unit definition files
            config: Battle configuration

        Returns:
            Battle instance

        Example:
            >>> battle = Battle.from_files(
            ...     "fighter.yaml",
            ...     "tank.yaml"
            ... )
        """
        ...

    def simulate(self) -> 'BattleResult':
        """
        Run complete battle simulation.

        Executes the battle from start to finish and returns
        the final result.

        Returns:
            BattleResult with winner, events, and statistics

        Example:
            >>> result = battle.simulate()
            >>> print(f"Winner: {result.winner}")
            >>> print(f"Duration: {result.duration}s")
        """
        ...

    def simulate_step_by_step(self) -> Iterator['BattleStep']:
        """
        Simulate battle step-by-step.

        Yields battle state after each turn for visualization
        or analysis.

        Yields:
            BattleStep for each turn

        Example:
            >>> for step in battle.simulate_step_by_step():
            ...     print(f"Turn {step.turn}: {len(step.events)} events")
            ...     if step.is_finished:
            ...         break
        """
        ...

    def get_state(self) -> 'BattleState':
        """
        Get current battle state.

        Returns:
            Current BattleState snapshot
        """
        ...

    def reset(self) -> None:
        """Reset battle to initial state."""
        ...
```

### BattleResult

Result of a battle simulation:

```python
from typing import List, Optional, Dict, Any

@dataclass
class BattleResult:
    """
    Result of a battle simulation.

    Contains complete information about the battle outcome,
    including winner, events, and statistics.

    Attributes:
        winner: Winning team/unit ID or None for draw
        duration: Battle duration in seconds
        turns: Number of turns executed
        events: List of all battle events
        final_state: Final battle state snapshot
        statistics: Battle statistics
    """

    winner: Optional[str]
    duration: float
    turns: int
    events: List['Event']
    final_state: Dict[str, Any]
    statistics: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        ...

    def save(self, file_path: str) -> None:
        """
        Save result to file.

        Args:
            file_path: Output path (.json)
        """
        ...

    @classmethod
    def load(cls, file_path: str) -> 'BattleResult':
        """
        Load result from file.

        Args:
            file_path: Path to result file

        Returns:
            BattleResult instance
        """
        ...

    def get_events_by_type(self, event_type: str) -> List['Event']:
        """
        Filter events by type.

        Args:
            event_type: Event type to filter

        Returns:
            List of matching events
        """
        ...

    def get_damage_dealt(self, unit_id: str) -> int:
        """
        Get total damage dealt by unit.

        Args:
            unit_id: Unit identifier

        Returns:
            Total damage dealt
        """
        ...
```

### BattleReplay

Replay battle from event log:

```python
class BattleReplay:
    """
    Replay a battle from event log.

    Allows step-by-step replay of a completed battle
    for visualization or analysis.

    Example:
        >>> replay = BattleReplay.from_file("battle.json")
        >>> for event in replay:
        ...     print(f"[{event.turn}] {event.type}: {event.data}")
    """

    def __init__(self, result: BattleResult):
        """
        Initialize replay from result.

        Args:
            result: BattleResult to replay
        """
        ...

    @classmethod
    def from_file(cls, file_path: str) -> 'BattleReplay':
        """
        Load replay from file.

        Args:
            file_path: Path to battle result file

        Returns:
            BattleReplay instance
        """
        ...

    def reset(self) -> None:
        """Reset replay to beginning."""
        ...

    def step_forward(self) -> Optional['Event']:
        """
        Step to next event.

        Returns:
            Next event or None if at end
        """
        ...

    def step_to_turn(self, turn: int) -> List['Event']:
        """
        Step to specific turn.

        Args:
            turn: Turn number to jump to

        Returns:
            All events up to that turn
        """
        ...

    def __iter__(self) -> Iterator['Event']:
        """Iterate through all events."""
        ...
```

---

## Data Loading API

### Engine (Facade)

High-level facade for all operations:

```python
from typing import Optional, Dict
from pathlib import Path

class Engine:
    """
    Main engine facade.

    Provides a high-level interface to all engine functionality.
    This is the recommended entry point for most applications.

    Example:
        >>> from battle_automata.api import Engine
        >>>
        >>> # Initialize engine
        >>> engine = Engine(data_directory="./data")
        >>>
        >>> # Load theme
        >>> engine.load_theme("space-ships")
        >>>
        >>> # Quick battle
        >>> result = engine.quick_battle(
        ...     "fighter.yaml",
        ...     "tank.yaml",
        ...     seed=12345
        ... )
    """

    def __init__(
        self,
        data_directory: Optional[Path] = None,
        config_file: Optional[Path] = None
    ):
        """
        Initialize the engine.

        Args:
            data_directory: Root data directory (default: ./data)
            config_file: Engine configuration file (optional)
        """
        ...

    @property
    def components(self) -> ComponentRegistry:
        """Get component registry."""
        ...

    @property
    def themes(self) -> 'ThemeManager':
        """Get theme manager."""
        ...

    def load_theme(self, theme_name: str) -> int:
        """
        Load a theme.

        Args:
            theme_name: Theme to load

        Returns:
            Number of components loaded

        Example:
            >>> engine.load_theme("space-ships")
            15
        """
        ...

    def create_unit(self, name: str, theme: str) -> UnitBuilder:
        """
        Create a new unit builder.

        Args:
            name: Unit name
            theme: Theme name

        Returns:
            UnitBuilder instance

        Example:
            >>> builder = engine.create_unit("Fighter", "space-ships")
        """
        ...

    def load_unit(self, file_path: str) -> Unit:
        """
        Load unit from file.

        Args:
            file_path: Path to unit file

        Returns:
            Unit instance
        """
        ...

    def create_battle(self, *units: Unit, **config) -> Battle:
        """
        Create a battle.

        Args:
            *units: Units to battle
            **config: Battle configuration parameters

        Returns:
            Battle instance
        """
        ...

    def quick_battle(
        self,
        unit1_file: str,
        unit2_file: str,
        seed: Optional[int] = None,
        **config
    ) -> BattleResult:
        """
        Run a quick battle between two unit files.

        Convenience method that loads units and simulates battle.

        Args:
            unit1_file: Path to first unit
            unit2_file: Path to second unit
            seed: Random seed for determinism
            **config: Additional battle configuration

        Returns:
            BattleResult

        Example:
            >>> result = engine.quick_battle(
            ...     "fighter.yaml",
            ...     "tank.yaml",
            ...     seed=12345
            ... )
        """
        ...
```

### ThemeLoader

Theme loading and management:

```python
from typing import List, Dict, Optional
from pathlib import Path

class ThemeLoader:
    """
    Load and manage themes.

    Handles loading theme metadata, components, and units.

    Example:
        >>> loader = ThemeLoader("./data/themes")
        >>> theme = loader.load_theme("space-ships")
        >>> print(theme.name)
        "Space Ships"
    """

    def __init__(self, themes_directory: Path):
        """
        Initialize theme loader.

        Args:
            themes_directory: Directory containing themes
        """
        ...

    def list_themes(self) -> List[str]:
        """
        List available themes.

        Returns:
            List of theme names
        """
        ...

    def load_theme(self, theme_name: str) -> 'Theme':
        """
        Load a theme.

        Args:
            theme_name: Theme to load

        Returns:
            Theme instance

        Raises:
            ThemeNotFoundError: If theme doesn't exist
        """
        ...

    def get_theme_info(self, theme_name: str) -> Dict[str, Any]:
        """
        Get theme metadata.

        Args:
            theme_name: Theme name

        Returns:
            Theme metadata dictionary
        """
        ...

@dataclass
class Theme:
    """
    A theme definition.

    Attributes:
        name: Theme display name
        id: Theme identifier
        description: Theme description
        version: Theme version
        components_dir: Components directory
        units_dir: Units directory
    """
    name: str
    id: str
    description: str
    version: str
    components_dir: Path
    units_dir: Path
```

---

## Extension Points

### Custom Components

Register custom component types:

```python
from battle_automata.api import ComponentRegistry, Component

# Custom component class
class CustomWeapon(Component):
    """Custom weapon with special mechanics."""

    def special_ability(self):
        """Custom ability logic."""
        ...

# Register with registry
registry = ComponentRegistry()
registry.register_type("custom_weapon", CustomWeapon)
```

### Plugin System

Hook into engine events:

```python
from battle_automata.api import PluginRegistry, Event

@PluginRegistry.register_hook("on_damage_dealt")
def log_damage(event: Event):
    """Log all damage events."""
    print(f"Damage: {event.data['amount']}")

@PluginRegistry.register_hook("on_component_destroyed")
def on_destruction(event: Event):
    """Handle component destruction."""
    # Custom logic
    ...
```

### Custom AI Behaviors

Define custom unit AI:

```python
from battle_automata.api import AIBehavior, Unit, BattleState

class AggressiveAI(AIBehavior):
    """Aggressive AI that charges enemies."""

    def decide_movement(
        self,
        unit: Unit,
        state: BattleState
    ) -> Tuple[float, float]:
        """
        Decide unit movement.

        Args:
            unit: Unit to control
            state: Current battle state

        Returns:
            (velocity_x, velocity_y) tuple
        """
        # Custom AI logic
        ...

# Use custom AI
unit.set_ai(AggressiveAI())
```

### Theme Creation

Create custom themes:

```python
# Directory structure
# data/themes/my-theme/
#   theme.yaml
#   components/
#     weapon1.yaml
#     weapon2.yaml
#   units/
#     unit1.yaml

# theme.yaml
"""
name: "My Custom Theme"
id: my-theme
description: "A custom theme"
version: "1.0.0"
"""

# Load theme
engine = Engine()
engine.load_theme("my-theme")
```

---

## CLI Interface

### Command Structure

```bash
battle-sim <command> [arguments] [options]
```

### Commands

#### Initialize Project

```bash
# Create new project
battle-sim init [--theme THEME] [--directory DIR]

# Examples
battle-sim init --theme space-ships
battle-sim init --theme mechs --directory ./my-game
```

#### Theme Commands

```bash
# List available themes
battle-sim theme list

# Show theme information
battle-sim theme info THEME_NAME

# Validate theme
battle-sim theme validate PATH
```

#### Component Commands

```bash
# List components
battle-sim component list [--theme THEME] [--type TYPE]

# Show component details
battle-sim component show COMPONENT_ID

# Create new component
battle-sim component create OUTPUT_FILE [--interactive]

# Validate component
battle-sim component validate FILE
```

#### Unit Commands

```bash
# List units
battle-sim unit list [--theme THEME]

# Show unit details
battle-sim unit show UNIT_FILE

# Create new unit
battle-sim unit create OUTPUT_FILE [--interactive]

# Validate unit
battle-sim unit validate FILE

# Export unit (for sharing)
battle-sim unit export FILE [--format FORMAT]
```

#### Battle Commands

```bash
# Simulate battle
battle-sim battle simulate UNIT1 UNIT2 [OPTIONS]

# Options:
#   --seed SEED           Random seed
#   --output FILE         Save result to file
#   --verbose            Show detailed output
#   --replay             Generate replay file
#   --no-animation       Skip animation
#   --config FILE        Use custom battle config

# Examples
battle-sim battle simulate fighter.yaml tank.yaml --seed 12345
battle-sim battle simulate u1.yaml u2.yaml --output result.json
battle-sim battle simulate u1.yaml u2.yaml --verbose --replay

# Run tournament
battle-sim battle tournament UNIT1 UNIT2 UNIT3 [OPTIONS]

# Replay battle
battle-sim battle replay RESULT_FILE

# Analyze battle
battle-sim battle analyze RESULT_FILE
```

#### Server Commands

```bash
# Start development server (for future web UI)
battle-sim server start [--port PORT] [--host HOST]
```

### Global Options

```bash
--version             Show version
--help               Show help
--data-dir DIR       Set data directory
--config FILE        Use config file
--verbose            Verbose output
--quiet              Quiet mode
--debug              Debug mode
```

### Configuration File

```yaml
# .battle-sim.yaml or battle-sim.yaml
data_directory: "./data"
default_theme: "space-ships"

simulation:
  default_seed: null
  time_step: 0.1
  max_duration: 300.0

output:
  format: "json"
  verbose: false
  color: true

cli:
  editor: "vim"
  pager: "less"
```

### Environment Variables

```bash
BATTLE_SIM_DATA_DIR    # Data directory
BATTLE_SIM_THEME       # Default theme
BATTLE_SIM_SEED        # Default random seed
```

---

## Error Handling

### Exception Hierarchy

```python
class BattleAutomataError(Exception):
    """Base exception for all engine errors."""
    pass

class ValidationError(BattleAutomataError):
    """Data validation error."""

    def __init__(
        self,
        message: str,
        field: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.field = field
        self.details = details or {}
        super().__init__(message)

class ComponentError(BattleAutomataError):
    """Component-related error."""
    pass

class ComponentNotFoundError(ComponentError):
    """Component not found in registry."""
    pass

class UnitError(BattleAutomataError):
    """Unit-related error."""
    pass

class BattleError(BattleAutomataError):
    """Battle simulation error."""
    pass

class ThemeError(BattleAutomataError):
    """Theme loading error."""
    pass

class ThemeNotFoundError(ThemeError):
    """Theme not found."""
    pass
```

### Error Response Format

```python
{
    "error": "ValidationError",
    "message": "Component 'laser_cannon' requires power generator",
    "field": "components[2]",
    "details": {
        "component_id": "laser_cannon",
        "missing_dependency": "power_generator",
        "suggestion": "Add a component with type 'power_generator'"
    }
}
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

    builder = (engine.create_unit("Fighter", "space-ships")
        .add_component("laser_cannon", (5, 2))
        .validate()
        .build())

except ValidationError as e:
    print(f"Validation failed: {e.message}")
    if e.field:
        print(f"  Field: {e.field}")
    if e.details:
        print(f"  Details: {e.details}")

except ComponentNotFoundError as e:
    print(f"Component not found: {e}")

except Exception as e:
    print(f"Unexpected error: {e}")
```

---

## Type Definitions

### Common Types

```python
from typing import Tuple, Dict, Any, List, Optional, Union
from enum import Enum

# Position types
Position = Tuple[int, int]
Vector2D = Tuple[float, float]

# Resource types
ResourceDict = Dict[str, int]
StatsDict = Dict[str, Any]

# Component types
ComponentID = str
ComponentCategory = Enum('ComponentCategory',
    'OFFENSIVE DEFENSIVE MOBILITY SUPPORT')

# Unit types
UnitID = str

# Battle types
TeamID = str
Seed = int

# Configuration types
ConfigDict = Dict[str, Any]

# Event types
EventType = str
EventData = Dict[str, Any]
```

### Validation Types

```python
from dataclasses import dataclass
from typing import List

@dataclass
class ValidationResult:
    """
    Result of validation check.

    Attributes:
        valid: True if validation passed
        errors: List of error messages
        warnings: List of warning messages
    """
    valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def __bool__(self) -> bool:
        """True if valid."""
        return self.valid

    def __str__(self) -> str:
        """String representation."""
        if self.valid:
            result = "✓ Validation passed"
        else:
            result = "✗ Validation failed"

        if self.errors:
            result += "\n  Errors:\n"
            result += "\n".join(f"    - {e}" for e in self.errors)

        if self.warnings:
            result += "\n  Warnings:\n"
            result += "\n".join(f"    - {w}" for w in self.warnings)

        return result
```

---

## Usage Examples

### Example 1: Quick Battle

```python
from battle_automata.api import Engine

# Initialize engine
engine = Engine(data_directory="./data")

# Load theme
engine.load_theme("space-ships")

# Run quick battle
result = engine.quick_battle(
    "data/themes/space-ships/units/fighter.yaml",
    "data/themes/space-ships/units/tank.yaml",
    seed=12345
)

# Print results
print(f"Winner: {result.winner}")
print(f"Duration: {result.duration:.1f}s ({result.turns} turns)")
print(f"Events: {len(result.events)}")

# Save result
result.save("battle_result.json")
```

### Example 2: Build Custom Unit

```python
from battle_automata.api import Engine

engine = Engine()
engine.load_theme("space-ships")

# Build unit with fluent API
unit = (engine.create_unit("Custom Fighter", "space-ships")
    .with_layout(12, 12)
    .with_resources(power=150, weight=600, slots=25)
    .add_component("laser_cannon_mk1", position=(6, 2), facing=0)
    .add_component("laser_cannon_mk1", position=(6, 2), facing=0)  # Dual lasers
    .add_component("shield_generator", position=(6, 6))
    .add_component("fusion_reactor", position=(6, 6))
    .add_component("ion_engine", position=(6, 10), facing=180)
    .add_component("armor_plate_heavy", position=(6, 5))
    .validate()
    .build())

# Save unit
unit.to_file("custom_fighter.yaml")

# Use in battle
battle = engine.create_battle(unit, enemy_unit, seed=42)
result = battle.simulate()
```

### Example 3: Component Registry

```python
from battle_automata.api import ComponentRegistry

# Initialize registry
registry = ComponentRegistry(data_directory="./data")

# Load theme components
count = registry.load_theme("space-ships")
print(f"Loaded {count} components")

# Get specific component
laser = registry.get("laser_cannon_mk1")
print(f"Laser damage: {laser.get_stat('damage')}")

# Filter components
weapons = registry.filter(category="offensive")
print(f"Found {len(weapons)} weapons")

heavy_weapons = registry.filter(
    category="offensive",
    min_stat={"damage": 50}
)
print(f"Found {len(heavy_weapons)} heavy weapons")

# Search by tags
energy_weapons = registry.filter(tags=["energy_weapon"])
anti_fighter = registry.filter(tags=["anti_fighter"])
```

### Example 4: Battle Analysis

```python
from battle_automata.api import Engine, BattleReplay

engine = Engine()

# Simulate battle
result = engine.quick_battle("fighter.yaml", "tank.yaml", seed=12345)

# Analyze damage
fighter_damage = result.get_damage_dealt("fighter")
tank_damage = result.get_damage_dealt("tank")
print(f"Fighter dealt {fighter_damage} damage")
print(f"Tank dealt {tank_damage} damage")

# Replay battle
replay = BattleReplay(result)
for event in replay:
    if event.type == "attack_hit":
        print(f"[Turn {event.turn}] "
              f"{event.data['attacker']} hit {event.data['target']} "
              f"for {event.data['damage']} damage")

# Get specific events
hits = result.get_events_by_type("attack_hit")
misses = result.get_events_by_type("attack_miss")
print(f"Hit rate: {len(hits) / (len(hits) + len(misses)):.1%}")
```

### Example 5: Step-by-Step Simulation

```python
from battle_automata.api import Battle

battle = Battle.from_files("fighter.yaml", "tank.yaml", seed=12345)

# Simulate step by step for visualization
for step in battle.simulate_step_by_step():
    print(f"\n=== Turn {step.turn} ===")
    print(f"Time: {step.time:.1f}s")

    # Show events this turn
    for event in step.events:
        print(f"  - {event.type}: {event.data}")

    # Show unit states
    for unit_id, unit_state in step.state['units'].items():
        health = unit_state['health']
        pos = unit_state['position']
        print(f"  {unit_id}: HP={health} @ {pos}")

    if step.is_finished:
        print(f"\nBattle ended! Winner: {step.result.winner}")
        break
```

### Example 6: Custom Theme

```python
from battle_automata.api import Engine, Component

engine = Engine()

# Create custom component programmatically
custom_weapon = Component(
    name="Plasma Destroyer",
    id="plasma_destroyer",
    category="offensive",
    stats={
        "damage": 100,
        "range": 150,
        "fire_rate": 0.5,
        "accuracy": 0.9
    },
    resources={
        "power_draw": 80,
        "weight": 200,
        "slots": 3
    },
    special={
        "damage_type": "plasma",
        "splash_radius": 20,
        "armor_piercing": 0.5
    },
    tags=["heavy_weapon", "anti_capital"]
)

# Register component
engine.components.register(custom_weapon)

# Use in unit
unit = (engine.create_unit("Destroyer", "custom-theme")
    .add_component_instance(custom_weapon, (5, 5))
    .build())
```

### Example 7: Tournament

```python
from battle_automata.api import Engine

engine = Engine()
engine.load_theme("space-ships")

# Load units
units = [
    engine.load_unit("fighter.yaml"),
    engine.load_unit("tank.yaml"),
    engine.load_unit("bomber.yaml"),
    engine.load_unit("interceptor.yaml")
]

# Run round-robin tournament
results = {}
for i, unit1 in enumerate(units):
    for unit2 in units[i+1:]:
        matchup = f"{unit1.name} vs {unit2.name}"
        result = engine.create_battle(unit1, unit2, seed=42).simulate()
        results[matchup] = result.winner
        print(f"{matchup}: {result.winner} wins")

# Tally wins
wins = {}
for matchup, winner in results.items():
    wins[winner] = wins.get(winner, 0) + 1

# Print standings
print("\nStandings:")
for unit, win_count in sorted(wins.items(), key=lambda x: x[1], reverse=True):
    print(f"  {unit}: {win_count} wins")
```

### Example 8: Validation

```python
from battle_automata.api import Engine, ValidationError

engine = Engine()
engine.load_theme("space-ships")

builder = engine.create_unit("Test Unit", "space-ships")
builder.with_resources(power=100, weight=500, slots=10)

# Add components
builder.add_component("laser_cannon", (5, 2))
builder.add_component("shield_generator", (5, 5))  # Requires power
builder.add_component("engine", (5, 8))

# Get validation result without raising
result = builder.get_validation_result()

if not result.valid:
    print("Validation failed!")
    for error in result.errors:
        print(f"  ERROR: {error}")

if result.warnings:
    print("Warnings:")
    for warning in result.warnings:
        print(f"  WARNING: {warning}")

# Fix issues
builder.add_component("fusion_reactor", (5, 6))  # Add power generator

# Now validate (raises if invalid)
try:
    builder.validate()
    unit = builder.build()
    print("Unit built successfully!")
except ValidationError as e:
    print(f"Still invalid: {e}")
```

---

## Summary

This API design provides:

1. **Simplicity**: Easy to use for common cases
2. **Power**: Advanced features when needed
3. **Type Safety**: Full type hints throughout
4. **Extensibility**: Multiple extension points
5. **Consistency**: Uniform patterns across API
6. **Documentation**: Comprehensive docstrings

### Key Design Decisions

1. **Facade Pattern**: `Engine` class as main entry point
2. **Fluent Builders**: Chainable API for unit construction
3. **Registry Pattern**: Component discovery and loading
4. **Result Objects**: Structured results with rich metadata
5. **Event Sourcing**: Complete battle history for replay
6. **Type Hints**: Full typing for IDE support
7. **Clear Errors**: Descriptive exceptions with context

### Next Steps

1. **Developer**: Implement these interfaces
2. **QA**: Create test cases for all public APIs
3. **Documentation**: Expand with more examples
4. **User Testing**: Validate API usability

The API is designed to be stable, intuitive, and powerful enough to support the Battle Automata Engine's vision of theme-agnostic, deterministic battle simulation.
