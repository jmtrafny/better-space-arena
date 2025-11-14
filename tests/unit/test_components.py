"""
Unit tests for component schemas and validation.
"""

import pytest
from pydantic import ValidationError

from battle_automata.schemas.component import (
    ArmorComponentConfig,
    ArmorResistances,
    ArmorStats,
    ArmorType,
    ComponentCategory,
    ComponentType,
    DamageType,
    EngineComponentConfig,
    EngineStats,
    PowerGeneratorComponentConfig,
    PowerGeneratorStats,
    ResourceCost,
    ShieldComponentConfig,
    ShieldStats,
    TargetingPriority,
    WeaponComponentConfig,
    WeaponSpecial,
    WeaponStats,
    WeaponTargeting,
)


class TestResourceCost:
    """Test ResourceCost validation."""

    def test_valid_resource_cost(self):
        """Test valid resource cost creation."""
        cost = ResourceCost(power_draw=50, weight=100, slots=2, cost=150)
        assert cost.power_draw == 50
        assert cost.weight == 100
        assert cost.slots == 2
        assert cost.cost == 150

    def test_power_draw_exceeds_limit(self):
        """Test power draw validation."""
        with pytest.raises(ValidationError):
            ResourceCost(power_draw=1001, weight=100, slots=2, cost=150)

    def test_zero_weight_invalid(self):
        """Test weight must be positive."""
        with pytest.raises(ValidationError):
            ResourceCost(power_draw=50, weight=0, slots=2, cost=150)

    def test_negative_cost_invalid(self):
        """Test cost cannot be negative."""
        with pytest.raises(ValidationError):
            ResourceCost(power_draw=50, weight=100, slots=2, cost=-10)


class TestWeaponComponentConfig:
    """Test WeaponComponentConfig validation."""

    def test_valid_weapon(self):
        """Test valid weapon configuration."""
        weapon = WeaponComponentConfig(
            id="test_laser",
            name="Test Laser",
            type=ComponentType.OFFENSIVE,
            category=ComponentCategory.WEAPON,
            damage_type=DamageType.ENERGY,
            stats=WeaponStats(
                damage=50, range=100, fire_rate=1.0, accuracy=0.85, projectile_speed=None
            ),
            resources=ResourceCost(power_draw=50, weight=50, slots=1, cost=100),
        )

        assert weapon.id == "test_laser"
        assert weapon.stats.damage == 50
        assert weapon.damage_type == DamageType.ENERGY

    def test_weapon_id_must_be_lowercase(self):
        """Test weapon ID must be lowercase."""
        with pytest.raises(ValidationError):
            WeaponComponentConfig(
                id="TestLaser",  # Uppercase
                name="Test Laser",
                type=ComponentType.OFFENSIVE,
                category=ComponentCategory.WEAPON,
                damage_type=DamageType.ENERGY,
                stats=WeaponStats(damage=50, range=100, fire_rate=1.0, accuracy=0.85),
                resources=ResourceCost(power_draw=50, weight=50, slots=1, cost=100),
            )

    def test_weapon_dps_too_high(self):
        """Test DPS validation."""
        with pytest.raises(ValidationError):
            WeaponComponentConfig(
                id="overpowered_weapon",
                name="Overpowered Weapon",
                type=ComponentType.OFFENSIVE,
                category=ComponentCategory.WEAPON,
                damage_type=DamageType.ENERGY,
                stats=WeaponStats(
                    damage=1000,  # High damage
                    range=100,
                    fire_rate=10.0,  # High fire rate
                    accuracy=0.85,
                ),
                resources=ResourceCost(power_draw=50, weight=50, slots=1, cost=100),
            )

    def test_weapon_power_balance(self):
        """Test power draw scales with DPS."""
        with pytest.raises(ValidationError):
            WeaponComponentConfig(
                id="underpowered_weapon",
                name="Underpowered Weapon",
                type=ComponentType.OFFENSIVE,
                category=ComponentCategory.WEAPON,
                damage_type=DamageType.ENERGY,
                stats=WeaponStats(damage=100, range=100, fire_rate=1.0, accuracy=0.85),
                resources=ResourceCost(
                    power_draw=1, weight=50, slots=1, cost=100  # Too low power
                ),
            )

    def test_energy_weapon_needs_more_power(self):
        """Test energy weapons require more power than kinetic."""
        with pytest.raises(ValidationError):
            WeaponComponentConfig(
                id="weak_energy_weapon",
                name="Weak Energy Weapon",
                type=ComponentType.OFFENSIVE,
                category=ComponentCategory.WEAPON,
                damage_type=DamageType.ENERGY,
                stats=WeaponStats(damage=50, range=100, fire_rate=1.0, accuracy=0.85),
                resources=ResourceCost(power_draw=20, weight=50, slots=1, cost=100),
            )

    def test_firing_arc_validation(self):
        """Test firing arc must be a standard value."""
        with pytest.raises(ValidationError):
            WeaponComponentConfig(
                id="weird_arc_weapon",
                name="Weird Arc Weapon",
                type=ComponentType.OFFENSIVE,
                category=ComponentCategory.WEAPON,
                damage_type=DamageType.KINETIC,
                stats=WeaponStats(damage=50, range=100, fire_rate=1.0, accuracy=0.85),
                targeting=WeaponTargeting(firing_arc=75),  # Non-standard arc
                resources=ResourceCost(power_draw=50, weight=50, slots=1, cost=100),
            )


class TestArmorComponentConfig:
    """Test ArmorComponentConfig validation."""

    def test_valid_armor(self):
        """Test valid armor configuration."""
        armor = ArmorComponentConfig(
            id="test_armor",
            name="Test Armor",
            type=ComponentType.DEFENSIVE,
            category=ComponentCategory.ARMOR,
            armor_type=ArmorType.COMPOSITE,
            stats=ArmorStats(armor_value=100, coverage=0.8, durability=300),
            resources=ResourceCost(power_draw=0, weight=100, slots=2, cost=150),
        )

        assert armor.id == "test_armor"
        assert armor.stats.armor_value == 100
        assert armor.armor_type == ArmorType.COMPOSITE

    def test_armor_efficiency_limit(self):
        """Test armor cannot be too efficient (armor per kg)."""
        with pytest.raises(ValidationError):
            ArmorComponentConfig(
                id="super_light_armor",
                name="Super Light Armor",
                type=ComponentType.DEFENSIVE,
                category=ComponentCategory.ARMOR,
                armor_type=ArmorType.COMPOSITE,
                stats=ArmorStats(armor_value=300, coverage=0.8, durability=300),
                resources=ResourceCost(
                    power_draw=0, weight=10, slots=2, cost=150  # Too light
                ),
            )

    def test_armor_resistances_balanced(self):
        """Test armor resistances cannot be too high overall."""
        with pytest.raises(ValidationError):
            ArmorComponentConfig(
                id="super_armor",
                name="Super Armor",
                type=ComponentType.DEFENSIVE,
                category=ComponentCategory.ARMOR,
                armor_type=ArmorType.COMPOSITE,
                stats=ArmorStats(armor_value=100, coverage=0.8, durability=300),
                resistances=ArmorResistances(
                    kinetic_resist=2.0,  # Max
                    energy_resist=2.0,  # Max
                    explosive_resist=2.0,  # Max - total too high!
                ),
                resources=ResourceCost(power_draw=0, weight=100, slots=2, cost=150),
            )


class TestShieldComponentConfig:
    """Test ShieldComponentConfig validation."""

    def test_valid_shield(self):
        """Test valid shield configuration."""
        shield = ShieldComponentConfig(
            id="test_shield",
            name="Test Shield",
            type=ComponentType.DEFENSIVE,
            category=ComponentCategory.SHIELD,
            stats=ShieldStats(
                shield_strength=200, recharge_rate=20.0, recharge_delay=3.0, coverage=1.0
            ),
            resources=ResourceCost(power_draw=20, weight=60, slots=2, cost=200),
        )

        assert shield.id == "test_shield"
        assert shield.stats.shield_strength == 200

    def test_shield_power_requirement(self):
        """Test shields need sufficient power."""
        with pytest.raises(ValidationError):
            ShieldComponentConfig(
                id="weak_shield",
                name="Weak Shield",
                type=ComponentType.DEFENSIVE,
                category=ComponentCategory.SHIELD,
                stats=ShieldStats(
                    shield_strength=500,  # High shield
                    recharge_rate=20.0,
                    recharge_delay=3.0,
                    coverage=1.0,
                ),
                resources=ResourceCost(
                    power_draw=10, weight=60, slots=2, cost=200  # Too low power
                ),
            )


class TestEngineComponentConfig:
    """Test EngineComponentConfig validation."""

    def test_valid_engine(self):
        """Test valid engine configuration."""
        engine = EngineComponentConfig(
            id="test_engine",
            name="Test Engine",
            type=ComponentType.MOBILITY,
            category=ComponentCategory.ENGINE,
            stats=EngineStats(thrust=300.0, max_speed=20.0, acceleration=5.0, turn_rate=90.0),
            resources=ResourceCost(power_draw=60, weight=100, slots=2, cost=120),
        )

        assert engine.id == "test_engine"
        assert engine.stats.thrust == 300.0

    def test_engine_power_scaling(self):
        """Test engine power scales with thrust."""
        with pytest.raises(ValidationError):
            EngineComponentConfig(
                id="weak_engine",
                name="Weak Engine",
                type=ComponentType.MOBILITY,
                category=ComponentCategory.ENGINE,
                stats=EngineStats(
                    thrust=1000.0,  # High thrust
                    max_speed=20.0,
                    acceleration=5.0,
                    turn_rate=90.0,
                ),
                resources=ResourceCost(
                    power_draw=10, weight=100, slots=2, cost=120  # Too low power
                ),
            )


class TestPowerGeneratorComponentConfig:
    """Test PowerGeneratorComponentConfig validation."""

    def test_valid_power_generator(self):
        """Test valid power generator configuration."""
        generator = PowerGeneratorComponentConfig(
            id="test_generator",
            name="Test Generator",
            type=ComponentType.SUPPORT,
            category=ComponentCategory.POWER,
            stats=PowerGeneratorStats(max_output=200, efficiency=1.0),
            resources=ResourceCost(power_draw=0, weight=150, slots=2, cost=200),
        )

        assert generator.id == "test_generator"
        assert generator.stats.max_output == 200

    def test_power_generator_no_power_draw(self):
        """Test power generators cannot consume power."""
        with pytest.raises(ValidationError):
            PowerGeneratorComponentConfig(
                id="broken_generator",
                name="Broken Generator",
                type=ComponentType.SUPPORT,
                category=ComponentCategory.POWER,
                stats=PowerGeneratorStats(max_output=200, efficiency=1.0),
                resources=ResourceCost(
                    power_draw=50, weight=150, slots=2, cost=200  # Cannot draw power!
                ),
            )


class TestTypeCategoryMatching:
    """Test type-category validation."""

    def test_weapon_must_be_offensive(self):
        """Test weapons must have offensive type."""
        with pytest.raises(ValidationError):
            WeaponComponentConfig(
                id="test",
                name="Test",
                type=ComponentType.DEFENSIVE,  # Wrong type!
                category=ComponentCategory.WEAPON,
                damage_type=DamageType.ENERGY,
                stats=WeaponStats(damage=50, range=100, fire_rate=1.0, accuracy=0.85),
                resources=ResourceCost(power_draw=50, weight=50, slots=1, cost=100),
            )
