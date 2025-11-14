"""
Frozen dataclasses for runtime components.

These are immutable, lightweight component definitions used during battle simulation.
They are converted from Pydantic validation models after loading from YAML.
"""

from dataclasses import dataclass
from typing import Optional, Tuple

from battle_automata.schemas.component import ArmorType, DamageType, TargetingPriority


# ============================================================================
# Base Component
# ============================================================================


@dataclass(frozen=True)
class Component:
    """Base immutable runtime component."""

    # Identity
    id: str
    name: str

    # Resources
    power_draw: int
    weight: int
    slots: int

    # Metadata (frozen)
    tags: Tuple[str, ...] = ()


# ============================================================================
# Weapon Component
# ============================================================================


@dataclass(frozen=True)
class WeaponComponent(Component):
    """Immutable runtime weapon component (used in simulation)."""

    # Core stats
    damage_type: DamageType
    damage: int
    range: float
    fire_rate: float
    accuracy: float
    projectile_speed: Optional[float]

    # Special properties
    armor_piercing: float = 0.0
    shield_penetration: float = 0.0
    splash_radius: Optional[float] = None
    critical_chance: float = 0.0
    critical_multiplier: float = 2.0

    # Targeting
    firing_arc: float = 360.0
    targeting_priority: TargetingPriority = TargetingPriority.CLOSEST

    def __post_init__(self) -> None:
        """Validate runtime invariants (should never fail if config was validated)."""
        assert self.damage > 0, "Damage must be positive"
        assert 0 <= self.accuracy <= 1, "Accuracy must be 0-1"
        assert self.fire_rate > 0, "Fire rate must be positive"


# ============================================================================
# Armor Component
# ============================================================================


@dataclass(frozen=True)
class ArmorComponent(Component):
    """Immutable runtime armor component."""

    # Stats
    armor_type: ArmorType
    armor_value: int
    coverage: float
    max_durability: int

    # Resistances
    kinetic_resist: float
    energy_resist: float
    explosive_resist: float

    def get_effective_armor(self, damage_type: DamageType) -> float:
        """Calculate effective armor vs damage type."""
        multiplier = {
            DamageType.KINETIC: self.kinetic_resist,
            DamageType.ENERGY: self.energy_resist,
            DamageType.EXPLOSIVE: self.explosive_resist,
        }.get(damage_type, 1.0)

        return self.armor_value * multiplier


# ============================================================================
# Shield Component
# ============================================================================


@dataclass(frozen=True)
class ShieldComponent(Component):
    """Immutable runtime shield component."""

    # Stats
    max_strength: int
    recharge_rate: float
    recharge_delay: float
    coverage: float

    # Absorption
    energy_absorption: float
    kinetic_absorption: float

    def get_damage_absorbed(self, incoming_damage: float, damage_type: DamageType) -> float:
        """Calculate how much damage shield absorbs."""
        multiplier = {
            DamageType.ENERGY: self.energy_absorption,
            DamageType.KINETIC: self.kinetic_absorption,
            DamageType.EXPLOSIVE: 1.0,  # Normal
        }.get(damage_type, 1.0)

        return incoming_damage * multiplier


# ============================================================================
# Engine Component
# ============================================================================


@dataclass(frozen=True)
class EngineComponent(Component):
    """Immutable runtime engine component."""

    # Stats
    thrust: float
    max_speed: float
    acceleration: float
    turn_rate: float


# ============================================================================
# Power Generator Component
# ============================================================================


@dataclass(frozen=True)
class PowerGeneratorComponent(Component):
    """Immutable runtime power generator."""

    # Stats
    max_output: int
    base_efficiency: float

    def get_output(self, current_efficiency: float = 1.0) -> int:
        """Calculate current power output."""
        return int(self.max_output * self.base_efficiency * current_efficiency)
