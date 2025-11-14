"""
Runtime component representations (frozen dataclasses for simulation).

These are immutable runtime objects used during battle simulation.
"""

from dataclasses import dataclass
from typing import Tuple, Optional


@dataclass(frozen=True)
class Component:
    """Base immutable runtime component"""
    id: str
    name: str
    type: str
    category: str

    # Resources
    power_draw: int
    weight: int
    slots: int
    cost: int

    # Metadata
    tags: Tuple[str, ...] = ()


@dataclass(frozen=True)
class WeaponComponent(Component):
    """Immutable runtime weapon component (stub)"""
    damage: int = 0
    range: float = 0.0
    fire_rate: float = 0.0


@dataclass(frozen=True)
class ArmorComponent(Component):
    """Immutable runtime armor component (stub)"""
    armor_value: int = 0
    coverage: float = 0.0


@dataclass(frozen=True)
class EngineComponent(Component):
    """Immutable runtime engine component (stub)"""
    thrust: float = 0.0
    max_speed: float = 0.0


@dataclass(frozen=True)
class PowerGeneratorComponent(Component):
    """Immutable runtime power generator (stub)"""
    max_output: int = 0


# Component registry stub
class ComponentRegistry:
    """Registry for component definitions"""

    def __init__(self):
        self._components: dict[str, Component] = {}

    def register(self, component: Component) -> None:
        """Register a component"""
        self._components[component.id] = component

    def get(self, component_id: str) -> Optional[Component]:
        """Get component by ID"""
        return self._components.get(component_id)

    def has(self, component_id: str) -> bool:
        """Check if component exists"""
        return component_id in self._components

    def list_all(self) -> list[Component]:
        """List all components"""
        return list(self._components.values())
