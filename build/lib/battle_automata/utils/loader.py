"""
YAML loader utilities for components and units.

This module provides utilities to load and validate component definitions
from YAML files using Pydantic schemas.
"""

from pathlib import Path
from typing import Any, Dict, Type, Union

import yaml
from pydantic import ValidationError

from battle_automata.core.component import (
    ArmorComponent,
    Component,
    EngineComponent,
    PowerGeneratorComponent,
    ShieldComponent,
    WeaponComponent,
)
from battle_automata.schemas.component import (
    ArmorComponentConfig,
    ComponentCategory,
    ComponentConfig,
    EngineComponentConfig,
    PowerGeneratorComponentConfig,
    ShieldComponentConfig,
    WeaponComponentConfig,
)


class ComponentLoader:
    """Loads components from YAML files with validation."""

    # Map category to config class
    CONFIG_CLASS_MAP: Dict[ComponentCategory, Type[ComponentConfig]] = {
        ComponentCategory.WEAPON: WeaponComponentConfig,
        ComponentCategory.ARMOR: ArmorComponentConfig,
        ComponentCategory.SHIELD: ShieldComponentConfig,
        ComponentCategory.ENGINE: EngineComponentConfig,
        ComponentCategory.POWER: PowerGeneratorComponentConfig,
    }

    @classmethod
    def load_component_from_file(cls, file_path: Union[str, Path]) -> Component:
        """
        Load and validate a component from a YAML file.

        Args:
            file_path: Path to component YAML file

        Returns:
            Validated runtime component

        Raises:
            FileNotFoundError: If file doesn't exist
            ValidationError: If component data is invalid
            ValueError: If component category is unsupported
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"Component file not found: {file_path}")

        # Load YAML
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        return cls.load_component_from_dict(data, source_file=str(file_path))

    @classmethod
    def load_component_from_dict(
        cls, data: Dict[str, Any], source_file: str = "<dict>"
    ) -> Component:
        """
        Load and validate a component from a dictionary.

        Args:
            data: Component data dictionary
            source_file: Source file name for error messages

        Returns:
            Validated runtime component

        Raises:
            ValidationError: If component data is invalid
            ValueError: If component category is unsupported
        """
        # Detect component category
        category_str = data.get("category")
        if not category_str:
            raise ValueError(f"Component missing 'category' field in {source_file}")

        try:
            category = ComponentCategory(category_str)
        except ValueError:
            raise ValueError(
                f"Unknown component category '{category_str}' in {source_file}"
            )

        # Get the appropriate config class
        config_class = cls.CONFIG_CLASS_MAP.get(category)
        if not config_class:
            raise ValueError(
                f"No loader for category '{category}' in {source_file}. "
                f"Supported: {list(cls.CONFIG_CLASS_MAP.keys())}"
            )

        # Validate with Pydantic
        try:
            config = config_class(**data)
        except ValidationError as e:
            raise ValidationError.from_exception_data(
                title=f"Invalid component in {source_file}",
                line_errors=e.errors(),
            )

        # Convert to runtime component
        return cls._config_to_runtime(config)

    @classmethod
    def _config_to_runtime(cls, config: ComponentConfig) -> Component:
        """
        Convert a Pydantic config model to a frozen runtime component.

        Args:
            config: Validated Pydantic config

        Returns:
            Immutable runtime component
        """
        if isinstance(config, WeaponComponentConfig):
            return WeaponComponent(
                id=config.id,
                name=config.name,
                damage_type=config.damage_type,
                damage=config.stats.damage,
                range=config.stats.range,
                fire_rate=config.stats.fire_rate,
                accuracy=config.stats.accuracy,
                projectile_speed=config.stats.projectile_speed,
                power_draw=config.resources.power_draw,
                weight=config.resources.weight,
                slots=config.resources.slots,
                armor_piercing=config.special.armor_piercing,
                shield_penetration=config.special.shield_penetration,
                splash_radius=config.special.splash_radius,
                critical_chance=config.special.critical_chance,
                critical_multiplier=config.special.critical_multiplier,
                firing_arc=config.targeting.firing_arc,
                targeting_priority=config.targeting.priority,
                tags=tuple(config.tags),
            )

        elif isinstance(config, ArmorComponentConfig):
            return ArmorComponent(
                id=config.id,
                name=config.name,
                armor_type=config.armor_type,
                armor_value=config.stats.armor_value,
                coverage=config.stats.coverage,
                max_durability=config.stats.durability,
                kinetic_resist=config.resistances.kinetic_resist,
                energy_resist=config.resistances.energy_resist,
                explosive_resist=config.resistances.explosive_resist,
                power_draw=config.resources.power_draw,
                weight=config.resources.weight,
                slots=config.resources.slots,
                tags=tuple(config.tags),
            )

        elif isinstance(config, ShieldComponentConfig):
            return ShieldComponent(
                id=config.id,
                name=config.name,
                max_strength=config.stats.shield_strength,
                recharge_rate=config.stats.recharge_rate,
                recharge_delay=config.stats.recharge_delay,
                coverage=config.stats.coverage,
                energy_absorption=config.energy_absorption,
                kinetic_absorption=config.kinetic_absorption,
                power_draw=config.resources.power_draw,
                weight=config.resources.weight,
                slots=config.resources.slots,
                tags=tuple(config.tags),
            )

        elif isinstance(config, EngineComponentConfig):
            return EngineComponent(
                id=config.id,
                name=config.name,
                thrust=config.stats.thrust,
                max_speed=config.stats.max_speed,
                acceleration=config.stats.acceleration,
                turn_rate=config.stats.turn_rate,
                power_draw=config.resources.power_draw,
                weight=config.resources.weight,
                slots=config.resources.slots,
                tags=tuple(config.tags),
            )

        elif isinstance(config, PowerGeneratorComponentConfig):
            return PowerGeneratorComponent(
                id=config.id,
                name=config.name,
                max_output=config.stats.max_output,
                base_efficiency=config.stats.efficiency,
                power_draw=config.resources.power_draw,
                weight=config.resources.weight,
                slots=config.resources.slots,
                tags=tuple(config.tags),
            )

        else:
            raise ValueError(f"Unknown config type: {type(config)}")


def load_components_from_directory(directory: Union[str, Path]) -> Dict[str, Component]:
    """
    Load all components from a directory (recursively).

    Args:
        directory: Directory to scan for YAML files

    Returns:
        Dictionary mapping component IDs to components

    Raises:
        ValidationError: If any component is invalid
    """
    directory = Path(directory)
    components: Dict[str, Component] = {}

    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")

    # Find all YAML files recursively
    for yaml_file in directory.rglob("*.yaml"):
        try:
            component = ComponentLoader.load_component_from_file(yaml_file)
            components[component.id] = component
        except Exception as e:
            print(f"Warning: Failed to load {yaml_file}: {e}")
            # Continue loading other components

    return components
