# Component-Based Architecture Patterns

## Research Report: ECS and Modular Design for Battle Automata Engine

**Research Date**: 2025-11-13
**Purpose**: Inform architectural design for a theme-agnostic battle simulation engine
**Focus**: Component-based entity systems, data-driven design, and extensibility patterns

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [ECS (Entity Component System)](#ecs-entity-component-system)
3. [Component Composition](#component-composition)
4. [Data-Driven Design](#data-driven-design)
5. [Plugin Architectures](#plugin-architectures)
6. [Validation and Constraints](#validation-and-constraints)
7. [Resource Systems](#resource-systems)
8. [Recommendations for Battle Automata Engine](#recommendations-for-battle-automata-engine)
9. [Code Examples](#code-examples)
10. [References and Resources](#references-and-resources)

---

## Executive Summary

### Key Findings

**Entity Component System (ECS)** is the dominant architectural pattern for component-based game development, offering:
- **Composition over inheritance**: Build complex entities from simple, reusable components
- **Data-oriented design**: Separate data (components) from behavior (systems)
- **Flexibility**: Easy to add, remove, or modify components without affecting other parts
- **Testability**: Components are simple data containers that are easy to test

**Best Practices for Battle Automata Engine**:
1. Use **dataclasses + Pydantic** for component definition with built-in validation
2. Implement **decorator-based component registry** for automatic discovery
3. Store configurations in **YAML** for readability (JSON as alternative)
4. Design **constraint validation systems** to check component compatibility
5. Create **builder pattern** for unit assembly with resource budget validation
6. Use **plugin architecture** for theme extensibility

### When to Use ECS

**ECS is ideal for**:
- Games with many entity types built from common components
- Systems requiring runtime composition of behaviors
- Performance-critical applications (though less critical in Python)
- Projects requiring modding/extensibility

**For Battle Automata Engine**: ECS is a perfect fit because:
- Units are composed of modular components (weapons, armor, engines)
- Different themes use similar component types with different data
- Components can be added/removed dynamically (damage system)
- Moddability is a core requirement

---

## ECS (Entity Component System)

### Core Principles

**Three fundamental concepts**:

1. **Entity**: A unique identifier (UID) representing a game object
   - In pure ECS: Just an integer or string ID
   - No behavior, no data of its own
   - Acts as a container for components

2. **Component**: Pure data, no logic
   - Simple data structures (dataclasses, structs)
   - Examples: Position, Health, Weapon, Armor
   - Attached to entities to define what they are

3. **System**: Pure logic, no data
   - Processes entities that have specific component combinations
   - Examples: MovementSystem, CombatSystem, RenderSystem
   - Queries for entities with required components

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                     GAME WORLD                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Entity Manager                                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │ Entity 1 │  │ Entity 2 │  │ Entity 3 │             │
│  │  ID: 42  │  │  ID: 43  │  │  ID: 44  │             │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘             │
│       │             │             │                     │
│       ▼             ▼             ▼                     │
│  ┌─────────────────────────────────────┐               │
│  │     Component Storage                │               │
│  ├─────────────────────────────────────┤               │
│  │ Position Components                  │               │
│  │  {42: (10,20), 43: (5,15), ...}     │               │
│  ├─────────────────────────────────────┤               │
│  │ Weapon Components                    │               │
│  │  {42: LaserData, 44: MissileData}   │               │
│  ├─────────────────────────────────────┤               │
│  │ Health Components                    │               │
│  │  {42: 100, 43: 150, 44: 200}        │               │
│  └─────────────────────────────────────┘               │
│                                                         │
│  Systems Layer                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐│
│  │  Movement    │  │   Combat     │  │   Render     ││
│  │   System     │  │   System     │  │   System     ││
│  │              │  │              │  │              ││
│  │ Queries for: │  │ Queries for: │  │ Queries for: ││
│  │ Position +   │  │ Weapon +     │  │ Position +   ││
│  │ Velocity     │  │ Health       │  │ Sprite       ││
│  └──────────────┘  └──────────────┘  └──────────────┘│
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Python ECS Libraries

**1. Esper** (Most Popular)
- MIT licensed, pure Python
- Simple API: `world.add_component()`, `world.get_component()`
- Active development, well-documented
- Installation: `pip install esper`

**2. ecs-pattern** (Lightweight)
- Decorator-based component definition
- Uses Python dataclasses
- Focus on simplicity over performance
- Installation: `pip install ecs-pattern`

**3. python-utilities ebs** (Academic)
- Entity-based system framework
- Good for learning concepts
- Less active development

### When NOT to Use ECS

**Avoid ECS when**:
- Object hierarchies are simple and stable
- You have few entity types with distinct behaviors
- Team is unfamiliar with ECS (steep learning curve)
- Pure OOP would be simpler and clearer

**For Battle Automata Engine**: These concerns don't apply
- Component types are numerous and varied
- Composition is natural for the domain
- Extensibility requirements favor ECS

---

## Component Composition

### Composition Over Inheritance

**Traditional OOP Problem**:
```python
# Anti-pattern: Deep inheritance hierarchy
class Unit:
    pass

class ArmedUnit(Unit):
    def attack(self): pass

class FlyingArmedUnit(ArmedUnit):
    def fly(self): pass

class HealingFlyingArmedUnit(FlyingArmedUnit):
    def heal(self): pass

# What if we want ArmedUnit that can heal but not fly?
# Need to create a new class or multiple inheritance (messy)
```

**ECS Solution**:
```python
# Clean: Compose from components
fighter = Entity()
fighter.add(WeaponComponent(type="laser"))
fighter.add(EngineComponent(speed=10))

medic = Entity()
medic.add(WeaponComponent(type="stun"))
medic.add(HealingComponent(heal_rate=5))

heavy_fighter = Entity()
heavy_fighter.add(WeaponComponent(type="laser"))
heavy_fighter.add(WeaponComponent(type="missile"))  # Two weapons!
heavy_fighter.add(ArmorComponent(thickness=5))
```

### Component Design Patterns

**1. Single Responsibility Components**
```python
@dataclass
class Position:
    """Pure data: Where the entity is"""
    x: float
    y: float
    facing: float = 0.0

@dataclass
class Velocity:
    """Pure data: How the entity moves"""
    dx: float
    dy: float
    rotation_speed: float = 0.0

@dataclass
class Health:
    """Pure data: Entity durability"""
    current: int
    maximum: int
    armor: int = 0
```

**2. Grouped Components for Complex Entities**
```python
@dataclass
class WeaponStats:
    """Weapon characteristics"""
    damage: int
    range: float
    fire_rate: float
    accuracy: float
    damage_type: str  # "kinetic", "energy", "explosive"

@dataclass
class WeaponComponent:
    """Complete weapon with stats and state"""
    stats: WeaponStats
    cooldown_remaining: float = 0.0
    ammo_current: int = -1  # -1 for unlimited
    ammo_max: int = -1
    target_preference: str = "closest"  # "closest", "weakest", "strongest"
```

**3. Tag Components**
```python
@dataclass
class PlayerControlled:
    """Tag: This entity is controlled by a player"""
    pass

@dataclass
class AIControlled:
    """Tag: This entity is controlled by AI"""
    difficulty: str = "normal"

# Systems can query for entities with tags
# Example: ai_system.process(query=[AIControlled, Position, Weapon])
```

### Component Relationships

**Dependencies**:
```python
# Some components require others
@dataclass
class Shield:
    strength: int
    recharge_rate: float
    power_draw: int  # Requires PowerGenerator

@dataclass
class PowerGenerator:
    max_output: int
    current_output: int = 0

# Validation: Shield requires PowerGenerator
def validate_unit(entity):
    has_shield = entity.has(Shield)
    has_power = entity.has(PowerGenerator)

    if has_shield and not has_power:
        raise ValidationError("Shield requires PowerGenerator")

    if has_shield and has_power:
        shield = entity.get(Shield)
        power = entity.get(PowerGenerator)
        if shield.power_draw > power.max_output:
            raise ValidationError("Insufficient power for shield")
```

**Conflicts**:
```python
# Some components are mutually exclusive
conflict_groups = {
    "engine_type": [HoverEngine, WheelEngine, LeggedEngine],
    "armor_type": [LightArmor, MediumArmor, HeavyArmor],
}

def check_conflicts(entity):
    for group_name, component_types in conflict_groups.items():
        present = [c for c in component_types if entity.has(c)]
        if len(present) > 1:
            raise ValidationError(
                f"Cannot have multiple {group_name} components: {present}"
            )
```

### Building Complex Entities

**Prefab Pattern**:
```python
# Define reusable entity templates
class UnitPrefabs:
    @staticmethod
    def light_fighter():
        """Fast, lightly armed ship"""
        entity = Entity()
        entity.add(Position(x=0, y=0))
        entity.add(Health(current=100, maximum=100))
        entity.add(WeaponComponent(
            stats=WeaponStats(damage=25, range=50, fire_rate=2.0,
                            accuracy=0.85, damage_type="energy")
        ))
        entity.add(EngineComponent(max_speed=15, acceleration=3.0))
        entity.add(LightArmor(protection=10))
        return entity

    @staticmethod
    def heavy_tank():
        """Slow, heavily armed and armored"""
        entity = Entity()
        entity.add(Position(x=0, y=0))
        entity.add(Health(current=300, maximum=300))
        entity.add(WeaponComponent(
            stats=WeaponStats(damage=75, range=40, fire_rate=0.5,
                            accuracy=0.95, damage_type="kinetic")
        ))
        entity.add(EngineComponent(max_speed=5, acceleration=1.0))
        entity.add(HeavyArmor(protection=50))
        entity.add(ShieldComponent(strength=100, recharge_rate=5))
        return entity
```

---

## Data-Driven Design

### Core Concept

**Data-driven design** means behavior is governed by external data rather than hard-coded logic. This allows:
- Non-programmers to create content
- Rapid iteration without recompilation
- Easy balancing and tuning
- Modding support
- Configuration versioning

### Origins in Game Development

Emerged in the 1990s when studios realized:
- Rebuilding the entire game for minor tweaks was slow and expensive
- Designers needed to iterate without programmer involvement
- Community modding extended game longevity

### File Format Comparison

| Format | Pros | Cons | Best For |
|--------|------|------|----------|
| **JSON** | - Universal support<br>- Lightweight<br>- Easy parsing<br>- Good for APIs | - Less readable<br>- No comments<br>- Verbose | - Data exchange<br>- Web integration<br>- Structured data |
| **YAML** | - Very readable<br>- Supports comments<br>- Less verbose<br>- Anchors & references | - More complex parsing<br>- Whitespace sensitive<br>- Multiple parsers | - Configuration files<br>- Game data<br>- Human editing |
| **XML** | - Schema validation<br>- Industry standard<br>- Tool support | - Very verbose<br>- Harder to read<br>- Legacy feel | - Enterprise apps<br>- When validation is critical |

**Recommendation for Battle Automata Engine**: **YAML for primary data, JSON for interchange**
- YAML for component definitions (human-readable, editable)
- JSON for unit serialization (machine-readable, compact)
- Support both through abstraction layer

### Component Definition Example

**YAML Format** (Recommended):
```yaml
# data/themes/space-ships/components/laser_cannon_mk1.yaml
name: "Laser Cannon Mk1"
id: laser_cannon_mk1
type: offensive
category: weapon

description: >
  Basic energy weapon with good accuracy and fire rate.
  Effective against shields, less so against armor.

stats:
  damage: 50
  range: 100
  fire_rate: 1.0      # shots per second
  accuracy: 0.85
  projectile_speed: 200

resources:
  power_draw: 20      # watts consumed
  weight: 50          # kg
  slots: 1            # grid slots occupied
  cost: 100           # credits

special:
  damage_type: energy
  armor_piercing: 0.3
  shield_bonus: 1.5   # 50% more damage to shields

targeting:
  arc: 90             # degrees of firing arc
  preference: closest # closest, weakest, strongest
  ignore_allies: true

effects:
  - type: overheat
    threshold: 10     # shots before overheat
    cooldown: 2.0     # seconds to cool down

tags:
  - energy_weapon
  - point_defense
  - anti_fighter
```

**Equivalent JSON** (For interchange):
```json
{
  "name": "Laser Cannon Mk1",
  "id": "laser_cannon_mk1",
  "type": "offensive",
  "category": "weapon",
  "description": "Basic energy weapon with good accuracy and fire rate.",
  "stats": {
    "damage": 50,
    "range": 100,
    "fire_rate": 1.0,
    "accuracy": 0.85,
    "projectile_speed": 200
  },
  "resources": {
    "power_draw": 20,
    "weight": 50,
    "slots": 1,
    "cost": 100
  },
  "special": {
    "damage_type": "energy",
    "armor_piercing": 0.3,
    "shield_bonus": 1.5
  },
  "targeting": {
    "arc": 90,
    "preference": "closest",
    "ignore_allies": true
  },
  "effects": [
    {
      "type": "overheat",
      "threshold": 10,
      "cooldown": 2.0
    }
  ],
  "tags": ["energy_weapon", "point_defense", "anti_fighter"]
}
```

### Unit Definition Example

```yaml
# data/themes/space-ships/units/interceptor.yaml
name: "Interceptor Mk1"
id: interceptor_mk1
theme: space-ships
class: fighter

description: >
  Fast and maneuverable light fighter. Excellent for hit-and-run
  tactics and anti-fighter roles. Vulnerable to heavy weapons.

layout:
  type: grid
  size: [10, 10]    # 10x10 grid

resources:
  power_budget: 100
  weight_limit: 500
  slot_capacity: 20

# Component placement
components:
  # Weapons
  - id: laser_cannon_mk1
    position: [5, 2]
    facing: front
    slot: weapon_1

  - id: laser_cannon_mk1
    position: [5, 2]
    facing: front
    slot: weapon_2

  # Defense
  - id: light_armor_plate
    position: [5, 5]
    coverage: [
      [4, 4], [5, 4], [6, 4],
      [4, 5], [5, 5], [6, 5],
      [4, 6], [5, 6], [6, 6]
    ]

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

# Starting state
initial_state:
  health: 100
  position: [0, 0]
  facing: 0
  velocity: [0, 0]

# AI behavior (if AI-controlled)
ai:
  type: aggressive_fighter
  engagement_range: 150
  retreat_threshold: 30  # % health
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
```

### Data Loading Architecture

```python
from pathlib import Path
from typing import Dict, Any
import yaml
import json
from pydantic import BaseModel, ValidationError

class DataLoader:
    """Load and validate game data from files"""

    def __init__(self, data_dir: Path):
        self.data_dir = Path(data_dir)
        self.cache: Dict[str, Any] = {}

    def load_yaml(self, file_path: Path) -> Dict[str, Any]:
        """Load YAML file with caching"""
        key = str(file_path)
        if key not in self.cache:
            with open(file_path, 'r') as f:
                self.cache[key] = yaml.safe_load(f)
        return self.cache[key]

    def load_json(self, file_path: Path) -> Dict[str, Any]:
        """Load JSON file with caching"""
        key = str(file_path)
        if key not in self.cache:
            with open(file_path, 'r') as f:
                self.cache[key] = json.load(f)
        return self.cache[key]

    def load_component(self, component_id: str, theme: str) -> 'Component':
        """Load and validate component definition"""
        # Try YAML first, then JSON
        yaml_path = self.data_dir / "themes" / theme / "components" / f"{component_id}.yaml"
        json_path = yaml_path.with_suffix('.json')

        if yaml_path.exists():
            data = self.load_yaml(yaml_path)
        elif json_path.exists():
            data = self.load_json(json_path)
        else:
            raise FileNotFoundError(f"Component not found: {component_id}")

        # Validate against schema
        try:
            return ComponentFactory.create_from_data(data)
        except ValidationError as e:
            raise ValueError(f"Invalid component data for {component_id}: {e}")

    def load_all_components(self, theme: str) -> Dict[str, 'Component']:
        """Load all components for a theme"""
        components = {}
        component_dir = self.data_dir / "themes" / theme / "components"

        for file_path in component_dir.glob("*.yaml"):
            component_id = file_path.stem
            components[component_id] = self.load_component(component_id, theme)

        return components
```

### Component Factory Pattern

```python
from typing import Dict, Type, Callable
from dataclasses import dataclass

class ComponentFactory:
    """Factory for creating components from data files"""

    # Registry of component types
    _registry: Dict[str, Type] = {}

    @classmethod
    def register(cls, component_type: str):
        """Decorator to register component classes"""
        def decorator(component_class: Type):
            cls._registry[component_type] = component_class
            return component_class
        return decorator

    @classmethod
    def create_from_data(cls, data: Dict[str, Any]) -> 'Component':
        """Create component instance from data dictionary"""
        component_type = data.get('type')
        if component_type not in cls._registry:
            raise ValueError(f"Unknown component type: {component_type}")

        component_class = cls._registry[component_type]

        # Use Pydantic for validation if available
        if hasattr(component_class, 'parse_obj'):
            return component_class.parse_obj(data)
        else:
            # Fallback to direct instantiation
            return component_class(**data)

# Usage: Register component types
@ComponentFactory.register('offensive')
@dataclass
class WeaponComponent:
    name: str
    id: str
    type: str
    stats: Dict[str, float]
    resources: Dict[str, int]
    # ... other fields

@ComponentFactory.register('defensive')
@dataclass
class ArmorComponent:
    name: str
    id: str
    type: str
    protection: int
    coverage: float
    # ... other fields
```

---

## Plugin Architectures

### Core Concepts

A **plugin architecture** separates core functionality from extensions:
- **Core System**: Stable, well-defined API
- **Plugin Modules**: Add features without modifying core
- **Plugin Discovery**: Automatic detection and loading
- **Extension Points**: Well-defined hooks for plugins

### Benefits for Battle Automata Engine

1. **Theme Extensibility**: Users can create custom themes without modifying engine
2. **Custom Components**: Add new component types via plugins
3. **Mod Support**: Community can extend the game
4. **Testability**: Plugins can be tested independently
5. **Hot Reload**: Update plugins without restarting (advanced)

### Design Questions

**1. Plugin Discovery**: How does the application find plugins?
- **Directory scanning**: Look in `plugins/` folder
- **Naming convention**: Files matching `plugin_*.py`
- **Registration**: Explicit registration via decorator
- **Entry points**: Use setuptools entry points (most robust)

**2. Application API**: How do plugins interact with the application?
- **Hooks**: Defined extension points (e.g., `on_component_loaded`)
- **Interfaces**: Plugins implement specific interfaces
- **Registry**: Plugins register their capabilities
- **Event system**: Pub/sub for loose coupling

### Implementation Patterns

**1. Decorator-Based Registry** (Simplest)

```python
# core/plugin_system.py
from typing import Dict, Callable, List
import importlib
import pkgutil

class PluginRegistry:
    """Registry for plugin components"""

    def __init__(self):
        self._components: Dict[str, type] = {}
        self._systems: Dict[str, Callable] = {}
        self._hooks: Dict[str, List[Callable]] = {}

    def register_component(self, component_type: str):
        """Decorator to register a component type"""
        def decorator(cls):
            self._components[component_type] = cls
            return cls
        return decorator

    def register_system(self, system_name: str):
        """Decorator to register a system"""
        def decorator(func):
            self._systems[system_name] = func
            return func
        return decorator

    def register_hook(self, hook_name: str):
        """Decorator to register a hook handler"""
        def decorator(func):
            if hook_name not in self._hooks:
                self._hooks[hook_name] = []
            self._hooks[hook_name].append(func)
            return func
        return decorator

    def get_component(self, component_type: str) -> type:
        """Get registered component class"""
        return self._components.get(component_type)

    def get_system(self, system_name: str) -> Callable:
        """Get registered system function"""
        return self._systems.get(system_name)

    def trigger_hook(self, hook_name: str, *args, **kwargs):
        """Trigger all handlers for a hook"""
        for handler in self._hooks.get(hook_name, []):
            handler(*args, **kwargs)

    def discover_plugins(self, plugin_package: str = 'plugins'):
        """Automatically discover and load plugins"""
        try:
            package = importlib.import_module(plugin_package)
            for _, name, is_pkg in pkgutil.iter_modules(package.__path__):
                module_name = f"{plugin_package}.{name}"
                importlib.import_module(module_name)
        except ImportError:
            pass  # No plugins package found

# Global registry instance
registry = PluginRegistry()

# Usage in plugin files:
# plugins/energy_weapons.py
from core.plugin_system import registry
from dataclasses import dataclass

@registry.register_component('laser_weapon')
@dataclass
class LaserWeapon:
    damage: int
    range: float
    power_draw: int

@registry.register_hook('on_weapon_fire')
def laser_visual_effect(weapon, target):
    print(f"BZZZZT! Laser fired from {weapon} to {target}")
```

**2. Namespace-Based Discovery** (More Structured)

```python
# Setup plugins as a namespace package
# plugins/
#   __init__.py  (empty or with __path__ declaration)
#   theme_space/
#     __init__.py
#     components.py
#   theme_mech/
#     __init__.py
#     components.py

# core/plugin_loader.py
import importlib
import pkgutil
from typing import Protocol

class ThemePlugin(Protocol):
    """Interface that theme plugins must implement"""

    THEME_NAME: str
    THEME_DESCRIPTION: str

    def load_components(self) -> Dict[str, Any]:
        """Load all components for this theme"""
        ...

    def load_units(self) -> Dict[str, Any]:
        """Load all preset units for this theme"""
        ...

class PluginLoader:
    """Load plugins from namespace package"""

    def __init__(self, namespace: str = 'plugins'):
        self.namespace = namespace
        self.plugins: Dict[str, ThemePlugin] = {}

    def discover(self):
        """Discover all plugins in namespace"""
        try:
            # Import the namespace package
            ns_pkg = importlib.import_module(self.namespace)

            # Iterate over all modules in namespace
            for finder, name, ispkg in pkgutil.iter_modules(
                ns_pkg.__path__,
                ns_pkg.__name__ + "."
            ):
                module = importlib.import_module(name)

                # Look for ThemePlugin implementation
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if (isinstance(attr, type) and
                        hasattr(attr, 'THEME_NAME') and
                        hasattr(attr, 'load_components')):
                        plugin = attr()
                        self.plugins[plugin.THEME_NAME] = plugin

        except ImportError as e:
            print(f"Error loading plugins: {e}")

    def get_plugin(self, theme_name: str) -> ThemePlugin:
        """Get a specific theme plugin"""
        return self.plugins.get(theme_name)

    def list_plugins(self) -> List[str]:
        """List all available theme names"""
        return list(self.plugins.keys())

# Example plugin implementation
# plugins/theme_space/__init__.py
from typing import Dict, Any
import yaml
from pathlib import Path

class SpaceThemePlugin:
    THEME_NAME = "space-ships"
    THEME_DESCRIPTION = "Sci-fi space combat theme"

    def __init__(self):
        self.data_dir = Path(__file__).parent / "data"

    def load_components(self) -> Dict[str, Any]:
        """Load space ship components"""
        components = {}
        for yaml_file in (self.data_dir / "components").glob("*.yaml"):
            with open(yaml_file) as f:
                data = yaml.safe_load(f)
                components[data['id']] = data
        return components

    def load_units(self) -> Dict[str, Any]:
        """Load preset space ship units"""
        units = {}
        for yaml_file in (self.data_dir / "units").glob("*.yaml"):
            with open(yaml_file) as f:
                data = yaml.safe_load(f)
                units[data['id']] = data
        return units
```

**3. Entry Points** (Most Robust, for distributed plugins)

```python
# setup.py for a plugin package
from setuptools import setup

setup(
    name='battle-automata-mech-theme',
    version='1.0.0',
    packages=['mech_theme'],
    entry_points={
        'battle_automata.themes': [
            'mechs = mech_theme:MechThemePlugin',
        ],
    },
)

# core/plugin_loader.py
from importlib.metadata import entry_points

class PluginManager:
    """Load plugins via setuptools entry points"""

    def __init__(self, group: str = 'battle_automata.themes'):
        self.group = group
        self.plugins = {}

    def load_plugins(self):
        """Load all plugins from entry points"""
        discovered = entry_points(group=self.group)

        for entry_point in discovered:
            try:
                plugin_class = entry_point.load()
                plugin = plugin_class()
                self.plugins[entry_point.name] = plugin
            except Exception as e:
                print(f"Failed to load plugin {entry_point.name}: {e}")

    def get_plugin(self, name: str):
        """Get a loaded plugin by name"""
        return self.plugins.get(name)
```

### Extension Points (Hooks)

Define clear extension points where plugins can add functionality:

```python
# core/hooks.py
from typing import List, Callable, Any
from dataclasses import dataclass

@dataclass
class HookContext:
    """Context passed to hook handlers"""
    data: Any
    metadata: dict

class HookSystem:
    """Event-based hook system for plugins"""

    def __init__(self):
        self._hooks: Dict[str, List[Callable]] = {}

    def register(self, hook_name: str, handler: Callable):
        """Register a handler for a hook"""
        if hook_name not in self._hooks:
            self._hooks[hook_name] = []
        self._hooks[hook_name].append(handler)

    def trigger(self, hook_name: str, context: HookContext) -> HookContext:
        """Trigger all handlers for a hook, allowing modification"""
        for handler in self._hooks.get(hook_name, []):
            context = handler(context) or context
        return context

    def decorator(self, hook_name: str):
        """Decorator to register a hook handler"""
        def wrapper(func):
            self.register(hook_name, func)
            return func
        return wrapper

# Global hook system
hooks = HookSystem()

# Define standard hooks
HOOK_COMPONENT_LOADED = "component_loaded"
HOOK_UNIT_CREATED = "unit_created"
HOOK_BATTLE_START = "battle_start"
HOOK_BATTLE_TICK = "battle_tick"
HOOK_DAMAGE_DEALT = "damage_dealt"
HOOK_COMPONENT_DESTROYED = "component_destroyed"
HOOK_BATTLE_END = "battle_end"

# Example: Plugin using hooks
# plugins/damage_logger.py
from core.hooks import hooks, HOOK_DAMAGE_DEALT, HookContext

@hooks.decorator(HOOK_DAMAGE_DEALT)
def log_damage(context: HookContext):
    """Log all damage events"""
    damage_event = context.data
    print(f"{damage_event['attacker']} dealt {damage_event['amount']} "
          f"damage to {damage_event['target']}")
    return context

# Example: Core engine triggering hooks
def deal_damage(attacker, target, amount):
    # Apply damage
    target.health -= amount

    # Trigger hook for plugins
    context = HookContext(
        data={
            'attacker': attacker,
            'target': target,
            'amount': amount,
            'damage_type': attacker.weapon.damage_type
        },
        metadata={'timestamp': time.time()}
    )
    hooks.trigger(HOOK_DAMAGE_DEALT, context)
```

---

## Validation and Constraints

### Why Validation Matters

In component-based systems, validation ensures:
1. **Component Compatibility**: Required dependencies are present
2. **Resource Constraints**: Power, weight, slots within limits
3. **Logical Consistency**: No conflicting components
4. **Data Integrity**: All required fields are present and valid
5. **Balance**: Units follow game rules

### Validation Layers

```
┌─────────────────────────────────────────┐
│  Layer 1: Schema Validation             │
│  (Pydantic, JSON Schema)                │
│  - Field types correct                  │
│  - Required fields present              │
│  - Value ranges valid                   │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│  Layer 2: Component Validation          │
│  (Business rules)                       │
│  - Component dependencies met           │
│  - No conflicting components            │
│  - Placement rules followed             │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│  Layer 3: Resource Validation           │
│  (Budget constraints)                   │
│  - Power budget not exceeded            │
│  - Weight limit not exceeded            │
│  - Slot capacity not exceeded           │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│  Layer 4: Balance Validation            │
│  (Optional, game rules)                 │
│  - Cost within limits                   │
│  - Power level appropriate              │
│  - No banned combinations               │
└─────────────────────────────────────────┘
```

### Schema Validation with Pydantic

```python
from pydantic import BaseModel, Field, validator, root_validator
from typing import List, Optional, Literal
from enum import Enum

class DamageType(str, Enum):
    KINETIC = "kinetic"
    ENERGY = "energy"
    EXPLOSIVE = "explosive"

class ComponentType(str, Enum):
    OFFENSIVE = "offensive"
    DEFENSIVE = "defensive"
    MOBILITY = "mobility"
    SUPPORT = "support"

class WeaponStats(BaseModel):
    """Weapon statistics with validation"""
    damage: int = Field(gt=0, description="Base damage per hit")
    range: float = Field(gt=0, le=500, description="Maximum range in meters")
    fire_rate: float = Field(gt=0, le=10, description="Shots per second")
    accuracy: float = Field(ge=0, le=1, description="Hit probability (0-1)")
    damage_type: DamageType

    @validator('fire_rate')
    def fire_rate_reasonable(cls, v):
        if v > 5:
            raise ValueError('Fire rate above 5/sec requires special approval')
        return v

class ResourceCost(BaseModel):
    """Resource requirements"""
    power_draw: int = Field(ge=0, description="Power consumed in watts")
    weight: int = Field(gt=0, description="Weight in kg")
    slots: int = Field(gt=0, description="Grid slots occupied")
    cost: int = Field(ge=0, description="Build cost in credits")

    @validator('power_draw')
    def power_non_negative(cls, v):
        if v < 0:
            raise ValueError('Power draw cannot be negative')
        return v

class WeaponComponent(BaseModel):
    """Complete weapon component with validation"""
    name: str = Field(min_length=1, max_length=100)
    id: str = Field(regex=r'^[a-z0-9_]+$')  # lowercase, numbers, underscores only
    type: Literal[ComponentType.OFFENSIVE]
    category: Literal["weapon"]

    stats: WeaponStats
    resources: ResourceCost

    # Optional fields
    description: Optional[str] = None
    tags: List[str] = []

    @root_validator
    def check_balance(cls, values):
        """Cross-field validation for balance"""
        stats = values.get('stats')
        resources = values.get('resources')

        if stats and resources:
            # Simple balance check: high damage = high cost
            dps = stats.damage * stats.fire_rate
            if dps > 100 and resources.cost < 500:
                raise ValueError('High DPS weapons must cost at least 500 credits')

        return values

    class Config:
        # Allow using enum values
        use_enum_values = True

        # Example JSON schema generation
        schema_extra = {
            "example": {
                "name": "Laser Cannon Mk1",
                "id": "laser_cannon_mk1",
                "type": "offensive",
                "category": "weapon",
                "stats": {
                    "damage": 50,
                    "range": 100,
                    "fire_rate": 1.0,
                    "accuracy": 0.85,
                    "damage_type": "energy"
                },
                "resources": {
                    "power_draw": 20,
                    "weight": 50,
                    "slots": 1,
                    "cost": 100
                }
            }
        }

# Usage
try:
    weapon = WeaponComponent(
        name="Test Weapon",
        id="test_weapon",
        type="offensive",
        category="weapon",
        stats={
            "damage": 50,
            "range": 100,
            "fire_rate": 1.0,
            "accuracy": 0.85,
            "damage_type": "energy"
        },
        resources={
            "power_draw": 20,
            "weight": 50,
            "slots": 1,
            "cost": 100
        }
    )
except ValidationError as e:
    print(f"Validation failed: {e}")
```

### Component Dependency Validation

```python
from typing import Set, Dict, List
from dataclasses import dataclass, field

@dataclass
class ComponentRequirements:
    """Define what a component needs to function"""
    requires: Set[str] = field(default_factory=set)  # Must have these component types
    conflicts: Set[str] = field(default_factory=set)  # Cannot have these
    min_power: int = 0  # Minimum power generation required

class DependencyValidator:
    """Validate component dependencies"""

    def __init__(self):
        # Define component requirements
        self.requirements: Dict[str, ComponentRequirements] = {
            'shield': ComponentRequirements(
                requires={'power_generator'},
                min_power=50
            ),
            'laser_weapon': ComponentRequirements(
                requires={'power_generator'},
                min_power=20
            ),
            'plasma_weapon': ComponentRequirements(
                requires={'power_generator', 'cooling_system'},
                min_power=100
            ),
            'hover_engine': ComponentRequirements(
                conflicts={'wheeled_engine', 'legged_engine'}
            ),
            'heavy_armor': ComponentRequirements(
                conflicts={'light_armor'}
            ),
        }

    def validate_unit(self, components: List[Component]) -> ValidationResult:
        """Validate all component dependencies in a unit"""
        errors = []
        warnings = []

        # Get component types present
        present_types = {c.type for c in components}

        # Check each component's requirements
        for component in components:
            req = self.requirements.get(component.id)
            if not req:
                continue

            # Check required dependencies
            missing = req.requires - present_types
            if missing:
                errors.append(
                    f"{component.name} requires {missing} but they are not present"
                )

            # Check conflicts
            conflicts = req.conflicts & present_types
            if conflicts:
                errors.append(
                    f"{component.name} conflicts with {conflicts}"
                )

            # Check power requirements
            if req.min_power > 0:
                total_power = sum(
                    c.power_output for c in components
                    if hasattr(c, 'power_output')
                )
                if total_power < req.min_power:
                    errors.append(
                        f"{component.name} needs {req.min_power}W but only "
                        f"{total_power}W available"
                    )

        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )

@dataclass
class ValidationResult:
    """Result of validation check"""
    valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def __str__(self):
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

### Resource Budget Validation

```python
from dataclasses import dataclass
from typing import List

@dataclass
class ResourceBudget:
    """Resource limits for a unit"""
    max_power: int
    max_weight: int
    max_slots: int
    max_cost: int = float('inf')  # Optional cost limit

@dataclass
class ResourceUsage:
    """Current resource usage"""
    power: int = 0
    weight: int = 0
    slots: int = 0
    cost: int = 0

    def add(self, component):
        """Add a component's resource costs"""
        self.power += component.resources.power_draw
        self.weight += component.resources.weight
        self.slots += component.resources.slots
        self.cost += component.resources.cost

    def within_budget(self, budget: ResourceBudget) -> bool:
        """Check if within budget"""
        return (
            self.power <= budget.max_power and
            self.weight <= budget.max_weight and
            self.slots <= budget.max_slots and
            self.cost <= budget.max_cost
        )

    def get_violations(self, budget: ResourceBudget) -> List[str]:
        """Get list of budget violations"""
        violations = []

        if self.power > budget.max_power:
            violations.append(
                f"Power: {self.power}/{budget.max_power}W "
                f"(over by {self.power - budget.max_power}W)"
            )

        if self.weight > budget.max_weight:
            violations.append(
                f"Weight: {self.weight}/{budget.max_weight}kg "
                f"(over by {self.weight - budget.max_weight}kg)"
            )

        if self.slots > budget.max_slots:
            violations.append(
                f"Slots: {self.slots}/{budget.max_slots} "
                f"(over by {self.slots - budget.max_slots})"
            )

        if self.cost > budget.max_cost:
            violations.append(
                f"Cost: {self.cost}/{budget.max_cost} credits "
                f"(over by {self.cost - budget.max_cost})"
            )

        return violations

    def get_remaining(self, budget: ResourceBudget) -> 'ResourceUsage':
        """Get remaining budget"""
        return ResourceUsage(
            power=max(0, budget.max_power - self.power),
            weight=max(0, budget.max_weight - self.weight),
            slots=max(0, budget.max_slots - self.slots),
            cost=max(0, budget.max_cost - self.cost)
        )

class BudgetValidator:
    """Validate resource budgets"""

    @staticmethod
    def validate(components: List[Component], budget: ResourceBudget) -> ValidationResult:
        """Validate components against budget"""
        usage = ResourceUsage()

        # Calculate total usage
        for component in components:
            usage.add(component)

        # Check budget
        if usage.within_budget(budget):
            remaining = usage.get_remaining(budget)
            return ValidationResult(
                valid=True,
                warnings=[
                    f"Resource usage: Power {usage.power}/{budget.max_power}W, "
                    f"Weight {usage.weight}/{budget.max_weight}kg, "
                    f"Slots {usage.slots}/{budget.max_slots}"
                ]
            )
        else:
            return ValidationResult(
                valid=False,
                errors=usage.get_violations(budget)
            )
```

---

## Resource Systems

### Common Resource Types

In component-based systems, resources constrain what can be built:

| Resource | Purpose | Examples |
|----------|---------|----------|
| **Power** | Energy generation/consumption | Generators produce, weapons consume |
| **Weight** | Mass and carrying capacity | Engines limited by total weight |
| **Space** | Physical slots/volume | Grid-based or volumetric |
| **Cost** | Build/purchase limitation | Credits, materials, build points |
| **Heat** | Thermal management | Weapons generate, cooling dissipates |
| **Ammo** | Consumable resources | Missile launchers, ballistic weapons |
| **Crew** | Personnel requirements | Larger ships need more crew |

### Power System Design

**Power Generation and Consumption**:

```python
from dataclasses import dataclass, field
from typing import List, Dict
from enum import Enum

class PowerPriority(Enum):
    """Power allocation priority"""
    CRITICAL = 1   # Life support, core systems
    HIGH = 2       # Shields, primary weapons
    NORMAL = 3     # Sensors, secondary weapons
    LOW = 4        # Luxury systems

@dataclass
class PowerGenerator:
    """Component that generates power"""
    name: str
    max_output: int  # Watts
    current_output: int = 0
    efficiency: float = 1.0  # 0.0-1.0, degrades with damage

    def get_available_power(self) -> int:
        """Get current power generation"""
        return int(self.max_output * self.efficiency)

@dataclass
class PowerConsumer:
    """Component that consumes power"""
    name: str
    power_draw: int  # Watts when active
    priority: PowerPriority = PowerPriority.NORMAL
    is_active: bool = True
    current_draw: int = 0

    def get_power_need(self) -> int:
        """Get current power needs"""
        return self.power_draw if self.is_active else 0

class PowerSystem:
    """Manages power generation and distribution"""

    def __init__(self):
        self.generators: List[PowerGenerator] = []
        self.consumers: List[PowerConsumer] = []

    def add_generator(self, generator: PowerGenerator):
        """Add a power generator"""
        self.generators.append(generator)

    def add_consumer(self, consumer: PowerConsumer):
        """Add a power consumer"""
        self.consumers.append(consumer)

    def get_total_generation(self) -> int:
        """Calculate total power generation"""
        return sum(g.get_available_power() for g in self.generators)

    def get_total_demand(self) -> int:
        """Calculate total power demand"""
        return sum(c.get_power_need() for c in self.consumers)

    def allocate_power(self) -> Dict[str, int]:
        """Allocate power to consumers based on priority"""
        available_power = self.get_total_generation()
        allocation = {}

        # Sort consumers by priority
        sorted_consumers = sorted(
            self.consumers,
            key=lambda c: c.priority.value
        )

        # Allocate power by priority
        for consumer in sorted_consumers:
            need = consumer.get_power_need()

            if available_power >= need:
                # Full power
                consumer.current_draw = need
                available_power -= need
                allocation[consumer.name] = need
            elif available_power > 0:
                # Partial power
                consumer.current_draw = available_power
                allocation[consumer.name] = available_power
                available_power = 0
            else:
                # No power
                consumer.current_draw = 0
                allocation[consumer.name] = 0

        return allocation

    def is_power_sufficient(self) -> bool:
        """Check if power generation meets demand"""
        return self.get_total_generation() >= self.get_total_demand()

    def get_power_status(self) -> Dict[str, any]:
        """Get detailed power system status"""
        generation = self.get_total_generation()
        demand = self.get_total_demand()

        return {
            'generation': generation,
            'demand': demand,
            'surplus': generation - demand,
            'efficiency': generation / demand if demand > 0 else float('inf'),
            'generators': len(self.generators),
            'consumers': len([c for c in self.consumers if c.is_active])
        }

# Example usage
power_system = PowerSystem()

# Add generators
reactor = PowerGenerator(name="Fusion Reactor", max_output=1000)
solar = PowerGenerator(name="Solar Panels", max_output=200, efficiency=0.8)
power_system.add_generator(reactor)
power_system.add_generator(solar)

# Add consumers
shields = PowerConsumer(
    name="Shield Generator",
    power_draw=400,
    priority=PowerPriority.HIGH
)
laser = PowerConsumer(
    name="Laser Cannon",
    power_draw=200,
    priority=PowerPriority.NORMAL
)
life_support = PowerConsumer(
    name="Life Support",
    power_draw=100,
    priority=PowerPriority.CRITICAL
)

power_system.add_consumer(shields)
power_system.add_consumer(laser)
power_system.add_consumer(life_support)

# Allocate power
allocation = power_system.allocate_power()
status = power_system.get_power_status()

print(f"Power Status: {status}")
print(f"Allocation: {allocation}")
```

### Weight and Center of Mass

```python
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class ComponentPlacement:
    """Component with position and weight"""
    component_id: str
    weight: int  # kg
    position: Tuple[int, int]  # (x, y) on grid

class MassSystem:
    """Calculate weight distribution and center of mass"""

    def __init__(self, max_weight: int):
        self.max_weight = max_weight
        self.placements: List[ComponentPlacement] = []

    def add_component(self, placement: ComponentPlacement):
        """Add a component placement"""
        self.placements.append(placement)

    def get_total_weight(self) -> int:
        """Calculate total weight"""
        return sum(p.weight for p in self.placements)

    def is_within_limit(self) -> bool:
        """Check if within weight limit"""
        return self.get_total_weight() <= self.max_weight

    def get_center_of_mass(self) -> Tuple[float, float]:
        """Calculate center of mass"""
        if not self.placements:
            return (0.0, 0.0)

        total_weight = self.get_total_weight()
        if total_weight == 0:
            return (0.0, 0.0)

        # Weighted average of positions
        cm_x = sum(p.weight * p.position[0] for p in self.placements) / total_weight
        cm_y = sum(p.weight * p.position[1] for p in self.placements) / total_weight

        return (cm_x, cm_y)

    def get_balance_score(self, center: Tuple[float, float]) -> float:
        """
        Calculate how balanced the unit is.
        Lower score = better balance.
        Score is distance from ideal center.
        """
        cm = self.get_center_of_mass()
        dx = cm[0] - center[0]
        dy = cm[1] - center[1]
        return (dx**2 + dy**2) ** 0.5

    def get_weight_distribution(self) -> Dict[str, int]:
        """Get weight by component type"""
        distribution = {}
        for placement in self.placements:
            comp_type = placement.component_id.split('_')[0]  # Crude type extraction
            distribution[comp_type] = distribution.get(comp_type, 0) + placement.weight
        return distribution
```

### Slot/Space System

```python
from typing import Set, Tuple, List
from dataclasses import dataclass

@dataclass
class GridSpace:
    """Grid-based space management"""
    width: int
    height: int
    occupied: Set[Tuple[int, int]] = field(default_factory=set)

    def is_free(self, x: int, y: int) -> bool:
        """Check if grid position is free"""
        return (0 <= x < self.width and
                0 <= y < self.height and
                (x, y) not in self.occupied)

    def can_place(self, x: int, y: int, size: Tuple[int, int]) -> bool:
        """Check if component of given size can be placed"""
        width, height = size
        for dx in range(width):
            for dy in range(height):
                if not self.is_free(x + dx, y + dy):
                    return False
        return True

    def place(self, x: int, y: int, size: Tuple[int, int]) -> bool:
        """Place component on grid"""
        if not self.can_place(x, y, size):
            return False

        width, height = size
        for dx in range(width):
            for dy in range(height):
                self.occupied.add((x + dx, y + dy))
        return True

    def remove(self, x: int, y: int, size: Tuple[int, int]):
        """Remove component from grid"""
        width, height = size
        for dx in range(width):
            for dy in range(height):
                self.occupied.discard((x + dx, y + dy))

    def get_available_spaces(self) -> int:
        """Get number of free spaces"""
        return (self.width * self.height) - len(self.occupied)

    def get_utilization(self) -> float:
        """Get space utilization (0.0 - 1.0)"""
        total = self.width * self.height
        return len(self.occupied) / total if total > 0 else 0.0
```

### Multi-Resource Budget System

```python
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class ResourceLimits:
    """Maximum resource limits"""
    power: int
    weight: int
    slots: int
    heat_capacity: int = 1000
    crew: int = 0

@dataclass
class ResourceCosts:
    """Resource costs of a component"""
    power: int = 0
    weight: int = 0
    slots: int = 0
    heat: int = 0
    crew: int = 0

class ResourceManager:
    """Manage multiple resource types"""

    def __init__(self, limits: ResourceLimits):
        self.limits = limits
        self.used = ResourceCosts()
        self.components: Dict[str, ResourceCosts] = {}

    def add_component(self, component_id: str, costs: ResourceCosts) -> bool:
        """Add component if resources available"""
        # Calculate new totals
        new_used = ResourceCosts(
            power=self.used.power + costs.power,
            weight=self.used.weight + costs.weight,
            slots=self.used.slots + costs.slots,
            heat=self.used.heat + costs.heat,
            crew=self.used.crew + costs.crew
        )

        # Check limits
        if not self._within_limits(new_used):
            return False

        # Add component
        self.used = new_used
        self.components[component_id] = costs
        return True

    def remove_component(self, component_id: str) -> bool:
        """Remove component and free resources"""
        if component_id not in self.components:
            return False

        costs = self.components[component_id]
        self.used.power -= costs.power
        self.used.weight -= costs.weight
        self.used.slots -= costs.slots
        self.used.heat -= costs.heat
        self.used.crew -= costs.crew

        del self.components[component_id]
        return True

    def _within_limits(self, costs: ResourceCosts) -> bool:
        """Check if costs are within limits"""
        return (
            costs.power <= self.limits.power and
            costs.weight <= self.limits.weight and
            costs.slots <= self.limits.slots and
            costs.heat <= self.limits.heat_capacity and
            costs.crew <= self.limits.crew
        )

    def get_available(self) -> ResourceCosts:
        """Get remaining resources"""
        return ResourceCosts(
            power=self.limits.power - self.used.power,
            weight=self.limits.weight - self.used.weight,
            slots=self.limits.slots - self.used.slots,
            heat=self.limits.heat_capacity - self.used.heat,
            crew=self.limits.crew - self.used.crew
        )

    def get_violations(self) -> List[str]:
        """Get list of resource violations"""
        violations = []

        if self.used.power > self.limits.power:
            violations.append(
                f"Power over budget: {self.used.power}/{self.limits.power}"
            )
        if self.used.weight > self.limits.weight:
            violations.append(
                f"Weight over budget: {self.used.weight}/{self.limits.weight}"
            )
        if self.used.slots > self.limits.slots:
            violations.append(
                f"Slots over budget: {self.used.slots}/{self.limits.slots}"
            )
        if self.used.heat > self.limits.heat_capacity:
            violations.append(
                f"Heat over capacity: {self.used.heat}/{self.limits.heat_capacity}"
            )
        if self.used.crew > self.limits.crew:
            violations.append(
                f"Crew over limit: {self.used.crew}/{self.limits.crew}"
            )

        return violations

    def can_add(self, costs: ResourceCosts) -> bool:
        """Check if component can be added"""
        test_used = ResourceCosts(
            power=self.used.power + costs.power,
            weight=self.used.weight + costs.weight,
            slots=self.used.slots + costs.slots,
            heat=self.used.heat + costs.heat,
            crew=self.used.crew + costs.crew
        )
        return self._within_limits(test_used)
```

---

## Recommendations for Battle Automata Engine

Based on the research, here are specific recommendations for the Battle Automata Engine project:

### 1. Architecture Choice: ECS with Data-Driven Components

**Rationale**:
- Perfect fit for component-based unit building
- Theme-agnostic design requirement
- Modding/extensibility is a core goal
- Components naturally map to ECS entities

**Implementation**:
```python
# Core entity system
# src/core/entity.py
from dataclasses import dataclass, field
from typing import Dict, Any, Type, Set
import uuid

class Entity:
    """Lightweight entity (just an ID)"""
    def __init__(self):
        self.id = uuid.uuid4()
        self.components: Dict[Type, Any] = {}

    def add(self, component: Any):
        """Add a component"""
        self.components[type(component)] = component
        return self

    def get(self, component_type: Type):
        """Get a component by type"""
        return self.components.get(component_type)

    def has(self, component_type: Type) -> bool:
        """Check if entity has component"""
        return component_type in self.components

    def remove(self, component_type: Type):
        """Remove a component"""
        self.components.pop(component_type, None)

class World:
    """Container for all entities"""
    def __init__(self):
        self.entities: Dict[uuid.UUID, Entity] = {}

    def create_entity(self) -> Entity:
        """Create a new entity"""
        entity = Entity()
        self.entities[entity.id] = entity
        return entity

    def destroy_entity(self, entity: Entity):
        """Remove an entity"""
        self.entities.pop(entity.id, None)

    def query(self, *component_types: Type) -> List[Entity]:
        """Find entities with specific components"""
        return [
            entity for entity in self.entities.values()
            if all(entity.has(ct) for ct in component_types)
        ]
```

### 2. Component Definition: Pydantic + Dataclasses

**Rationale**:
- Automatic validation
- Type safety
- JSON/YAML serialization
- Clear error messages

**Implementation**:
```python
# src/core/components.py
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class ComponentCategory(str, Enum):
    WEAPON = "weapon"
    ARMOR = "armor"
    ENGINE = "engine"
    POWER = "power"
    SHIELD = "shield"
    SENSOR = "sensor"

class BaseComponent(BaseModel):
    """Base class for all components"""
    name: str
    id: str = Field(regex=r'^[a-z0-9_]+$')
    category: ComponentCategory
    description: Optional[str] = None

    class Config:
        use_enum_values = True

class WeaponComponent(BaseComponent):
    """Weapon component definition"""
    category: ComponentCategory = ComponentCategory.WEAPON
    damage: int = Field(gt=0)
    range: float = Field(gt=0)
    fire_rate: float = Field(gt=0)
    accuracy: float = Field(ge=0, le=1)
    power_draw: int = Field(ge=0)

# Load from YAML
import yaml
weapon_data = yaml.safe_load(open('laser_cannon.yaml'))
weapon = WeaponComponent(**weapon_data)  # Automatic validation!
```

### 3. Data Format: YAML Primary, JSON Secondary

**Rationale**:
- YAML more readable for component definitions
- JSON better for unit serialization
- Both supported through abstraction

**Directory Structure**:
```
data/
├── themes/
│   ├── space-ships/
│   │   ├── theme.yaml           # Theme metadata
│   │   ├── components/
│   │   │   ├── weapons/
│   │   │   │   ├── laser_cannon_mk1.yaml
│   │   │   │   ├── missile_launcher.yaml
│   │   │   │   └── ...
│   │   │   ├── armor/
│   │   │   │   ├── light_plating.yaml
│   │   │   │   └── ...
│   │   │   ├── engines/
│   │   │   └── power/
│   │   └── units/
│   │       ├── fighter.yaml
│   │       ├── bomber.yaml
│   │       └── ...
│   └── mechs/
│       └── ...
└── battles/
    ├── scenario_01.yaml
    └── ...
```

### 4. Plugin System: Decorator-Based Registry

**Rationale**:
- Simple to implement
- No external dependencies
- Easy for modders to understand
- Works well with Python's import system

**Implementation**:
```python
# src/core/registry.py
from typing import Dict, Type
from .components import BaseComponent

class ComponentRegistry:
    """Global component registry"""
    _components: Dict[str, Type[BaseComponent]] = {}

    @classmethod
    def register(cls, component_id: str):
        """Decorator to register component types"""
        def decorator(component_class: Type[BaseComponent]):
            cls._components[component_id] = component_class
            return component_class
        return decorator

    @classmethod
    def get(cls, component_id: str) -> Type[BaseComponent]:
        """Get component class by ID"""
        return cls._components.get(component_id)

    @classmethod
    def create(cls, component_id: str, **kwargs) -> BaseComponent:
        """Create component instance"""
        component_class = cls.get(component_id)
        if not component_class:
            raise ValueError(f"Unknown component: {component_id}")
        return component_class(**kwargs)

# Plugin usage:
# plugins/custom_weapons.py
from src.core.registry import ComponentRegistry
from src.core.components import WeaponComponent

@ComponentRegistry.register('plasma_cannon')
class PlasmaCannon(WeaponComponent):
    heat_generation: int = 50
    cooling_rate: int = 10
```

### 5. Validation: Multi-Layer Approach

**Implementation**:
```python
# src/core/validation.py
from typing import List
from pydantic import ValidationError

class UnitValidator:
    """Multi-layer unit validation"""

    def validate(self, unit: 'Unit') -> ValidationResult:
        """Run all validation layers"""
        errors = []
        warnings = []

        # Layer 1: Schema validation (already done by Pydantic)

        # Layer 2: Component dependencies
        dep_result = self._validate_dependencies(unit)
        errors.extend(dep_result.errors)
        warnings.extend(dep_result.warnings)

        # Layer 3: Resource budgets
        budget_result = self._validate_budgets(unit)
        errors.extend(budget_result.errors)
        warnings.extend(budget_result.warnings)

        # Layer 4: Balance rules (optional)
        balance_result = self._validate_balance(unit)
        warnings.extend(balance_result.warnings)

        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )

    def _validate_dependencies(self, unit) -> ValidationResult:
        """Check component dependencies"""
        # Implementation from earlier sections
        pass

    def _validate_budgets(self, unit) -> ValidationResult:
        """Check resource budgets"""
        # Implementation from earlier sections
        pass

    def _validate_balance(self, unit) -> ValidationResult:
        """Check balance rules"""
        # Optional: cost limits, power caps, etc.
        pass
```

### 6. Resource System: Unified Manager

**Implementation**:
```python
# src/core/resources.py
from dataclasses import dataclass

@dataclass
class UnitResources:
    """Unit-level resource management"""
    # Budgets
    max_power: int
    max_weight: int
    max_slots: int

    # Current usage
    power_used: int = 0
    weight_used: int = 0
    slots_used: int = 0

    # Runtime resources
    power_generation: int = 0
    power_consumption: int = 0

    def add_component(self, component) -> bool:
        """Add component if resources available"""
        new_power = self.power_used + component.power_draw
        new_weight = self.weight_used + component.weight
        new_slots = self.slots_used + component.slots

        if (new_power <= self.max_power and
            new_weight <= self.max_weight and
            new_slots <= self.max_slots):
            self.power_used = new_power
            self.weight_used = new_weight
            self.slots_used = new_slots
            return True
        return False

    def has_capacity(self, component) -> bool:
        """Check if component can fit"""
        return (
            self.power_used + component.power_draw <= self.max_power and
            self.weight_used + component.weight <= self.max_weight and
            self.slots_used + component.slots <= self.max_slots
        )
```

### 7. Builder Pattern for Unit Construction

**Implementation**:
```python
# src/core/builder.py
from typing import List, Optional
from .entity import Entity
from .components import BaseComponent
from .validation import UnitValidator
from .resources import UnitResources

class UnitBuilder:
    """Fluent interface for building units"""

    def __init__(self, name: str, max_power: int, max_weight: int, max_slots: int):
        self.entity = Entity()
        self.name = name
        self.resources = UnitResources(max_power, max_weight, max_slots)
        self.components: List[BaseComponent] = []
        self.validator = UnitValidator()

    def add_component(self, component: BaseComponent) -> 'UnitBuilder':
        """Add a component with validation"""
        if not self.resources.has_capacity(component):
            raise ValueError(f"Cannot add {component.name}: insufficient resources")

        self.components.append(component)
        self.resources.add_component(component)
        self.entity.add(component)
        return self

    def validate(self) -> ValidationResult:
        """Validate the current unit configuration"""
        return self.validator.validate(self)

    def build(self) -> Entity:
        """Build the final unit (with validation)"""
        result = self.validate()
        if not result.valid:
            raise ValueError(f"Unit validation failed: {result.errors}")

        if result.warnings:
            print(f"Warnings: {result.warnings}")

        return self.entity

# Usage
unit = (UnitBuilder("Fighter", max_power=100, max_weight=500, max_slots=10)
    .add_component(laser_cannon)
    .add_component(light_armor)
    .add_component(ion_engine)
    .build())
```

### 8. System Architecture

**Recommended structure**:
```python
# src/core/systems.py
from typing import List
from .entity import Entity, World

class System:
    """Base class for systems"""
    def process(self, world: World, delta_time: float):
        """Process entities in the world"""
        raise NotImplementedError

class MovementSystem(System):
    """Move entities based on velocity"""
    def process(self, world: World, delta_time: float):
        # Query entities with Position and Velocity components
        entities = world.query(Position, Velocity)

        for entity in entities:
            pos = entity.get(Position)
            vel = entity.get(Velocity)

            # Update position
            pos.x += vel.dx * delta_time
            pos.y += vel.dy * delta_time
            pos.facing += vel.rotation * delta_time

class CombatSystem(System):
    """Handle weapon firing and damage"""
    def process(self, world: World, delta_time: float):
        entities = world.query(Position, WeaponComponent)

        for entity in entities:
            weapon = entity.get(WeaponComponent)

            # Update cooldown
            weapon.cooldown_remaining = max(0, weapon.cooldown_remaining - delta_time)

            # Find targets and fire if ready
            if weapon.cooldown_remaining == 0:
                target = self.find_target(entity, world)
                if target:
                    self.fire_weapon(entity, target, weapon)
```

---

## Code Examples

### Complete Mini-Example: Simple ECS Battle System

```python
# mini_ecs_example.py
"""
Minimal ECS implementation for battle simulation.
Demonstrates core concepts in ~200 lines.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Type, Any, Optional
import uuid
from enum import Enum

# ============================================================================
# COMPONENTS (Pure Data)
# ============================================================================

@dataclass
class Position:
    x: float
    y: float
    facing: float = 0.0  # radians

@dataclass
class Health:
    current: int
    maximum: int

@dataclass
class Weapon:
    damage: int
    range: float
    cooldown: float = 0.0
    fire_rate: float = 1.0  # shots per second

@dataclass
class Team:
    team_id: int  # 0 = player, 1 = enemy

# ============================================================================
# ENTITY (Just an ID with components)
# ============================================================================

class Entity:
    def __init__(self):
        self.id = uuid.uuid4()
        self.components: Dict[Type, Any] = {}

    def add(self, component: Any) -> 'Entity':
        self.components[type(component)] = component
        return self

    def get(self, component_type: Type) -> Optional[Any]:
        return self.components.get(component_type)

    def has(self, component_type: Type) -> bool:
        return component_type in self.components

# ============================================================================
# WORLD (Entity container)
# ============================================================================

class World:
    def __init__(self):
        self.entities: Dict[uuid.UUID, Entity] = {}

    def create_entity(self) -> Entity:
        entity = Entity()
        self.entities[entity.id] = entity
        return entity

    def destroy_entity(self, entity: Entity):
        self.entities.pop(entity.id, None)

    def query(self, *component_types: Type) -> List[Entity]:
        """Find all entities with the specified components"""
        return [
            entity for entity in self.entities.values()
            if all(entity.has(ct) for ct in component_types)
        ]

# ============================================================================
# SYSTEMS (Pure Logic)
# ============================================================================

class CombatSystem:
    """Handle weapon firing and damage"""

    def process(self, world: World, delta_time: float):
        # Update weapon cooldowns
        for entity in world.query(Weapon):
            weapon = entity.get(Weapon)
            weapon.cooldown = max(0, weapon.cooldown - delta_time)

        # Process attacks
        attackers = world.query(Position, Weapon, Team)

        for attacker in attackers:
            weapon = attacker.get(Weapon)
            if weapon.cooldown > 0:
                continue  # Still on cooldown

            # Find target
            target = self._find_target(attacker, world)
            if target:
                self._fire_weapon(attacker, target, world)

    def _find_target(self, attacker: Entity, world: World) -> Optional[Entity]:
        """Find closest enemy in range"""
        attacker_pos = attacker.get(Position)
        attacker_team = attacker.get(Team)
        weapon = attacker.get(Weapon)

        targets = world.query(Position, Health, Team)
        valid_targets = [
            t for t in targets
            if t.get(Team).team_id != attacker_team.team_id
        ]

        closest = None
        closest_dist = float('inf')

        for target in valid_targets:
            target_pos = target.get(Position)
            dx = target_pos.x - attacker_pos.x
            dy = target_pos.y - attacker_pos.y
            dist = (dx**2 + dy**2) ** 0.5

            if dist <= weapon.range and dist < closest_dist:
                closest = target
                closest_dist = dist

        return closest

    def _fire_weapon(self, attacker: Entity, target: Entity, world: World):
        """Fire weapon at target"""
        weapon = attacker.get(Weapon)
        target_health = target.get(Health)

        # Deal damage
        target_health.current -= weapon.damage

        # Log event
        print(f"Entity {attacker.id} fired at {target.id} for {weapon.damage} damage")

        # Reset cooldown
        weapon.cooldown = 1.0 / weapon.fire_rate

        # Check if target destroyed
        if target_health.current <= 0:
            print(f"Entity {target.id} destroyed!")
            world.destroy_entity(target)

class BattleEngine:
    """Main battle loop"""

    def __init__(self):
        self.world = World()
        self.systems = [CombatSystem()]
        self.time = 0.0

    def simulate(self, duration: float, time_step: float = 0.1):
        """Run simulation"""
        steps = int(duration / time_step)

        for step in range(steps):
            self.time += time_step

            # Process all systems
            for system in self.systems:
                system.process(self.world, time_step)

            # Check win condition
            teams = {}
            for entity in self.world.query(Team):
                team_id = entity.get(Team).team_id
                teams[team_id] = teams.get(team_id, 0) + 1

            if len(teams) <= 1:
                winner = list(teams.keys())[0] if teams else None
                print(f"\nBattle ended at {self.time:.1f}s")
                print(f"Winner: Team {winner}")
                break

# ============================================================================
# USAGE EXAMPLE
# ============================================================================

def main():
    engine = BattleEngine()

    # Create player units
    fighter1 = engine.world.create_entity()
    fighter1.add(Position(x=0, y=0))
    fighter1.add(Health(current=100, maximum=100))
    fighter1.add(Weapon(damage=25, range=50, fire_rate=1.0))
    fighter1.add(Team(team_id=0))

    fighter2 = engine.world.create_entity()
    fighter2.add(Position(x=10, y=0))
    fighter2.add(Health(current=100, maximum=100))
    fighter2.add(Weapon(damage=20, range=50, fire_rate=1.5))
    fighter2.add(Team(team_id=0))

    # Create enemy units
    enemy1 = engine.world.create_entity()
    enemy1.add(Position(x=100, y=0))
    enemy1.add(Health(current=150, maximum=150))
    enemy1.add(Weapon(damage=30, range=50, fire_rate=0.8))
    enemy1.add(Team(team_id=1))

    # Run simulation
    print("=== Battle Start ===\n")
    engine.simulate(duration=30.0, time_step=0.1)

if __name__ == "__main__":
    main()
```

### Component Loading from YAML

```python
# component_loader_example.py
"""
Example of loading components from YAML with validation.
"""

import yaml
from pydantic import BaseModel, Field, validator
from pathlib import Path
from typing import Dict, Any, Optional

class WeaponStats(BaseModel):
    """Weapon statistics"""
    damage: int = Field(gt=0)
    range: float = Field(gt=0, le=500)
    fire_rate: float = Field(gt=0, le=10)
    accuracy: float = Field(ge=0, le=1)

    @validator('damage')
    def damage_reasonable(cls, v):
        if v > 1000:
            raise ValueError('Damage must be <= 1000')
        return v

class ResourceCosts(BaseModel):
    """Resource requirements"""
    power_draw: int = Field(ge=0)
    weight: int = Field(gt=0)
    slots: int = Field(gt=0)
    cost: int = Field(ge=0)

class WeaponComponent(BaseModel):
    """Complete weapon definition"""
    name: str = Field(min_length=1, max_length=100)
    id: str = Field(regex=r'^[a-z0-9_]+$')
    type: str = "offensive"
    category: str = "weapon"
    description: Optional[str] = None

    stats: WeaponStats
    resources: ResourceCosts

    class Config:
        schema_extra = {
            "example": {
                "name": "Laser Cannon Mk1",
                "id": "laser_cannon_mk1",
                "type": "offensive",
                "category": "weapon",
                "stats": {
                    "damage": 50,
                    "range": 100,
                    "fire_rate": 1.0,
                    "accuracy": 0.85
                },
                "resources": {
                    "power_draw": 20,
                    "weight": 50,
                    "slots": 1,
                    "cost": 100
                }
            }
        }

class ComponentLoader:
    """Load and validate components from YAML"""

    @staticmethod
    def load_weapon(file_path: Path) -> WeaponComponent:
        """Load weapon from YAML file"""
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)

        # Pydantic automatically validates
        return WeaponComponent(**data)

    @staticmethod
    def load_all_weapons(directory: Path) -> Dict[str, WeaponComponent]:
        """Load all weapons from directory"""
        weapons = {}

        for yaml_file in directory.glob("*.yaml"):
            try:
                weapon = ComponentLoader.load_weapon(yaml_file)
                weapons[weapon.id] = weapon
            except Exception as e:
                print(f"Error loading {yaml_file}: {e}")

        return weapons

# Usage
if __name__ == "__main__":
    # Example YAML content
    yaml_content = """
name: "Laser Cannon Mk1"
id: laser_cannon_mk1
type: offensive
category: weapon
description: Basic energy weapon with good accuracy

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
"""

    # Parse and validate
    data = yaml.safe_load(yaml_content)
    weapon = WeaponComponent(**data)

    print(f"Loaded: {weapon.name}")
    print(f"Damage: {weapon.stats.damage}")
    print(f"Valid: {weapon.id}")
```

---

## References and Resources

### Python ECS Libraries

1. **Esper** - https://github.com/benmoran56/esper
   - Most popular Python ECS library
   - Simple API, well-documented
   - `pip install esper`

2. **ecs-pattern** - https://github.com/ikvk/ecs_pattern
   - Decorator-based approach
   - Uses dataclasses
   - `pip install ecs-pattern`

3. **python-utilities ebs** - https://python-utilities.readthedocs.io/en/latest/ebs.html
   - Academic implementation
   - Good for learning concepts

### Design Patterns

4. **Game Programming Patterns** - https://gameprogrammingpatterns.com/
   - Excellent free book
   - Component pattern chapter
   - Many other useful patterns

5. **Component Pattern** - https://gameprogrammingpatterns.com/component.html
   - Specific chapter on component-based design
   - Examples and rationale

### Data-Driven Design

6. **Data-Driven Design Article** - DEV Community
   - Origins in game development
   - Benefits and trade-offs
   - Practical examples

7. **JSON vs YAML vs XML** - GameDev.net
   - Format comparison for game data
   - Community preferences
   - Performance considerations

### Plugin Architectures

8. **Plugin Architecture in Python** - DEV Community
   - Decorator-based registry pattern
   - Namespace packages
   - Entry points

9. **Building a Minimal Plugin Architecture** - Stack Overflow
   - Practical implementation examples
   - Common pitfalls
   - Best practices

10. **Python Factory Pattern with Decorators** - Medium
    - Dynamic registry implementation
    - Automatic registration
    - Type-safe factories

### Validation

11. **Pydantic Documentation** - https://docs.pydantic.dev/
    - Data validation library
    - JSON schema generation
    - Excellent Python integration

12. **Pydantic Dataclasses** - https://docs.pydantic.dev/latest/concepts/dataclasses/
    - Combining dataclasses with validation
    - Performance considerations

### Game-Specific

13. **Space Arena** (Mobile Game)
    - Inspiration for the project
    - Component-based ship building
    - Deterministic battles

14. **Entity Component System Wikipedia** - https://en.wikipedia.org/wiki/Entity_component_system
    - ECS history and concepts
    - Performance considerations
    - Common implementations

### Academic

15. **Understanding Component-Entity-Systems** - GameDev.net Tutorial
    - Deep dive into ECS architecture
    - Performance analysis
    - Implementation strategies

---

## Appendix: Architectural Diagrams

### ECS Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    BATTLE SIMULATION FLOW                   │
└─────────────────────────────────────────────────────────────┘

1. INITIALIZATION
   ┌──────────────┐
   │ Load Theme   │
   │ Components   │
   └──────┬───────┘
          │
          ▼
   ┌──────────────┐
   │ Create Units │
   │ from YAML    │
   └──────┬───────┘
          │
          ▼
   ┌──────────────┐
   │  Validate    │
   │   Units      │
   └──────┬───────┘
          │
          ▼

2. SIMULATION LOOP (Each Time Step)
   ┌─────────────────────────────────────────┐
   │  For each System:                       │
   │  ┌───────────────────────────────────┐ │
   │  │ Query entities with required      │ │
   │  │ component types                   │ │
   │  └─────────┬─────────────────────────┘ │
   │            │                             │
   │            ▼                             │
   │  ┌───────────────────────────────────┐ │
   │  │ Process each entity              │ │
   │  │ - Read component data            │ │
   │  │ - Apply logic                    │ │
   │  │ - Update component data          │ │
   │  └─────────┬─────────────────────────┘ │
   │            │                             │
   │            ▼                             │
   │  ┌───────────────────────────────────┐ │
   │  │ Trigger hooks for events         │ │
   │  └───────────────────────────────────┘ │
   └─────────────────────────────────────────┘
          │
          ▼
   ┌──────────────┐
   │ Check Win    │
   │ Conditions   │
   └──────┬───────┘
          │
          ▼
   ┌──────────────┐
   │ Log Events   │
   └──────────────┘

3. RESULTS
   ┌──────────────┐
   │ Generate     │
   │ Battle       │
   │ Report       │
   └──────────────┘
```

### Component Composition Example

```
┌─────────────────────────────────────────────────────────────┐
│                  UNIT: "Interceptor Mk1"                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Entity ID: 12345                                           │
│                                                             │
│  Components:                                                │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────┐ │
│  │   Position     │  │    Health      │  │     Team     │ │
│  ├────────────────┤  ├────────────────┤  ├──────────────┤ │
│  │ x: 100         │  │ current: 100   │  │ team_id: 0   │ │
│  │ y: 50          │  │ maximum: 100   │  └──────────────┘ │
│  │ facing: 0°     │  │ armor: 10      │                    │
│  └────────────────┘  └────────────────┘                    │
│                                                             │
│  ┌──────────────────────────┐  ┌─────────────────────────┐│
│  │    Weapon (Laser)        │  │    Engine               ││
│  ├──────────────────────────┤  ├─────────────────────────┤│
│  │ damage: 25               │  │ max_speed: 15           ││
│  │ range: 50                │  │ acceleration: 3.0       ││
│  │ fire_rate: 2.0           │  │ turn_rate: 90°/s        ││
│  │ cooldown: 0.0            │  └─────────────────────────┘│
│  │ power_draw: 20W          │                             │
│  └──────────────────────────┘                             │
│                                                             │
│  ┌──────────────────────────┐                             │
│  │   Resources              │                             │
│  ├──────────────────────────┤                             │
│  │ Power: 50/100 W          │                             │
│  │ Weight: 200/500 kg       │                             │
│  │ Slots: 8/20              │                             │
│  └──────────────────────────┘                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘

Systems that process this entity:
- MovementSystem (Position + Engine)
- CombatSystem (Position + Weapon + Team)
- RenderSystem (Position + Sprite)
- DamageSystem (Health + Armor)
```

### Plugin Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     CORE ENGINE                             │
│  ┌────────────────────────────────────────────────────┐    │
│  │              Component Registry                     │    │
│  │  - register(type, class)                           │    │
│  │  - get(type) -> class                              │    │
│  │  - create(type, **kwargs) -> instance              │    │
│  └────────────────────┬───────────────────────────────┘    │
│                       │                                     │
│  ┌────────────────────▼───────────────────────────────┐    │
│  │              Hook System                            │    │
│  │  - register_hook(name, handler)                    │    │
│  │  - trigger_hook(name, context)                     │    │
│  └────────────────────┬───────────────────────────────┘    │
│                       │                                     │
│  ┌────────────────────▼───────────────────────────────┐    │
│  │            Plugin Loader                            │    │
│  │  - discover_plugins()                              │    │
│  │  - load_plugin(name)                               │    │
│  └────────────────────────────────────────────────────┘    │
└──────────────────────────┬──────────────────────────────────┘
                           │
              ┌────────────┴────────────┐
              │                         │
    ┌─────────▼──────┐      ┌──────────▼────────┐
    │  Theme Plugin  │      │  Theme Plugin     │
    │  "Space Ships" │      │     "Mechs"       │
    ├────────────────┤      ├───────────────────┤
    │ Components:    │      │ Components:       │
    │ - LaserCannon  │      │ - PulseCannon     │
    │ - ShieldGen    │      │ - ArmorPlate      │
    │ - IonEngine    │      │ - HydraulicLeg    │
    │                │      │                   │
    │ Hooks:         │      │ Hooks:            │
    │ - on_fire      │      │ - on_step         │
    │ - on_hit       │      │ - on_melee        │
    └────────────────┘      └───────────────────┘
```

---

## Conclusion

This research report provides a comprehensive foundation for designing the Battle Automata Engine using component-based architecture patterns. The key takeaways are:

1. **ECS is the right choice** for this project due to its flexibility, modularity, and extensibility
2. **Pydantic + Dataclasses** provide robust validation and type safety for components
3. **YAML primary, JSON secondary** offers the best balance of readability and functionality
4. **Decorator-based plugin system** is simple yet powerful for theme extensibility
5. **Multi-layer validation** ensures units are valid at schema, dependency, and resource levels
6. **Resource management** is critical for balanced, interesting unit building

The provided code examples and architectural patterns should serve as a solid starting point for the Architect agent to design a robust, maintainable, and extensible battle simulation engine.

### Next Steps

1. **Architect** should review this research and create detailed technical specifications
2. **Developer** should implement core ECS framework based on examples provided
3. **QA Tester** should validate component loading and validation systems
4. **Documentation** should create user guides for theme and component creation

The architecture is designed to be:
- **Simple** to understand and implement
- **Flexible** to accommodate multiple themes
- **Extensible** through plugins and data files
- **Robust** with comprehensive validation
- **Testable** with clear separation of concerns

Good luck building the Battle Automata Engine!
