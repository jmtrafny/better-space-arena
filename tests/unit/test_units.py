"""
Unit tests for Unit data structures and validation.
"""

import pytest

from battle_automata.schemas.unit import (
    Position,
    ComponentPlacement,
    UnitLayout,
    UnitResourceBudget,
    AIBehavior,
    UnitConfig,
)
from battle_automata.api.units import Unit, PlacedComponent
from pydantic import ValidationError


class TestPosition:
    """Test Position model"""

    def test_valid_position(self):
        """Test creating valid position"""
        pos = Position(x=5, y=10)
        assert pos.x == 5
        assert pos.y == 10

    def test_negative_position_fails(self):
        """Test negative coordinates fail"""
        with pytest.raises(ValidationError):
            Position(x=-1, y=5)

    def test_to_tuple(self):
        """Test converting to tuple"""
        pos = Position(x=3, y=7)
        assert pos.to_tuple() == (3, 7)

    def test_position_immutable(self):
        """Test position is immutable"""
        pos = Position(x=5, y=10)
        with pytest.raises(Exception):
            pos.x = 10  # Should fail


class TestComponentPlacement:
    """Test ComponentPlacement model"""

    def test_valid_placement(self):
        """Test creating valid placement"""
        placement = ComponentPlacement(
            component_id="laser_mk1",
            position=Position(x=5, y=2),
            facing=0.0
        )
        assert placement.component_id == "laser_mk1"
        assert placement.position.x == 5
        assert placement.facing == 0.0

    def test_facing_range(self):
        """Test facing must be 0-360"""
        with pytest.raises(ValidationError):
            ComponentPlacement(
                component_id="laser_mk1",
                position=Position(x=5, y=2),
                facing=400.0  # Out of range
            )

    def test_optional_slot_name(self):
        """Test slot_name is optional"""
        placement = ComponentPlacement(
            component_id="laser_mk1",
            position=Position(x=5, y=2),
            slot_name="weapon_1"
        )
        assert placement.slot_name == "weapon_1"


class TestUnitLayout:
    """Test UnitLayout model"""

    def test_valid_layout(self):
        """Test creating valid layout"""
        layout = UnitLayout(width=10, height=10)
        assert layout.width == 10
        assert layout.height == 10

    def test_zero_dimensions_fail(self):
        """Test zero dimensions fail"""
        with pytest.raises(ValidationError):
            UnitLayout(width=0, height=10)

    def test_too_large_layout_fails(self):
        """Test excessively large layout fails"""
        with pytest.raises(ValidationError):
            UnitLayout(width=20, height=20)  # 400 > 100 max


class TestUnitResourceBudget:
    """Test UnitResourceBudget model"""

    def test_valid_budget(self):
        """Test creating valid budget"""
        budget = UnitResourceBudget(
            max_power=100,
            max_weight=500,
            max_slots=20
        )
        assert budget.max_power == 100
        assert budget.max_weight == 500
        assert budget.max_slots == 20

    def test_optional_cost(self):
        """Test max_cost is optional"""
        budget = UnitResourceBudget(
            max_power=100,
            max_weight=500,
            max_slots=20,
            max_cost=1000
        )
        assert budget.max_cost == 1000

    def test_negative_values_fail(self):
        """Test negative values fail"""
        with pytest.raises(ValidationError):
            UnitResourceBudget(
                max_power=-100,
                max_weight=500,
                max_slots=20
            )


class TestAIBehavior:
    """Test AIBehavior model"""

    def test_valid_ai(self):
        """Test creating valid AI behavior"""
        ai = AIBehavior(
            movement_style="aggressive",
            engagement_range=100.0,
            retreat_threshold=0.3
        )
        assert ai.movement_style == "aggressive"
        assert ai.engagement_range == 100.0

    def test_invalid_movement_style_fails(self):
        """Test invalid movement style fails"""
        with pytest.raises(ValidationError):
            AIBehavior(movement_style="invalid")

    def test_retreat_threshold_range(self):
        """Test retreat threshold must be 0-1"""
        with pytest.raises(ValidationError):
            AIBehavior(retreat_threshold=1.5)


class TestUnitConfig:
    """Test UnitConfig model"""

    def test_valid_unit_config(self):
        """Test creating valid unit configuration"""
        config = UnitConfig(
            id="fighter_mk1",
            name="Fighter Mk1",
            theme="space-ships",
            layout=UnitLayout(width=10, height=10),
            components=[
                ComponentPlacement(
                    component_id="laser_mk1",
                    position=Position(x=5, y=2)
                )
            ],
            resources=UnitResourceBudget(
                max_power=100,
                max_weight=500,
                max_slots=20
            )
        )
        assert config.id == "fighter_mk1"
        assert config.name == "Fighter Mk1"
        assert len(config.components) == 1

    def test_empty_components_fails(self):
        """Test unit must have at least one component"""
        with pytest.raises(ValidationError):
            UnitConfig(
                id="fighter_mk1",
                name="Fighter Mk1",
                theme="space-ships",
                layout=UnitLayout(width=10, height=10),
                components=[],  # Empty!
                resources=UnitResourceBudget(
                    max_power=100,
                    max_weight=500,
                    max_slots=20
                )
            )

    def test_component_outside_grid_fails(self):
        """Test component placement outside grid fails"""
        with pytest.raises(ValidationError):
            UnitConfig(
                id="fighter_mk1",
                name="Fighter Mk1",
                theme="space-ships",
                layout=UnitLayout(width=10, height=10),
                components=[
                    ComponentPlacement(
                        component_id="laser_mk1",
                        position=Position(x=15, y=2)  # Outside 10x10 grid
                    )
                ],
                resources=UnitResourceBudget(
                    max_power=100,
                    max_weight=500,
                    max_slots=20
                )
            )


class TestUnit:
    """Test runtime Unit dataclass"""

    def test_create_unit(self, sample_laser):
        """Test creating a runtime unit"""
        placed_comp = PlacedComponent(
            component=sample_laser,
            position=(5, 2),
            facing=0.0
        )

        unit = Unit(
            id="fighter_mk1",
            name="Fighter Mk1",
            theme="space-ships",
            grid_width=10,
            grid_height=10,
            components=(placed_comp,),
            max_power=100,
            max_weight=500,
            max_slots=20,
            ai_behavior="aggressive"
        )

        assert unit.name == "Fighter Mk1"
        assert len(unit.components) == 1
        assert unit.grid_width == 10

    def test_unit_resource_calculations(self, sample_laser, sample_reactor):
        """Test unit resource calculation methods"""
        placed_laser = PlacedComponent(
            component=sample_laser,
            position=(5, 2),
            facing=0.0
        )
        placed_reactor = PlacedComponent(
            component=sample_reactor,
            position=(5, 5),
            facing=0.0
        )

        unit = Unit(
            id="fighter_mk1",
            name="Fighter Mk1",
            theme="space-ships",
            grid_width=10,
            grid_height=10,
            components=(placed_laser, placed_reactor),
            max_power=100,
            max_weight=500,
            max_slots=20,
            ai_behavior="aggressive"
        )

        assert unit.get_total_power_draw() == 20  # Laser only
        assert unit.get_total_power_generation() == 200  # Reactor
        assert unit.get_total_weight() == 200  # 50 + 150
        assert unit.get_total_slots() == 3  # 1 + 2

    def test_unit_get_weapons(self, sample_laser, sample_armor):
        """Test getting weapon components from unit"""
        placed_laser = PlacedComponent(
            component=sample_laser,
            position=(5, 2),
            facing=0.0
        )
        placed_armor = PlacedComponent(
            component=sample_armor,
            position=(5, 5),
            facing=0.0
        )

        unit = Unit(
            id="fighter_mk1",
            name="Fighter Mk1",
            theme="space-ships",
            grid_width=10,
            grid_height=10,
            components=(placed_laser, placed_armor),
            max_power=100,
            max_weight=500,
            max_slots=20,
            ai_behavior="aggressive"
        )

        weapons = unit.get_weapons()
        assert len(weapons) == 1
        assert weapons[0].component == sample_laser
