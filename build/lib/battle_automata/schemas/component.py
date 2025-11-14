"""
Pydantic models for component configuration validation.

This module defines the validation schemas for loading components from YAML files.
Components are validated through Pydantic models, then converted to immutable
frozen dataclasses for runtime use.
"""

from enum import Enum
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


# ============================================================================
# Enums
# ============================================================================


class ComponentType(str, Enum):
    """Top-level component categories."""

    OFFENSIVE = "offensive"
    DEFENSIVE = "defensive"
    MOBILITY = "mobility"
    SUPPORT = "support"


class ComponentCategory(str, Enum):
    """Specific component categories."""

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


class DamageType(str, Enum):
    """Damage type for weapons."""

    KINETIC = "kinetic"  # Ballistic weapons
    ENERGY = "energy"  # Lasers, plasma
    EXPLOSIVE = "explosive"  # Missiles, grenades


class ArmorType(str, Enum):
    """Armor material types."""

    COMPOSITE = "composite"  # Balanced
    REACTIVE = "reactive"  # Good vs explosives
    ABLATIVE = "ablative"  # Good vs energy
    KINETIC = "kinetic"  # Good vs ballistics


class TargetingPriority(str, Enum):
    """How weapon selects targets."""

    CLOSEST = "closest"
    WEAKEST = "weakest"
    STRONGEST = "strongest"
    RANDOM = "random"
    PRIORITY_LIST = "priority_list"


# ============================================================================
# Base Component Schemas
# ============================================================================


class ResourceCost(BaseModel):
    """Resource requirements for a component."""

    power_draw: int = Field(ge=0, description="Power consumed in watts")
    weight: int = Field(gt=0, description="Mass in kilograms")
    slots: int = Field(gt=0, le=10, description="Grid slots occupied (1-10)")
    cost: int = Field(ge=0, description="Build cost in credits")

    @field_validator("power_draw")
    @classmethod
    def power_reasonable(cls, v: int) -> int:
        """Ensure power draw is reasonable."""
        if v > 1000:
            raise ValueError("Power draw must be ≤ 1000W")
        return v


class ComponentConfig(BaseModel):
    """Base configuration for all components (Pydantic model for validation)."""

    # Identity
    id: str = Field(pattern=r"^[a-z0-9_]+$", description="Unique identifier")
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
        default_factory=list, description="IDs of components this requires"
    )
    conflicts_with: List[str] = Field(
        default_factory=list, description="IDs of components this conflicts with"
    )

    @field_validator("id")
    @classmethod
    def id_valid(cls, v: str) -> str:
        """Ensure ID follows naming conventions."""
        if not v.islower():
            raise ValueError("ID must be lowercase")
        if len(v) > 50:
            raise ValueError("ID must be ≤ 50 characters")
        return v

    @model_validator(mode="after")
    def check_type_category_match(self) -> "ComponentConfig":
        """Ensure category matches type."""
        # Define valid category-type mappings
        valid_mappings = {
            ComponentType.OFFENSIVE: {ComponentCategory.WEAPON, ComponentCategory.TARGETING},
            ComponentType.DEFENSIVE: {
                ComponentCategory.ARMOR,
                ComponentCategory.SHIELD,
                ComponentCategory.POINT_DEFENSE,
            },
            ComponentType.MOBILITY: {
                ComponentCategory.ENGINE,
                ComponentCategory.THRUSTER,
                ComponentCategory.GYROSCOPE,
            },
            ComponentType.SUPPORT: {
                ComponentCategory.POWER,
                ComponentCategory.SENSOR,
                ComponentCategory.REPAIR,
                ComponentCategory.COOLING,
            },
        }

        if self.category not in valid_mappings.get(self.type, set()):
            raise ValueError(f"Category {self.category} not valid for type {self.type}")

        return self

    model_config = {"use_enum_values": True}


# ============================================================================
# Weapon Component Schemas
# ============================================================================


class WeaponStats(BaseModel):
    """Core weapon statistics."""

    damage: int = Field(gt=0, le=1000, description="Base damage per hit")
    range: float = Field(gt=0, le=500, description="Maximum range in meters")
    fire_rate: float = Field(gt=0, le=10, description="Shots per second")
    accuracy: float = Field(ge=0, le=1, description="Base hit probability")
    projectile_speed: Optional[float] = Field(
        None, gt=0, description="Projectile speed (null for instant)"
    )

    @field_validator("fire_rate")
    @classmethod
    def fire_rate_reasonable(cls, v: float, info) -> float:
        """High fire rate requires low damage."""
        if "damage" in info.data:
            damage = info.data["damage"]
            dps = damage * v
            if dps > 200:
                raise ValueError(f"DPS ({dps}) too high. Reduce damage or fire_rate.")
        return v


class WeaponSpecial(BaseModel):
    """Special weapon properties."""

    armor_piercing: float = Field(
        default=0, ge=0, le=1, description="Ignore % of armor (0-1)"
    )
    shield_penetration: float = Field(
        default=0, ge=0, le=1, description="Bypass % of shields (0-1)"
    )
    splash_radius: Optional[float] = Field(None, ge=0, description="Area of effect radius")
    splash_damage_falloff: float = Field(
        default=0.5, ge=0, le=1, description="Damage % at splash edge"
    )
    critical_chance: float = Field(
        default=0, ge=0, le=0.5, description="Critical hit chance (max 50%)"
    )
    critical_multiplier: float = Field(
        default=2.0, ge=1.0, le=5.0, description="Critical damage multiplier"
    )


class WeaponTargeting(BaseModel):
    """Targeting configuration."""

    firing_arc: float = Field(default=360, gt=0, le=360, description="Firing arc in degrees")
    priority: TargetingPriority = TargetingPriority.CLOSEST
    component_priorities: List[str] = Field(
        default_factory=list, description="Target these component types first"
    )
    ignore_allies: bool = Field(default=True, description="Cannot target friendly units")

    @field_validator("firing_arc")
    @classmethod
    def arc_valid(cls, v: float) -> float:
        """Common arcs are 90, 180, 270, 360."""
        valid_arcs = {30, 45, 60, 90, 120, 180, 270, 360}
        if v not in valid_arcs:
            raise ValueError(f"Firing arc {v}° not standard. Use one of {valid_arcs}")
        return v


class WeaponComponentConfig(ComponentConfig):
    """Complete weapon component configuration."""

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

    @model_validator(mode="after")
    def validate_balance(self) -> "WeaponComponentConfig":
        """Cross-field balance validation."""
        # Calculate DPS
        dps = self.stats.damage * self.stats.fire_rate

        # Higher DPS should require more power
        expected_power = dps * 0.5  # 0.5W per DPS
        if self.resources.power_draw < expected_power * 0.5:
            raise ValueError(f"Weapon with {dps} DPS needs ≥{expected_power * 0.5}W power")

        # Energy weapons need more power than kinetic
        if self.damage_type == DamageType.ENERGY:
            if self.resources.power_draw < dps * 0.8:
                raise ValueError(f"Energy weapons need ≥{dps * 0.8}W power for {dps} DPS")

        return self


# ============================================================================
# Armor Component Schemas
# ============================================================================


class ArmorStats(BaseModel):
    """Armor statistics."""

    armor_value: int = Field(gt=0, le=500, description="Damage reduction value")
    coverage: float = Field(ge=0, le=1, description="% of unit covered (0-1)")
    durability: int = Field(gt=0, description="Armor health points")


class ArmorResistances(BaseModel):
    """Damage type resistances."""

    kinetic_resist: float = Field(
        default=1.0,
        ge=0,
        le=2.0,
        description="Multiplier vs kinetic (1.0=normal, 1.5=+50% resist)",
    )
    energy_resist: float = Field(default=1.0, ge=0, le=2.0)
    explosive_resist: float = Field(default=1.0, ge=0, le=2.0)

    @model_validator(mode="after")
    def resistances_balanced(self) -> "ArmorResistances":
        """Can't be strong against everything."""
        total = self.kinetic_resist + self.energy_resist + self.explosive_resist
        # Average resistance should be around 1.0
        if total > 4.0:  # Allows some specialization
            raise ValueError("Total resistances too high. Specialize, not generalize.")
        return self


class ArmorComponentConfig(ComponentConfig):
    """Armor component configuration."""

    type: Literal[ComponentType.DEFENSIVE] = ComponentType.DEFENSIVE
    category: Literal[ComponentCategory.ARMOR] = ComponentCategory.ARMOR

    armor_type: ArmorType
    stats: ArmorStats
    resistances: ArmorResistances = Field(default_factory=ArmorResistances)

    @model_validator(mode="after")
    def validate_balance(self) -> "ArmorComponentConfig":
        """Balance validation."""
        # Heavier armor = better protection
        armor_per_kg = self.stats.armor_value / self.resources.weight
        if armor_per_kg > 2.0:  # Max 2 armor per kg
            raise ValueError(f"Armor too efficient: {armor_per_kg:.1f} armor/kg (max 2.0)")

        return self


# ============================================================================
# Shield Component Schemas
# ============================================================================


class ShieldStats(BaseModel):
    """Shield statistics."""

    shield_strength: int = Field(gt=0, le=1000, description="Shield hit points")
    recharge_rate: float = Field(gt=0, le=100, description="HP recharged per second")
    recharge_delay: float = Field(
        ge=0, le=10, description="Seconds before recharge starts"
    )
    coverage: float = Field(default=1.0, ge=0, le=1, description="% of unit covered")


class ShieldComponentConfig(ComponentConfig):
    """Shield component configuration."""

    type: Literal[ComponentType.DEFENSIVE] = ComponentType.DEFENSIVE
    category: Literal[ComponentCategory.SHIELD] = ComponentCategory.SHIELD

    stats: ShieldStats

    # Shields resist energy better than kinetic
    energy_absorption: float = Field(
        default=1.0, ge=0.5, le=2.0, description="Energy damage multiplier (>1 = better)"
    )
    kinetic_absorption: float = Field(
        default=1.0, ge=0.5, le=2.0, description="Kinetic damage multiplier (<1 = worse)"
    )

    @model_validator(mode="after")
    def validate_power_requirement(self) -> "ShieldComponentConfig":
        """Shields need significant power."""
        # Power draw should scale with shield strength
        expected_power = self.stats.shield_strength * 0.1
        if self.resources.power_draw < expected_power:
            raise ValueError(
                f"Shield needs ≥{expected_power}W for {self.stats.shield_strength} HP shield"
            )

        return self


# ============================================================================
# Engine Component Schemas
# ============================================================================


class EngineStats(BaseModel):
    """Engine statistics."""

    thrust: float = Field(gt=0, le=1000, description="Forward thrust in newtons")
    max_speed: float = Field(gt=0, le=100, description="Maximum speed in m/s")
    acceleration: float = Field(gt=0, le=50, description="Acceleration in m/s²")
    turn_rate: float = Field(default=90, gt=0, le=360, description="Turning rate in degrees/s")


class EngineComponentConfig(ComponentConfig):
    """Engine component configuration."""

    type: Literal[ComponentType.MOBILITY] = ComponentType.MOBILITY
    category: Literal[ComponentCategory.ENGINE] = ComponentCategory.ENGINE

    stats: EngineStats

    @model_validator(mode="after")
    def validate_thrust_vs_power(self) -> "EngineComponentConfig":
        """More thrust needs more power."""
        # Power scales with thrust
        expected_power = self.stats.thrust * 0.2
        if self.resources.power_draw < expected_power * 0.7:
            raise ValueError(
                f"Engine with {self.stats.thrust}N thrust needs ≥{expected_power * 0.7}W power"
            )

        return self


# ============================================================================
# Power Generator Component Schemas
# ============================================================================


class PowerGeneratorStats(BaseModel):
    """Power generator statistics."""

    max_output: int = Field(gt=0, le=2000, description="Maximum power output in watts")
    efficiency: float = Field(
        default=1.0,
        ge=0.5,
        le=1.0,
        description="Operating efficiency (degrades with damage)",
    )


class PowerGeneratorComponentConfig(ComponentConfig):
    """Power generator configuration."""

    type: Literal[ComponentType.SUPPORT] = ComponentType.SUPPORT
    category: Literal[ComponentCategory.POWER] = ComponentCategory.POWER

    stats: PowerGeneratorStats

    @field_validator("resources")
    @classmethod
    def power_generator_no_draw(cls, v: ResourceCost) -> ResourceCost:
        """Generators produce power, they don't consume it."""
        if v.power_draw > 0:
            raise ValueError("Power generators cannot have power_draw > 0")
        # Set it to 0 to indicate no consumption
        v.power_draw = 0
        return v
