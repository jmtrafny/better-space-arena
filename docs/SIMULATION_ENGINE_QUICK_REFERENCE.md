# Battle Simulation Engine - Quick Reference

**Full Specification**: See [SIMULATION_ENGINE_ARCHITECTURE.md](SIMULATION_ENGINE_ARCHITECTURE.md)

---

## Core Simulation Loop

```
Initialize → Turn Loop → Finalize
              ↓
    ┌─────────┴─────────┐
    │ 1. Movement       │
    │ 2. Targeting      │
    │ 3. Combat         │
    │ 4. Effects        │
    │ 5. State Update   │
    │ 6. Win Check      │
    └───────────────────┘
```

**Time Model**: Fixed time step (default 0.1s per turn)

---

## Phase Execution Order

### 1. Movement Phase
- Process all units in deterministic order (sorted by ID)
- Calculate desired movement based on AI behavior
- Validate movement (bounds, collisions)
- Apply movement and log events

### 2. Targeting Phase
- For each weapon on each unit:
  - Find valid targets (range, LOS, firing arc)
  - Select best target based on priority
  - Assign target to weapon

### 3. Combat Phase
- Collect all attacks (weapons with targets)
- For each attack:
  - Calculate hit chance
  - Roll for hit (seeded RNG)
  - Calculate damage (armor, type effectiveness)
  - Apply damage to target component
  - Handle component/unit destruction

### 4. Effects Phase
- Process active effects (DoT, buffs, debuffs)
- Update cooldowns
- Remove expired effects

### 5. State Update
- Increment turn counter
- Update elapsed time
- Invalidate caches

### 6. Win Condition Check
- Check elimination (all enemies destroyed)
- Check timeout (turn/time limit)
- Check objectives (future)

---

## Determinism Guarantees

| Requirement | Implementation |
|-------------|----------------|
| Random numbers | Seeded PRNG (MT19937) |
| Execution order | Sort by ID before processing |
| Floating point | Consistent math libraries |
| External state | No I/O during simulation |

**Test**: Same config + same seed = identical results (every time)

---

## Event Logging

All state changes generate events:
- BattleStart / BattleEnd
- TurnStart / TurnEnd
- Movement
- TargetAcquired
- AttackHit / AttackMiss
- ComponentDestroyed
- UnitDestroyed

**Events are**:
- Immutable
- Timestamped (simulation time + turn)
- Complete (contain all relevant data)
- Serializable (JSON)

**Use cases**:
- Perfect replay
- Debugging
- Statistics
- Visualization

---

## Combat Mechanics Summary

### Movement
```
thrust / mass = acceleration
acceleration * time_step = velocity_change
velocity * time_step = displacement
```

**AI Behaviors**:
- AGGRESSIVE: Move toward nearest enemy
- DEFENSIVE: Move away from enemies
- KITING: Maintain optimal weapon range
- STATIONARY: No movement

### Targeting
```
valid_targets = units in (range ∩ LOS ∩ firing_arc)
best_target = select_by_priority(valid_targets)
```

**Targeting Priorities**:
- CLOSEST: Nearest target
- WEAKEST: Lowest health
- STRONGEST: Highest health
- PRIORITY: Specific component types

### Damage
```
damage_after_armor = base_damage * (1 - armor/(armor + 100))
damage_after_type = damage_after_armor * type_multiplier
final_damage = damage_after_type * variance(0.9, 1.1)
```

**Armor Piercing**: Reduces effective armor
**Type Effectiveness**: Rock-paper-scissors modifiers

---

## Win Conditions

### Elimination (Primary)
- One team has no active units
- Most common win condition
- Winner: Last team standing

### Timeout (Failsafe)
- Turn limit exceeded (default: 1000 turns)
- Time limit exceeded (default: 100s)
- Winner: Team with most remaining health

### Objectives (Future)
- Custom objectives per scenario
- Examples: Protect target, reach location, survive duration

---

## Performance Optimizations

### Spatial Indexing
- Grid-based spatial hash
- O(1) proximity queries
- Faster than checking all units

### Caching
- Distance calculations
- Line of sight checks
- Target lists
- Invalidated each turn

### Early Termination
- Detect when outcome is mathematically certain
- Skip remaining simulation
- Example: No weapons remaining = instant loss

---

## Data Structures

### Core Types
```python
Vector2D: {x, y}              # Velocity, direction
Position: {x, y}              # Location in battlefield
Battlefield: {width, height}  # Arena bounds
```

### Battle State
```python
BattleState:
  - units: List[Unit]
  - turn: int
  - time_elapsed: float
  - config: BattleConfig
```

### Unit
```python
Unit:
  - id, team, name
  - position, facing, velocity
  - components: List[Component]
  - is_active: bool
  - movement_behavior
```

### Component
```python
Component:
  - id, type, name
  - stats: ComponentStats
  - health, max_health
  - is_destroyed: bool
  - current_target (for weapons)
```

---

## Public API

```python
# Create simulator
config = BattleConfig(seed=42)
simulator = BattleSimulator(config)

# Load units
simulator.load_units([unit1, unit2])

# Run simulation
result = simulator.simulate()

# Access results
print(f"Winner: {result.winner}")
print(f"Duration: {result.duration}s")
print(f"Turns: {result.turns}")

# Save results
result.save("battle.json")

# Replay
for event in result.events:
    print(event)
```

---

## Implementation Checklist

**Phase 1: Core**
- [ ] Data structures (Vector2D, Position, Unit, Component)
- [ ] BattleState and state management
- [ ] SeededRandom implementation
- [ ] Event system and EventLogger

**Phase 2: Simulation Loop**
- [ ] SimulationEngine class
- [ ] Main simulation loop
- [ ] Turn execution framework
- [ ] Win condition detection

**Phase 3: Combat Mechanics**
- [ ] Movement system and AI behaviors
- [ ] Targeting system (range, LOS, arcs)
- [ ] Damage system (calculation, types, armor)
- [ ] Effects system (DoT, buffs, cooldowns)

**Phase 4: Polish**
- [ ] Spatial indexing for performance
- [ ] Replay system
- [ ] Statistics calculation
- [ ] API documentation

**Phase 5: Testing**
- [ ] Determinism validation tests
- [ ] Unit tests for each system
- [ ] Integration tests
- [ ] Performance benchmarks

---

## Key Algorithms

### Distance Calculation
```python
distance = sqrt((x2-x1)² + (y2-y1)²)
```

### Hit Chance
```python
hit_chance = base_accuracy * range_factor * size_factor * speed_factor
hit_chance = clamp(hit_chance, 0.05, 0.95)
```

### Armor Reduction
```python
reduction = armor / (armor + K)  # K = 100
effective_reduction = reduction * (1 - armor_piercing)
damage = base_damage * (1 - effective_reduction)
```

### Max Speed
```python
total_thrust = sum(engine.thrust for engine in engines)
max_speed = total_thrust / unit_mass
```

---

## Configuration Example

```python
BattleConfig(
    seed=12345,
    max_turns=1000,
    max_time=100.0,
    time_step=0.1,
    win_conditions=[WinCondition.ELIMINATION],
    battlefield=Battlefield(width=1000, height=1000)
)
```

---

## Event Example

```json
{
  "timestamp": 1.5,
  "turn": 15,
  "event_type": "attack_hit",
  "data": {
    "attacker_id": "unit_1",
    "weapon_id": "laser_cannon_mk1",
    "target_unit_id": "unit_2",
    "target_component_id": "armor_plate_3",
    "damage": 42.7,
    "damage_type": "energy",
    "old_health": 100.0,
    "new_health": 57.3
  }
}
```

---

**For complete details, algorithms, and pseudocode, see the full architecture specification.**
