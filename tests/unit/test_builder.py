"""
Unit tests for UnitBuilder fluent API.
"""

import pytest

from battle_automata.api.units import UnitBuilder
from battle_automata.api.components import ComponentRegistry
from battle_automata.utils.validator import ValidationResult


class TestUnitBuilder:
    """Test UnitBuilder fluent interface"""

    def test_create_builder(self):
        """Test creating a unit builder"""
        builder = UnitBuilder("Fighter", theme="space-ships")
        assert builder._name == "Fighter"
        assert builder._theme == "space-ships"

    def test_with_layout(self):
        """Test setting layout"""
        builder = UnitBuilder("Fighter", theme="space-ships")
        result = builder.with_layout(12, 12)

        assert result is builder  # Fluent API returns self
        assert builder._layout_width == 12
        assert builder._layout_height == 12

    def test_with_resources(self):
        """Test setting resource budgets"""
        builder = UnitBuilder("Fighter", theme="space-ships")
        result = builder.with_resources(power=150, weight=600, slots=25)

        assert result is builder
        assert builder._max_power == 150
        assert builder._max_weight == 600
        assert builder._max_slots == 25

    def test_with_description(self):
        """Test setting description"""
        builder = UnitBuilder("Fighter", theme="space-ships")
        result = builder.with_description("A fast fighter")

        assert result is builder
        assert builder._description == "A fast fighter"

    def test_with_tags(self):
        """Test adding tags"""
        builder = UnitBuilder("Fighter", theme="space-ships")
        result = builder.with_tags("fast", "agile")

        assert result is builder
        assert "fast" in builder._tags
        assert "agile" in builder._tags

    def test_add_component_instance(self, sample_laser):
        """Test adding component instance"""
        builder = UnitBuilder("Fighter", theme="space-ships")
        result = builder.add_component_instance(sample_laser, (5, 2), facing=0.0)

        assert result is builder
        assert len(builder._components) == 1
        comp, pos, facing = builder._components[0]
        assert comp == sample_laser
        assert pos == (5, 2)
        assert facing == 0.0

    def test_add_component_by_id(self, registry_with_components):
        """Test adding component by ID from registry"""
        builder = UnitBuilder(
            "Fighter",
            theme="space-ships",
            registry=registry_with_components
        )
        result = builder.add_component("laser_mk1", (5, 2))

        assert result is builder
        assert len(builder._components) == 1

    def test_add_component_not_found_fails(self):
        """Test adding non-existent component fails"""
        registry = ComponentRegistry()
        builder = UnitBuilder("Fighter", theme="space-ships", registry=registry)

        with pytest.raises(ValueError, match="Component not found"):
            builder.add_component("nonexistent", (5, 2))

    def test_remove_component_at(self, sample_laser, sample_armor):
        """Test removing component at position"""
        builder = UnitBuilder("Fighter", theme="space-ships")
        builder.add_component_instance(sample_laser, (5, 2))
        builder.add_component_instance(sample_armor, (5, 5))

        assert len(builder._components) == 2

        builder.remove_component_at((5, 2))
        assert len(builder._components) == 1

        # Armor should remain
        comp, pos, _ = builder._components[0]
        assert comp == sample_armor

    def test_fluent_chaining(self, sample_laser, sample_engine, sample_reactor):
        """Test method chaining works"""
        builder = (UnitBuilder("Fighter", theme="space-ships")
            .with_layout(10, 10)
            .with_resources(power=100, weight=500)
            .with_description("Fast fighter")
            .with_tags("fast", "agile")
            .add_component_instance(sample_laser, (5, 2))
            .add_component_instance(sample_engine, (5, 8))
            .add_component_instance(sample_reactor, (5, 5)))

        assert builder._layout_width == 10
        assert len(builder._components) == 3

    def test_build_complete_unit(self, registry_with_components):
        """Test building a complete valid unit"""
        builder = (UnitBuilder("Fighter", theme="space-ships", registry=registry_with_components)
            .with_layout(10, 10)
            .with_resources(power=200, weight=500, slots=20)
            .add_component("laser_mk1", (5, 2))
            .add_component("reactor_mk1", (5, 5))
            .add_component("engine_mk1", (5, 8)))

        unit = builder.build()

        assert unit.name == "Fighter"
        assert unit.theme == "space-ships"
        assert len(unit.components) == 3
        assert unit.grid_width == 10
        assert unit.grid_height == 10

    def test_build_validates_automatically(self):
        """Test build() validates the unit"""
        builder = UnitBuilder("Fighter", theme="space-ships")
        builder.with_layout(10, 10)
        # No components - should fail validation

        with pytest.raises(ValueError, match="validation failed"):
            builder.build()

    def test_validate_method(self, registry_with_components):
        """Test explicit validate() method"""
        builder = (UnitBuilder("Fighter", theme="space-ships", registry=registry_with_components)
            .with_layout(10, 10)
            .with_resources(power=200, weight=500, slots=20)
            .add_component("laser_mk1", (5, 2))
            .add_component("reactor_mk1", (5, 5))
            .add_component("engine_mk1", (5, 8)))

        result = builder.validate()
        assert result is builder  # Returns self for chaining

    def test_get_validation_result(self, registry_with_components):
        """Test getting validation result without raising"""
        builder = (UnitBuilder("Fighter", theme="space-ships", registry=registry_with_components)
            .with_layout(10, 10)
            .with_resources(power=200, weight=500, slots=20)
            .add_component("laser_mk1", (5, 2))
            .add_component("reactor_mk1", (5, 5))
            .add_component("engine_mk1", (5, 8)))

        result = builder.get_validation_result()

        assert isinstance(result, ValidationResult)
        assert result.valid


class TestValidationResult:
    """Test ValidationResult class"""

    def test_valid_result(self):
        """Test creating valid result"""
        result = ValidationResult(valid=True)
        assert result.valid
        assert bool(result) is True
        assert len(result.errors) == 0
        assert len(result.warnings) == 0

    def test_invalid_result(self):
        """Test creating invalid result"""
        result = ValidationResult(
            valid=False,
            errors=["Error 1", "Error 2"]
        )
        assert not result.valid
        assert bool(result) is False
        assert len(result.errors) == 2

    def test_result_with_warnings(self):
        """Test result with warnings"""
        result = ValidationResult(
            valid=True,
            warnings=["Warning 1"]
        )
        assert result.valid
        assert len(result.warnings) == 1

    def test_string_representation(self):
        """Test string formatting"""
        result = ValidationResult(
            valid=False,
            errors=["Test error"],
            warnings=["Test warning"]
        )
        string = str(result)
        assert "✗ Validation failed" in string
        assert "Test error" in string
        assert "Test warning" in string


class TestBuildValidation:
    """Test validation during build process"""

    def test_power_budget_exceeded(self, registry_with_components):
        """Test validation catches power budget exceeded"""
        builder = (UnitBuilder("Fighter", theme="space-ships", registry=registry_with_components)
            .with_layout(10, 10)
            .with_resources(power=50, weight=500, slots=20)  # Too low power
            .add_component("laser_mk1", (5, 2))  # 20W
            .add_component("reactor_mk1", (5, 5))  # 0W
            .add_component("engine_mk1", (5, 8)))  # 60W - total 80W > 50W budget

        result = builder.get_validation_result()
        assert not result.valid
        assert any("Power budget exceeded" in e for e in result.errors)

    def test_weight_budget_exceeded(self, registry_with_components):
        """Test validation catches weight budget exceeded"""
        builder = (UnitBuilder("Fighter", theme="space-ships", registry=registry_with_components)
            .with_layout(10, 10)
            .with_resources(power=200, weight=200, slots=20)  # Too low weight
            .add_component("laser_mk1", (5, 2))  # 50kg
            .add_component("reactor_mk1", (5, 5))  # 150kg
            .add_component("engine_mk1", (5, 8)))  # 100kg - total 300kg > 200kg budget

        result = builder.get_validation_result()
        assert not result.valid
        assert any("Weight limit exceeded" in e for e in result.errors)

    def test_insufficient_power_generation(self, registry_with_components):
        """Test validation catches insufficient power generation"""
        builder = (UnitBuilder("Fighter", theme="space-ships", registry=registry_with_components)
            .with_layout(10, 10)
            .with_resources(power=200, weight=500, slots=20)
            .add_component("laser_mk1", (5, 2))  # 20W draw
            .add_component("engine_mk1", (5, 8)))  # 60W draw, but no reactor!

        result = builder.get_validation_result()
        assert not result.valid
        # Should fail on missing power generator or insufficient power
        assert len(result.errors) > 0
