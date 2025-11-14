# Integration Guide
## Battle Automata Engine

**How to integrate the Battle Automata Engine into your project**

---

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Integration Methods](#integration-methods)
4. [API Reference](#api-reference)
5. [CLI Usage](#cli-usage)
6. [Web API](#web-api)
7. [Custom Extensions](#custom-extensions)
8. [Best Practices](#best-practices)

---

## Installation

### From PyPI (Recommended)

```bash
# Install base package
pip install battle-automata

# Install with web API support
pip install battle-automata[web]

# Install with all extras
pip install battle-automata[web,docs]
```

### From Source

```bash
# Clone repository
git clone https://github.com/yourusername/battle-automata.git
cd battle-automata

# Install in development mode
pip install -e .

# Or with development dependencies
pip install -e ".[dev]"
```

### Verify Installation

```bash
# Check version
battle-sim --version

# Run health check
battle-sim config show
```

---

## Quick Start

### 1. Initialize Project

```bash
# Create new project
battle-sim init --theme space-ships --name "My Battle Game"

# This creates:
# ./data/themes/space-ships/
# ./data/config/engine.yaml
```

### 2. Python Library Usage

```python
from battle_automata.api import initialize, Unit, Battle

# Initialize engine
engine = initialize(data_directory="./data")

# Load units
fighter = Unit.from_file("data/themes/space-ships/units/fighter.yaml")
tank = Unit.from_file("data/themes/space-ships/units/tank.yaml")

# Create and simulate battle
battle = Battle(fighter, tank, config={"seed": 12345})
result = battle.simulate()

# Print results
print(f"Winner: {result.winner}")
print(f"Duration: {result.duration}s")
print(f"Damage dealt: Fighter={result.unit1_damage_dealt}, Tank={result.unit2_damage_dealt}")
```

### 3. CLI Usage

```bash
# Simulate battle
battle-sim battle simulate \
  data/themes/space-ships/units/fighter.yaml \
  data/themes/space-ships/units/tank.yaml \
  --seed 12345

# Run tournament
battle-sim battle tournament \
  data/themes/space-ships/units/*.yaml \
  --rounds 5
```

---

## Integration Methods

### Method 1: Python Library

**Best for:** Python applications, scripts, Jupyter notebooks

```python
# Complete example

from battle_automata.api import (
    initialize,
    Unit,
    UnitBuilder,
    Component,
    Battle,
    BattleConfig
)

# 1. Initialize engine
engine = initialize(data_directory="./data")

# 2. Load theme
theme = engine.load_theme("space-ships")

# 3. Create unit programmatically
unit = (UnitBuilder("Custom Fighter", "space-ships")
    .with_layout(size=(10, 10))
    .with_resources(power=100, weight=500, slots=10)
    .add_component("laser_cannon_mk1", position=(5, 2), facing="forward")
    .add_component("armor_plate_light", position=(5, 5))
    .add_component("engine_basic", position=(5, 8), facing="rear")
    .build())

# 4. Load preset unit
preset_unit = engine.load_unit("data/themes/space-ships/units/tank.yaml")

# 5. Create battle with custom config
config = BattleConfig(
    arena_size=(100, 100),
    time_step=0.1,
    max_duration=300.0,
    seed=42
)

battle = Battle(unit, preset_unit, config=config)

# 6. Add event observer (optional)
def on_event(event):
    print(f"[{event.timestamp:.1f}s] {event.event_type}")

battle.add_observer(on_event)

# 7. Simulate
result = battle.simulate()

# 8. Process results
if result.outcome == "unit1_victory":
    print(f"{result.winner} won in {result.duration}s!")

# Export results
result.to_json("battle_results.json")
```

### Method 2: Command Line Interface

**Best for:** Shell scripts, automation, testing

```bash
#!/bin/bash
# battle_script.sh

# Configuration
DATA_DIR="./data"
THEME="space-ships"
SEED=12345

# List available components
echo "Available components:"
battle-sim component list --theme $THEME --type offensive

# Create units
echo "Creating units..."
battle-sim unit create --theme $THEME fighter.yaml
battle-sim unit create --theme $THEME tank.yaml

# Validate units
echo "Validating units..."
battle-sim unit validate fighter.yaml
battle-sim unit validate tank.yaml

# Run battle
echo "Running battle..."
battle-sim battle simulate \
  fighter.yaml \
  tank.yaml \
  --seed $SEED \
  --output battle_result.json \
  --verbose

# Analyze results
echo "Analyzing results..."
battle-sim battle analyze battle_result.json --metric damage
```

### Method 3: Web API

**Best for:** Web applications, microservices, remote access

```python
# server.py - FastAPI integration

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from battle_automata.api import Engine, BattleConfig

# Initialize FastAPI app
app = FastAPI(title="Battle Automata API")

# Initialize engine
engine = Engine(data_directory="./data")
engine.initialize()

# Request/Response models
class BattleRequest(BaseModel):
    unit1_id: str
    unit2_id: str
    seed: Optional[int] = None
    arena_size: tuple[int, int] = (100, 100)
    max_duration: float = 300.0

class BattleResponse(BaseModel):
    outcome: str
    winner: Optional[str]
    duration: float
    unit1_damage_dealt: int
    unit2_damage_dealt: int

# Endpoints
@app.post("/api/battles/simulate", response_model=BattleResponse)
async def simulate_battle(request: BattleRequest):
    """Simulate a battle between two units"""
    try:
        # Load units
        unit1 = engine.load_unit(f"data/themes/units/{request.unit1_id}.yaml")
        unit2 = engine.load_unit(f"data/themes/units/{request.unit2_id}.yaml")

        # Create battle
        config = BattleConfig(
            arena_size=request.arena_size,
            max_duration=request.max_duration,
            seed=request.seed
        )
        battle = engine.create_battle(unit1, unit2, config=config)

        # Simulate
        result = battle.simulate()

        return BattleResponse(
            outcome=result.outcome.value,
            winner=result.winner,
            duration=result.duration,
            unit1_damage_dealt=result.unit1_damage_dealt,
            unit2_damage_dealt=result.unit2_damage_dealt
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/components")
async def list_components(type: Optional[str] = None):
    """List available components"""
    components = engine.component_registry.list(type=type)
    return [{"id": c.id, "name": c.name, "type": c.type} for c in components]

@app.get("/api/units/{theme}")
async def list_units(theme: str):
    """List units in a theme"""
    theme_obj = engine.load_theme(theme)
    units = theme_obj.list_units()
    return {"theme": theme, "units": units}

# Run server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

Client usage:

```python
# client.py
import requests

# Simulate battle
response = requests.post(
    "http://localhost:8000/api/battles/simulate",
    json={
        "unit1_id": "fighter",
        "unit2_id": "tank",
        "seed": 12345
    }
)

result = response.json()
print(f"Winner: {result['winner']}")
```

### Method 4: Docker Container

**Best for:** Containerized deployments, cloud hosting

```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY src/ ./src/
COPY data/ ./data/
COPY pyproject.toml .

# Install package
RUN pip install -e .

# Expose port
EXPOSE 8000

# Run server
CMD ["battle-sim", "server", "start", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  battle-api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
    environment:
      - ENGINE_DATA_DIR=/app/data
      - LOG_LEVEL=INFO
```

Usage:

```bash
# Build and run
docker-compose up -d

# Use API
curl -X POST http://localhost:8000/api/battles/simulate \
  -H "Content-Type: application/json" \
  -d '{"unit1_id": "fighter", "unit2_id": "tank", "seed": 12345}'
```

---

## API Reference

### Core Classes

#### Engine

```python
from battle_automata.api import Engine

# Create engine
engine = Engine(data_directory="./data")
engine.initialize()

# Load theme
theme = engine.load_theme("space-ships")

# Load unit
unit = engine.load_unit("path/to/unit.yaml")

# Create battle
battle = engine.create_battle(unit1, unit2, config=...)

# Quick simulate
result = engine.simulate_battle("unit1.yaml", "unit2.yaml", seed=12345)

# Configuration
config = engine.get_config()
engine.set_config({"simulation.default_seed": 42})
```

#### Component

```python
from battle_automata.api import Component, ComponentRegistry

# Load component from file
component = Component.from_file("laser_cannon.yaml")

# Access properties
print(component.name)
print(component.type)  # ComponentType.OFFENSIVE
print(component.stats.damage)
print(component.resources.power_draw)

# Validate
is_valid = component.validate()

# Registry
registry = ComponentRegistry()
registry.load_from_directory("data/themes/space-ships/components")
laser = registry.get("laser_cannon_mk1")
weapons = registry.list(type="offensive")
```

#### Unit

```python
from battle_automata.api import Unit, UnitBuilder

# Load from file
unit = Unit.from_file("fighter.yaml")

# Build programmatically
unit = (UnitBuilder("Fighter", "space-ships")
    .with_layout((10, 10))
    .with_resources(power=100, weight=500, slots=10)
    .add_component("laser", (5, 2), "forward")
    .build())

# Validate
is_valid, errors = unit.validate()

# Get stats
stats = unit.get_total_stats()

# Save
unit.to_file("my_unit.yaml")
```

#### Battle

```python
from battle_automata.api import Battle, BattleConfig

# Create battle
config = BattleConfig(
    arena_size=(100, 100),
    time_step=0.1,
    max_duration=300.0,
    seed=12345
)

battle = Battle(unit1, unit2, config=config)

# Add observer
def on_event(event):
    print(f"{event.timestamp}: {event.event_type}")

battle.add_observer(on_event)

# Simulate (blocking)
result = battle.simulate()

# Or step-by-step
while battle.step():
    state = battle.get_state()
    # Process state...

# Results
print(result.winner)
print(result.duration)
print(result.outcome)
for event in result.events:
    print(event)

# Export
result.to_json("battle_log.json")
summary = result.to_summary()
```

#### BattleSimulator (Helper)

```python
from battle_automata.api import BattleSimulator

# Quick battle
result = BattleSimulator.quick_battle(
    "fighter.yaml",
    "tank.yaml",
    seed=12345
)

# Tournament
results = BattleSimulator.tournament(
    units=["fighter.yaml", "tank.yaml", "bomber.yaml"],
    rounds=5
)

# Replay
result = BattleSimulator.replay("battle_log.json")
```

---

## CLI Usage

### Global Options

```bash
battle-sim --help
battle-sim --version
battle-sim --data-dir ./custom/data [command]
```

### Component Commands

```bash
# List all components
battle-sim component list

# List by type
battle-sim component list --type offensive

# Show component details
battle-sim component show laser_cannon_mk1

# Create component template
battle-sim component create --theme space-ships --type offensive laser.yaml

# Validate component
battle-sim component validate laser_cannon.yaml
```

### Unit Commands

```bash
# List units
battle-sim unit list
battle-sim unit list --theme space-ships

# Show unit details
battle-sim unit show fighter --detail

# Create unit interactively
battle-sim unit create --theme space-ships --interactive my_unit.yaml

# Validate unit
battle-sim unit validate my_unit.yaml

# Export unit
battle-sim unit export my_unit.yaml --format json my_unit.json
```

### Battle Commands

```bash
# Simulate battle
battle-sim battle simulate unit1.yaml unit2.yaml

# With options
battle-sim battle simulate unit1.yaml unit2.yaml \
  --seed 12345 \
  --output result.json \
  --verbose \
  --watch

# Tournament
battle-sim battle tournament unit1.yaml unit2.yaml unit3.yaml \
  --rounds 5 \
  --output tournament.json \
  --format table

# Replay battle
battle-sim battle replay battle_log.json --speed 2.0

# Analyze results
battle-sim battle analyze battle_log.json --metric damage
```

### Theme Commands

```bash
# List themes
battle-sim theme list

# Show theme info
battle-sim theme info space-ships

# Validate theme
battle-sim theme validate ./data/themes/space-ships
```

### Server Commands

```bash
# Start dev server
battle-sim server start

# With options
battle-sim server start --host 0.0.0.0 --port 8080 --reload
```

---

## Web API

### Endpoints

```
GET  /api/components              List components
GET  /api/components/{id}         Get component details
GET  /api/units/{theme}           List units in theme
GET  /api/units/{theme}/{id}      Get unit details
POST /api/battles/simulate        Simulate battle
POST /api/battles/tournament      Run tournament
GET  /api/battles/{id}            Get battle results
WS   /api/battles/{id}/watch      Watch battle real-time
```

### Example: Simulate Battle

```bash
curl -X POST http://localhost:8000/api/battles/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "unit1_id": "fighter",
    "unit2_id": "tank",
    "seed": 12345,
    "arena_size": [100, 100],
    "max_duration": 300.0
  }'
```

Response:

```json
{
  "outcome": "unit1_victory",
  "winner": "fighter",
  "duration": 25.3,
  "total_turns": 253,
  "unit1_damage_dealt": 450,
  "unit2_damage_dealt": 200,
  "unit1_damage_taken": 200,
  "unit2_damage_taken": 450
}
```

### WebSocket: Real-time Battle

```javascript
// JavaScript client
const ws = new WebSocket('ws://localhost:8000/api/battles/123/watch');

ws.onmessage = (event) => {
  const battleEvent = JSON.parse(event.data);
  console.log(`[${battleEvent.timestamp}] ${battleEvent.event_type}`);

  if (battleEvent.event_type === 'battle_end') {
    console.log(`Winner: ${battleEvent.data.winner}`);
  }
};

ws.send(JSON.stringify({action: 'start'}));
```

---

## Custom Extensions

### Custom Component Type

```yaml
# data/themes/my-theme/components/custom/teleporter.yaml

id: teleporter_mk1
name: "Teleporter Mk1"
type: support
category: mobility_enhancement

stats:
  teleport_range: 50
  cooldown: 10.0

resources:
  power_draw: 50
  weight: 30
  slots: 1

special:
  effect: "teleport"
  max_uses: 3
```

### Custom Theme

```bash
# Create theme structure
mkdir -p data/themes/my-theme/{components,units}

# Create theme metadata
cat > data/themes/my-theme/theme.yaml << EOF
id: my-theme
name: "My Custom Theme"
version: "1.0.0"
description: "Custom battle theme"
author: "Your Name"
tags: [custom, experimental]
EOF

# Add components
# ...

# Add units
# ...

# Validate theme
battle-sim theme validate data/themes/my-theme
```

### Custom Mechanics (Advanced)

```python
# custom_mechanics.py

from battle_automata.mechanics import DamageCalculator

class CustomDamageCalculator(DamageCalculator):
    """Custom damage calculation with critical hits"""

    def calculate(self, attacker, defender, weapon):
        # Base damage
        base_damage = super().calculate(attacker, defender, weapon)

        # Add critical hit chance
        if self.rng.random() < 0.1:  # 10% crit chance
            return base_damage * 2

        return base_damage

# Register custom mechanic
from battle_automata.api import Engine

engine = Engine()
engine.register_mechanic("damage", CustomDamageCalculator())
```

---

## Best Practices

### 1. Error Handling

```python
from battle_automata.api import (
    Engine,
    ValidationError,
    UnitError,
    BattleError
)

try:
    engine = Engine(data_directory="./data")
    engine.initialize()

    unit = engine.load_unit("fighter.yaml")
    is_valid, errors = unit.validate()

    if not is_valid:
        print(f"Unit validation failed: {errors}")
        return

    result = engine.simulate_battle("unit1.yaml", "unit2.yaml")

except ValidationError as e:
    print(f"Validation error: {e.message}")
    print(f"Details: {e.details}")

except UnitError as e:
    print(f"Unit error: {e}")

except BattleError as e:
    print(f"Battle simulation error: {e}")

except Exception as e:
    print(f"Unexpected error: {e}")
```

### 2. Performance Optimization

```python
# Cache engine instance
_engine = None

def get_engine():
    global _engine
    if _engine is None:
        _engine = Engine(data_directory="./data")
        _engine.initialize()
    return _engine

# Reuse for multiple battles
engine = get_engine()

for i in range(100):
    result = engine.simulate_battle("unit1.yaml", "unit2.yaml", seed=i)
    # Process result...
```

### 3. Deterministic Testing

```python
import pytest
from battle_automata.api import Battle

def test_battle_determinism():
    """Ensure battles are deterministic"""
    unit1 = load_test_unit("fighter")
    unit2 = load_test_unit("tank")

    # Run same battle twice with same seed
    result1 = Battle(unit1, unit2, config={"seed": 42}).simulate()
    result2 = Battle(unit1, unit2, config={"seed": 42}).simulate()

    # Results must be identical
    assert result1.winner == result2.winner
    assert result1.duration == result2.duration
    assert len(result1.events) == len(result2.events)
```

### 4. Configuration Management

```python
# config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    data_directory: str = "./data"
    default_theme: str = "space-ships"
    default_seed: int = None
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        env_prefix = "BATTLE_"

# Usage
settings = Settings()
engine = Engine(data_directory=settings.data_directory)
```

### 5. Logging

```python
import logging
from battle_automata.api import Engine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Use logger
engine = Engine()
logger.info("Engine initialized")

result = engine.simulate_battle("unit1.yaml", "unit2.yaml")
logger.info(f"Battle completed: winner={result.winner}")
```

---

## Troubleshooting

### Common Issues

#### 1. Import Error

```python
# Error: ModuleNotFoundError: No module named 'battle_automata'

# Solution: Install package
pip install battle-automata
# or for development
pip install -e .
```

#### 2. Validation Error

```python
# Error: ValidationError: Invalid component configuration

# Solution: Check schema
battle-sim component validate my_component.yaml

# Fix common issues:
# - Missing required fields
# - Invalid types
# - Negative values where not allowed
```

#### 3. File Not Found

```python
# Error: FileNotFoundError: [Errno 2] No such file or directory

# Solution: Use absolute paths or verify working directory
import os
print(f"Current dir: {os.getcwd()}")

# Or use Path
from pathlib import Path
unit_path = Path("data/themes/space-ships/units/fighter.yaml")
if not unit_path.exists():
    print(f"File not found: {unit_path}")
```

#### 4. Battle Not Deterministic

```python
# Issue: Same battle produces different results

# Solution: Always set seed
battle = Battle(unit1, unit2, config={"seed": 12345})

# Verify RNG is seeded
import random
random.seed(12345)  # If using custom mechanics
```

---

## Support

### Resources

- **Documentation**: Full docs at `/home/user/better-space-arena/docs/`
- **API Reference**: `/home/user/better-space-arena/docs/api/`
- **Examples**: `/home/user/better-space-arena/examples/`
- **GitHub**: Issues and discussions

### Getting Help

1. Check documentation
2. Review examples
3. Search existing issues
4. Ask in community discussions
5. Create issue if bug found

---

## Next Steps

1. **Learn More**: Read the [User Guide](/home/user/better-space-arena/docs/user-guide/)
2. **Explore API**: See [API Reference](/home/user/better-space-arena/docs/api/)
3. **Build Custom Theme**: Follow [Theme Creation Guide](/home/user/better-space-arena/docs/developer-guide/extending.md)
4. **Contribute**: Read [Contributing Guide](/home/user/better-space-arena/CONTRIBUTING.md)

---

**Document Version**: 1.0
**Last Updated**: 2025-11-14
**Maintained By**: Integration Team