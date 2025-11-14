"""
Component System Demo

This script demonstrates the complete component system:
- Loading components from YAML files
- Validating component data with Pydantic
- Using the component registry
- Filtering and querying components
"""

from pathlib import Path

from battle_automata.core.component import WeaponComponent
from battle_automata.core.registry import ComponentRegistry
from battle_automata.utils.loader import ComponentLoader


def main():
    """Demonstrate the component system."""
    # Setup
    data_dir = Path(__file__).parent.parent / "data"

    print("=" * 60)
    print("Battle Automata Engine - Component System Demo")
    print("=" * 60)
    print()

    # 1. Load a single component from file
    print("1. Loading a single component from YAML file...")
    print("-" * 60)

    laser_file = data_dir / "themes" / "space-ships" / "components" / "weapons" / "laser_cannon_mk1.yaml"
    laser = ComponentLoader.load_component_from_file(laser_file)

    print(f"Loaded: {laser.name} (ID: {laser.id})")
    print(f"  Type: {type(laser).__name__}")
    print(f"  Damage: {laser.damage}")
    print(f"  Range: {laser.range}m")
    print(f"  Fire Rate: {laser.fire_rate} shots/sec")
    print(f"  Power Draw: {laser.power_draw}W")
    print(f"  Tags: {', '.join(laser.tags)}")
    print()

    # 2. Create and use a registry
    print("2. Creating component registry and loading theme...")
    print("-" * 60)

    registry = ComponentRegistry(data_directory=data_dir)
    count = registry.load_theme("space-ships")

    print(f"Loaded {count} components from 'space-ships' theme")
    print(f"Registry stats: {registry}")
    print()

    # 3. Query components
    print("3. Querying components...")
    print("-" * 60)

    # Get all weapons
    weapons = registry.filter_by_type(WeaponComponent)
    print(f"Found {len(weapons)} weapons:")
    for weapon in weapons:
        dps = weapon.damage * weapon.fire_rate
        print(f"  - {weapon.name}: {dps:.1f} DPS ({weapon.power_draw}W)")

    print()

    # 4. Filter by tags
    print("4. Filtering by tags...")
    print("-" * 60)

    energy_weapons = registry.filter_by_tags(["energy_weapon"])
    print(f"Energy weapons ({len(energy_weapons)}):")
    for weapon in energy_weapons:
        print(f"  - {weapon.name}")

    print()

    # 5. Get specific component
    print("5. Getting specific component...")
    print("-" * 60)

    missile = registry.get("missile_launcher_mk1")
    if missile:
        print(f"Retrieved: {missile.name}")
        if isinstance(missile, WeaponComponent):
            print(f"  Has splash damage: {missile.splash_radius is not None}")
            if missile.splash_radius:
                print(f"  Splash radius: {missile.splash_radius}m")
    else:
        print("Missile launcher not found (might not be in example data)")

    print()

    # 6. Display all component IDs
    print("6. All registered components:")
    print("-" * 60)

    all_ids = registry.list_ids()
    for i, component_id in enumerate(sorted(all_ids), 1):
        component = registry.get(component_id)
        print(f"  {i}. {component_id} - {component.name}")

    print()
    print("=" * 60)
    print("Demo complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
