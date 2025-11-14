"""
Pytest configuration and fixtures.
"""

from pathlib import Path

import pytest

from battle_automata.core.registry import ComponentRegistry


@pytest.fixture
def data_dir() -> Path:
    """Get the data directory path."""
    return Path(__file__).parent.parent / "data"


@pytest.fixture
def test_data_dir() -> Path:
    """Get the test fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def component_registry(data_dir: Path) -> ComponentRegistry:
    """Create a fresh component registry."""
    return ComponentRegistry(data_directory=data_dir)


@pytest.fixture
def loaded_registry(component_registry: ComponentRegistry) -> ComponentRegistry:
    """Create a registry with space-ships theme loaded."""
    component_registry.load_theme("space-ships")
    return component_registry
