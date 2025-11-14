"""Theme loading and management utilities."""

from pathlib import Path
from typing import Dict, List, Optional, Any
import yaml
from dataclasses import dataclass


@dataclass
class ThemeInfo:
    """Information about a theme."""

    id: str
    name: str
    version: str
    description: str
    author: Optional[str] = None
    license: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ThemeInfo":
        """Create ThemeInfo from dictionary."""
        return cls(
            id=data.get("id", "unknown"),
            name=data.get("name", "Unknown Theme"),
            version=data.get("version", "0.0.0"),
            description=data.get("description", ""),
            author=data.get("author"),
            license=data.get("license"),
        )


class ThemeLoader:
    """Loader for theme data including components and units."""

    def __init__(self, themes_directory: Optional[Path] = None):
        """
        Initialize theme loader.

        Args:
            themes_directory: Path to themes directory (default: ./data/themes)
        """
        if themes_directory is None:
            themes_directory = Path.cwd() / "data" / "themes"
        self.themes_dir = Path(themes_directory)

    def list_themes(self) -> List[str]:
        """
        List available theme names.

        Returns:
            List of theme directory names
        """
        if not self.themes_dir.exists():
            return []

        themes = []
        for path in self.themes_dir.iterdir():
            if path.is_dir() and not path.name.startswith("."):
                themes.append(path.name)

        return sorted(themes)

    def get_theme_path(self, theme_name: str) -> Path:
        """
        Get path to theme directory.

        Args:
            theme_name: Name of the theme

        Returns:
            Path to theme directory

        Raises:
            FileNotFoundError: If theme doesn't exist
        """
        theme_path = self.themes_dir / theme_name
        if not theme_path.exists():
            raise FileNotFoundError(f"Theme not found: {theme_name}")
        return theme_path

    def load_theme_info(self, theme_name: str) -> ThemeInfo:
        """
        Load theme metadata from theme.yaml.

        Args:
            theme_name: Name of the theme

        Returns:
            ThemeInfo object

        Raises:
            FileNotFoundError: If theme or theme.yaml doesn't exist
        """
        theme_path = self.get_theme_path(theme_name)
        theme_file = theme_path / "theme.yaml"

        if not theme_file.exists():
            # Return basic info if theme.yaml doesn't exist
            return ThemeInfo(
                id=theme_name,
                name=theme_name.replace("-", " ").title(),
                version="0.0.0",
                description=f"Theme: {theme_name}",
            )

        with open(theme_file, "r") as f:
            data = yaml.safe_load(f)

        return ThemeInfo.from_dict(data)

    def discover_components(self, theme_name: str) -> List[Path]:
        """
        Discover all component files in theme.

        Args:
            theme_name: Name of the theme

        Returns:
            List of paths to component YAML files
        """
        theme_path = self.get_theme_path(theme_name)
        components_dir = theme_path / "components"

        if not components_dir.exists():
            return []

        # Find all .yaml and .yml files recursively
        component_files = []
        for ext in ["*.yaml", "*.yml"]:
            component_files.extend(components_dir.rglob(ext))

        return sorted(component_files)

    def discover_units(self, theme_name: str) -> List[Path]:
        """
        Discover all unit files in theme.

        Args:
            theme_name: Name of the theme

        Returns:
            List of paths to unit YAML files
        """
        theme_path = self.get_theme_path(theme_name)
        units_dir = theme_path / "units"

        if not units_dir.exists():
            return []

        # Find all .yaml and .yml files
        unit_files = []
        for ext in ["*.yaml", "*.yml"]:
            unit_files.extend(units_dir.glob(ext))

        return sorted(unit_files)

    def load_component_data(self, component_path: Path) -> Dict[str, Any]:
        """
        Load component data from YAML file.

        Args:
            component_path: Path to component file

        Returns:
            Component data dictionary
        """
        with open(component_path, "r") as f:
            return yaml.safe_load(f)

    def load_unit_data(self, unit_path: Path) -> Dict[str, Any]:
        """
        Load unit data from YAML file.

        Args:
            unit_path: Path to unit file

        Returns:
            Unit data dictionary
        """
        with open(unit_path, "r") as f:
            return yaml.safe_load(f)
