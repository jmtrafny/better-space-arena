"""
Example: Building units with the UnitBuilder fluent API

This demonstrates how to use the UnitBuilder to create custom units.
"""

from battle_automata.api.units import UnitBuilder
from battle_automata.api.components import (
    ComponentRegistry,
    WeaponComponent,
    PowerGeneratorComponent,
    EngineComponent,
    ArmorComponent,
)


def create_sample_components():
    """Create sample components for demonstration"""
    laser = WeaponComponent(
        id="laser_mk1",
        name="Laser Cannon Mk1",
        type="offensive",
        category="weapon",
        damage=50,
        range=100.0,
        fire_rate=1.0,
        power_draw=25,
        weight=50,
        slots=1,
        cost=100,
        tags=("energy", "weapon")
    )

    reactor = PowerGeneratorComponent(
        id="reactor_mk1",
        name="Fusion Reactor",
        type="support",
        category="power",
        max_output=150,
        power_draw=0,
        weight=120,
        slots=2,
        cost=200,
        tags=("power",)
    )

    engine = EngineComponent(
        id="ion_engine_mk1",
        name="Ion Engine",
        type="mobility",
        category="engine",
        thrust=300.0,
        max_speed=20.0,
        power_draw=45,
        weight=100,
        slots=2,
        cost=150,
        tags=("engine",)
    )

    armor = ArmorComponent(
        id="armor_mk1",
        name="Light Armor",
        type="defensive",
        category="armor",
        armor_value=80,
        coverage=0.6,
        power_draw=0,
        weight=80,
        slots=2,
        cost=120,
        tags=("armor",)
    )

    return [laser, reactor, engine, armor]


def main():
    """Demonstrate unit building"""

    # 1. Create a component registry
    registry = ComponentRegistry()

    # 2. Register components
    for comp in create_sample_components():
        registry.register(comp)

    # 3. Build a unit using fluent API
    print("Building Fighter unit...")
    fighter = (UnitBuilder("Fighter Mk1", theme="space-ships", registry=registry)
        .with_layout(10, 10)
        .with_resources(power=200, weight=500, slots=20)
        .with_description("Fast and agile fighter")
        .with_tags("fighter", "fast", "energy_weapons")
        .add_component("laser_mk1", (5, 2), facing=0)
        .add_component("laser_mk1", (4, 2), facing=0)  # Dual lasers
        .add_component("reactor_mk1", (5, 5), facing=0)
        .add_component("ion_engine_mk1", (5, 8), facing=180)
        .add_component("armor_mk1", (5, 5), facing=0)
        .validate()  # Validate configuration
        .build())  # Build final immutable unit

    # 4. Inspect the unit
    print(f"\nUnit: {fighter.name}")
    print(f"Theme: {fighter.theme}")
    print(f"Grid: {fighter.grid_width}x{fighter.grid_height}")
    print(f"Components: {len(fighter.components)}")
    print(f"\nResources:")
    print(f"  Power: {fighter.get_total_power_draw()}W / {fighter.max_power}W")
    print(f"  Generation: {fighter.get_total_power_generation()}W")
    print(f"  Weight: {fighter.get_total_weight()}kg / {fighter.max_weight}kg")
    print(f"  Slots: {fighter.get_total_slots()} / {fighter.max_slots}")
    print(f"  Cost: {fighter.get_total_cost()} credits")

    print(f"\nWeapons: {len(fighter.get_weapons())}")
    print(f"Engines: {len(fighter.get_engines())}")

    print("\nFighter built successfully!")


if __name__ == "__main__":
    main()
