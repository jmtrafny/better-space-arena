"""
Unit Builder API - Fluent interface for constructing units.

Provides a chainable API for assembling units from components with validation.
"""

from dataclasses import dataclass
from typing import Tuple, Optional, List
from pathlib import Path

from ..schemas.unit import (
    UnitConfig,
    ComponentPlacement,
    Position,
    UnitLayout,
    UnitResourceBudget,
    AIBehavior,
)
from .components import Component, ComponentRegistry


@dataclass(frozen=True)
class PlacedComponent:
    """A component placed on a unit at runtime"""
    component: Component
    position: Tuple[int, int]
    facing: float


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

    # Components (immutable tuple)
    components: Tuple[PlacedComponent, ...]

    # Resource limits
    max_power: int
    max_weight: int
    max_slots: int

    # AI
    ai_behavior: str

    # Metadata
    tags: Tuple[str, ...] = ()
    cost: Optional[int] = None
    build_time: Optional[int] = None

    def __post_init__(self):
        """Validate unit (should never fail if config was validated)"""
        assert len(self.components) > 0, "Unit must have components"
        assert self.grid_width > 0 and self.grid_height > 0, "Invalid grid"

    def get_total_power_draw(self) -> int:
        """Calculate total power consumption"""
        return sum(comp.component.power_draw for comp in self.components)

    def get_total_power_generation(self) -> int:
        """Calculate total power generation"""
        from .components import PowerGeneratorComponent
        total = 0
        for placed in self.components:
            if isinstance(placed.component, PowerGeneratorComponent):
                total += placed.component.max_output
        return total

    def get_total_weight(self) -> int:
        """Calculate total unit weight"""
        return sum(comp.component.weight for comp in self.components)

    def get_total_slots(self) -> int:
        """Calculate total slots used"""
        return sum(comp.component.slots for comp in self.components)

    def get_total_cost(self) -> int:
        """Calculate total unit cost"""
        return sum(comp.component.cost for comp in self.components)

    def get_weapons(self) -> List[PlacedComponent]:
        """Get all weapon components"""
        from .components import WeaponComponent
        return [
            comp for comp in self.components
            if isinstance(comp.component, WeaponComponent)
        ]

    def get_armor(self) -> List[Component]:
        """Get all armor components"""
        from .components import ArmorComponent
        return [
            comp.component for comp in self.components
            if isinstance(comp.component, ArmorComponent)
        ]

    def get_engines(self) -> List[Component]:
        """Get all engines"""
        from .components import EngineComponent
        return [
            comp.component for comp in self.components
            if isinstance(comp.component, EngineComponent)
        ]


class ValidationResult:
    """Result of validation check"""

    def __init__(
        self,
        valid: bool,
        errors: Optional[List[str]] = None,
        warnings: Optional[List[str]] = None
    ):
        self.valid = valid
        self.errors = errors or []
        self.warnings = warnings or []

    def __bool__(self) -> bool:
        """True if valid"""
        return self.valid

    def __str__(self) -> str:
        """String representation"""
        if self.valid:
            result = "✓ Validation passed"
        else:
            result = "✗ Validation failed"

        if self.errors:
            result += "\n  Errors:"
            for e in self.errors:
                result += f"\n    - {e}"

        if self.warnings:
            result += "\n  Warnings:"
            for w in self.warnings:
                result += f"\n    - {w}"

        return result


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
        unit_id: Optional[str] = None,
        registry: Optional[ComponentRegistry] = None
    ):
        """
        Initialize unit builder.

        Args:
            name: Unit name
            theme: Theme name
            unit_id: Optional unit identifier (auto-generated if None)
            registry: Component registry (uses global if None)
        """
        self._name = name
        self._theme = theme
        self._id = unit_id or name.lower().replace(" ", "_")
        self._registry = registry or ComponentRegistry()

        # Layout
        self._layout_width = 10
        self._layout_height = 10

        # Resources
        self._max_power = 100
        self._max_weight = 500
        self._max_slots = 20
        self._max_cost: Optional[int] = None

        # Components
        self._components: List[Tuple[Component, Tuple[int, int], float]] = []

        # AI
        self._ai_behavior = "aggressive"

        # Metadata
        self._description: Optional[str] = None
        self._class_name: Optional[str] = None
        self._tags: List[str] = []
        self._cost: Optional[int] = None
        self._build_time: Optional[int] = None

    def with_layout(self, width: int, height: int) -> 'UnitBuilder':
        """
        Set unit layout grid size.

        Args:
            width: Grid width
            height: Grid height

        Returns:
            Self for chaining
        """
        self._layout_width = width
        self._layout_height = height
        return self

    def with_resources(
        self,
        power: Optional[int] = None,
        weight: Optional[int] = None,
        slots: Optional[int] = None,
        cost: Optional[int] = None
    ) -> 'UnitBuilder':
        """
        Set resource budgets.

        Args:
            power: Maximum power budget
            weight: Maximum weight limit
            slots: Maximum slot capacity
            cost: Maximum cost limit

        Returns:
            Self for chaining
        """
        if power is not None:
            self._max_power = power
        if weight is not None:
            self._max_weight = weight
        if slots is not None:
            self._max_slots = slots
        if cost is not None:
            self._max_cost = cost
        return self

    def with_description(self, description: str) -> 'UnitBuilder':
        """Set unit description"""
        self._description = description
        return self

    def with_class(self, class_name: str) -> 'UnitBuilder':
        """Set unit class"""
        self._class_name = class_name
        return self

    def with_tags(self, *tags: str) -> 'UnitBuilder':
        """Add tags"""
        self._tags.extend(tags)
        return self

    def with_ai_behavior(self, behavior: str) -> 'UnitBuilder':
        """Set AI behavior"""
        self._ai_behavior = behavior
        return self

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
            ValueError: If component not in registry
        """
        component = self._registry.get(component_id)
        if component is None:
            raise ValueError(f"Component not found in registry: {component_id}")

        self._components.append((component, position, facing))
        return self

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
        self._components.append((component, position, facing))
        return self

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
        self._components = [
            (comp, pos, facing) for comp, pos, facing in self._components
            if pos != position
        ]
        return self

    def validate(self) -> 'UnitBuilder':
        """
        Validate current configuration.

        Checks resource budgets, dependencies, and placement rules.
        Raises exception if validation fails.

        Returns:
            Self for chaining

        Raises:
            ValueError: If unit is invalid
        """
        result = self.get_validation_result()
        if not result.valid:
            raise ValueError(f"Unit validation failed:\n{result}")
        return self

    def get_validation_result(self) -> ValidationResult:
        """
        Get validation result without raising.

        Returns:
            ValidationResult with errors and warnings
        """
        from ..utils.validator import UnitValidator

        # Build temporary config for validation
        try:
            config = self._to_config()
            validator = UnitValidator(self._registry)
            return validator.validate_unit(config)
        except Exception as e:
            return ValidationResult(
                valid=False,
                errors=[str(e)]
            )

    def _to_config(self) -> UnitConfig:
        """Convert current state to UnitConfig for validation"""
        return UnitConfig(
            id=self._id,
            name=self._name,
            theme=self._theme,
            description=self._description,
            class_name=self._class_name,
            layout=UnitLayout(
                width=self._layout_width,
                height=self._layout_height
            ),
            components=[
                ComponentPlacement(
                    component_id=comp.id,
                    position=Position(x=pos[0], y=pos[1]),
                    facing=facing
                )
                for comp, pos, facing in self._components
            ],
            resources=UnitResourceBudget(
                max_power=self._max_power,
                max_weight=self._max_weight,
                max_slots=self._max_slots,
                max_cost=self._max_cost
            ),
            ai=AIBehavior(movement_style=self._ai_behavior) if self._ai_behavior else None,
            tags=self._tags,
            cost=self._cost,
            build_time=self._build_time
        )

    def build(self) -> Unit:
        """
        Build the final unit.

        Performs final validation and returns unit instance.

        Returns:
            Constructed unit

        Raises:
            ValueError: If unit is invalid
        """
        # Validate first
        self.validate()

        # Convert components to runtime format
        placed_components = tuple(
            PlacedComponent(
                component=comp,
                position=pos,
                facing=facing
            )
            for comp, pos, facing in self._components
        )

        # Build unit
        return Unit(
            id=self._id,
            name=self._name,
            theme=self._theme,
            grid_width=self._layout_width,
            grid_height=self._layout_height,
            components=placed_components,
            max_power=self._max_power,
            max_weight=self._max_weight,
            max_slots=self._max_slots,
            ai_behavior=self._ai_behavior,
            tags=tuple(self._tags),
            cost=self._cost,
            build_time=self._build_time
        )

    def save(self, file_path: str) -> None:
        """
        Build and save unit to file.

        Args:
            file_path: Output file path (.yaml or .json)
        """
        from ..utils.loader import UnitLoader

        config = self._to_config()
        loader = UnitLoader(Path("."), self._registry)
        loader.save_unit(config, Path(file_path))
