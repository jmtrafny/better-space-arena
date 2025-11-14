"""
Component registry for storing and retrieving components.

The registry provides centralized access to all loaded components,
with filtering and query capabilities.
"""

from pathlib import Path
from typing import Dict, List, Optional, Type, Union

from battle_automata.core.component import (
    ArmorComponent,
    Component,
    EngineComponent,
    PowerGeneratorComponent,
    ShieldComponent,
    WeaponComponent,
)
from battle_automata.utils.loader import ComponentLoader, load_components_from_directory


class ComponentRegistry:
    """
    Registry for component definitions.

    The registry provides centralized access to all components
    and supports loading from themes and custom sources.

    Example:
        >>> registry = ComponentRegistry()
        >>> registry.load_theme("space-ships")
        >>> laser = registry.get("laser_cannon_mk1")
        >>> all_weapons = registry.filter_by_type(WeaponComponent)
    """

    def __init__(self, data_directory: Optional[Path] = None):
        """
        Initialize component registry.

        Args:
            data_directory: Root data directory (defaults to ./data)
        """
        self._components: Dict[str, Component] = {}
        self.data_directory = Path(data_directory) if data_directory else Path("data")

    def register(self, component: Component) -> None:
        """
        Register a component instance.

        Allows programmatic component creation.

        Args:
            component: Component to register

        Raises:
            ValueError: If component with same ID already exists

        Example:
            >>> custom = WeaponComponent(id="custom_laser", ...)
            >>> registry.register(custom)
        """
        if component.id in self._components:
            raise ValueError(
                f"Component with ID '{component.id}' already registered. "
                f"Use a different ID or unregister the existing component first."
            )

        self._components[component.id] = component

    def register_multiple(self, components: Dict[str, Component]) -> int:
        """
        Register multiple components at once.

        Args:
            components: Dictionary mapping component IDs to components

        Returns:
            Number of components registered
        """
        for component in components.values():
            self.register(component)

        return len(components)

    def unregister(self, component_id: str) -> None:
        """
        Unregister a component by ID.

        Args:
            component_id: Component identifier

        Raises:
            KeyError: If component not found
        """
        if component_id not in self._components:
            raise KeyError(f"Component '{component_id}' not found in registry")

        del self._components[component_id]

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
        return self._components.get(component_id)

    def get_or_raise(self, component_id: str) -> Component:
        """
        Get component by ID or raise error.

        Args:
            component_id: Component identifier

        Returns:
            Component instance

        Raises:
            KeyError: If component does not exist
        """
        component = self.get(component_id)
        if component is None:
            raise KeyError(
                f"Component '{component_id}' not found in registry. "
                f"Available components: {self.list_ids()}"
            )
        return component

    def has(self, component_id: str) -> bool:
        """
        Check if component exists.

        Args:
            component_id: Component identifier

        Returns:
            True if component exists
        """
        return component_id in self._components

    def list_all(self) -> List[Component]:
        """
        List all components.

        Returns:
            List of all components
        """
        return list(self._components.values())

    def list_ids(self) -> List[str]:
        """
        Get list of all component IDs.

        Returns:
            List of component IDs
        """
        return list(self._components.keys())

    def count(self) -> int:
        """
        Get number of registered components.

        Returns:
            Component count
        """
        return len(self._components)

    def clear(self) -> None:
        """Clear all registered components."""
        self._components.clear()

    def filter_by_type(self, component_type: Type[Component]) -> List[Component]:
        """
        Filter components by type.

        Args:
            component_type: Type of component to filter

        Returns:
            List of matching components

        Example:
            >>> weapons = registry.filter_by_type(WeaponComponent)
        """
        return [c for c in self._components.values() if isinstance(c, component_type)]

    def filter_by_tags(self, tags: List[str], require_all: bool = True) -> List[Component]:
        """
        Filter components by tags.

        Args:
            tags: List of tags to filter by
            require_all: If True, component must have all tags. If False, any tag matches.

        Returns:
            List of matching components

        Example:
            >>> energy_weapons = registry.filter_by_tags(["energy_weapon"])
            >>> heavy_kinetic = registry.filter_by_tags(["heavy", "kinetic"], require_all=True)
        """
        results = []
        tag_set = set(tags)

        for component in self._components.values():
            component_tags = set(component.tags)

            if require_all:
                # Component must have all specified tags
                if tag_set.issubset(component_tags):
                    results.append(component)
            else:
                # Component must have at least one specified tag
                if tag_set.intersection(component_tags):
                    results.append(component)

        return results

    def load_from_file(self, file_path: Union[str, Path]) -> Component:
        """
        Load a single component file.

        Args:
            file_path: Path to component file

        Returns:
            Loaded component

        Raises:
            ValidationError: If component is invalid
            FileNotFoundError: If file doesn't exist
        """
        component = ComponentLoader.load_component_from_file(file_path)
        self.register(component)
        return component

    def load_from_directory(self, directory: Union[str, Path]) -> int:
        """
        Load components from a directory.

        Recursively scans directory for YAML component files.

        Args:
            directory: Directory to scan

        Returns:
            Number of components loaded
        """
        components = load_components_from_directory(directory)
        return self.register_multiple(components)

    def load_theme(self, theme_name: str) -> int:
        """
        Load all components from a theme.

        Args:
            theme_name: Name of theme (e.g., "space-ships")

        Returns:
            Number of components loaded

        Raises:
            FileNotFoundError: If theme does not exist

        Example:
            >>> registry.load_theme("space-ships")
            15  # Loaded 15 components
        """
        theme_dir = self.data_directory / "themes" / theme_name / "components"

        if not theme_dir.exists():
            raise FileNotFoundError(
                f"Theme '{theme_name}' not found at {theme_dir}. "
                f"Available themes: {self.list_available_themes()}"
            )

        return self.load_from_directory(theme_dir)

    def list_available_themes(self) -> List[str]:
        """
        List available themes in the data directory.

        Returns:
            List of theme names
        """
        themes_dir = self.data_directory / "themes"

        if not themes_dir.exists():
            return []

        return [d.name for d in themes_dir.iterdir() if d.is_dir()]

    def get_stats_summary(self) -> Dict[str, int]:
        """
        Get registry statistics.

        Returns:
            Dictionary with component counts by type
        """
        return {
            "total": self.count(),
            "weapons": len(self.filter_by_type(WeaponComponent)),
            "armor": len(self.filter_by_type(ArmorComponent)),
            "shields": len(self.filter_by_type(ShieldComponent)),
            "engines": len(self.filter_by_type(EngineComponent)),
            "power_generators": len(self.filter_by_type(PowerGeneratorComponent)),
        }

    def __repr__(self) -> str:
        """String representation."""
        stats = self.get_stats_summary()
        return (
            f"ComponentRegistry("
            f"total={stats['total']}, "
            f"weapons={stats['weapons']}, "
            f"armor={stats['armor']}, "
            f"shields={stats['shields']}, "
            f"engines={stats['engines']}, "
            f"power={stats['power_generators']})"
        )
