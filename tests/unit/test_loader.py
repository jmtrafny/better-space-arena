"""
Unit tests for component loader and registry.
"""

from pathlib import Path

import pytest

from battle_automata.core.component import (
    ArmorComponent,
    EngineComponent,
    PowerGeneratorComponent,
    WeaponComponent,
)
from battle_automata.core.registry import ComponentRegistry
from battle_automata.utils.loader import ComponentLoader


class TestComponentLoader:
    """Test ComponentLoader functionality."""

    def test_load_weapon_from_file(self, data_dir: Path):
        """Test loading a weapon component from YAML file."""
        weapon_file = data_dir / "themes" / "space-ships" / "components" / "weapons" / "laser_cannon_mk1.yaml"

        component = ComponentLoader.load_component_from_file(weapon_file)

        assert isinstance(component, WeaponComponent)
        assert component.id == "laser_cannon_mk1"
        assert component.name == "Laser Cannon Mk1"
        assert component.damage == 50
        assert component.range == 100.0

    def test_load_armor_from_file(self, data_dir: Path):
        """Test loading an armor component from YAML file."""
        armor_file = data_dir / "themes" / "space-ships" / "components" / "armor" / "composite_armor_mk1.yaml"

        component = ComponentLoader.load_component_from_file(armor_file)

        assert isinstance(component, ArmorComponent)
        assert component.id == "composite_armor_mk1"
        assert component.name == "Composite Armor Plate Mk1"
        assert component.armor_value == 100

    def test_load_engine_from_file(self, data_dir: Path):
        """Test loading an engine component from YAML file."""
        engine_file = data_dir / "themes" / "space-ships" / "components" / "engines" / "ion_engine_mk1.yaml"

        component = ComponentLoader.load_component_from_file(engine_file)

        assert isinstance(component, EngineComponent)
        assert component.id == "ion_engine_mk1"
        assert component.name == "Ion Engine Mk1"
        assert component.thrust == 300.0

    def test_load_power_generator_from_file(self, data_dir: Path):
        """Test loading a power generator from YAML file."""
        power_file = data_dir / "themes" / "space-ships" / "components" / "power" / "fusion_reactor_small.yaml"

        component = ComponentLoader.load_component_from_file(power_file)

        assert isinstance(component, PowerGeneratorComponent)
        assert component.id == "fusion_reactor_small"
        assert component.name == "Small Fusion Reactor"

    def test_load_nonexistent_file_raises_error(self):
        """Test loading non-existent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            ComponentLoader.load_component_from_file("nonexistent.yaml")


class TestComponentRegistry:
    """Test ComponentRegistry functionality."""

    def test_empty_registry(self, component_registry: ComponentRegistry):
        """Test newly created registry is empty."""
        assert component_registry.count() == 0
        assert len(component_registry.list_ids()) == 0

    def test_register_component(self, component_registry: ComponentRegistry, data_dir: Path):
        """Test registering a component."""
        weapon_file = data_dir / "themes" / "space-ships" / "components" / "weapons" / "laser_cannon_mk1.yaml"
        component = ComponentLoader.load_component_from_file(weapon_file)

        component_registry.register(component)

        assert component_registry.count() == 1
        assert component_registry.has("laser_cannon_mk1")

    def test_get_component(self, component_registry: ComponentRegistry, data_dir: Path):
        """Test getting a component by ID."""
        weapon_file = data_dir / "themes" / "space-ships" / "components" / "weapons" / "laser_cannon_mk1.yaml"
        component = ComponentLoader.load_component_from_file(weapon_file)
        component_registry.register(component)

        retrieved = component_registry.get("laser_cannon_mk1")

        assert retrieved is not None
        assert retrieved.id == "laser_cannon_mk1"

    def test_get_nonexistent_component_returns_none(self, component_registry: ComponentRegistry):
        """Test getting non-existent component returns None."""
        result = component_registry.get("nonexistent")
        assert result is None

    def test_get_or_raise_success(self, component_registry: ComponentRegistry, data_dir: Path):
        """Test get_or_raise returns component when it exists."""
        weapon_file = data_dir / "themes" / "space-ships" / "components" / "weapons" / "laser_cannon_mk1.yaml"
        component = ComponentLoader.load_component_from_file(weapon_file)
        component_registry.register(component)

        retrieved = component_registry.get_or_raise("laser_cannon_mk1")
        assert retrieved.id == "laser_cannon_mk1"

    def test_get_or_raise_failure(self, component_registry: ComponentRegistry):
        """Test get_or_raise raises KeyError when component doesn't exist."""
        with pytest.raises(KeyError):
            component_registry.get_or_raise("nonexistent")

    def test_load_theme(self, component_registry: ComponentRegistry):
        """Test loading an entire theme."""
        count = component_registry.load_theme("space-ships")

        assert count > 0
        assert component_registry.count() == count

        # Check that we loaded various types
        assert component_registry.has("laser_cannon_mk1")
        assert component_registry.has("composite_armor_mk1")
        assert component_registry.has("ion_engine_mk1")

    def test_filter_by_type(self, loaded_registry: ComponentRegistry):
        """Test filtering components by type."""
        weapons = loaded_registry.filter_by_type(WeaponComponent)
        assert len(weapons) > 0
        assert all(isinstance(c, WeaponComponent) for c in weapons)

        engines = loaded_registry.filter_by_type(EngineComponent)
        assert len(engines) > 0
        assert all(isinstance(c, EngineComponent) for c in engines)

    def test_filter_by_tags(self, loaded_registry: ComponentRegistry):
        """Test filtering components by tags."""
        energy_weapons = loaded_registry.filter_by_tags(["energy_weapon"])
        assert len(energy_weapons) > 0

        # Check components have the tag
        for component in energy_weapons:
            assert "energy_weapon" in component.tags

    def test_filter_by_multiple_tags_all_required(self, loaded_registry: ComponentRegistry):
        """Test filtering by multiple tags (all required)."""
        # Find components with both tags
        results = loaded_registry.filter_by_tags(
            ["energy_weapon", "point_defense"], require_all=True
        )

        for component in results:
            assert "energy_weapon" in component.tags
            assert "point_defense" in component.tags

    def test_filter_by_multiple_tags_any_match(self, loaded_registry: ComponentRegistry):
        """Test filtering by multiple tags (any match)."""
        results = loaded_registry.filter_by_tags(
            ["energy_weapon", "fusion"], require_all=False
        )

        assert len(results) > 0
        for component in results:
            assert "energy_weapon" in component.tags or "fusion" in component.tags

    def test_get_stats_summary(self, loaded_registry: ComponentRegistry):
        """Test getting registry statistics."""
        stats = loaded_registry.get_stats_summary()

        assert "total" in stats
        assert "weapons" in stats
        assert "armor" in stats
        assert stats["total"] > 0

    def test_unregister_component(self, component_registry: ComponentRegistry, data_dir: Path):
        """Test unregistering a component."""
        weapon_file = data_dir / "themes" / "space-ships" / "components" / "weapons" / "laser_cannon_mk1.yaml"
        component = ComponentLoader.load_component_from_file(weapon_file)
        component_registry.register(component)

        assert component_registry.has("laser_cannon_mk1")

        component_registry.unregister("laser_cannon_mk1")

        assert not component_registry.has("laser_cannon_mk1")

    def test_unregister_nonexistent_raises_error(self, component_registry: ComponentRegistry):
        """Test unregistering non-existent component raises KeyError."""
        with pytest.raises(KeyError):
            component_registry.unregister("nonexistent")

    def test_clear_registry(self, loaded_registry: ComponentRegistry):
        """Test clearing the registry."""
        assert loaded_registry.count() > 0

        loaded_registry.clear()

        assert loaded_registry.count() == 0

    def test_repr(self, loaded_registry: ComponentRegistry):
        """Test registry string representation."""
        repr_str = repr(loaded_registry)

        assert "ComponentRegistry" in repr_str
        assert "total=" in repr_str
        assert "weapons=" in repr_str
