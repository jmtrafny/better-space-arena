# Data Model Architecture
## Battle Automata Engine

**Version:** 1.0
**Date:** 2025-11-13
**Status:** Design Specification
**Author:** Data Architect

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Design Philosophy](#design-philosophy)
3. [Component Data Model](#component-data-model)
4. [Unit Data Model](#unit-data-model)
5. [Battle Data Model](#battle-data-model)
6. [Validation Rules](#validation-rules)
7. [YAML Schema Examples](#yaml-schema-examples)
8. [Data Pipeline](#data-pipeline)
9. [Implementation Guidelines](#implementation-guidelines)

---

## Executive Summary

### Purpose

This document defines the complete data model architecture for the Battle Automata Engine, specifying how game data flows from YAML configuration files through Pydantic validation to frozen dataclasses used at runtime.

### Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **Pydantic for configuration** | Schema validation, type coercion, excellent error messages |
| **Frozen dataclasses for runtime** | Immutable state for determinism, performance, simplicity |
| **YAML for config** | Human-readable, supports comments, great for modding |
| **Three-layer validation** | Schema → Business Rules → Resource Constraints |
| **Rock-paper-scissors balance** | Damage types vs defense types create strategic depth |
| **Event sourcing pattern** | Complete battle history enables perfect replay |

### Data Flow Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    DATA PIPELINE OVERVIEW                        │
└─────────────────────────────────────────────────────────────────┘

1. CONFIGURATION LAYER (YAML Files)
   ┌──────────────────────────────────────┐
   │ data/themes/space-ships/components/  │
   │   laser_cannon.yaml                  │
   │   armor_plate.yaml                   │
   │   ...                                │
   └────────────────┬─────────────────────┘
                    │ yaml.safe_load()
                    ▼
2. VALIDATION LAYER (Pydantic Models)
   ┌──────────────────────────────────────┐
   │ ComponentConfig(BaseModel)           │
   │  - Schema validation                 │
   │  - Type coercion                     │
   │  - Cross-field validation            │
   │  - Business rule checks              │
   └────────────────┬─────────────────────┘
                    │ .to_runtime()
                    ▼
3. RUNTIME LAYER (Frozen Dataclasses)
   ┌──────────────────────────────────────┐
   │ Component (frozen dataclass)         │
   │  - Immutable                         │
   │  - Lightweight                       │
   │  - Hash-able                         │
   │  - Fast access                       │
   └────────────────┬─────────────────────┘
                    │
                    ▼
4. SIMULATION (Battle Engine)
   ┌──────────────────────────────────────┐
   │ BattleState                          │
   │  - Uses runtime objects              │
   │  - No mutations (creates new state)  │
   │  - Deterministic execution           │
   └──────────────────────────────────────┘
```

---

## Design Philosophy

### 1. Separation of Concerns

**Three Distinct Layers**:

```python
# Layer 1: Configuration (Mutable, Validating)
class ComponentConfig(BaseModel):
    """Pydantic model for loading and validating YAML"""
    name: str
    damage: int
    # ... validation rules

# Layer 2: Runtime (Immutable, Fast)
@dataclass(frozen=True)
class Component:
    """Runtime representation used in simulation"""
    name: str
    damage: int
    # ... no validation

# Layer 3: State (Mutable during simulation)
@dataclass
class ComponentState:
    """Current state of a component instance"""
    component: Component  # Reference to immutable definition
    current_health: float
    is_destroyed: bool
```

### 2. Immutability for Determinism

**Why Frozen Dataclasses?**

- **Deterministic**: Can't be accidentally modified during simulation
- **Thread-safe**: Can be safely shared (future parallelization)
- **Hash-able**: Can be used as dict keys, in sets
- **Debuggable**: State changes are explicit, not hidden

### 3. Validation Philosophy

**Fail Fast, Fail Loudly**:

```
Load YAML → Validate Schema → Validate Business Rules → Validate Resources
                ↓                    ↓                        ↓
            Type errors        Dependency errors        Budget errors
            Missing fields     Conflict errors          Balance errors
            Range errors       Compatibility errors     Cost errors
```

**Never let invalid data enter the simulation.**

### 4. Type Safety

**Full type hints throughout**:

```python
from typing import Literal, Union, Optional, List
from enum import Enum

class DamageType(str, Enum):
    KINETIC = "kinetic"
    ENERGY = "energy"
    EXPLOSIVE = "explosive"

# Type-safe component definition
@dataclass(frozen=True)
class WeaponComponent:
    damage: int
    damage_type: DamageType  # Not just 'str'
    range: float

# This won't type-check:
weapon = WeaponComponent(
    damage=50,
    damage_type="laser",  # mypy error: not a DamageType
    range=100
)

# This will:
weapon = WeaponComponent(
    damage=50,
    damage_type=DamageType.ENERGY,
    range=100
)
```

---

## Component Data Model

### Component Type Hierarchy

```
Component (base)
├── OffensiveComponent
│   ├── WeaponComponent
│   │   ├── BallisticWeapon
│   │   ├── MissileWeapon
│   │   └── EnergyWeapon
│   └── SupportOffensive
│       └── TargetingSystem
├── DefensiveComponent
│   ├── ArmorComponent
│   ├── ShieldComponent
│   └── PointDefenseComponent
├── MobilityComponent
│   ├── EngineComponent
│   ├── ThrusterComponent
│   └── GyroscopeComponent
└── SupportComponent
    ├── PowerComponent
    ├── SensorComponent
    ├── RepairComponent
    └── CoolingComponent
```

### Core Component Schema

#### 1. Base Component (Configuration)

```python
from pydantic import BaseModel, Field, validator, root_validator
from typing import Optional, Dict, Any, List, Literal
from enum import Enum

class ComponentType(str, Enum):
    """Top-level component categories"""
    OFFENSIVE = "offensive"
    DEFENSIVE = "defensive"
    MOBILITY = "mobility"
    SUPPORT = "support"

class ComponentCategory(str, Enum):
    """Specific component categories"""
    # Offensive
    WEAPON = "weapon"
    TARGETING = "targeting"

    # Defensive
    ARMOR = "armor"
    SHIELD = "shield"
    POINT_DEFENSE = "point_defense"

    # Mobility
    ENGINE = "engine"
    THRUSTER = "thruster"
    GYROSCOPE = "gyroscope"

    # Support
    POWER = "power"
    SENSOR = "sensor"
    REPAIR = "repair"
    COOLING = "cooling"

class ResourceCost(BaseModel):
    """Resource requirements for a component"""
    power_draw: int = Field(ge=0, description="Power consumed in watts")
    weight: int = Field(gt=0, description="Mass in kilograms")
    slots: int = Field(gt=0, le=10, description="Grid slots occupied (1-10)")
    cost: int = Field(ge=0, description="Build cost in credits")

    @validator('power_draw')
    def power_reasonable(cls, v):
        if v > 1000:
            raise ValueError('Power draw must be ≤ 1000W')
        return v

class ComponentConfig(BaseModel):
    """Base configuration for all components (Pydantic model for validation)"""

    # Identity
    id: str = Field(regex=r'^[a-z0-9_]+$', description="Unique identifier")
    name: str = Field(min_length=1, max_length=100, description="Display name")
    type: ComponentType
    category: ComponentCategory
    description: Optional[str] = Field(None, max_length=500)

    # Resources
    resources: ResourceCost

    # Metadata
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    # Constraints
    requires: List[str] = Field(
        default_factory=list,
        description="IDs of components this requires"
    )
    conflicts_with: List[str] = Field(
        default_factory=list,
        description="IDs of components this conflicts with"
    )

    @validator('id')
    def id_valid(cls, v):
        """Ensure ID follows naming conventions"""
        if not v.islower():
            raise ValueError('ID must be lowercase')
        if len(v) > 50:
            raise ValueError('ID must be ≤ 50 characters')
        return v

    @root_validator
    def check_type_category_match(cls, values):
        """Ensure category matches type"""
        type_val = values.get('type')
        category_val = values.get('category')

        # Define valid category-type mappings
        valid_mappings = {
            ComponentType.OFFENSIVE: {
                ComponentCategory.WEAPON,
                ComponentCategory.TARGETING
            },
            ComponentType.DEFENSIVE: {
                ComponentCategory.ARMOR,
                ComponentCategory.SHIELD,
                ComponentCategory.POINT_DEFENSE
            },
            ComponentType.MOBILITY: {
                ComponentCategory.ENGINE,
                ComponentCategory.THRUSTER,
                ComponentCategory.GYROSCOPE
            },
            ComponentType.SUPPORT: {
                ComponentCategory.POWER,
                ComponentCategory.SENSOR,
                ComponentCategory.REPAIR,
                ComponentCategory.COOLING
            }
        }

        if type_val and category_val:
            if category_val not in valid_mappings.get(type_val, set()):
                raise ValueError(
                    f"Category {category_val} not valid for type {type_val}"
                )

        return values

    def to_runtime(self) -> 'Component':
        """Convert to immutable runtime component"""
        # Implemented by subclasses
        raise NotImplementedError

    class Config:
        use_enum_values = True
```

#### 2. Weapon Component (Configuration)

```python
from typing import Literal

class DamageType(str, Enum):
    """Damage type for weapons"""
    KINETIC = "kinetic"      # Ballistic weapons
    ENERGY = "energy"        # Lasers, plasma
    EXPLOSIVE = "explosive"  # Missiles, grenades

class TargetingPriority(str, Enum):
    """How weapon selects targets"""
    CLOSEST = "closest"
    WEAKEST = "weakest"
    STRONGEST = "strongest"
    RANDOM = "random"
    PRIORITY_LIST = "priority_list"

class WeaponStats(BaseModel):
    """Core weapon statistics"""
    damage: int = Field(gt=0, le=1000, description="Base damage per hit")
    range: float = Field(gt=0, le=500, description="Maximum range in meters")
    fire_rate: float = Field(gt=0, le=10, description="Shots per second")
    accuracy: float = Field(ge=0, le=1, description="Base hit probability")
    projectile_speed: Optional[float] = Field(
        None,
        gt=0,
        description="Projectile speed (null for instant)"
    )

    @validator('fire_rate')
    def fire_rate_reasonable(cls, v, values):
        """High fire rate requires low damage"""
        damage = values.get('damage', 0)
        dps = damage * v
        if dps > 200:
            raise ValueError(
                f'DPS ({dps}) too high. Reduce damage or fire_rate.'
            )
        return v

class WeaponSpecial(BaseModel):
    """Special weapon properties"""
    armor_piercing: float = Field(
        default=0,
        ge=0,
        le=1,
        description="Ignore % of armor (0-1)"
    )
    shield_penetration: float = Field(
        default=0,
        ge=0,
        le=1,
        description="Bypass % of shields (0-1)"
    )
    splash_radius: Optional[float] = Field(
        None,
        ge=0,
        description="Area of effect radius"
    )
    splash_damage_falloff: float = Field(
        default=0.5,
        ge=0,
        le=1,
        description="Damage % at splash edge"
    )
    critical_chance: float = Field(
        default=0,
        ge=0,
        le=0.5,
        description="Critical hit chance (max 50%)"
    )
    critical_multiplier: float = Field(
        default=2.0,
        ge=1.0,
        le=5.0,
        description="Critical damage multiplier"
    )

class WeaponTargeting(BaseModel):
    """Targeting configuration"""
    firing_arc: float = Field(
        default=360,
        gt=0,
        le=360,
        description="Firing arc in degrees"
    )
    priority: TargetingPriority = TargetingPriority.CLOSEST
    component_priorities: List[str] = Field(
        default_factory=list,
        description="Target these component types first"
    )
    ignore_allies: bool = Field(
        default=True,
        description="Cannot target friendly units"
    )

    @validator('firing_arc')
    def arc_valid(cls, v):
        """Common arcs are 90, 180, 270, 360"""
        valid_arcs = {30, 45, 60, 90, 120, 180, 270, 360}
        if v not in valid_arcs:
            raise ValueError(
                f'Firing arc {v}° not standard. Use one of {valid_arcs}'
            )
        return v

class WeaponComponentConfig(ComponentConfig):
    """Complete weapon component configuration"""

    # Override to restrict type
    type: Literal[ComponentType.OFFENSIVE] = ComponentType.OFFENSIVE
    category: Literal[ComponentCategory.WEAPON] = ComponentCategory.WEAPON

    # Weapon-specific fields
    damage_type: DamageType
    stats: WeaponStats
    special: WeaponSpecial = Field(default_factory=WeaponSpecial)
    targeting: WeaponTargeting = Field(default_factory=WeaponTargeting)

    # Effects (for future expansion)
    on_hit_effects: List[Dict[str, Any]] = Field(default_factory=list)

    @root_validator
    def validate_balance(cls, values):
        """Cross-field balance validation"""
        resources = values.get('resources')
        stats = values.get('stats')

        if not (resources and stats):
            return values

        # Calculate DPS
        dps = stats.damage * stats.fire_rate

        # Higher DPS should require more power
        expected_power = dps * 0.5  # 0.5W per DPS
        if resources.power_draw < expected_power * 0.5:
            raise ValueError(
                f'Weapon with {dps} DPS needs ≥{expected_power * 0.5}W power'
            )

        # Energy weapons need more power than kinetic
        damage_type = values.get('damage_type')
        if damage_type == DamageType.ENERGY:
            if resources.power_draw < dps * 0.8:
                raise ValueError(
                    f'Energy weapons need ≥{dps * 0.8}W power for {dps} DPS'
                )

        return values

    def to_runtime(self) -> 'WeaponComponent':
        """Convert to immutable runtime weapon"""
        return WeaponComponent(
            id=self.id,
            name=self.name,
            damage_type=self.damage_type,
            damage=self.stats.damage,
            range=self.stats.range,
            fire_rate=self.stats.fire_rate,
            accuracy=self.stats.accuracy,
            projectile_speed=self.stats.projectile_speed,
            power_draw=self.resources.power_draw,
            weight=self.resources.weight,
            slots=self.resources.slots,
            armor_piercing=self.special.armor_piercing,
            shield_penetration=self.special.shield_penetration,
            splash_radius=self.special.splash_radius,
            critical_chance=self.special.critical_chance,
            critical_multiplier=self.special.critical_multiplier,
            firing_arc=self.targeting.firing_arc,
            targeting_priority=self.targeting.priority,
            tags=tuple(self.tags),  # Frozen
        )
```

#### 3. Weapon Component (Runtime)

```python
from dataclasses import dataclass
from typing import Tuple, Optional

@dataclass(frozen=True)
class WeaponComponent:
    """Immutable runtime weapon component (used in simulation)"""

    # Identity
    id: str
    name: str

    # Core stats
    damage_type: DamageType
    damage: int
    range: float
    fire_rate: float
    accuracy: float
    projectile_speed: Optional[float]

    # Resources
    power_draw: int
    weight: int
    slots: int

    # Special properties
    armor_piercing: float = 0.0
    shield_penetration: float = 0.0
    splash_radius: Optional[float] = None
    critical_chance: float = 0.0
    critical_multiplier: float = 2.0

    # Targeting
    firing_arc: float = 360.0
    targeting_priority: TargetingPriority = TargetingPriority.CLOSEST

    # Metadata (frozen)
    tags: Tuple[str, ...] = ()

    def __post_init__(self):
        """Validate runtime invariants (should never fail if config was validated)"""
        assert self.damage > 0, "Damage must be positive"
        assert 0 <= self.accuracy <= 1, "Accuracy must be 0-1"
        assert self.fire_rate > 0, "Fire rate must be positive"
```

### Defense Components

#### 1. Armor Component

```python
class ArmorType(str, Enum):
    """Armor material types"""
    COMPOSITE = "composite"      # Balanced
    REACTIVE = "reactive"        # Good vs explosives
    ABLATIVE = "ablative"        # Good vs energy
    KINETIC = "kinetic"          # Good vs ballistics

class ArmorStats(BaseModel):
    """Armor statistics"""
    armor_value: int = Field(
        gt=0,
        le=500,
        description="Damage reduction value"
    )
    coverage: float = Field(
        ge=0,
        le=1,
        description="% of unit covered (0-1)"
    )
    durability: int = Field(
        gt=0,
        description="Armor health points"
    )

class ArmorResistances(BaseModel):
    """Damage type resistances"""
    kinetic_resist: float = Field(
        default=1.0,
        ge=0,
        le=2.0,
        description="Multiplier vs kinetic (1.0=normal, 1.5=+50% resist)"
    )
    energy_resist: float = Field(default=1.0, ge=0, le=2.0)
    explosive_resist: float = Field(default=1.0, ge=0, le=2.0)

    @root_validator
    def resistances_balanced(cls, values):
        """Can't be strong against everything"""
        total = (
            values.get('kinetic_resist', 1.0) +
            values.get('energy_resist', 1.0) +
            values.get('explosive_resist', 1.0)
        )
        # Average resistance should be around 1.0
        if total > 4.0:  # Allows some specialization
            raise ValueError(
                'Total resistances too high. Specialize, not generalize.'
            )
        return values

class ArmorComponentConfig(ComponentConfig):
    """Armor component configuration"""

    type: Literal[ComponentType.DEFENSIVE] = ComponentType.DEFENSIVE
    category: Literal[ComponentCategory.ARMOR] = ComponentCategory.ARMOR

    armor_type: ArmorType
    stats: ArmorStats
    resistances: ArmorResistances = Field(default_factory=ArmorResistances)

    @root_validator
    def validate_balance(cls, values):
        """Balance validation"""
        stats = values.get('stats')
        resources = values.get('resources')

        if stats and resources:
            # Heavier armor = better protection
            armor_per_kg = stats.armor_value / resources.weight
            if armor_per_kg > 2.0:  # Max 2 armor per kg
                raise ValueError(
                    f'Armor too efficient: {armor_per_kg:.1f} armor/kg (max 2.0)'
                )

        return values

    def to_runtime(self) -> 'ArmorComponent':
        """Convert to runtime armor"""
        return ArmorComponent(
            id=self.id,
            name=self.name,
            armor_type=self.armor_type,
            armor_value=self.stats.armor_value,
            coverage=self.stats.coverage,
            max_durability=self.stats.durability,
            kinetic_resist=self.resistances.kinetic_resist,
            energy_resist=self.resistances.energy_resist,
            explosive_resist=self.resistances.explosive_resist,
            weight=self.resources.weight,
            slots=self.resources.slots,
            tags=tuple(self.tags),
        )

@dataclass(frozen=True)
class ArmorComponent:
    """Immutable runtime armor component"""

    # Identity
    id: str
    name: str

    # Stats
    armor_type: ArmorType
    armor_value: int
    coverage: float
    max_durability: int

    # Resistances
    kinetic_resist: float
    energy_resist: float
    explosive_resist: float

    # Resources
    weight: int
    slots: int

    # Metadata
    tags: Tuple[str, ...] = ()

    def get_effective_armor(self, damage_type: DamageType) -> float:
        """Calculate effective armor vs damage type"""
        multiplier = {
            DamageType.KINETIC: self.kinetic_resist,
            DamageType.ENERGY: self.energy_resist,
            DamageType.EXPLOSIVE: self.explosive_resist,
        }.get(damage_type, 1.0)

        return self.armor_value * multiplier
```

#### 2. Shield Component

```python
class ShieldStats(BaseModel):
    """Shield statistics"""
    shield_strength: int = Field(
        gt=0,
        le=1000,
        description="Shield hit points"
    )
    recharge_rate: float = Field(
        gt=0,
        le=100,
        description="HP recharged per second"
    )
    recharge_delay: float = Field(
        ge=0,
        le=10,
        description="Seconds before recharge starts"
    )
    coverage: float = Field(
        default=1.0,
        ge=0,
        le=1,
        description="% of unit covered"
    )

class ShieldComponentConfig(ComponentConfig):
    """Shield component configuration"""

    type: Literal[ComponentType.DEFENSIVE] = ComponentType.DEFENSIVE
    category: Literal[ComponentCategory.SHIELD] = ComponentCategory.SHIELD

    stats: ShieldStats

    # Shields resist energy better than kinetic
    energy_absorption: float = Field(
        default=1.0,
        ge=0.5,
        le=2.0,
        description="Energy damage multiplier (>1 = better)"
    )
    kinetic_absorption: float = Field(
        default=1.0,
        ge=0.5,
        le=2.0,
        description="Kinetic damage multiplier (<1 = worse)"
    )

    @root_validator
    def validate_power_requirement(cls, values):
        """Shields need significant power"""
        stats = values.get('stats')
        resources = values.get('resources')

        if stats and resources:
            # Power draw should scale with shield strength
            expected_power = stats.shield_strength * 0.1
            if resources.power_draw < expected_power:
                raise ValueError(
                    f'Shield needs ≥{expected_power}W for '
                    f'{stats.shield_strength} HP shield'
                )

        return values

    def to_runtime(self) -> 'ShieldComponent':
        return ShieldComponent(
            id=self.id,
            name=self.name,
            max_strength=self.stats.shield_strength,
            recharge_rate=self.stats.recharge_rate,
            recharge_delay=self.stats.recharge_delay,
            coverage=self.stats.coverage,
            energy_absorption=self.energy_absorption,
            kinetic_absorption=self.kinetic_absorption,
            power_draw=self.resources.power_draw,
            weight=self.resources.weight,
            slots=self.resources.slots,
            tags=tuple(self.tags),
        )

@dataclass(frozen=True)
class ShieldComponent:
    """Immutable runtime shield component"""

    id: str
    name: str

    # Stats
    max_strength: int
    recharge_rate: float
    recharge_delay: float
    coverage: float

    # Absorption
    energy_absorption: float
    kinetic_absorption: float

    # Resources
    power_draw: int
    weight: int
    slots: int

    tags: Tuple[str, ...] = ()

    def get_damage_absorbed(
        self,
        incoming_damage: float,
        damage_type: DamageType
    ) -> float:
        """Calculate how much damage shield absorbs"""
        multiplier = {
            DamageType.ENERGY: self.energy_absorption,
            DamageType.KINETIC: self.kinetic_absorption,
            DamageType.EXPLOSIVE: 1.0,  # Normal
        }.get(damage_type, 1.0)

        return incoming_damage * multiplier
```

### Mobility Components

#### Engine Component

```python
class EngineStats(BaseModel):
    """Engine statistics"""
    thrust: float = Field(
        gt=0,
        le=1000,
        description="Forward thrust in newtons"
    )
    max_speed: float = Field(
        gt=0,
        le=100,
        description="Maximum speed in m/s"
    )
    acceleration: float = Field(
        gt=0,
        le=50,
        description="Acceleration in m/s²"
    )
    turn_rate: float = Field(
        default=90,
        gt=0,
        le=360,
        description="Turning rate in degrees/s"
    )

class EngineComponentConfig(ComponentConfig):
    """Engine component configuration"""

    type: Literal[ComponentType.MOBILITY] = ComponentType.MOBILITY
    category: Literal[ComponentCategory.ENGINE] = ComponentCategory.ENGINE

    stats: EngineStats

    @root_validator
    def validate_thrust_vs_power(cls, values):
        """More thrust needs more power"""
        stats = values.get('stats')
        resources = values.get('resources')

        if stats and resources:
            # Power scales with thrust
            expected_power = stats.thrust * 0.2
            if resources.power_draw < expected_power * 0.7:
                raise ValueError(
                    f'Engine with {stats.thrust}N thrust needs '
                    f'≥{expected_power * 0.7}W power'
                )

        return values

    def to_runtime(self) -> 'EngineComponent':
        return EngineComponent(
            id=self.id,
            name=self.name,
            thrust=self.stats.thrust,
            max_speed=self.stats.max_speed,
            acceleration=self.stats.acceleration,
            turn_rate=self.stats.turn_rate,
            power_draw=self.resources.power_draw,
            weight=self.resources.weight,
            slots=self.resources.slots,
            tags=tuple(self.tags),
        )

@dataclass(frozen=True)
class EngineComponent:
    """Immutable runtime engine component"""

    id: str
    name: str

    # Stats
    thrust: float
    max_speed: float
    acceleration: float
    turn_rate: float

    # Resources
    power_draw: int
    weight: int
    slots: int

    tags: Tuple[str, ...] = ()
```

### Support Components

#### Power Generator Component

```python
class PowerGeneratorStats(BaseModel):
    """Power generator statistics"""
    max_output: int = Field(
        gt=0,
        le=2000,
        description="Maximum power output in watts"
    )
    efficiency: float = Field(
        default=1.0,
        ge=0.5,
        le=1.0,
        description="Operating efficiency (degrades with damage)"
    )

class PowerGeneratorComponentConfig(ComponentConfig):
    """Power generator configuration"""

    type: Literal[ComponentType.SUPPORT] = ComponentType.SUPPORT
    category: Literal[ComponentCategory.POWER] = ComponentCategory.POWER

    stats: PowerGeneratorStats

    @validator('resources')
    def power_generator_no_draw(cls, v):
        """Generators produce power, they don't consume it"""
        if v.power_draw > 0:
            raise ValueError('Power generators cannot have power_draw > 0')
        # Actually, set it to negative to indicate generation
        v.power_draw = 0
        return v

    def to_runtime(self) -> 'PowerGeneratorComponent':
        return PowerGeneratorComponent(
            id=self.id,
            name=self.name,
            max_output=self.stats.max_output,
            base_efficiency=self.stats.efficiency,
            weight=self.resources.weight,
            slots=self.resources.slots,
            tags=tuple(self.tags),
        )

@dataclass(frozen=True)
class PowerGeneratorComponent:
    """Immutable runtime power generator"""

    id: str
    name: str

    # Stats
    max_output: int
    base_efficiency: float

    # Resources
    weight: int
    slots: int

    tags: Tuple[str, ...] = ()

    def get_output(self, current_efficiency: float = 1.0) -> int:
        """Calculate current power output"""
        return int(self.max_output * self.base_efficiency * current_efficiency)
```

---

## Unit Data Model

### Unit Configuration Schema

```python
from typing import List, Tuple

class UnitLayout(BaseModel):
    """Unit grid layout"""
    width: int = Field(gt=0, le=20, description="Grid width")
    height: int = Field(gt=0, le=20, description="Grid height")

    @root_validator
    def size_reasonable(cls, values):
        """Limit total grid size"""
        width = values.get('width', 0)
        height = values.get('height', 0)
        total = width * height
        if total > 100:
            raise ValueError(
                f'Grid size {width}x{height}={total} too large (max 100)'
            )
        return values

class Position(BaseModel):
    """2D position"""
    x: int = Field(ge=0)
    y: int = Field(ge=0)

    def to_tuple(self) -> Tuple[int, int]:
        return (self.x, self.y)

class ComponentPlacement(BaseModel):
    """Component placement on unit grid"""
    component_id: str = Field(description="ID of component to place")
    position: Position
    facing: float = Field(
        default=0,
        ge=0,
        lt=360,
        description="Facing in degrees (0=forward)"
    )
    slot_name: Optional[str] = Field(
        None,
        description="Logical slot name (e.g., 'weapon_1')"
    )

class UnitResourceBudget(BaseModel):
    """Resource limits for unit"""
    max_power: int = Field(
        gt=0,
        le=2000,
        description="Maximum power budget in watts"
    )
    max_weight: int = Field(
        gt=0,
        le=10000,
        description="Maximum weight in kg"
    )
    max_slots: int = Field(
        gt=0,
        le=100,
        description="Maximum component slots"
    )
    max_cost: Optional[int] = Field(
        None,
        ge=0,
        description="Optional cost limit in credits"
    )

class AIBehavior(BaseModel):
    """AI behavior configuration"""
    movement_style: Literal[
        "aggressive",
        "defensive",
        "kiting",
        "stationary"
    ] = "aggressive"
    engagement_range: float = Field(
        default=100,
        gt=0,
        description="Preferred combat range"
    )
    retreat_threshold: float = Field(
        default=0.2,
        ge=0,
        le=1,
        description="Retreat when health < this % (0-1)"
    )

class UnitConfig(BaseModel):
    """Complete unit configuration (validated from YAML)"""

    # Identity
    id: str = Field(regex=r'^[a-z0-9_]+$')
    name: str = Field(min_length=1, max_length=100)
    theme: str = Field(description="Theme this unit belongs to")

    # Description
    description: Optional[str] = Field(None, max_length=1000)
    class_name: Optional[str] = Field(
        None,
        description="Unit class (fighter, bomber, etc.)"
    )

    # Layout
    layout: UnitLayout

    # Components
    components: List[ComponentPlacement]

    # Resources
    resources: UnitResourceBudget

    # AI (optional)
    ai: Optional[AIBehavior] = None

    # Metadata
    tags: List[str] = Field(default_factory=list)
    cost: Optional[int] = Field(None, ge=0)
    build_time: Optional[int] = Field(None, ge=0)

    @validator('components')
    def components_not_empty(cls, v):
        """Unit must have components"""
        if not v:
            raise ValueError('Unit must have at least one component')
        return v

    @root_validator
    def validate_component_positions(cls, values):
        """Ensure components fit on grid"""
        layout = values.get('layout')
        components = values.get('components', [])

        if not layout:
            return values

        for comp in components:
            pos = comp.position
            if pos.x >= layout.width or pos.y >= layout.height:
                raise ValueError(
                    f'Component at ({pos.x},{pos.y}) outside grid '
                    f'({layout.width}x{layout.height})'
                )

        return values

    def to_runtime(
        self,
        component_registry: 'ComponentRegistry'
    ) -> 'Unit':
        """Convert to runtime unit

        Requires component registry to resolve component IDs.
        """
        # Resolve component instances
        component_instances = []
        for placement in self.components:
            component = component_registry.get(placement.component_id)
            if not component:
                raise ValueError(
                    f'Component not found: {placement.component_id}'
                )
            component_instances.append((component, placement))

        return Unit(
            id=self.id,
            name=self.name,
            theme=self.theme,
            grid_width=self.layout.width,
            grid_height=self.layout.height,
            components=tuple(component_instances),  # Frozen
            max_power=self.resources.max_power,
            max_weight=self.resources.max_weight,
            max_slots=self.resources.max_slots,
            ai_behavior=self.ai.movement_style if self.ai else "aggressive",
            tags=tuple(self.tags),
        )
```

### Unit Runtime Schema

```python
@dataclass(frozen=True)
class Unit:
    """Immutable runtime unit definition"""

    # Identity
    id: str
    name: str
    theme: str

    # Layout
    grid_width: int
    grid_height: int

    # Components (immutable tuple of (component, placement) pairs)
    components: Tuple[Tuple['Component', ComponentPlacement], ...]

    # Resource limits
    max_power: int
    max_weight: int
    max_slots: int

    # AI
    ai_behavior: str

    # Metadata
    tags: Tuple[str, ...] = ()

    def __post_init__(self):
        """Validate unit (should never fail if config was validated)"""
        # These are runtime safety checks
        assert len(self.components) > 0, "Unit must have components"
        assert self.grid_width > 0 and self.grid_height > 0, "Invalid grid"

    def get_total_power_draw(self) -> int:
        """Calculate total power consumption"""
        total = 0
        for component, _ in self.components:
            if hasattr(component, 'power_draw'):
                total += component.power_draw
        return total

    def get_total_power_generation(self) -> int:
        """Calculate total power generation"""
        total = 0
        for component, _ in self.components:
            if isinstance(component, PowerGeneratorComponent):
                total += component.max_output
        return total

    def get_total_weight(self) -> int:
        """Calculate total unit weight"""
        return sum(comp.weight for comp, _ in self.components)

    def get_total_slots(self) -> int:
        """Calculate total slots used"""
        return sum(comp.slots for comp, _ in self.components)

    def get_weapons(self) -> List[Tuple['WeaponComponent', ComponentPlacement]]:
        """Get all weapon components"""
        return [
            (comp, placement)
            for comp, placement in self.components
            if isinstance(comp, WeaponComponent)
        ]

    def get_armor(self) -> List['ArmorComponent']:
        """Get all armor components"""
        return [
            comp
            for comp, _ in self.components
            if isinstance(comp, ArmorComponent)
        ]

    def get_shields(self) -> List['ShieldComponent']:
        """Get all shield components"""
        return [
            comp
            for comp, _ in self.components
            if isinstance(comp, ShieldComponent)
        ]

    def get_engines(self) -> List['EngineComponent']:
        """Get all engines"""
        return [
            comp
            for comp, _ in self.components
            if isinstance(comp, EngineComponent)
        ]
```

---

## Battle Data Model

### Battle Configuration

```python
class BattleConfig(BaseModel):
    """Battle simulation configuration"""

    # Random seed for determinism
    seed: int = Field(description="Random seed for reproducible battles")

    # Time parameters
    time_step: float = Field(
        default=0.1,
        gt=0,
        le=1.0,
        description="Simulation time step in seconds"
    )
    max_duration: float = Field(
        default=300.0,
        gt=0,
        le=3600.0,
        description="Maximum battle duration in seconds"
    )
    max_turns: int = Field(
        default=3000,
        gt=0,
        description="Maximum turns (failsafe)"
    )

    # Arena
    arena_width: float = Field(
        default=1000,
        gt=0,
        le=5000,
        description="Arena width in meters"
    )
    arena_height: float = Field(
        default=1000,
        gt=0,
        le=5000,
        description="Arena height in meters"
    )

    # Starting positions
    unit1_position: Tuple[float, float] = Field(
        default=(100, 500),
        description="Unit 1 starting position (x, y)"
    )
    unit2_position: Tuple[float, float] = Field(
        default=(900, 500),
        description="Unit 2 starting position (x, y)"
    )

    # Win conditions
    timeout_is_draw: bool = Field(
        default=False,
        description="Timeout results in draw (else most health wins)"
    )

    @root_validator
    def validate_positions(cls, values):
        """Ensure starting positions are in arena"""
        width = values.get('arena_width')
        height = values.get('arena_height')
        pos1 = values.get('unit1_position')
        pos2 = values.get('unit2_position')

        if pos1:
            if not (0 <= pos1[0] <= width and 0 <= pos1[1] <= height):
                raise ValueError(f'Unit 1 position {pos1} outside arena')

        if pos2:
            if not (0 <= pos2[0] <= width and 0 <= pos2[1] <= height):
                raise ValueError(f'Unit 2 position {pos2} outside arena')

        return values

@dataclass(frozen=True)
class BattleSetup:
    """Immutable battle setup"""
    config: BattleConfig
    unit1: Unit
    unit2: Unit

    def __post_init__(self):
        """Validate setup"""
        assert self.unit1.id != self.unit2.id, "Units must be different"
```

### Battle State (Mutable during simulation)

```python
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class ComponentState:
    """Mutable state of a component instance during battle"""
    component: 'Component'  # Immutable definition
    current_health: float
    is_destroyed: bool = False

    # Weapon-specific state
    cooldown_remaining: float = 0.0
    current_target: Optional[str] = None

    # Shield-specific state
    shield_strength: float = 0.0
    time_since_last_hit: float = 0.0

    def __post_init__(self):
        """Initialize state from component"""
        # Set initial health based on component type
        if hasattr(self.component, 'max_durability'):
            # Armor
            self.current_health = self.component.max_durability
        elif hasattr(self.component, 'max_strength'):
            # Shield
            self.shield_strength = self.component.max_strength
        else:
            # Default: 100 HP
            self.current_health = 100.0

@dataclass
class UnitState:
    """Mutable state of a unit during battle"""
    unit: Unit  # Immutable definition

    # Position and motion
    x: float
    y: float
    facing: float  # Radians
    velocity_x: float = 0.0
    velocity_y: float = 0.0
    angular_velocity: float = 0.0

    # Component states
    component_states: List[ComponentState] = field(default_factory=list)

    # Status
    is_active: bool = True
    team: int = 0  # 0 or 1

    def __post_init__(self):
        """Initialize component states"""
        if not self.component_states:
            self.component_states = [
                ComponentState(component=comp)
                for comp, _ in self.unit.components
            ]

    def get_total_health(self) -> float:
        """Sum of all component health"""
        return sum(
            cs.current_health
            for cs in self.component_states
            if not cs.is_destroyed
        )

    def is_destroyed(self) -> bool:
        """Check if unit is destroyed (all components gone)"""
        # Unit is destroyed if it has no functional components
        functional = [
            cs for cs in self.component_states
            if not cs.is_destroyed
        ]
        return len(functional) == 0

    def get_active_weapons(self) -> List[Tuple[WeaponComponent, ComponentState]]:
        """Get weapons that can fire"""
        result = []
        for cs in self.component_states:
            if (isinstance(cs.component, WeaponComponent) and
                not cs.is_destroyed and
                cs.cooldown_remaining <= 0):
                result.append((cs.component, cs))
        return result

@dataclass
class BattleState:
    """Complete mutable battle state"""

    # Setup
    setup: BattleSetup

    # Current state
    turn: int = 0
    time_elapsed: float = 0.0

    # Units
    unit1_state: UnitState = field(default=None)
    unit2_state: UnitState = field(default=None)

    # RNG state (for determinism)
    rng_state: Optional[Any] = None

    # Result
    winner: Optional[int] = None  # 0, 1, or None (draw)
    outcome: Optional[str] = None  # "elimination", "timeout", "draw"

    def __post_init__(self):
        """Initialize unit states if not provided"""
        if self.unit1_state is None:
            x, y = self.setup.config.unit1_position
            self.unit1_state = UnitState(
                unit=self.setup.unit1,
                x=x,
                y=y,
                facing=0.0,
                team=0
            )

        if self.unit2_state is None:
            x, y = self.setup.config.unit2_position
            self.unit2_state = UnitState(
                unit=self.setup.unit2,
                x=x,
                y=y,
                facing=3.14159,  # Face opposite direction
                team=1
            )

    def is_finished(self) -> bool:
        """Check if battle is over"""
        if self.winner is not None:
            return True
        if self.turn >= self.setup.config.max_turns:
            return True
        if self.time_elapsed >= self.setup.config.max_duration:
            return True
        return False

    def get_active_units(self) -> List[UnitState]:
        """Get units still in battle"""
        return [
            us for us in [self.unit1_state, self.unit2_state]
            if us.is_active and not us.is_destroyed()
        ]
```

### Event Logging

```python
from enum import Enum
from typing import Any, Dict

class EventType(str, Enum):
    """Battle event types"""
    # Battle lifecycle
    BATTLE_START = "battle_start"
    BATTLE_END = "battle_end"
    TURN_START = "turn_start"
    TURN_END = "turn_end"

    # Combat
    WEAPON_FIRED = "weapon_fired"
    PROJECTILE_HIT = "projectile_hit"
    PROJECTILE_MISS = "projectile_miss"
    DAMAGE_DEALT = "damage_dealt"
    SHIELD_HIT = "shield_hit"
    ARMOR_HIT = "armor_hit"
    CRITICAL_HIT = "critical_hit"
    COMPONENT_DESTROYED = "component_destroyed"
    UNIT_DESTROYED = "unit_destroyed"

    # Movement
    UNIT_MOVED = "unit_moved"
    UNIT_ROTATED = "unit_rotated"
    COLLISION = "collision"

    # Other
    TIMEOUT = "timeout"

@dataclass(frozen=True)
class BattleEvent:
    """Immutable battle event (for logging)"""

    # When
    timestamp: float
    turn: int

    # What
    event_type: EventType

    # Who
    actor_unit: Optional[int]  # 0 or 1
    target_unit: Optional[int] = None

    # Details (frozen dict-like structure)
    data: Tuple[Tuple[str, Any], ...] = ()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            'timestamp': self.timestamp,
            'turn': self.turn,
            'event_type': self.event_type.value,
            'actor_unit': self.actor_unit,
            'target_unit': self.target_unit,
            'data': dict(self.data)
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> 'BattleEvent':
        """Deserialize from dictionary"""
        return cls(
            timestamp=d['timestamp'],
            turn=d['turn'],
            event_type=EventType(d['event_type']),
            actor_unit=d.get('actor_unit'),
            target_unit=d.get('target_unit'),
            data=tuple(d.get('data', {}).items())
        )

# Factory functions for creating events
def create_weapon_fired_event(
    timestamp: float,
    turn: int,
    unit: int,
    weapon_id: str,
    target: int
) -> BattleEvent:
    """Create weapon fired event"""
    return BattleEvent(
        timestamp=timestamp,
        turn=turn,
        event_type=EventType.WEAPON_FIRED,
        actor_unit=unit,
        target_unit=target,
        data=(
            ('weapon_id', weapon_id),
        )
    )

def create_damage_event(
    timestamp: float,
    turn: int,
    attacker: int,
    target: int,
    damage: float,
    damage_type: str,
    component_id: str
) -> BattleEvent:
    """Create damage dealt event"""
    return BattleEvent(
        timestamp=timestamp,
        turn=turn,
        event_type=EventType.DAMAGE_DEALT,
        actor_unit=attacker,
        target_unit=target,
        data=(
            ('damage', damage),
            ('damage_type', damage_type),
            ('component_id', component_id),
        )
    )

# Event logger
@dataclass
class EventLogger:
    """Logger for battle events"""
    events: List[BattleEvent] = field(default_factory=list)

    def log(self, event: BattleEvent) -> None:
        """Add event to log"""
        self.events.append(event)

    def get_events(
        self,
        event_type: Optional[EventType] = None,
        unit: Optional[int] = None
    ) -> List[BattleEvent]:
        """Query events"""
        result = self.events

        if event_type is not None:
            result = [e for e in result if e.event_type == event_type]

        if unit is not None:
            result = [
                e for e in result
                if e.actor_unit == unit or e.target_unit == unit
            ]

        return result

    def to_json(self) -> List[Dict[str, Any]]:
        """Export to JSON-serializable format"""
        return [e.to_dict() for e in self.events]
```

### Battle Result

```python
@dataclass(frozen=True)
class BattleStatistics:
    """Immutable battle statistics"""

    # Outcome
    winner: Optional[int]  # 0, 1, or None
    outcome_reason: str  # "elimination", "timeout", etc.

    # Duration
    total_turns: int
    total_time: float

    # Unit 0 stats
    unit0_damage_dealt: float
    unit0_damage_taken: float
    unit0_final_health: float
    unit0_components_destroyed: int

    # Unit 1 stats
    unit1_damage_dealt: float
    unit1_damage_taken: float
    unit1_final_health: float
    unit1_components_destroyed: int

    # Combat stats
    total_shots_fired: int
    total_hits: int
    total_misses: int
    total_critical_hits: int

    def get_accuracy(self) -> float:
        """Calculate overall accuracy"""
        if self.total_shots_fired == 0:
            return 0.0
        return self.total_hits / self.total_shots_fired

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'winner': self.winner,
            'outcome_reason': self.outcome_reason,
            'total_turns': self.total_turns,
            'total_time': self.total_time,
            'accuracy': self.get_accuracy(),
            'unit_0': {
                'damage_dealt': self.unit0_damage_dealt,
                'damage_taken': self.unit0_damage_taken,
                'final_health': self.unit0_final_health,
                'components_destroyed': self.unit0_components_destroyed,
            },
            'unit_1': {
                'damage_dealt': self.unit1_damage_dealt,
                'damage_taken': self.unit1_damage_taken,
                'final_health': self.unit1_final_health,
                'components_destroyed': self.unit1_components_destroyed,
            },
            'combat': {
                'shots_fired': self.total_shots_fired,
                'hits': self.total_hits,
                'misses': self.total_misses,
                'critical_hits': self.total_critical_hits,
            }
        }

@dataclass(frozen=True)
class BattleResult:
    """Complete immutable battle result"""

    # Configuration
    setup: BattleSetup

    # Statistics
    statistics: BattleStatistics

    # Event log
    events: Tuple[BattleEvent, ...]  # Frozen

    # Final state snapshot
    final_state: Dict[str, Any]  # Snapshot for replay

    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary"""
        return {
            'config': {
                'seed': self.setup.config.seed,
                'time_step': self.setup.config.time_step,
                'max_duration': self.setup.config.max_duration,
            },
            'units': {
                'unit_0': self.setup.unit1.name,
                'unit_1': self.setup.unit2.name,
            },
            'statistics': self.statistics.to_dict(),
            'events': [e.to_dict() for e in self.events],
            'final_state': self.final_state,
        }

    def save_json(self, filepath: str) -> None:
        """Save result to JSON file"""
        import json
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    def get_winner_name(self) -> Optional[str]:
        """Get name of winning unit"""
        if self.statistics.winner == 0:
            return self.setup.unit1.name
        elif self.statistics.winner == 1:
            return self.setup.unit2.name
        return None

    def print_summary(self) -> str:
        """Generate human-readable summary"""
        winner = self.get_winner_name() or "DRAW"

        summary = f"""
=== Battle Result ===
Winner: {winner}
Reason: {self.statistics.outcome_reason}

Duration: {self.statistics.total_time:.1f}s ({self.statistics.total_turns} turns)
Accuracy: {self.statistics.get_accuracy():.1%}

{self.setup.unit1.name}:
  Damage Dealt: {self.statistics.unit0_damage_dealt:.0f}
  Damage Taken: {self.statistics.unit0_damage_taken:.0f}
  Final Health: {self.statistics.unit0_final_health:.0f}

{self.setup.unit2.name}:
  Damage Dealt: {self.statistics.unit1_damage_dealt:.0f}
  Damage Taken: {self.statistics.unit1_damage_taken:.0f}
  Final Health: {self.statistics.unit1_final_health:.0f}
"""
        return summary
```

---

## Validation Rules

### Validation Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  VALIDATION PIPELINE                     │
└─────────────────────────────────────────────────────────┘

LAYER 1: Schema Validation (Pydantic)
┌──────────────────────────────────────┐
│ • Field types correct                 │
│ • Required fields present             │
│ • Value ranges valid                  │
│ • Regex patterns match                │
└────────────┬─────────────────────────┘
             │ PASS
             ▼
LAYER 2: Business Rules (Custom Validators)
┌──────────────────────────────────────┐
│ • Component dependencies met          │
│ • No conflicting components           │
│ • Type-category alignment             │
│ • Balance rules (DPS, armor/kg, etc.) │
└────────────┬─────────────────────────┘
             │ PASS
             ▼
LAYER 3: Resource Constraints
┌──────────────────────────────────────┐
│ • Power budget not exceeded           │
│ • Weight limit not exceeded           │
│ • Slot capacity not exceeded          │
│ • Cost limit not exceeded (optional)  │
└────────────┬─────────────────────────┘
             │ PASS
             ▼
LAYER 4: Integration Validation
┌──────────────────────────────────────┐
│ • All component IDs resolve           │
│ • Components fit on grid              │
│ • Power generation ≥ consumption      │
│ • Unit has required components        │
└────────────┬─────────────────────────┘
             │ PASS
             ▼
         VALID UNIT
```

### Component Validation

```python
from typing import Set, List, Dict

class ComponentValidator:
    """Validates component definitions"""

    @staticmethod
    def validate_config(config: ComponentConfig) -> ValidationResult:
        """Validate component configuration

        Pydantic already did schema validation,
        now check business rules.
        """
        errors = []
        warnings = []

        # Check ID conventions
        if config.id.startswith('test_'):
            warnings.append('Component ID starts with "test_" (dev component?)')

        # Check resource costs are reasonable
        if config.resources.weight < 10:
            warnings.append('Very light component (< 10kg)')

        if config.resources.power_draw > 500:
            warnings.append('High power draw (> 500W)')

        # Check tags
        if not config.tags:
            warnings.append('No tags defined (recommended for filtering)')

        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )

class WeaponValidator:
    """Validates weapon components"""

    @staticmethod
    def validate_balance(weapon: WeaponComponentConfig) -> ValidationResult:
        """Check weapon balance"""
        errors = []
        warnings = []

        # DPS calculation
        dps = weapon.stats.damage * weapon.stats.fire_rate

        # DPS vs power
        power_per_dps = weapon.resources.power_draw / dps
        if power_per_dps < 0.3:
            errors.append(
                f'Weapon too power-efficient: {power_per_dps:.2f}W/DPS '
                f'(min 0.3W/DPS)'
            )

        # DPS vs weight
        dps_per_kg = dps / weapon.resources.weight
        if dps_per_kg > 3.0:
            errors.append(
                f'Weapon too light for DPS: {dps_per_kg:.1f} DPS/kg (max 3.0)'
            )

        # Range vs DPS
        if weapon.stats.range > 200 and dps > 150:
            warnings.append(
                'Long-range high-DPS weapon may be overpowered'
            )

        # Accuracy vs fire rate
        if weapon.stats.fire_rate > 3.0 and weapon.stats.accuracy > 0.9:
            warnings.append(
                'High fire-rate + high accuracy may be too strong'
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

    def __str__(self) -> str:
        if self.valid:
            result = "✓ Valid"
        else:
            result = "✗ Invalid"

        if self.errors:
            result += "\nErrors:"
            for e in self.errors:
                result += f"\n  - {e}"

        if self.warnings:
            result += "\nWarnings:"
            for w in self.warnings:
                result += f"\n  - {w}"

        return result
```

### Unit Validation

```python
class UnitValidator:
    """Validates unit configurations"""

    def __init__(self, component_registry: 'ComponentRegistry'):
        self.registry = component_registry

    def validate_unit(self, unit_config: UnitConfig) -> ValidationResult:
        """Complete unit validation"""
        errors = []
        warnings = []

        # STEP 1: Validate component references
        component_ids = [cp.component_id for cp in unit_config.components]
        for comp_id in component_ids:
            if not self.registry.has(comp_id):
                errors.append(f'Unknown component: {comp_id}')

        if errors:
            return ValidationResult(valid=False, errors=errors)

        # STEP 2: Load actual components
        components = [
            self.registry.get(cp.component_id)
            for cp in unit_config.components
        ]

        # STEP 3: Check dependencies
        dep_result = self._check_dependencies(components)
        errors.extend(dep_result.errors)
        warnings.extend(dep_result.warnings)

        # STEP 4: Check resource budgets
        budget_result = self._check_resources(components, unit_config.resources)
        errors.extend(budget_result.errors)
        warnings.extend(budget_result.warnings)

        # STEP 5: Check power generation vs consumption
        power_result = self._check_power(components)
        errors.extend(power_result.errors)
        warnings.extend(power_result.warnings)

        # STEP 6: Check unit has required components
        req_result = self._check_required_components(components)
        errors.extend(req_result.errors)
        warnings.extend(req_result.warnings)

        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )

    def _check_dependencies(
        self,
        components: List[ComponentConfig]
    ) -> ValidationResult:
        """Check component dependencies"""
        errors = []
        warnings = []

        # Build set of present component IDs
        present_ids = {c.id for c in components}

        for comp in components:
            # Check requires
            for required_id in comp.requires:
                if required_id not in present_ids:
                    errors.append(
                        f'{comp.name} requires {required_id} but it is missing'
                    )

            # Check conflicts
            for conflict_id in comp.conflicts_with:
                if conflict_id in present_ids:
                    errors.append(
                        f'{comp.name} conflicts with {conflict_id}'
                    )

        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )

    def _check_resources(
        self,
        components: List[ComponentConfig],
        budget: UnitResourceBudget
    ) -> ValidationResult:
        """Check resource budgets"""
        errors = []
        warnings = []

        # Calculate totals
        total_power = sum(c.resources.power_draw for c in components)
        total_weight = sum(c.resources.weight for c in components)
        total_slots = sum(c.resources.slots for c in components)
        total_cost = sum(c.resources.cost for c in components)

        # Check limits
        if total_power > budget.max_power:
            errors.append(
                f'Power budget exceeded: {total_power}/{budget.max_power}W'
            )

        if total_weight > budget.max_weight:
            errors.append(
                f'Weight limit exceeded: {total_weight}/{budget.max_weight}kg'
            )

        if total_slots > budget.max_slots:
            errors.append(
                f'Slot capacity exceeded: {total_slots}/{budget.max_slots}'
            )

        if budget.max_cost and total_cost > budget.max_cost:
            errors.append(
                f'Cost limit exceeded: {total_cost}/{budget.max_cost} credits'
            )

        # Warnings for poor utilization
        power_util = total_power / budget.max_power
        if power_util < 0.5:
            warnings.append(
                f'Low power utilization: {power_util:.0%} (< 50%)'
            )

        weight_util = total_weight / budget.max_weight
        if weight_util < 0.5:
            warnings.append(
                f'Low weight utilization: {weight_util:.0%} (< 50%)'
            )

        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )

    def _check_power(
        self,
        components: List[ComponentConfig]
    ) -> ValidationResult:
        """Check power generation vs consumption"""
        errors = []
        warnings = []

        # Calculate generation
        generation = sum(
            c.stats.max_output
            for c in components
            if isinstance(c, PowerGeneratorComponentConfig)
        )

        # Calculate consumption
        consumption = sum(c.resources.power_draw for c in components)

        # Check balance
        if consumption > generation:
            errors.append(
                f'Insufficient power: {consumption}W needed, {generation}W available'
            )
        elif generation > consumption * 1.5:
            warnings.append(
                f'Excess power generation: {generation}W vs {consumption}W needed'
            )

        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )

    def _check_required_components(
        self,
        components: List[ComponentConfig]
    ) -> ValidationResult:
        """Check unit has required component types"""
        errors = []
        warnings = []

        # Count component types
        has_weapon = any(
            isinstance(c, WeaponComponentConfig) for c in components
        )
        has_power = any(
            isinstance(c, PowerGeneratorComponentConfig) for c in components
        )
        has_engine = any(
            isinstance(c, EngineComponentConfig) for c in components
        )

        # Requirements
        if not has_weapon:
            warnings.append('Unit has no weapons')

        if not has_power:
            errors.append('Unit must have at least one power generator')

        if not has_engine:
            warnings.append('Unit has no engines (stationary unit?)')

        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
```

---

## YAML Schema Examples

### Component Example: Laser Cannon

```yaml
# data/themes/space-ships/components/weapons/laser_cannon_mk1.yaml

# Identity
id: laser_cannon_mk1
name: "Laser Cannon Mk1"
type: offensive
category: weapon

# Description
description: >
  Basic energy weapon with good accuracy and fire rate.
  Effective against shields, less effective against armor.
  Standard choice for light fighters.

# Weapon-specific
damage_type: energy

stats:
  damage: 50
  range: 100.0        # meters
  fire_rate: 1.0      # shots/second
  accuracy: 0.85      # 85% base hit chance
  projectile_speed: 200.0  # m/s (null for instant)

special:
  armor_piercing: 0.3       # Ignore 30% of armor
  shield_penetration: 0.0   # No shield bypass
  critical_chance: 0.1      # 10% crit chance
  critical_multiplier: 2.0  # 2x damage on crit

targeting:
  firing_arc: 90            # degrees
  priority: closest
  ignore_allies: true

# Resource costs
resources:
  power_draw: 20    # watts
  weight: 50        # kg
  slots: 1          # grid slots
  cost: 100         # credits

# Metadata
tags:
  - energy_weapon
  - point_defense
  - anti_fighter

# Advanced: on-hit effects (future expansion)
on_hit_effects: []
```

### Component Example: Heavy Armor Plate

```yaml
# data/themes/space-ships/components/armor/heavy_armor_mk1.yaml

id: heavy_armor_mk1
name: "Heavy Armor Plate Mk1"
type: defensive
category: armor

description: >
  Thick composite armor providing excellent protection.
  Strong against kinetic weapons, moderate vs energy.

armor_type: composite

stats:
  armor_value: 150
  coverage: 0.8        # Covers 80% of unit
  durability: 500      # Armor HP

resistances:
  kinetic_resist: 1.5  # 50% better vs kinetic
  energy_resist: 0.9   # 10% worse vs energy
  explosive_resist: 1.2  # 20% better vs explosive

resources:
  power_draw: 0        # Passive, no power needed
  weight: 200          # Heavy!
  slots: 3             # Takes up space
  cost: 150

tags:
  - heavy_armor
  - composite
  - tank
```

### Component Example: Ion Engine

```yaml
# data/themes/space-ships/components/engines/ion_engine_mk1.yaml

id: ion_engine_mk1
name: "Ion Engine Mk1"
type: mobility
category: engine

description: >
  Efficient ion drive providing good acceleration.
  Balanced thrust-to-power ratio.

stats:
  thrust: 300.0          # Newtons
  max_speed: 20.0        # m/s
  acceleration: 5.0      # m/s²
  turn_rate: 90.0        # degrees/s

resources:
  power_draw: 60         # watts
  weight: 100            # kg
  slots: 2
  cost: 120

tags:
  - ion_drive
  - balanced
  - standard
```

### Component Example: Fusion Reactor

```yaml
# data/themes/space-ships/components/power/fusion_reactor_small.yaml

id: fusion_reactor_small
name: "Small Fusion Reactor"
type: support
category: power

description: >
  Compact fusion reactor providing steady power output.
  Core component for any combat unit.

stats:
  max_output: 200      # watts generated
  efficiency: 1.0      # 100% efficiency when undamaged

resources:
  power_draw: 0        # Generates, doesn't consume
  weight: 150          # kg
  slots: 2             # Compact
  cost: 200            # Expensive

tags:
  - power_generation
  - fusion
  - core_component
```

### Unit Example: Light Fighter

```yaml
# data/themes/space-ships/units/interceptor_mk1.yaml

# Identity
id: interceptor_mk1
name: "Interceptor Mk1"
theme: space-ships
class_name: fighter

description: >
  Fast and maneuverable light fighter designed for hit-and-run
  tactics. Excellent against other fighters but vulnerable to
  heavy weapons. Relies on speed and shields over armor.

# Grid layout
layout:
  width: 10
  height: 10

# Component placement
components:
  # Weapons (front)
  - component_id: laser_cannon_mk1
    position:
      x: 5
      y: 2
    facing: 0        # Forward
    slot_name: weapon_primary

  - component_id: laser_cannon_mk1
    position:
      x: 4
      y: 2
    facing: 0
    slot_name: weapon_secondary

  # Defense (center)
  - component_id: shield_generator_light
    position:
      x: 5
      y: 5
    facing: 0
    slot_name: shield

  - component_id: light_armor_mk1
    position:
      x: 5
      y: 5
    facing: 0
    slot_name: armor_core

  # Power (center)
  - component_id: fusion_reactor_small
    position:
      x: 5
      y: 5
    facing: 0
    slot_name: reactor

  # Propulsion (rear)
  - component_id: ion_engine_mk1
    position:
      x: 5
      y: 8
    facing: 180      # Rear
    slot_name: main_engine

  - component_id: maneuvering_thruster
    position:
      x: 2
      y: 5
    facing: 270      # Left
    slot_name: thruster_left

  - component_id: maneuvering_thruster
    position:
      x: 8
      y: 5
    facing: 90       # Right
    slot_name: thruster_right

# Resource budgets
resources:
  max_power: 200     # watts
  max_weight: 800    # kg
  max_slots: 20      # grid slots
  max_cost: 1000     # credits (optional)

# AI behavior
ai:
  movement_style: kiting
  engagement_range: 80.0
  retreat_threshold: 0.3    # Retreat at 30% health

# Metadata
tags:
  - fighter
  - fast
  - anti_fighter
  - energy_weapons

cost: 850
build_time: 60      # seconds
```

### Battle Configuration Example

```yaml
# data/battles/test_battle_01.yaml

# Random seed for reproducibility
seed: 42

# Time parameters
time_step: 0.1        # 0.1 second per turn
max_duration: 300.0   # 5 minutes max
max_turns: 3000       # Failsafe

# Arena
arena_width: 1000.0   # meters
arena_height: 1000.0

# Starting positions
unit1_position: [100.0, 500.0]
unit2_position: [900.0, 500.0]

# Win conditions
timeout_is_draw: false  # Timeout = most health wins
```

---

## Data Pipeline

### Loading Pipeline

```
┌──────────────────────────────────────────────────────┐
│            DATA LOADING PIPELINE                      │
└──────────────────────────────────────────────────────┘

1. DISCOVER FILES
   ┌────────────────────────────┐
   │ Scan data/themes/*/        │
   │ Find all *.yaml files      │
   └──────────┬─────────────────┘
              │
              ▼
2. LOAD YAML
   ┌────────────────────────────┐
   │ yaml.safe_load(file)       │
   │ → Dict[str, Any]           │
   └──────────┬─────────────────┘
              │
              ▼
3. VALIDATE (Pydantic)
   ┌────────────────────────────┐
   │ ComponentConfig(**data)    │
   │ - Schema validation        │
   │ - Type coercion            │
   │ - Custom validators        │
   └──────────┬─────────────────┘
              │ If valid
              ▼
4. CONVERT TO RUNTIME
   ┌────────────────────────────┐
   │ config.to_runtime()        │
   │ → Component (frozen)       │
   └──────────┬─────────────────┘
              │
              ▼
5. REGISTER
   ┌────────────────────────────┐
   │ registry.register(comp)    │
   │ Store by ID                │
   └────────────────────────────┘
```

### Implementation

```python
from pathlib import Path
import yaml
from typing import Dict, List, Type

class ComponentLoader:
    """Loads components from YAML files"""

    def __init__(self, data_dir: Path):
        self.data_dir = Path(data_dir)

    def load_component(
        self,
        file_path: Path,
        component_type: Type[ComponentConfig]
    ) -> ComponentConfig:
        """Load and validate single component"""
        # Load YAML
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)

        # Validate with Pydantic
        try:
            config = component_type(**data)
        except ValidationError as e:
            raise ValueError(
                f'Invalid component in {file_path}:\n{e}'
            )

        # Additional business validation
        result = ComponentValidator.validate_config(config)
        if not result.valid:
            raise ValueError(
                f'Component validation failed for {file_path}:\n{result}'
            )

        if result.warnings:
            print(f'Warnings for {file_path}:\n{result}')

        return config

    def load_theme_components(
        self,
        theme_name: str
    ) -> Dict[str, 'Component']:
        """Load all components for a theme"""
        theme_dir = self.data_dir / 'themes' / theme_name / 'components'

        if not theme_dir.exists():
            raise ValueError(f'Theme not found: {theme_name}')

        components = {}

        # Discover all YAML files
        for yaml_file in theme_dir.rglob('*.yaml'):
            try:
                # Detect component type from YAML
                with open(yaml_file, 'r') as f:
                    data = yaml.safe_load(f)

                # Determine config class
                config_class = self._get_config_class(data)

                # Load and validate
                config = self.load_component(yaml_file, config_class)

                # Convert to runtime
                runtime_comp = config.to_runtime()

                # Register
                components[runtime_comp.id] = runtime_comp

            except Exception as e:
                print(f'Error loading {yaml_file}: {e}')
                # Continue loading other components

        return components

    def _get_config_class(
        self,
        data: Dict[str, Any]
    ) -> Type[ComponentConfig]:
        """Determine which config class to use"""
        category = data.get('category')

        mapping = {
            'weapon': WeaponComponentConfig,
            'armor': ArmorComponentConfig,
            'shield': ShieldComponentConfig,
            'engine': EngineComponentConfig,
            'power': PowerGeneratorComponentConfig,
            # Add more as needed
        }

        config_class = mapping.get(category)
        if not config_class:
            raise ValueError(f'Unknown component category: {category}')

        return config_class

class UnitLoader:
    """Loads units from YAML files"""

    def __init__(
        self,
        data_dir: Path,
        component_registry: 'ComponentRegistry'
    ):
        self.data_dir = Path(data_dir)
        self.registry = component_registry

    def load_unit(self, file_path: Path) -> Unit:
        """Load and validate unit"""
        # Load YAML
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)

        # Validate with Pydantic
        try:
            config = UnitConfig(**data)
        except ValidationError as e:
            raise ValueError(f'Invalid unit in {file_path}:\n{e}')

        # Validate with business rules
        validator = UnitValidator(self.registry)
        result = validator.validate_unit(config)

        if not result.valid:
            raise ValueError(
                f'Unit validation failed for {file_path}:\n{result}'
            )

        if result.warnings:
            print(f'Warnings for {file_path}:\n{result}')

        # Convert to runtime
        unit = config.to_runtime(self.registry)

        return unit

class ComponentRegistry:
    """Registry of runtime components"""

    def __init__(self):
        self._components: Dict[str, Component] = {}

    def register(self, component: Component) -> None:
        """Register a component"""
        self._components[component.id] = component

    def get(self, component_id: str) -> Optional[Component]:
        """Get component by ID"""
        return self._components.get(component_id)

    def has(self, component_id: str) -> bool:
        """Check if component exists"""
        return component_id in self._components

    def list_all(self) -> List[Component]:
        """List all components"""
        return list(self._components.values())

    def list_by_type(
        self,
        component_type: Type[Component]
    ) -> List[Component]:
        """List components of specific type"""
        return [
            c for c in self._components.values()
            if isinstance(c, component_type)
        ]
```

---

## Implementation Guidelines

### For the Developer Agent

#### 1. File Organization

```
src/battle_automata/
├── models/
│   ├── __init__.py
│   ├── config/              # Pydantic configuration models
│   │   ├── __init__.py
│   │   ├── base.py         # ComponentConfig, UnitConfig
│   │   ├── weapons.py      # WeaponComponentConfig
│   │   ├── defense.py      # ArmorComponentConfig, ShieldComponentConfig
│   │   ├── mobility.py     # EngineComponentConfig
│   │   ├── support.py      # PowerGeneratorComponentConfig
│   │   └── battle.py       # BattleConfig
│   ├── runtime/             # Frozen dataclass runtime models
│   │   ├── __init__.py
│   │   ├── components.py   # Component, WeaponComponent, etc.
│   │   ├── units.py        # Unit
│   │   └── battle.py       # BattleState, BattleResult
│   └── enums.py            # All enums
├── validation/
│   ├── __init__.py
│   ├── component.py        # ComponentValidator
│   ├── unit.py             # UnitValidator
│   └── balance.py          # BalanceValidator
├── loading/
│   ├── __init__.py
│   ├── component_loader.py
│   ├── unit_loader.py
│   └── registry.py
└── schemas/                 # JSON schemas (generated from Pydantic)
    ├── component.json
    ├── unit.json
    └── battle.json
```

#### 2. Implementation Order

1. **Enums first** (all enum types)
2. **Base config models** (ComponentConfig)
3. **Specific config models** (WeaponComponentConfig, etc.)
4. **Runtime models** (Component dataclasses)
5. **Validators** (ComponentValidator, UnitValidator)
6. **Loaders** (ComponentLoader, UnitLoader)
7. **Registry** (ComponentRegistry)

#### 3. Testing Strategy

```python
# tests/test_models/test_weapon_config.py

def test_weapon_config_valid():
    """Test valid weapon loads correctly"""
    config = WeaponComponentConfig(
        id="test_laser",
        name="Test Laser",
        type=ComponentType.OFFENSIVE,
        category=ComponentCategory.WEAPON,
        damage_type=DamageType.ENERGY,
        stats=WeaponStats(
            damage=50,
            range=100,
            fire_rate=1.0,
            accuracy=0.85
        ),
        resources=ResourceCost(
            power_draw=20,
            weight=50,
            slots=1,
            cost=100
        )
    )

    assert config.id == "test_laser"
    assert config.stats.damage == 50

def test_weapon_config_invalid_dps():
    """Test overpowered weapon is rejected"""
    with pytest.raises(ValidationError):
        WeaponComponentConfig(
            id="overpowered",
            name="OP Weapon",
            type=ComponentType.OFFENSIVE,
            category=ComponentCategory.WEAPON,
            damage_type=DamageType.ENERGY,
            stats=WeaponStats(
                damage=1000,    # Too high
                range=100,
                fire_rate=10.0,  # Too high
                accuracy=0.85
            ),
            resources=ResourceCost(
                power_draw=1,    # Too low for DPS
                weight=1,
                slots=1,
                cost=1
            )
        )

def test_weapon_to_runtime():
    """Test conversion to runtime object"""
    config = WeaponComponentConfig(...)
    runtime = config.to_runtime()

    assert isinstance(runtime, WeaponComponent)
    assert runtime.damage == config.stats.damage

    # Runtime object is frozen
    with pytest.raises(FrozenInstanceError):
        runtime.damage = 999
```

#### 4. Documentation

Each model class should have:

```python
class WeaponComponentConfig(ComponentConfig):
    """Weapon component configuration.

    Represents a weapon loaded from YAML and validated.
    Use this class for loading, editing, and validating weapon data.

    For simulation, convert to WeaponComponent using .to_runtime().

    Attributes:
        damage_type: Type of damage (kinetic, energy, explosive)
        stats: Core weapon statistics
        special: Special properties (armor piercing, etc.)
        targeting: Targeting configuration

    Example:
        >>> config = WeaponComponentConfig.from_file('laser.yaml')
        >>> runtime = config.to_runtime()
        >>> print(runtime.damage)
        50

    Validation Rules:
        - DPS (damage * fire_rate) must be reasonable
        - Power draw must scale with DPS
        - Energy weapons need more power than kinetic
        - Accuracy + fire_rate combo checked for balance
    """
    ...
```

### Key Principles

1. **Immutability**: Runtime objects are frozen, config objects are mutable
2. **Validation**: Fail fast during loading, never during simulation
3. **Type Safety**: Full type hints, use mypy for type checking
4. **Separation**: Config (Pydantic) separate from runtime (dataclass)
5. **Documentation**: Every public class and function documented
6. **Testing**: High coverage, test both valid and invalid cases

---

## Conclusion

This data model architecture provides:

1. **Clear Separation**: Config layer (mutable, validating) vs runtime layer (immutable, fast)
2. **Type Safety**: Full type hints throughout, enabling static analysis
3. **Robust Validation**: Three-layer validation ensures only valid data enters simulation
4. **Determinism**: Frozen runtime objects ensure reproducible simulations
5. **Extensibility**: Easy to add new component types via inheritance
6. **Balance**: Built-in validation rules enforce game balance
7. **Developer Experience**: Clear examples, good error messages, comprehensive docs

The architecture is ready for implementation. The Developer agent can begin implementing the models following the provided specifications, starting with enums and base classes, then building up to complete component types.

All data flows from human-editable YAML files through rigorous validation to immutable runtime objects used in the deterministic simulation engine.
