# Battle Simulation Engine Architecture Specification

**Version:** 1.0
**Date:** 2025-11-14
**Status:** Design Specification
**Author:** Systems Architect

---

## Table of Contents

1. [Overview](#overview)
2. [Design Principles](#design-principles)
3. [Core Architecture](#core-architecture)
4. [Simulation Loop Algorithm](#simulation-loop-algorithm)
5. [Combat Mechanics](#combat-mechanics)
6. [Deterministic Execution Strategy](#deterministic-execution-strategy)
7. [Event Logging System](#event-logging-system)
8. [Win Condition Detection](#win-condition-detection)
9. [State Management](#state-management)
10. [Performance Considerations](#performance-considerations)
11. [Data Structures](#data-structures)
12. [API Design](#api-design)

---

## Overview

### Purpose

The Battle Simulation Engine is the core component responsible for executing deterministic, turn-based combat simulations between automata units. It must provide:

- **Deterministic execution**: Same inputs always produce same outputs
- **Complete observability**: Every action is logged for replay
- **Fair simulation**: No hidden state or non-deterministic behavior
- **Extensibility**: Easy to add new mechanics and behaviors
- **Performance**: Handle battles efficiently even with many units and components

### System Context

```
┌─────────────────────────────────────────────────────────────┐
│                     Battle Simulation Engine                 │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Simulation  │  │   Combat     │  │    Event     │      │
│  │     Loop     │──│  Mechanics   │──│   Logger     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         │                  │                  │              │
│         └──────────────────┴──────────────────┘              │
│                           │                                  │
└───────────────────────────┼──────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
  ┌─────▼─────┐      ┌─────▼─────┐      ┌─────▼─────┐
  │   Unit    │      │Component  │      │  Battle   │
  │  System   │      │  System   │      │  Config   │
  └───────────┘      └───────────┘      └───────────┘
```

---

## Design Principles

### 1. Determinism First

Every aspect of the simulation must be deterministic:
- Use seeded pseudo-random number generation
- Fixed execution order for all operations
- No external dependencies during simulation
- Consistent floating-point arithmetic

### 2. Event Sourcing

All state changes are derived from events:
- Events are immutable records of what happened
- State can be reconstructed from event log
- Enables perfect replay functionality
- Facilitates debugging and analysis

### 3. Separation of Concerns

Clear boundaries between subsystems:
- Simulation loop orchestrates high-level flow
- Combat mechanics handle specific calculations
- Event logger records all actions
- State manager maintains battle state

### 4. Data-Driven Design

Game logic driven by configuration:
- No hardcoded combat values
- Component properties define behavior
- Easy to modify balance without code changes
- Supports multiple themes and variants

---

## Core Architecture

### Component Diagram

```
┌────────────────────────────────────────────────────────────────┐
│                        BattleSimulator                          │
├────────────────────────────────────────────────────────────────┤
│ + initialize(config: BattleConfig) -> BattleState             │
│ + simulate() -> BattleResult                                   │
│ + step() -> bool                                               │
│ + get_state() -> BattleState                                   │
└───────────┬────────────────────────────────────────────────────┘
            │
            │ uses
            ▼
┌────────────────────────────────────────────────────────────────┐
│                      SimulationEngine                           │
├────────────────────────────────────────────────────────────────┤
│ - state: BattleState                                           │
│ - config: SimulationConfig                                     │
│ - rng: SeededRandom                                            │
│ - event_log: EventLogger                                       │
│ - turn_number: int                                             │
│ - time_elapsed: float                                          │
├────────────────────────────────────────────────────────────────┤
│ + execute_turn() -> void                                       │
│ + process_movement_phase() -> void                             │
│ + process_targeting_phase() -> void                            │
│ + process_combat_phase() -> void                               │
│ + process_effects_phase() -> void                              │
│ + check_win_conditions() -> Optional[Winner]                   │
└────────────┬───────────────────────────────────────────────────┘
             │
             │ delegates to
             ▼
     ┌───────────────┬───────────────┬──────────────┐
     │               │               │              │
┌────▼─────┐  ┌─────▼──────┐  ┌────▼──────┐  ┌───▼──────┐
│Movement  │  │ Targeting  │  │  Damage   │  │ Effects  │
│ System   │  │  System    │  │  System   │  │ System   │
└──────────┘  └────────────┘  └───────────┘  └──────────┘
```

### Class Responsibilities

#### BattleSimulator
- **Role**: Facade and coordinator for entire simulation
- **Responsibilities**:
  - Initialize battle from configuration
  - Execute complete simulation
  - Provide step-by-step execution for visualization
  - Return final results

#### SimulationEngine
- **Role**: Core simulation loop executor
- **Responsibilities**:
  - Maintain simulation state
  - Execute turn-based logic
  - Coordinate combat phases
  - Manage deterministic time progression

#### Combat Systems (Movement, Targeting, Damage, Effects)
- **Role**: Specialized mechanics handlers
- **Responsibilities**:
  - Implement specific combat calculations
  - Maintain internal consistency
  - Generate appropriate events
  - Query and update battle state

---

## Simulation Loop Algorithm

### High-Level Flow

```
┌─────────────────────────────────────────────────────────┐
│ START: Initialize Battle                                │
│  - Load units and configurations                        │
│  - Initialize positions and starting state              │
│  - Seed random number generator                         │
│  - Create event logger                                  │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │ Turn Loop             │
         │ (while not finished)  │
         └───────────┬───────────┘
                     │
          ┌──────────┴──────────┐
          │                     │
          ▼                     │
┌─────────────────────┐         │
│ 1. Movement Phase   │         │
│  - Process movement │         │
│  - Update positions │         │
│  - Check collisions │         │
└──────────┬──────────┘         │
           │                    │
           ▼                    │
┌─────────────────────┐         │
│ 2. Targeting Phase  │         │
│  - Scan for targets │         │
│  - Calculate ranges │         │
│  - Assign targets   │         │
└──────────┬──────────┘         │
           │                    │
           ▼                    │
┌─────────────────────┐         │
│ 3. Combat Phase     │         │
│  - Process attacks  │         │
│  - Calculate damage │         │
│  - Apply damage     │         │
│  - Handle destroyed │         │
└──────────┬──────────┘         │
           │                    │
           ▼                    │
┌─────────────────────┐         │
│ 4. Effects Phase    │         │
│  - Apply DoT/HoT    │         │
│  - Update buffs     │         │
│  - Tick cooldowns   │         │
└──────────┬──────────┘         │
           │                    │
           ▼                    │
┌─────────────────────┐         │
│ 5. State Update     │         │
│  - Increment turn   │         │
│  - Update timers    │         │
│  - Log events       │         │
└──────────┬──────────┘         │
           │                    │
           ▼                    │
┌─────────────────────┐         │
│ 6. Win Check        │         │
│  - Check conditions │─────────┘
│  - Determine winner │    continue if no winner
└──────────┬──────────┘
           │
           ▼ winner found or timeout
┌─────────────────────┐
│ END: Return Results │
│  - Winner           │
│  - Event log        │
│  - Final state      │
│  - Statistics       │
└─────────────────────┘
```

### Pseudocode: Main Simulation Loop

```python
class SimulationEngine:
    def simulate(self, config: BattleConfig) -> BattleResult:
        """
        Execute complete battle simulation.

        Returns:
            BattleResult containing winner, events, and statistics
        """
        # INITIALIZATION PHASE
        self.state = self._initialize_battle(config)
        self.rng = SeededRandom(config.seed)
        self.event_log = EventLogger()
        self.turn_number = 0
        self.time_elapsed = 0.0

        # Log initial state
        self.event_log.log_event(BattleStartEvent(
            timestamp=0.0,
            turn=0,
            units=self.state.get_unit_snapshots()
        ))

        # MAIN SIMULATION LOOP
        while not self._is_finished():
            # Execute one complete turn
            self._execute_turn()

            # Check if we've exceeded max turns (failsafe)
            if self.turn_number >= config.max_turns:
                self.event_log.log_event(TimeoutEvent(
                    timestamp=self.time_elapsed,
                    turn=self.turn_number
                ))
                break

        # FINALIZATION PHASE
        winner = self._determine_winner()
        statistics = self._calculate_statistics()

        self.event_log.log_event(BattleEndEvent(
            timestamp=self.time_elapsed,
            turn=self.turn_number,
            winner=winner,
            statistics=statistics
        ))

        return BattleResult(
            winner=winner,
            duration=self.time_elapsed,
            turns=self.turn_number,
            events=self.event_log.get_events(),
            final_state=self.state.snapshot(),
            statistics=statistics
        )

    def _execute_turn(self):
        """Execute one complete simulation turn."""
        self.turn_number += 1
        turn_start_time = self.time_elapsed

        # Log turn start
        self.event_log.log_event(TurnStartEvent(
            timestamp=turn_start_time,
            turn=self.turn_number
        ))

        # PHASE 1: MOVEMENT
        self._process_movement_phase()

        # PHASE 2: TARGETING
        self._process_targeting_phase()

        # PHASE 3: COMBAT
        self._process_combat_phase()

        # PHASE 4: EFFECTS
        self._process_effects_phase()

        # PHASE 5: CLEANUP
        self._cleanup_phase()

        # Update elapsed time (fixed time step)
        self.time_elapsed += self.config.time_step

        # Log turn end
        self.event_log.log_event(TurnEndEvent(
            timestamp=self.time_elapsed,
            turn=self.turn_number
        ))

    def _is_finished(self) -> bool:
        """Check if simulation should terminate."""
        winner = self._check_win_conditions()
        return winner is not None
```

### Pseudocode: Movement Phase

```python
def _process_movement_phase(self):
    """
    Process movement for all units.

    Movement order is deterministic (sorted by unit ID).
    Each unit's movement is independent and simultaneous.
    """
    # Get all active units in deterministic order
    units = sorted(self.state.get_active_units(), key=lambda u: u.id)

    for unit in units:
        # Skip if unit cannot move
        if not unit.can_move():
            continue

        # Calculate desired movement based on AI behavior
        movement_vector = self._calculate_movement(unit)

        if movement_vector.is_zero():
            continue

        # Calculate new position
        old_position = unit.position
        new_position = self._calculate_new_position(
            unit=unit,
            movement_vector=movement_vector,
            time_step=self.config.time_step
        )

        # Validate movement (bounds checking, collision detection)
        if self._is_valid_movement(unit, new_position):
            # Apply movement
            unit.position = new_position
            unit.velocity = movement_vector

            # Log movement event
            self.event_log.log_event(MovementEvent(
                timestamp=self.time_elapsed,
                turn=self.turn_number,
                unit_id=unit.id,
                old_position=old_position,
                new_position=new_position,
                distance=old_position.distance_to(new_position)
            ))
        else:
            # Movement blocked - log collision
            self.event_log.log_event(CollisionEvent(
                timestamp=self.time_elapsed,
                turn=self.turn_number,
                unit_id=unit.id,
                attempted_position=new_position
            ))

def _calculate_movement(self, unit: Unit) -> Vector2D:
    """
    Determine unit's movement direction and speed.

    This implements the AI behavior for autonomous movement.
    """
    # Get movement-capable components (engines, thrusters)
    engines = unit.get_components_by_type(ComponentType.ENGINE)

    if not engines:
        return Vector2D.zero()

    # Calculate total thrust capacity
    total_thrust = sum(engine.stats.thrust for engine in engines if engine.is_functional())

    if total_thrust == 0:
        return Vector2D.zero()

    # Determine movement strategy based on unit behavior
    target = self._find_nearest_enemy(unit)

    if target is None:
        return Vector2D.zero()

    # Calculate direction to target
    direction = (target.position - unit.position).normalized()

    # Calculate speed based on thrust and unit mass
    max_speed = total_thrust / unit.mass
    desired_velocity = direction * max_speed

    # Apply acceleration limits
    acceleration = (desired_velocity - unit.velocity) / self.config.time_step
    max_acceleration = total_thrust / unit.mass

    if acceleration.magnitude() > max_acceleration:
        acceleration = acceleration.normalized() * max_acceleration

    # Calculate final velocity
    new_velocity = unit.velocity + (acceleration * self.config.time_step)

    # Clamp to max speed
    if new_velocity.magnitude() > max_speed:
        new_velocity = new_velocity.normalized() * max_speed

    return new_velocity
```

### Pseudocode: Targeting Phase

```python
def _process_targeting_phase(self):
    """
    Process targeting for all weapons.

    Each weapon independently selects its target based on:
    - Range
    - Line of sight
    - Targeting priority
    - Weapon facing/arc
    """
    # Get all active units in deterministic order
    units = sorted(self.state.get_active_units(), key=lambda u: u.id)

    for unit in units:
        # Get all offensive components (weapons)
        weapons = unit.get_components_by_type(ComponentType.WEAPON)

        for weapon in sorted(weapons, key=lambda w: w.id):
            # Skip if weapon is not ready
            if not weapon.can_fire(self.time_elapsed):
                continue

            # Find valid targets
            potential_targets = self._find_targets_for_weapon(unit, weapon)

            if not potential_targets:
                continue

            # Select best target based on weapon's targeting priority
            target = self._select_target(weapon, potential_targets)

            # Assign target to weapon
            weapon.current_target = target

            # Log targeting event
            self.event_log.log_event(TargetAcquiredEvent(
                timestamp=self.time_elapsed,
                turn=self.turn_number,
                unit_id=unit.id,
                weapon_id=weapon.id,
                target_id=target.unit_id,
                target_component_id=target.component_id,
                range=unit.position.distance_to(target.position)
            ))

def _find_targets_for_weapon(self, unit: Unit, weapon: Component) -> List[Target]:
    """
    Find all valid targets for a weapon.

    Returns:
        List of valid targets sorted deterministically
    """
    potential_targets = []
    enemies = self.state.get_enemy_units(unit)

    for enemy in enemies:
        # Check if enemy is in range
        distance = unit.position.distance_to(enemy.position)
        if distance > weapon.stats.range:
            continue

        # Check line of sight
        if not self._has_line_of_sight(unit.position, enemy.position):
            continue

        # Check weapon firing arc
        angle_to_target = self._calculate_angle(unit, enemy)
        if not weapon.is_in_firing_arc(angle_to_target):
            continue

        # Add all components as potential targets
        for component in enemy.get_targetable_components():
            potential_targets.append(Target(
                unit_id=enemy.id,
                component_id=component.id,
                position=component.get_world_position(),
                component_type=component.type,
                health=component.health
            ))

    # Sort deterministically (by unit ID, then component ID)
    return sorted(potential_targets, key=lambda t: (t.unit_id, t.component_id))

def _select_target(self, weapon: Component, targets: List[Target]) -> Target:
    """
    Select best target based on weapon's targeting priority.

    Targeting priorities:
    - CLOSEST: Nearest target
    - STRONGEST: Highest health
    - WEAKEST: Lowest health
    - PRIORITY: Specific component types (e.g., weapons first)
    """
    priority = weapon.targeting_priority

    if priority == TargetingPriority.CLOSEST:
        return min(targets, key=lambda t: t.position.distance_to(weapon.position))

    elif priority == TargetingPriority.WEAKEST:
        return min(targets, key=lambda t: t.health)

    elif priority == TargetingPriority.STRONGEST:
        return max(targets, key=lambda t: t.health)

    elif priority == TargetingPriority.PRIORITY:
        # Sort by component type priority, then by distance
        priority_order = weapon.component_type_priority
        return min(targets, key=lambda t: (
            priority_order.index(t.component_type) if t.component_type in priority_order else 999,
            t.position.distance_to(weapon.position)
        ))

    else:
        # Default: first valid target (deterministic)
        return targets[0]
```

### Pseudocode: Combat Phase

```python
def _process_combat_phase(self):
    """
    Process all weapon attacks.

    All attacks are processed simultaneously (same turn).
    Damage is calculated but not applied until all attacks are calculated.
    """
    # Collect all attacks first
    attacks = []
    units = sorted(self.state.get_active_units(), key=lambda u: u.id)

    for unit in units:
        weapons = unit.get_components_by_type(ComponentType.WEAPON)

        for weapon in sorted(weapons, key=lambda w: w.id):
            if weapon.current_target is None:
                continue

            if not weapon.can_fire(self.time_elapsed):
                continue

            # Create attack descriptor
            attack = self._create_attack(unit, weapon, weapon.current_target)
            attacks.append(attack)

            # Update weapon cooldown
            weapon.last_fire_time = self.time_elapsed

    # Process all attacks simultaneously
    for attack in attacks:
        self._process_attack(attack)

def _create_attack(self, attacker: Unit, weapon: Component, target: Target) -> Attack:
    """
    Create an attack descriptor with all necessary information.
    """
    distance = attacker.position.distance_to(target.position)

    return Attack(
        attacker_id=attacker.id,
        weapon_id=weapon.id,
        target_unit_id=target.unit_id,
        target_component_id=target.component_id,
        weapon_type=weapon.weapon_type,
        base_damage=weapon.stats.damage,
        damage_type=weapon.damage_type,
        range=distance,
        accuracy=weapon.stats.accuracy,
        special_effects=weapon.special_effects
    )

def _process_attack(self, attack: Attack):
    """
    Process a single attack: hit calculation, damage calculation, application.
    """
    # STEP 1: Calculate hit chance
    hit_chance = self._calculate_hit_chance(attack)

    # STEP 2: Roll for hit (deterministic using seeded RNG)
    roll = self.rng.random()
    is_hit = roll <= hit_chance

    if not is_hit:
        # Log miss
        self.event_log.log_event(AttackMissEvent(
            timestamp=self.time_elapsed,
            turn=self.turn_number,
            attacker_id=attack.attacker_id,
            weapon_id=attack.weapon_id,
            target_unit_id=attack.target_unit_id,
            target_component_id=attack.target_component_id,
            roll=roll,
            required=hit_chance
        ))
        return

    # STEP 3: Calculate damage
    damage = self._calculate_damage(attack)

    # STEP 4: Apply damage to target component
    target_unit = self.state.get_unit(attack.target_unit_id)
    target_component = target_unit.get_component(attack.target_component_id)

    old_health = target_component.health
    actual_damage = min(damage, target_component.health)
    target_component.health -= actual_damage

    # STEP 5: Log hit event
    self.event_log.log_event(AttackHitEvent(
        timestamp=self.time_elapsed,
        turn=self.turn_number,
        attacker_id=attack.attacker_id,
        weapon_id=attack.weapon_id,
        target_unit_id=attack.target_unit_id,
        target_component_id=attack.target_component_id,
        damage=actual_damage,
        damage_type=attack.damage_type,
        old_health=old_health,
        new_health=target_component.health
    ))

    # STEP 6: Check if component destroyed
    if target_component.health <= 0:
        self._handle_component_destruction(target_unit, target_component)

def _calculate_hit_chance(self, attack: Attack) -> float:
    """
    Calculate probability of attack hitting target.

    Factors:
    - Base weapon accuracy
    - Range (falloff)
    - Target evasion
    - Environmental factors
    """
    base_accuracy = attack.accuracy

    # Range penalty
    weapon = self.state.get_component(attack.attacker_id, attack.weapon_id)
    max_range = weapon.stats.range
    range_factor = 1.0 - (attack.range / max_range) * 0.3  # 30% penalty at max range

    # Target evasion (based on size, speed)
    target_unit = self.state.get_unit(attack.target_unit_id)
    target_component = target_unit.get_component(attack.target_component_id)

    # Smaller components are harder to hit
    size_factor = target_component.size / 10.0  # Normalized size

    # Moving targets are harder to hit
    speed_factor = 1.0 - (target_unit.velocity.magnitude() / 100.0) * 0.2

    # Final calculation
    hit_chance = base_accuracy * range_factor * size_factor * speed_factor

    # Clamp between minimum and maximum
    return max(0.05, min(0.95, hit_chance))  # 5% min, 95% max

def _calculate_damage(self, attack: Attack) -> float:
    """
    Calculate actual damage dealt by attack.

    Factors:
    - Base weapon damage
    - Armor/shield reduction
    - Damage type effectiveness
    - Special modifiers
    """
    base_damage = attack.base_damage

    # Get target component
    target_unit = self.state.get_unit(attack.target_unit_id)
    target_component = target_unit.get_component(attack.target_component_id)

    # Armor reduction
    armor = target_component.stats.armor
    damage_reduction = armor / (armor + 100)  # Diminishing returns formula

    # Armor piercing
    armor_piercing = attack.special_effects.get('armor_piercing', 0.0)
    effective_reduction = damage_reduction * (1.0 - armor_piercing)

    # Apply reduction
    damage_after_armor = base_damage * (1.0 - effective_reduction)

    # Damage type effectiveness
    type_multiplier = self._get_damage_type_multiplier(
        attack.damage_type,
        target_component.type
    )

    final_damage = damage_after_armor * type_multiplier

    # Random variance (±10%)
    variance = self.rng.uniform(0.9, 1.1)
    final_damage *= variance

    return max(1.0, final_damage)  # Minimum 1 damage

def _handle_component_destruction(self, unit: Unit, component: Component):
    """
    Handle component being destroyed.
    """
    # Mark component as destroyed
    component.is_destroyed = True

    # Log destruction
    self.event_log.log_event(ComponentDestroyedEvent(
        timestamp=self.time_elapsed,
        turn=self.turn_number,
        unit_id=unit.id,
        component_id=component.id,
        component_type=component.type
    ))

    # Apply secondary effects (explosions, chain reactions, etc.)
    if component.has_special_effect('explosive'):
        self._handle_explosion(unit, component)

    # Check if unit is destroyed
    if unit.is_destroyed():
        self._handle_unit_destruction(unit)

def _handle_unit_destruction(self, unit: Unit):
    """
    Handle unit being completely destroyed.
    """
    # Mark unit as destroyed
    unit.is_active = False

    # Log unit destruction
    self.event_log.log_event(UnitDestroyedEvent(
        timestamp=self.time_elapsed,
        turn=self.turn_number,
        unit_id=unit.id,
        final_position=unit.position
    ))
```

### Pseudocode: Effects Phase

```python
def _process_effects_phase(self):
    """
    Process all active effects (DoT, buffs, debuffs).

    Effects are processed in deterministic order.
    """
    units = sorted(self.state.get_active_units(), key=lambda u: u.id)

    for unit in units:
        # Process active effects on unit
        for effect in sorted(unit.active_effects, key=lambda e: e.id):
            self._process_effect(unit, effect)

        # Process component-specific effects
        for component in sorted(unit.components, key=lambda c: c.id):
            for effect in sorted(component.active_effects, key=lambda e: e.id):
                self._process_component_effect(unit, component, effect)

        # Tick down cooldowns
        for component in unit.components:
            component.update_cooldowns(self.config.time_step)

def _process_effect(self, unit: Unit, effect: Effect):
    """
    Process a single active effect.
    """
    # Tick effect duration
    effect.remaining_duration -= self.config.time_step

    # Apply periodic effects (DoT, HoT, etc.)
    if effect.is_periodic():
        if self.time_elapsed - effect.last_tick >= effect.tick_interval:
            self._apply_periodic_effect(unit, effect)
            effect.last_tick = self.time_elapsed

    # Apply continuous effects (buffs, debuffs)
    if effect.is_continuous():
        self._apply_continuous_effect(unit, effect)

    # Remove expired effects
    if effect.remaining_duration <= 0:
        unit.remove_effect(effect)
        self.event_log.log_event(EffectExpiredEvent(
            timestamp=self.time_elapsed,
            turn=self.turn_number,
            unit_id=unit.id,
            effect_id=effect.id
        ))
```

---

## Combat Mechanics

### Movement System

#### Movement Calculation

```python
class MovementSystem:
    """
    Handles all movement-related calculations.
    """

    def calculate_thrust(self, unit: Unit) -> float:
        """
        Calculate total available thrust from engines.
        """
        engines = unit.get_components_by_type(ComponentType.ENGINE)
        total_thrust = 0.0

        for engine in engines:
            if engine.is_functional():
                # Damaged engines provide reduced thrust
                efficiency = engine.health / engine.max_health
                total_thrust += engine.stats.thrust * efficiency

        return total_thrust

    def calculate_max_speed(self, unit: Unit) -> float:
        """
        Calculate maximum speed based on thrust-to-weight ratio.
        """
        thrust = self.calculate_thrust(unit)
        mass = unit.calculate_mass()

        if mass == 0:
            return 0.0

        # Physics-based calculation
        return thrust / mass * self.config.speed_multiplier

    def calculate_rotation_speed(self, unit: Unit) -> float:
        """
        Calculate how fast unit can rotate.
        """
        thrusters = unit.get_components_by_type(ComponentType.THRUSTER)
        total_torque = sum(t.stats.torque for t in thrusters if t.is_functional())

        moment_of_inertia = unit.calculate_moment_of_inertia()

        if moment_of_inertia == 0:
            return 0.0

        return total_torque / moment_of_inertia

    def apply_movement(self, unit: Unit, velocity: Vector2D, time_step: float) -> Position:
        """
        Calculate new position given velocity and time step.
        """
        displacement = velocity * time_step
        new_position = unit.position + displacement

        # Clamp to battlefield bounds
        new_position = self._clamp_to_bounds(new_position)

        return new_position

    def check_collision(self, unit: Unit, new_position: Position) -> bool:
        """
        Check if movement would result in collision.
        """
        for other_unit in self.state.get_active_units():
            if other_unit.id == unit.id:
                continue

            distance = new_position.distance_to(other_unit.position)
            min_distance = unit.radius + other_unit.radius

            if distance < min_distance:
                return True  # Collision detected

        return False
```

#### Movement AI Behaviors

```python
class MovementAI:
    """
    AI behaviors for autonomous movement.
    """

    def calculate_desired_movement(self, unit: Unit, state: BattleState) -> Vector2D:
        """
        Determine desired movement based on tactical situation.
        """
        behavior = unit.movement_behavior

        if behavior == MovementBehavior.AGGRESSIVE:
            return self._aggressive_movement(unit, state)
        elif behavior == MovementBehavior.DEFENSIVE:
            return self._defensive_movement(unit, state)
        elif behavior == MovementBehavior.KITING:
            return self._kiting_movement(unit, state)
        elif behavior == MovementBehavior.STATIONARY:
            return Vector2D.zero()
        else:
            return self._default_movement(unit, state)

    def _aggressive_movement(self, unit: Unit, state: BattleState) -> Vector2D:
        """
        Move directly toward nearest enemy.
        """
        nearest_enemy = self._find_nearest_enemy(unit, state)

        if nearest_enemy is None:
            return Vector2D.zero()

        # Move toward enemy
        direction = (nearest_enemy.position - unit.position).normalized()
        max_speed = unit.calculate_max_speed()

        return direction * max_speed

    def _kiting_movement(self, unit: Unit, state: BattleState) -> Vector2D:
        """
        Maintain optimal weapon range while avoiding close combat.
        """
        nearest_enemy = self._find_nearest_enemy(unit, state)

        if nearest_enemy is None:
            return Vector2D.zero()

        # Get longest-range weapon
        max_weapon_range = max(
            (w.stats.range for w in unit.get_weapons()),
            default=0
        )

        current_distance = unit.position.distance_to(nearest_enemy.position)
        optimal_distance = max_weapon_range * 0.8  # Stay at 80% of max range

        direction = (nearest_enemy.position - unit.position).normalized()

        if current_distance < optimal_distance:
            # Too close - move away
            return -direction * unit.calculate_max_speed()
        elif current_distance > optimal_distance * 1.2:
            # Too far - move closer
            return direction * unit.calculate_max_speed()
        else:
            # Good distance - orbit
            perpendicular = Vector2D(-direction.y, direction.x)
            return perpendicular * unit.calculate_max_speed() * 0.5
```

### Targeting System

#### Line of Sight

```python
class TargetingSystem:
    """
    Handles target acquisition and line of sight.
    """

    def has_line_of_sight(self, from_pos: Position, to_pos: Position) -> bool:
        """
        Check if there's a clear line of sight between two positions.

        Currently simplified (no obstacles). Can be extended for:
        - Terrain blocking
        - Other units blocking
        - Stealth/cloaking
        """
        # For MVP: Always true if in range
        # Future: Raycasting for obstacles
        return True

    def calculate_firing_arc(self, weapon: Component, unit: Unit) -> Arc:
        """
        Calculate the firing arc for a weapon based on its mounting.
        """
        # Weapon position relative to unit center
        weapon_position = weapon.get_relative_position()
        weapon_facing = weapon.facing

        # Calculate absolute facing based on unit orientation
        absolute_facing = unit.facing + weapon_facing

        # Get weapon arc (degrees)
        arc_width = weapon.stats.firing_arc

        return Arc(
            center=absolute_facing,
            width=arc_width
        )

    def is_in_firing_arc(self, weapon: Component, unit: Unit, target: Position) -> bool:
        """
        Check if target is within weapon's firing arc.
        """
        arc = self.calculate_firing_arc(weapon, unit)

        # Calculate angle to target
        to_target = (target - unit.position).normalized()
        angle_to_target = math.atan2(to_target.y, to_target.x)

        # Normalize angles to [0, 2π]
        angle_to_target = angle_to_target % (2 * math.pi)
        arc_center = arc.center % (2 * math.pi)

        # Calculate angular difference
        diff = abs(angle_to_target - arc_center)
        if diff > math.pi:
            diff = 2 * math.pi - diff

        # Check if within arc
        return diff <= (arc.width / 2)
```

### Damage System

#### Damage Types and Effectiveness

```python
class DamageSystem:
    """
    Handles damage calculations and type effectiveness.
    """

    # Damage type effectiveness matrix
    # [attacker_type][defender_type] = multiplier
    DAMAGE_TYPE_EFFECTIVENESS = {
        DamageType.KINETIC: {
            ComponentType.ARMOR: 1.0,
            ComponentType.SHIELD: 0.5,
            ComponentType.STRUCTURE: 1.2
        },
        DamageType.ENERGY: {
            ComponentType.ARMOR: 0.8,
            ComponentType.SHIELD: 1.5,
            ComponentType.STRUCTURE: 0.9
        },
        DamageType.EXPLOSIVE: {
            ComponentType.ARMOR: 1.3,
            ComponentType.SHIELD: 0.7,
            ComponentType.STRUCTURE: 1.0
        },
        DamageType.PLASMA: {
            ComponentType.ARMOR: 1.1,
            ComponentType.SHIELD: 1.1,
            ComponentType.STRUCTURE: 1.1
        }
    }

    def calculate_damage(self, attack: Attack, target: Component) -> float:
        """
        Calculate final damage after all modifiers.
        """
        base_damage = attack.base_damage

        # Step 1: Apply armor reduction
        damage_after_armor = self._apply_armor_reduction(
            base_damage,
            target.stats.armor,
            attack.armor_penetration
        )

        # Step 2: Apply damage type effectiveness
        type_multiplier = self._get_type_effectiveness(
            attack.damage_type,
            target.type
        )
        damage_after_type = damage_after_armor * type_multiplier

        # Step 3: Apply special modifiers
        damage_after_special = self._apply_special_modifiers(
            damage_after_type,
            attack,
            target
        )

        # Step 4: Random variance (±10% for deterministic variety)
        variance = self.rng.uniform(0.9, 1.1)
        final_damage = damage_after_special * variance

        return max(1.0, final_damage)  # Minimum 1 damage

    def _apply_armor_reduction(self, damage: float, armor: float, penetration: float) -> float:
        """
        Calculate damage reduction from armor.

        Uses diminishing returns formula:
        reduction = armor / (armor + K)
        where K is a constant that determines armor effectiveness curve
        """
        K = 100.0  # Armor constant

        # Effective armor after penetration
        effective_armor = armor * (1.0 - penetration)

        # Damage reduction percentage
        reduction = effective_armor / (effective_armor + K)

        # Apply reduction
        return damage * (1.0 - reduction)

    def _apply_special_modifiers(self, damage: float, attack: Attack, target: Component) -> float:
        """
        Apply special damage modifiers (splash, critical, etc.)
        """
        modified_damage = damage

        # Critical hits
        if 'critical_chance' in attack.special_effects:
            crit_chance = attack.special_effects['critical_chance']
            crit_multiplier = attack.special_effects.get('critical_multiplier', 2.0)

            if self.rng.random() < crit_chance:
                modified_damage *= crit_multiplier
                self.event_log.log_event(CriticalHitEvent(
                    timestamp=self.time_elapsed,
                    turn=self.turn_number,
                    attacker_id=attack.attacker_id,
                    weapon_id=attack.weapon_id
                ))

        # Splash damage (affects nearby components)
        if 'splash_radius' in attack.special_effects:
            self._apply_splash_damage(attack, target, modified_damage)

        return modified_damage
```

---

## Deterministic Execution Strategy

### Principles of Determinism

The simulation must produce identical results given identical inputs. This requires:

1. **Seeded Random Number Generation**
   - All randomness uses a seeded PRNG
   - Same seed always produces same sequence
   - No external entropy sources

2. **Fixed Execution Order**
   - All operations execute in deterministic order
   - Sorted by IDs when processing multiple entities
   - No dependency on hash table iteration order

3. **Consistent Floating-Point Math**
   - Use same math libraries across platforms
   - Be aware of platform-specific differences
   - Consider using fixed-point math for critical calculations

4. **No External Dependencies**
   - No system time queries during simulation
   - No network calls
   - No file I/O during simulation loop

### Implementation

```python
class SeededRandom:
    """
    Deterministic random number generator.

    Uses Mersenne Twister algorithm (MT19937) for reproducibility.
    """

    def __init__(self, seed: int):
        """
        Initialize with seed.

        Args:
            seed: Integer seed value (0 to 2^32-1)
        """
        self.rng = random.Random(seed)
        self.seed = seed
        self.call_count = 0  # Track number of random calls for debugging

    def random(self) -> float:
        """
        Generate random float in [0.0, 1.0).
        """
        self.call_count += 1
        return self.rng.random()

    def randint(self, a: int, b: int) -> int:
        """
        Generate random integer in [a, b].
        """
        self.call_count += 1
        return self.rng.randint(a, b)

    def uniform(self, a: float, b: float) -> float:
        """
        Generate random float in [a, b].
        """
        self.call_count += 1
        return self.rng.uniform(a, b)

    def choice(self, sequence: list):
        """
        Choose random element from sequence.
        """
        self.call_count += 1
        return self.rng.choice(sequence)

    def get_state(self) -> dict:
        """
        Get current RNG state for serialization.
        """
        return {
            'seed': self.seed,
            'call_count': self.call_count,
            'state': self.rng.getstate()
        }

    def set_state(self, state: dict):
        """
        Restore RNG state from serialization.
        """
        self.seed = state['seed']
        self.call_count = state['call_count']
        self.rng.setstate(state['state'])

class DeterministicExecutor:
    """
    Ensures deterministic execution order.
    """

    @staticmethod
    def sort_entities(entities: List[Entity]) -> List[Entity]:
        """
        Sort entities deterministically by ID.
        """
        return sorted(entities, key=lambda e: e.id)

    @staticmethod
    def sort_components(components: List[Component]) -> List[Component]:
        """
        Sort components deterministically.
        """
        return sorted(components, key=lambda c: (c.unit_id, c.id))

    @staticmethod
    def process_in_order(entities: List[Entity], processor: Callable):
        """
        Process entities in deterministic order.
        """
        for entity in DeterministicExecutor.sort_entities(entities):
            processor(entity)
```

### Validation

```python
class DeterminismValidator:
    """
    Tools for validating deterministic behavior.
    """

    @staticmethod
    def run_comparison_test(config: BattleConfig, iterations: int = 10) -> bool:
        """
        Run same battle multiple times and verify identical results.

        Returns:
            True if all iterations produce identical results
        """
        results = []

        for i in range(iterations):
            simulator = BattleSimulator()
            result = simulator.simulate(config)
            results.append(result)

        # Compare all results
        reference = results[0]
        for i, result in enumerate(results[1:], 1):
            if not DeterminismValidator._results_equal(reference, result):
                print(f"Iteration {i} differs from reference!")
                return False

        return True

    @staticmethod
    def _results_equal(a: BattleResult, b: BattleResult) -> bool:
        """
        Deep comparison of battle results.
        """
        # Compare winners
        if a.winner != b.winner:
            return False

        # Compare duration
        if abs(a.duration - b.duration) > 1e-6:
            return False

        # Compare turn count
        if a.turns != b.turns:
            return False

        # Compare events
        if len(a.events) != len(b.events):
            return False

        for event_a, event_b in zip(a.events, b.events):
            if not event_a.equals(event_b):
                return False

        return True
```

---

## Event Logging System

### Event Architecture

```python
from dataclasses import dataclass
from typing import Any, Dict
from enum import Enum

class EventType(Enum):
    """All possible event types."""
    BATTLE_START = "battle_start"
    BATTLE_END = "battle_end"
    TURN_START = "turn_start"
    TURN_END = "turn_end"
    MOVEMENT = "movement"
    COLLISION = "collision"
    TARGET_ACQUIRED = "target_acquired"
    ATTACK_HIT = "attack_hit"
    ATTACK_MISS = "attack_miss"
    CRITICAL_HIT = "critical_hit"
    COMPONENT_DAMAGED = "component_damaged"
    COMPONENT_DESTROYED = "component_destroyed"
    UNIT_DESTROYED = "unit_destroyed"
    EFFECT_APPLIED = "effect_applied"
    EFFECT_EXPIRED = "effect_expired"
    TIMEOUT = "timeout"

@dataclass
class Event:
    """
    Base event class.

    All events are immutable and contain complete information
    about what happened at a specific point in time.
    """
    timestamp: float      # Simulation time
    turn: int            # Turn number
    event_type: EventType
    data: Dict[str, Any] # Event-specific data

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            'timestamp': self.timestamp,
            'turn': self.turn,
            'event_type': self.event_type.value,
            'data': self.data
        }

    @classmethod
    def from_dict(cls, d: dict) -> 'Event':
        """Deserialize from dictionary."""
        return cls(
            timestamp=d['timestamp'],
            turn=d['turn'],
            event_type=EventType(d['event_type']),
            data=d['data']
        )

class EventLogger:
    """
    Records all events during simulation.

    Features:
    - Append-only event log
    - Fast serialization
    - Query capabilities
    - Replay support
    """

    def __init__(self):
        self.events: List[Event] = []
        self.event_index: Dict[EventType, List[int]] = {}

    def log_event(self, event: Event):
        """
        Add event to log.
        """
        # Add to main log
        event_id = len(self.events)
        self.events.append(event)

        # Update index
        if event.event_type not in self.event_index:
            self.event_index[event.event_type] = []
        self.event_index[event.event_type].append(event_id)

    def get_events(self, event_type: Optional[EventType] = None) -> List[Event]:
        """
        Get events, optionally filtered by type.
        """
        if event_type is None:
            return self.events.copy()

        if event_type not in self.event_index:
            return []

        indices = self.event_index[event_type]
        return [self.events[i] for i in indices]

    def get_events_in_range(self, start_turn: int, end_turn: int) -> List[Event]:
        """
        Get events within turn range.
        """
        return [e for e in self.events if start_turn <= e.turn <= end_turn]

    def serialize(self) -> dict:
        """
        Serialize entire log to dictionary.
        """
        return {
            'events': [e.to_dict() for e in self.events],
            'count': len(self.events)
        }

    def export_json(self, filepath: str):
        """
        Export log to JSON file.
        """
        import json
        with open(filepath, 'w') as f:
            json.dump(self.serialize(), f, indent=2)

    def export_csv(self, filepath: str):
        """
        Export log to CSV file for analysis.
        """
        import csv
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Turn', 'Timestamp', 'EventType', 'Data'])

            for event in self.events:
                writer.writerow([
                    event.turn,
                    event.timestamp,
                    event.event_type.value,
                    str(event.data)
                ])
```

### Specific Event Types

```python
# Battle lifecycle events
@dataclass
class BattleStartEvent(Event):
    def __init__(self, timestamp: float, turn: int, units: List[UnitSnapshot]):
        super().__init__(
            timestamp=timestamp,
            turn=turn,
            event_type=EventType.BATTLE_START,
            data={
                'units': [u.to_dict() for u in units]
            }
        )

@dataclass
class BattleEndEvent(Event):
    def __init__(self, timestamp: float, turn: int, winner: str, statistics: dict):
        super().__init__(
            timestamp=timestamp,
            turn=turn,
            event_type=EventType.BATTLE_END,
            data={
                'winner': winner,
                'statistics': statistics
            }
        )

# Combat events
@dataclass
class AttackHitEvent(Event):
    def __init__(self, timestamp: float, turn: int, attacker_id: str,
                 weapon_id: str, target_unit_id: str, target_component_id: str,
                 damage: float, damage_type: str, old_health: float, new_health: float):
        super().__init__(
            timestamp=timestamp,
            turn=turn,
            event_type=EventType.ATTACK_HIT,
            data={
                'attacker_id': attacker_id,
                'weapon_id': weapon_id,
                'target_unit_id': target_unit_id,
                'target_component_id': target_component_id,
                'damage': damage,
                'damage_type': damage_type,
                'old_health': old_health,
                'new_health': new_health
            }
        )

# Movement events
@dataclass
class MovementEvent(Event):
    def __init__(self, timestamp: float, turn: int, unit_id: str,
                 old_position: Position, new_position: Position, distance: float):
        super().__init__(
            timestamp=timestamp,
            turn=turn,
            event_type=EventType.MOVEMENT,
            data={
                'unit_id': unit_id,
                'old_position': old_position.to_dict(),
                'new_position': new_position.to_dict(),
                'distance': distance
            }
        )
```

### Replay System

```python
class BattleReplay:
    """
    Reconstruct battle from event log.
    """

    def __init__(self, event_log: List[Event]):
        self.events = sorted(event_log, key=lambda e: (e.turn, e.timestamp))
        self.current_index = 0

    def reset(self):
        """Reset replay to beginning."""
        self.current_index = 0

    def step_forward(self) -> Optional[Event]:
        """
        Advance one event.

        Returns:
            Next event or None if at end
        """
        if self.current_index >= len(self.events):
            return None

        event = self.events[self.current_index]
        self.current_index += 1
        return event

    def step_to_turn(self, turn: int) -> List[Event]:
        """
        Advance to specific turn.

        Returns:
            All events up to and including that turn
        """
        events = []
        while self.current_index < len(self.events):
            event = self.events[self.current_index]
            if event.turn > turn:
                break
            events.append(event)
            self.current_index += 1
        return events

    def reconstruct_state_at_turn(self, turn: int, initial_state: BattleState) -> BattleState:
        """
        Reconstruct exact battle state at specific turn.

        This applies all events from beginning up to the turn.
        """
        state = initial_state.deep_copy()

        for event in self.events:
            if event.turn > turn:
                break
            self._apply_event_to_state(state, event)

        return state

    def _apply_event_to_state(self, state: BattleState, event: Event):
        """
        Apply event to state to reconstruct historical state.
        """
        if event.event_type == EventType.MOVEMENT:
            unit = state.get_unit(event.data['unit_id'])
            unit.position = Position.from_dict(event.data['new_position'])

        elif event.event_type == EventType.ATTACK_HIT:
            unit = state.get_unit(event.data['target_unit_id'])
            component = unit.get_component(event.data['target_component_id'])
            component.health = event.data['new_health']

        elif event.event_type == EventType.COMPONENT_DESTROYED:
            unit = state.get_unit(event.data['unit_id'])
            component = unit.get_component(event.data['component_id'])
            component.is_destroyed = True

        # ... handle other event types
```

---

## Win Condition Detection

### Win Conditions

```python
class WinCondition(Enum):
    """Possible win conditions."""
    ELIMINATION = "elimination"      # All enemy units destroyed
    TIMEOUT = "timeout"              # Time limit reached
    OBJECTIVE = "objective"          # Specific objective completed
    SURRENDER = "surrender"          # One side surrenders (future)

class WinConditionChecker:
    """
    Detects when battle should end and determines winner.
    """

    def __init__(self, config: BattleConfig):
        self.config = config
        self.win_conditions = config.win_conditions

    def check_win_conditions(self, state: BattleState) -> Optional[WinResult]:
        """
        Check all enabled win conditions.

        Returns:
            WinResult if battle is over, None otherwise
        """
        # Check elimination (most common)
        if WinCondition.ELIMINATION in self.win_conditions:
            result = self._check_elimination(state)
            if result is not None:
                return result

        # Check timeout
        if WinCondition.TIMEOUT in self.win_conditions:
            result = self._check_timeout(state)
            if result is not None:
                return result

        # Check objectives
        if WinCondition.OBJECTIVE in self.win_conditions:
            result = self._check_objectives(state)
            if result is not None:
                return result

        return None

    def _check_elimination(self, state: BattleState) -> Optional[WinResult]:
        """
        Check if one side has been eliminated.
        """
        active_teams = set()

        for unit in state.units:
            if unit.is_active:
                active_teams.add(unit.team)

        if len(active_teams) == 0:
            # Both sides destroyed simultaneously (rare but possible)
            return WinResult(
                winner=None,
                condition=WinCondition.ELIMINATION,
                reason="Mutual destruction"
            )

        if len(active_teams) == 1:
            # One team remains
            winner = list(active_teams)[0]
            return WinResult(
                winner=winner,
                condition=WinCondition.ELIMINATION,
                reason=f"All enemy units destroyed"
            )

        return None

    def _check_timeout(self, state: BattleState) -> Optional[WinResult]:
        """
        Check if time/turn limit exceeded.
        """
        if state.turn >= self.config.max_turns:
            # Determine winner by remaining health/units
            winner = self._determine_winner_by_health(state)
            return WinResult(
                winner=winner,
                condition=WinCondition.TIMEOUT,
                reason=f"Turn limit ({self.config.max_turns}) reached"
            )

        if state.time_elapsed >= self.config.max_time:
            winner = self._determine_winner_by_health(state)
            return WinResult(
                winner=winner,
                condition=WinCondition.TIMEOUT,
                reason=f"Time limit ({self.config.max_time}s) reached"
            )

        return None

    def _determine_winner_by_health(self, state: BattleState) -> Optional[str]:
        """
        Determine winner based on remaining health when timeout occurs.
        """
        team_health = {}

        for unit in state.units:
            if unit.team not in team_health:
                team_health[unit.team] = 0
            team_health[unit.team] += unit.calculate_total_health()

        if not team_health:
            return None

        # Team with most health wins
        winner = max(team_health.items(), key=lambda x: x[1])[0]
        return winner

    def _check_objectives(self, state: BattleState) -> Optional[WinResult]:
        """
        Check objective-based win conditions (future expansion).

        Examples:
        - Destroy specific unit/component
        - Reach specific location
        - Survive for duration
        - Protect target
        """
        # Future implementation
        return None

@dataclass
class WinResult:
    """Result of win condition check."""
    winner: Optional[str]  # Team ID or None for draw
    condition: WinCondition
    reason: str

    def is_draw(self) -> bool:
        return self.winner is None
```

---

## State Management

### Battle State

```python
@dataclass
class BattleState:
    """
    Complete battle state at a point in time.

    This is the single source of truth for all simulation state.
    """
    # Core state
    units: List[Unit]
    turn: int
    time_elapsed: float

    # Configuration
    config: BattleConfig
    battlefield: Battlefield

    # Derived state (cached for performance)
    _active_units_cache: Optional[List[Unit]] = None
    _spatial_index: Optional[SpatialIndex] = None

    def get_active_units(self) -> List[Unit]:
        """Get all active (not destroyed) units."""
        if self._active_units_cache is None:
            self._active_units_cache = [u for u in self.units if u.is_active]
        return self._active_units_cache

    def get_unit(self, unit_id: str) -> Optional[Unit]:
        """Get unit by ID."""
        for unit in self.units:
            if unit.id == unit_id:
                return unit
        return None

    def get_units_by_team(self, team: str) -> List[Unit]:
        """Get all units on a team."""
        return [u for u in self.units if u.team == team]

    def get_enemy_units(self, unit: Unit) -> List[Unit]:
        """Get all enemy units."""
        return [u for u in self.get_active_units() if u.team != unit.team]

    def invalidate_cache(self):
        """Invalidate cached derived state."""
        self._active_units_cache = None
        self._spatial_index = None

    def snapshot(self) -> dict:
        """
        Create a complete snapshot of current state.

        Used for:
        - Saving state at key points
        - Exporting final state
        - Debugging
        """
        return {
            'turn': self.turn,
            'time_elapsed': self.time_elapsed,
            'units': [u.to_dict() for u in self.units],
            'battlefield': self.battlefield.to_dict()
        }

    def deep_copy(self) -> 'BattleState':
        """Create deep copy of entire state."""
        import copy
        return copy.deepcopy(self)

@dataclass
class Unit:
    """
    A combat unit (composed of components).
    """
    id: str
    team: str
    name: str

    # Physical state
    position: Position
    facing: float  # Radians
    velocity: Vector2D

    # Components
    components: List[Component]

    # Status
    is_active: bool = True

    # Behavior
    movement_behavior: MovementBehavior = MovementBehavior.AGGRESSIVE

    def get_component(self, component_id: str) -> Optional[Component]:
        """Get component by ID."""
        for component in self.components:
            if component.id == component_id:
                return component
        return None

    def get_components_by_type(self, component_type: ComponentType) -> List[Component]:
        """Get all components of a type."""
        return [c for c in self.components if c.type == component_type]

    def is_destroyed(self) -> bool:
        """Check if unit is destroyed (critical components gone)."""
        # Unit is destroyed if it has no functional core components
        cores = self.get_components_by_type(ComponentType.CORE)
        return all(c.is_destroyed for c in cores)

    def calculate_total_health(self) -> float:
        """Calculate sum of all component health."""
        return sum(c.health for c in self.components if not c.is_destroyed)

    def calculate_mass(self) -> float:
        """Calculate total unit mass."""
        return sum(c.stats.weight for c in self.components)

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            'id': self.id,
            'team': self.team,
            'name': self.name,
            'position': self.position.to_dict(),
            'facing': self.facing,
            'velocity': self.velocity.to_dict(),
            'components': [c.to_dict() for c in self.components],
            'is_active': self.is_active
        }

@dataclass
class Component:
    """
    A component attached to a unit.
    """
    id: str
    unit_id: str
    name: str
    type: ComponentType

    # Stats
    stats: ComponentStats

    # State
    health: float
    max_health: float
    is_destroyed: bool = False

    # Position relative to unit
    relative_position: Vector2D
    facing: float  # Relative to unit facing

    # Combat state (for weapons)
    current_target: Optional[Target] = None
    last_fire_time: float = 0.0

    # Active effects
    active_effects: List[Effect] = field(default_factory=list)

    def is_functional(self) -> bool:
        """Check if component can function."""
        if self.is_destroyed:
            return False
        # Component at less than 10% health is non-functional
        return (self.health / self.max_health) >= 0.1

    def can_fire(self, current_time: float) -> bool:
        """Check if weapon can fire."""
        if not self.is_functional():
            return False
        cooldown = self.stats.fire_rate
        return (current_time - self.last_fire_time) >= cooldown

    def get_world_position(self) -> Position:
        """Get absolute world position of component."""
        # This would need the unit reference to calculate
        # Simplified for pseudocode
        pass

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type.value,
            'health': self.health,
            'max_health': self.max_health,
            'is_destroyed': self.is_destroyed,
            'stats': self.stats.to_dict()
        }
```

### State Transitions

```python
class StateManager:
    """
    Manages state transitions and ensures consistency.
    """

    def __init__(self, state: BattleState):
        self.state = state
        self.state_history: List[BattleState] = []
        self.checkpoint_interval = 10  # Save state every N turns

    def begin_turn(self):
        """Prepare state for new turn."""
        self.state.turn += 1
        self.state.invalidate_cache()

        # Create checkpoint if needed
        if self.state.turn % self.checkpoint_interval == 0:
            self.create_checkpoint()

    def end_turn(self):
        """Finalize turn."""
        self.state.time_elapsed += self.state.config.time_step

    def create_checkpoint(self):
        """Save current state as checkpoint."""
        checkpoint = self.state.deep_copy()
        self.state_history.append(checkpoint)

    def rollback_to_checkpoint(self, turn: int) -> bool:
        """
        Rollback to previous checkpoint (for debugging).

        Returns:
            True if rollback successful
        """
        for checkpoint in reversed(self.state_history):
            if checkpoint.turn == turn:
                self.state = checkpoint.deep_copy()
                return True
        return False

    def apply_damage(self, component: Component, damage: float) -> float:
        """
        Apply damage to component with validation.

        Returns:
            Actual damage dealt
        """
        if component.is_destroyed:
            return 0.0

        old_health = component.health
        component.health = max(0.0, component.health - damage)
        actual_damage = old_health - component.health

        if component.health == 0.0:
            component.is_destroyed = True

        # Invalidate cache since state changed
        self.state.invalidate_cache()

        return actual_damage

    def destroy_component(self, component: Component):
        """Mark component as destroyed."""
        component.is_destroyed = True
        component.health = 0.0
        self.state.invalidate_cache()

    def destroy_unit(self, unit: Unit):
        """Mark unit as destroyed."""
        unit.is_active = False
        for component in unit.components:
            self.destroy_component(component)
        self.state.invalidate_cache()
```

---

## Performance Considerations

### Optimization Strategies

#### 1. Spatial Indexing

```python
class SpatialIndex:
    """
    Spatial index for fast proximity queries.

    Uses grid-based spatial hashing for O(1) average-case queries.
    """

    def __init__(self, battlefield: Battlefield, cell_size: float = 50.0):
        self.battlefield = battlefield
        self.cell_size = cell_size
        self.grid: Dict[Tuple[int, int], List[Unit]] = {}

    def build(self, units: List[Unit]):
        """Build index from units."""
        self.grid.clear()

        for unit in units:
            if not unit.is_active:
                continue

            cell = self._get_cell(unit.position)
            if cell not in self.grid:
                self.grid[cell] = []
            self.grid[cell].append(unit)

    def find_nearby_units(self, position: Position, radius: float) -> List[Unit]:
        """
        Find all units within radius of position.

        Much faster than checking all units.
        """
        nearby = []

        # Calculate which cells to check
        cell_radius = int(math.ceil(radius / self.cell_size))
        center_cell = self._get_cell(position)

        # Check all cells in range
        for dx in range(-cell_radius, cell_radius + 1):
            for dy in range(-cell_radius, cell_radius + 1):
                cell = (center_cell[0] + dx, center_cell[1] + dy)

                if cell not in self.grid:
                    continue

                # Check units in cell
                for unit in self.grid[cell]:
                    distance = position.distance_to(unit.position)
                    if distance <= radius:
                        nearby.append(unit)

        return nearby

    def _get_cell(self, position: Position) -> Tuple[int, int]:
        """Get grid cell for position."""
        x = int(position.x / self.cell_size)
        y = int(position.y / self.cell_size)
        return (x, y)
```

#### 2. Caching

```python
class PerformanceCache:
    """
    Cache expensive calculations within a turn.

    Invalidated at end of each turn.
    """

    def __init__(self):
        self.range_cache: Dict[Tuple[str, str], float] = {}
        self.los_cache: Dict[Tuple[Position, Position], bool] = {}
        self.target_cache: Dict[str, List[Target]] = {}

    def get_distance(self, unit1_id: str, unit2_id: str,
                     calculator: Callable) -> float:
        """
        Get cached distance or calculate and cache.
        """
        # Cache key is sorted to handle (A,B) and (B,A) as same
        key = tuple(sorted([unit1_id, unit2_id]))

        if key not in self.range_cache:
            self.range_cache[key] = calculator()

        return self.range_cache[key]

    def clear(self):
        """Clear all caches."""
        self.range_cache.clear()
        self.los_cache.clear()
        self.target_cache.clear()
```

#### 3. Early Termination

```python
class EarlyTermination:
    """
    Strategies for ending simulation early when outcome is clear.
    """

    @staticmethod
    def is_outcome_certain(state: BattleState) -> Optional[str]:
        """
        Check if outcome is mathematically certain.

        Returns:
            Winner ID if outcome certain, None otherwise
        """
        teams = {}

        for unit in state.get_active_units():
            if unit.team not in teams:
                teams[unit.team] = {'health': 0, 'damage': 0}

            teams[unit.team]['health'] += unit.calculate_total_health()
            teams[unit.team]['damage'] += unit.calculate_damage_potential()

        if len(teams) != 2:
            return None

        team_list = list(teams.items())
        team1, stats1 = team_list[0]
        team2, stats2 = team_list[1]

        # If one team can't possibly kill the other
        if stats1['damage'] == 0 and stats2['health'] > 0:
            return team2
        if stats2['damage'] == 0 and stats1['health'] > 0:
            return team1

        return None
```

### Performance Targets

| Metric | Target | Notes |
|--------|--------|-------|
| Turn execution | < 10ms | For typical battle (2 units, 10 components each) |
| Full simulation | < 1s | For typical battle (< 1000 turns) |
| Event log size | < 10MB | For typical battle |
| Memory usage | < 100MB | Peak during simulation |
| Startup time | < 100ms | Load config and initialize |

### Profiling Points

```python
class PerformanceProfiler:
    """
    Track performance metrics during simulation.
    """

    def __init__(self):
        self.timings: Dict[str, List[float]] = {}
        self.counts: Dict[str, int] = {}

    @contextmanager
    def measure(self, operation: str):
        """
        Context manager for timing operations.

        Usage:
            with profiler.measure('movement_phase'):
                process_movement()
        """
        start = time.perf_counter()
        yield
        elapsed = time.perf_counter() - start

        if operation not in self.timings:
            self.timings[operation] = []
        self.timings[operation].append(elapsed)

    def increment(self, counter: str):
        """Increment a counter."""
        if counter not in self.counts:
            self.counts[counter] = 0
        self.counts[counter] += 1

    def report(self) -> dict:
        """Generate performance report."""
        report = {}

        for operation, times in self.timings.items():
            report[operation] = {
                'total': sum(times),
                'average': sum(times) / len(times),
                'min': min(times),
                'max': max(times),
                'count': len(times)
            }

        report['counts'] = self.counts
        return report
```

---

## Data Structures

### Core Types

```python
from dataclasses import dataclass
from typing import Tuple
import math

@dataclass
class Vector2D:
    """2D vector for velocity and direction."""
    x: float
    y: float

    def magnitude(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)

    def normalized(self) -> 'Vector2D':
        mag = self.magnitude()
        if mag == 0:
            return Vector2D(0, 0)
        return Vector2D(self.x / mag, self.y / mag)

    def dot(self, other: 'Vector2D') -> float:
        return self.x * other.x + self.y * other.y

    def __add__(self, other: 'Vector2D') -> 'Vector2D':
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Vector2D') -> 'Vector2D':
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> 'Vector2D':
        return Vector2D(self.x * scalar, self.y * scalar)

    def __neg__(self) -> 'Vector2D':
        return Vector2D(-self.x, -self.y)

    @staticmethod
    def zero() -> 'Vector2D':
        return Vector2D(0, 0)

    def to_dict(self) -> dict:
        return {'x': self.x, 'y': self.y}

@dataclass
class Position:
    """2D position in battlefield."""
    x: float
    y: float

    def distance_to(self, other: 'Position') -> float:
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx**2 + dy**2)

    def __add__(self, vector: Vector2D) -> 'Position':
        return Position(self.x + vector.x, self.y + vector.y)

    def __sub__(self, other: 'Position') -> Vector2D:
        return Vector2D(self.x - other.x, self.y - other.y)

    def to_dict(self) -> dict:
        return {'x': self.x, 'y': self.y}

    @classmethod
    def from_dict(cls, d: dict) -> 'Position':
        return cls(d['x'], d['y'])

@dataclass
class Battlefield:
    """Battlefield dimensions and properties."""
    width: float
    height: float

    def is_in_bounds(self, position: Position) -> bool:
        return (0 <= position.x <= self.width and
                0 <= position.y <= self.height)

    def clamp(self, position: Position) -> Position:
        """Clamp position to battlefield bounds."""
        x = max(0, min(self.width, position.x))
        y = max(0, min(self.height, position.y))
        return Position(x, y)

    def to_dict(self) -> dict:
        return {'width': self.width, 'height': self.height}
```

### Configuration Structures

```python
@dataclass
class BattleConfig:
    """Configuration for a battle simulation."""
    # Battle parameters
    seed: int
    max_turns: int = 1000
    max_time: float = 100.0  # seconds
    time_step: float = 0.1   # seconds per turn

    # Win conditions
    win_conditions: List[WinCondition] = field(default_factory=lambda: [WinCondition.ELIMINATION])

    # Battlefield
    battlefield: Battlefield = field(default_factory=lambda: Battlefield(1000, 1000))

    # Simulation parameters
    enable_fog_of_war: bool = False
    enable_friendly_fire: bool = False

    def to_dict(self) -> dict:
        return {
            'seed': self.seed,
            'max_turns': self.max_turns,
            'max_time': self.max_time,
            'time_step': self.time_step,
            'win_conditions': [wc.value for wc in self.win_conditions],
            'battlefield': self.battlefield.to_dict()
        }

@dataclass
class ComponentStats:
    """Statistics for a component."""
    # Combat stats
    damage: float = 0.0
    range: float = 0.0
    fire_rate: float = 1.0
    accuracy: float = 0.85
    armor: float = 0.0

    # Physical stats
    weight: float = 100.0
    power_draw: float = 0.0

    # Mobility stats (for engines)
    thrust: float = 0.0
    torque: float = 0.0

    # Special
    firing_arc: float = 360.0  # degrees

    def to_dict(self) -> dict:
        return {
            'damage': self.damage,
            'range': self.range,
            'fire_rate': self.fire_rate,
            'accuracy': self.accuracy,
            'armor': self.armor,
            'weight': self.weight,
            'thrust': self.thrust
        }
```

---

## API Design

### Public API

```python
class BattleSimulator:
    """
    Main entry point for battle simulation.

    This is the public API that clients use.
    """

    def __init__(self, config: BattleConfig):
        """
        Initialize simulator with configuration.

        Args:
            config: Battle configuration
        """
        self.config = config
        self.engine = None

    def load_units(self, units: List[UnitDefinition]):
        """
        Load units into battle.

        Args:
            units: List of unit definitions
        """
        self.units = [Unit.from_definition(u) for u in units]

    def simulate(self) -> BattleResult:
        """
        Run complete simulation.

        Returns:
            Battle result with winner, events, and statistics

        Example:
            simulator = BattleSimulator(config)
            simulator.load_units([unit1, unit2])
            result = simulator.simulate()
            print(f"Winner: {result.winner}")
        """
        # Initialize engine
        self.engine = SimulationEngine(self.config)
        state = self.engine.initialize_battle(self.units)

        # Run simulation
        result = self.engine.simulate()

        return result

    def simulate_step_by_step(self) -> Iterator[SimulationStep]:
        """
        Run simulation step-by-step for visualization.

        Yields:
            SimulationStep for each turn

        Example:
            for step in simulator.simulate_step_by_step():
                visualize(step.state)
                if step.is_finished:
                    break
        """
        self.engine = SimulationEngine(self.config)
        state = self.engine.initialize_battle(self.units)

        while not self.engine.is_finished():
            self.engine.execute_turn()

            yield SimulationStep(
                turn=self.engine.turn_number,
                time=self.engine.time_elapsed,
                state=state.snapshot(),
                events=self.engine.event_log.get_events_in_range(
                    self.engine.turn_number,
                    self.engine.turn_number
                ),
                is_finished=self.engine.is_finished()
            )

        # Final step with result
        yield SimulationStep(
            turn=self.engine.turn_number,
            time=self.engine.time_elapsed,
            state=state.snapshot(),
            events=[],
            is_finished=True,
            result=self.engine.get_result()
        )

@dataclass
class BattleResult:
    """Result of a battle simulation."""
    winner: Optional[str]
    duration: float
    turns: int
    events: List[Event]
    final_state: dict
    statistics: dict

    def to_dict(self) -> dict:
        return {
            'winner': self.winner,
            'duration': self.duration,
            'turns': self.turns,
            'events': [e.to_dict() for e in self.events],
            'final_state': self.final_state,
            'statistics': self.statistics
        }

    def save(self, filepath: str):
        """Save result to file."""
        import json
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
```

### Usage Examples

```python
# Example 1: Simple battle
config = BattleConfig(seed=42)
simulator = BattleSimulator(config)

# Load units from definitions
unit1 = load_unit_from_file("units/fighter.yaml")
unit2 = load_unit_from_file("units/tank.yaml")
simulator.load_units([unit1, unit2])

# Run simulation
result = simulator.simulate()
print(f"Winner: {result.winner}")
print(f"Duration: {result.duration}s in {result.turns} turns")

# Save results
result.save("battle_results.json")

# Example 2: Step-by-step with visualization
for step in simulator.simulate_step_by_step():
    print(f"Turn {step.turn}: {len(step.events)} events")

    # Visualize current state
    visualizer.render(step.state)

    if step.is_finished:
        print(f"Battle over! Winner: {step.result.winner}")
        break

# Example 3: Replay from saved results
replay = BattleReplay.load("battle_results.json")
for event in replay:
    print(f"[{event.turn}] {event.event_type}: {event.data}")
```

---

## Summary

This architecture provides:

1. **Deterministic Simulation**: Seeded RNG, fixed execution order, reproducible results
2. **Comprehensive Combat**: Movement, targeting, damage calculation with modifiers
3. **Complete Observability**: Event logging for every action, perfect replay capability
4. **Extensibility**: Data-driven design, clear interfaces, modular systems
5. **Performance**: Spatial indexing, caching, early termination strategies

The design supports the project vision of a theme-agnostic battle automata engine with deterministic, observable, and replayable combat simulations.

### Next Steps

1. **Implementation Priority**:
   - Core data structures (Position, Vector2D, Component, Unit)
   - SimulationEngine with basic loop
   - Movement system
   - Targeting system
   - Damage system
   - Event logging
   - Win condition detection

2. **Testing Strategy**:
   - Unit tests for each system
   - Determinism validation tests
   - Integration tests for full simulation
   - Performance benchmarks

3. **Documentation**:
   - API documentation
   - Component creation guide
   - Battle configuration guide
   - Replay format specification

---

**End of Specification**
