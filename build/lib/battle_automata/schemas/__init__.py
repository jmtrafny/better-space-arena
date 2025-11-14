"""
Pydantic schemas for data validation.
"""

from .component import (
    ArmorComponentConfig,
    ArmorResistances,
    ArmorStats,
    ArmorType,
    ComponentCategory,
    ComponentConfig,
    ComponentType,
    DamageType,
    EngineComponentConfig,
    EngineStats,
    PowerGeneratorComponentConfig,
    PowerGeneratorStats,
    ResourceCost,
    ShieldComponentConfig,
    ShieldStats,
    TargetingPriority,
    WeaponComponentConfig,
    WeaponSpecial,
    WeaponStats,
    WeaponTargeting,
)

__all__ = [
    # Base enums and types
    "ComponentType",
    "ComponentCategory",
    "DamageType",
    "ArmorType",
    "TargetingPriority",
    # Base schemas
    "ResourceCost",
    "ComponentConfig",
    # Weapon schemas
    "WeaponStats",
    "WeaponSpecial",
    "WeaponTargeting",
    "WeaponComponentConfig",
    # Armor schemas
    "ArmorStats",
    "ArmorResistances",
    "ArmorComponentConfig",
    # Shield schemas
    "ShieldStats",
    "ShieldComponentConfig",
    # Engine schemas
    "EngineStats",
    "EngineComponentConfig",
    # Power schemas
    "PowerGeneratorStats",
    "PowerGeneratorComponentConfig",
]
