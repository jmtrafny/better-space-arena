"""Engine facade - main entry point for Battle Automata Engine."""

from pathlib import Path
from typing import Optional, Dict, Any, List
from battle_automata.utils.theme import ThemeLoader, ThemeInfo


class Engine:
    """
    Main engine facade providing high-level API.

    This is the recommended entry point for most applications.

    Example:
        >>> engine = Engine(data_directory="./data")
        >>> engine.load_theme("space-ships")
        >>> components = engine.list_components()
    """

    def __init__(
        self,
        data_directory: Optional[Path] = None,
        config_file: Optional[Path] = None,
    ):
        """
        Initialize the engine.

        Args:
            data_directory: Root data directory (default: ./data)
            config_file: Engine configuration file (optional)
        """
        if data_directory is None:
            data_directory = Path.cwd() / "data"

        self.data_dir = Path(data_directory)
        self.config_file = Path(config_file) if config_file else None

        # Initialize theme loader
        self.theme_loader = ThemeLoader(self.data_dir / "themes")

        # Current loaded theme
        self._current_theme: Optional[str] = None
        self._components: Dict[str, Any] = {}
        self._units: Dict[str, Any] = {}

    @property
    def current_theme(self) -> Optional[str]:
        """Get current loaded theme name."""
        return self._current_theme

    def list_themes(self) -> List[str]:
        """
        List available themes.

        Returns:
            List of theme names
        """
        return self.theme_loader.list_themes()

    def get_theme_info(self, theme_name: str) -> ThemeInfo:
        """
        Get theme metadata.

        Args:
            theme_name: Theme name

        Returns:
            ThemeInfo object
        """
        return self.theme_loader.load_theme_info(theme_name)

    def load_theme(self, theme_name: str) -> int:
        """
        Load a theme's components and units.

        Args:
            theme_name: Theme to load

        Returns:
            Number of components loaded

        Example:
            >>> engine.load_theme("space-ships")
            15
        """
        self._current_theme = theme_name

        # Discover component files
        component_files = self.theme_loader.discover_components(theme_name)

        # Load components
        self._components.clear()
        for comp_file in component_files:
            try:
                data = self.theme_loader.load_component_data(comp_file)
                comp_id = data.get("id", comp_file.stem)
                self._components[comp_id] = data
            except Exception as e:
                print(f"Warning: Failed to load component {comp_file}: {e}")

        # Discover unit files
        unit_files = self.theme_loader.discover_units(theme_name)

        # Load units
        self._units.clear()
        for unit_file in unit_files:
            try:
                data = self.theme_loader.load_unit_data(unit_file)
                unit_id = data.get("id", unit_file.stem)
                self._units[unit_id] = data
            except Exception as e:
                print(f"Warning: Failed to load unit {unit_file}: {e}")

        return len(self._components)

    def list_components(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List loaded components.

        Args:
            category: Filter by category (optional)

        Returns:
            List of component data dictionaries
        """
        components = list(self._components.values())

        if category:
            components = [c for c in components if c.get("category") == category]

        return components

    def get_component(self, component_id: str) -> Optional[Dict[str, Any]]:
        """
        Get component by ID.

        Args:
            component_id: Component identifier

        Returns:
            Component data or None if not found
        """
        return self._components.get(component_id)

    def list_units(self) -> List[Dict[str, Any]]:
        """
        List loaded units.

        Returns:
            List of unit data dictionaries
        """
        return list(self._units.values())

    def get_unit(self, unit_id: str) -> Optional[Dict[str, Any]]:
        """
        Get unit by ID.

        Args:
            unit_id: Unit identifier

        Returns:
            Unit data or None if not found
        """
        return self._units.get(unit_id)

    def load_unit_from_file(self, file_path: str) -> Dict[str, Any]:
        """
        Load unit from external file.

        Args:
            file_path: Path to unit file

        Returns:
            Unit data dictionary
        """
        return self.theme_loader.load_unit_data(Path(file_path))

    def simulate_battle(
        self,
        unit1_id: str,
        unit2_id: str,
        seed: Optional[int] = None,
        **config
    ) -> Dict[str, Any]:
        """
        Simulate a battle between two units.

        NOTE: This is a placeholder. Full battle simulation will be
        implemented by other agents.

        Args:
            unit1_id: First unit ID
            unit2_id: Second unit ID
            seed: Random seed
            **config: Additional battle configuration

        Returns:
            Battle result (placeholder)
        """
        unit1 = self.get_unit(unit1_id)
        unit2 = self.get_unit(unit2_id)

        if not unit1:
            raise ValueError(f"Unit not found: {unit1_id}")
        if not unit2:
            raise ValueError(f"Unit not found: {unit2_id}")

        # Placeholder result
        return {
            "winner": unit1_id,
            "unit1": unit1_id,
            "unit2": unit2_id,
            "seed": seed,
            "note": "Battle simulation not yet implemented",
        }
