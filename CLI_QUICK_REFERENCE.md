# Battle Automata CLI - Quick Reference

## Installation

```bash
pip install -e .
```

## Basic Commands

### Get Help
```bash
python -m battle_automata.cli.main --help
python -m battle_automata.cli.main theme --help
python -m battle_automata.cli.main component --help
```

### Version
```bash
python -m battle_automata.cli.main --version
```

---

## Theme Commands

### List All Themes
```bash
python -m battle_automata.cli.main theme list
```

**Output:**
```
Available Themes:
  Space Ships (space-ships) - v1.0.0
    Sci-fi space combat theme...
```

### Show Theme Details
```bash
python -m battle_automata.cli.main theme info space-ships
```

**Output:**
```
Theme: Space Ships
ID: space-ships
Version: 1.0.0
Author: Battle Automata Team
License: MIT

Components: 8
Units: 3
```

---

## Component Commands

### List All Components
```bash
python -m battle_automata.cli.main component list --theme space-ships
```

**Output:**
```
Loaded 8 components from theme 'space-ships'

ID                        Name                           Category
----------------------------------------------------------------------
laser_cannon_mk1          Laser Cannon Mk1               weapon
light_armor_mk1           Light Armor Plate Mk1          armor
...
```

### Filter by Category
```bash
python -m battle_automata.cli.main component list --theme space-ships --type weapon
```

**Categories:**
- `weapon` - Offensive weapons
- `armor` - Defensive armor
- `shield` - Energy shields
- `engine` - Propulsion systems
- `power` - Power generators

### Show Component Details
```bash
python -m battle_automata.cli.main component show laser_cannon_mk1 --theme space-ships
```

**Output:**
```
Component: Laser Cannon Mk1
ID: laser_cannon_mk1
Type: offensive
Category: weapon

Description...

Stats:
  damage: 50
  range: 100.0
  ...

Resources:
  power_draw: 25
  weight: 50
  ...
```

---

## Unit Commands

### List All Units
```bash
python -m battle_automata.cli.main unit list --theme space-ships
```

**Output:**
```
Found 3 units in theme 'space-ships'

ID                   Name                           Class
-----------------------------------------------------------------
fighter_mk1          Fighter Mk1                    fighter
scout_mk1            Scout Mk1                      scout
tank_mk1             Tank Mk1                       tank
```

### Show Unit Details
```bash
python -m battle_automata.cli.main unit show data/themes/space-ships/units/fighter_mk1.yaml
```

**Output:**
```
Unit: Fighter Mk1
ID: fighter_mk1
Theme: space-ships
Class: fighter

Description...

Layout: 10x10

Components (5):
  - laser_cannon_mk1 at (5, 2)
  - light_armor_mk1 at (5, 5)
  ...

Resource Budgets:
  max_power: 200
  max_weight: 500
  ...
```

---

## Battle Commands

### Simulate Battle (Placeholder)
```bash
# Using unit IDs from a theme
python -m battle_automata.cli.main battle simulate fighter_mk1 tank_mk1 --theme space-ships --seed 42

# Using unit files
python -m battle_automata.cli.main battle simulate unit1.yaml unit2.yaml --seed 42

# Save results to file
python -m battle_automata.cli.main battle simulate fighter_mk1 tank_mk1 --theme space-ships --output results.json
```

**Note:** Full battle simulation is pending implementation by other agents.

---

## Global Options

### Verbose Output
```bash
python -m battle_automata.cli.main -v theme list
```

### Quiet Mode
```bash
python -m battle_automata.cli.main -q component list --theme space-ships
```

### Custom Data Directory
```bash
python -m battle_automata.cli.main --data-dir /path/to/data theme list
```

---

## Common Workflows

### Explore a New Theme
```bash
# 1. List available themes
python -m battle_automata.cli.main theme list

# 2. Get theme details
python -m battle_automata.cli.main theme info space-ships

# 3. Browse components
python -m battle_automata.cli.main component list --theme space-ships

# 4. View specific component
python -m battle_automata.cli.main component show laser_cannon_mk1 --theme space-ships

# 5. See available units
python -m battle_automata.cli.main unit list --theme space-ships

# 6. Inspect a unit
python -m battle_automata.cli.main unit show data/themes/space-ships/units/fighter_mk1.yaml
```

### Compare Components
```bash
# List all weapons
python -m battle_automata.cli.main component list --theme space-ships --type weapon

# Show details of each
python -m battle_automata.cli.main component show laser_cannon_mk1 --theme space-ships
python -m battle_automata.cli.main component show missile_launcher_mk1 --theme space-ships
```

### Inspect Unit Loadout
```bash
# Show unit details
python -m battle_automata.cli.main unit show data/themes/space-ships/units/fighter_mk1.yaml

# Then inspect each component
python -m battle_automata.cli.main component show laser_cannon_mk1 --theme space-ships
python -m battle_automata.cli.main component show ion_engine_mk1 --theme space-ships
```

---

## Output Formats

The CLI uses Rich for beautiful terminal output with:
- Color-coded text
- Formatted tables
- Clear hierarchical information
- Error highlighting

---

## Tips

1. **Tab Completion**: Shell completion not yet implemented, but planned
2. **Aliases**: Create shell aliases for common commands:
   ```bash
   alias ba='python -m battle_automata.cli.main'
   ba theme list
   ```
3. **Data Location**: Default is `./data/themes/` from current directory
4. **Custom Themes**: Place theme directories in `data/themes/` to make them available

---

## Troubleshooting

### Command Not Found
Make sure you're using the full module path:
```bash
python -m battle_automata.cli.main --help
```

### Theme Not Found
Check the data directory:
```bash
ls data/themes/
python -m battle_automata.cli.main --data-dir ./data theme list
```

### Component Not Found
Make sure you're specifying the correct theme:
```bash
python -m battle_automata.cli.main component show laser_cannon_mk1 --theme space-ships
```

---

## Future Commands (Coming Soon)

These commands are planned but not yet implemented:

```bash
# Component validation
python -m battle_automata.cli.main component validate data/my_weapon.yaml

# Unit validation
python -m battle_automata.cli.main unit validate data/my_unit.yaml

# Unit builder
python -m battle_automata.cli.main unit create --theme space-ships

# Battle replay
python -m battle_automata.cli.main battle replay results.json

# Statistics
python -m battle_automata.cli.main stats component --theme space-ships
python -m battle_automata.cli.main stats unit --theme space-ships
```

---

## Python API Usage

You can also use the Engine directly in Python:

```python
from battle_automata.api.engine import Engine

# Create engine
engine = Engine()

# List themes
themes = engine.list_themes()

# Load theme
engine.load_theme("space-ships")

# Get components
components = engine.list_components()
weapons = engine.list_components(category="weapon")

# Get specific component
laser = engine.get_component("laser_cannon_mk1")

# Get units
units = engine.list_units()
fighter = engine.get_unit("fighter_mk1")
```

---

## Examples Directory

Check `data/themes/space-ships/` for complete examples of:
- Theme configuration (`theme.yaml`)
- Component definitions (YAML files)
- Unit configurations (YAML files)

Use these as templates for creating your own themes!

---

**Version:** 0.1.0
**Last Updated:** 2025-11-13
