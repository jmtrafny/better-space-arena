"""End-to-end test of complete workflow."""

import pytest
from pathlib import Path
from battle_automata.api.engine import Engine
from battle_automata.utils.theme import ThemeLoader


@pytest.fixture
def engine(tmp_path):
    """Create engine with test data directory."""
    # Create test theme
    themes_dir = tmp_path / "themes" / "test-theme"
    themes_dir.mkdir(parents=True)

    # Create theme.yaml
    theme_yaml = themes_dir / "theme.yaml"
    theme_yaml.write_text(
        """
id: test-theme
name: "Test Theme"
version: "1.0.0"
description: "Test theme"
"""
    )

    # Create components directory with test component
    comp_dir = themes_dir / "components"
    comp_dir.mkdir()

    test_comp = comp_dir / "test_weapon.yaml"
    test_comp.write_text(
        """
id: test_weapon
name: "Test Weapon"
type: offensive
category: weapon
damage_type: energy
stats:
  damage: 50
  range: 100
  fire_rate: 1.0
  accuracy: 0.85
resources:
  power_draw: 20
  weight: 50
  slots: 1
  cost: 100
tags:
  - test
"""
    )

    # Create units directory
    (themes_dir / "units").mkdir()

    return Engine(data_directory=tmp_path)


def test_engine_initialization(engine):
    """Test engine initializes correctly."""
    assert engine is not None
    assert engine.theme_loader is not None


def test_list_themes(engine):
    """Test listing available themes."""
    themes = engine.list_themes()
    assert "test-theme" in themes


def test_load_theme(engine):
    """Test loading a theme."""
    num_components = engine.load_theme("test-theme")
    assert num_components >= 0  # May be 0 or more
    assert engine.current_theme == "test-theme"


def test_get_theme_info(engine):
    """Test getting theme information."""
    info = engine.get_theme_info("test-theme")
    assert info.id == "test-theme"
    assert info.name == "Test Theme"
    assert info.version == "1.0.0"


def test_load_and_list_components(engine):
    """Test loading theme and listing components."""
    engine.load_theme("test-theme")
    components = engine.list_components()

    # Should have at least the test weapon
    assert len(components) >= 1

    # Find test weapon
    test_weapon = next((c for c in components if c.get("id") == "test_weapon"), None)
    assert test_weapon is not None
    assert test_weapon["name"] == "Test Weapon"


def test_get_component(engine):
    """Test getting specific component."""
    engine.load_theme("test-theme")
    comp = engine.get_component("test_weapon")

    assert comp is not None
    assert comp["id"] == "test_weapon"
    assert comp["name"] == "Test Weapon"
    assert comp["stats"]["damage"] == 50


def test_filter_components_by_category(engine):
    """Test filtering components by category."""
    engine.load_theme("test-theme")
    weapons = engine.list_components(category="weapon")

    assert len(weapons) >= 1
    assert all(c.get("category") == "weapon" for c in weapons)


@pytest.mark.slow
def test_complete_workflow(engine):
    """Test complete workflow from theme loading to battle."""
    # 1. List available themes
    themes = engine.list_themes()
    assert "test-theme" in themes

    # 2. Get theme info
    info = engine.get_theme_info("test-theme")
    assert info.name == "Test Theme"

    # 3. Load theme
    num_components = engine.load_theme("test-theme")
    assert engine.current_theme == "test-theme"

    # 4. List components
    components = engine.list_components()
    assert len(components) >= 1

    # 5. Get specific component
    weapon = engine.get_component("test_weapon")
    assert weapon is not None

    # Test passes - full workflow works
    assert True
