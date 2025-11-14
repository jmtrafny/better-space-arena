"""Core simulation engine - turn execution and win condition checking."""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass

from .state import BattleState, UnitState, ComponentState, Position, Vector2D
from .events import EventLogger, EventType, Event
from .rng import SeededRandom
from ..mechanics.combat import DamageSystem, Attack, DamageType
from ..mechanics.targeting import TargetingSystem, TargetingPriority, Target
from ..mechanics.movement import MovementSystem, MovementBehavior


@dataclass
class SimulationConfig:
    """Configuration for simulation execution."""

    time_step: float = 0.1  # seconds per turn
    max_turns: int = 3000
    max_duration: float = 300.0  # seconds

    # Default unit parameters (simplified for MVP)
    default_max_speed: float = 10.0  # m/s
    default_weapon_range: float = 100.0  # meters
    default_weapon_damage: float = 50.0
    default_weapon_accuracy: float = 0.85
    default_weapon_fire_rate: float = 1.0  # seconds

    default_component_health: float = 100.0


class SimulationEngine:
    """
    Core simulation loop executor.

    Manages turn-based execution with deterministic behavior:
    1. Movement Phase
    2. Targeting Phase
    3. Combat Phase
    4. Cleanup/Update Phase
    5. Win Condition Check
    """

    def __init__(
        self,
        state: BattleState,
        config: SimulationConfig,
        event_logger: EventLogger
    ):
        """
        Initialize simulation engine.

        Args:
            state: Initial battle state
            config: Simulation configuration
            event_logger: Event logger for recording
        """
        self.state = state
        self.config = config
        self.event_log = event_logger

        # Initialize subsystems
        self.rng = SeededRandom(state.seed)
        self.damage_system = DamageSystem(self.rng)
        self.targeting_system = TargetingSystem()
        self.movement_system = MovementSystem(state.battlefield)

    def execute_turn(self) -> None:
        """Execute one complete simulation turn."""
        self.state.turn += 1
        turn_start_time = self.state.time_elapsed

        # Log turn start
        self.event_log.log(
            timestamp=turn_start_time,
            turn=self.state.turn,
            event_type=EventType.TURN_START
        )

        # PHASE 1: MOVEMENT
        self._process_movement_phase()

        # PHASE 2: TARGETING
        self._process_targeting_phase()

        # PHASE 3: COMBAT
        self._process_combat_phase()

        # PHASE 4: CLEANUP
        self._cleanup_phase()

        # Update elapsed time
        self.state.time_elapsed += self.config.time_step

        # Log turn end
        self.event_log.log(
            timestamp=self.state.time_elapsed,
            turn=self.state.turn,
            event_type=EventType.TURN_END
        )

        # Invalidate caches
        self.state.invalidate_cache()

    def _process_movement_phase(self) -> None:
        """Process movement for all units."""
        # Get all active units in deterministic order
        units = sorted(
            self.state.get_active_units(),
            key=lambda u: u.unit_id
        )

        for unit in units:
            # Find nearest enemy
            enemies = self.state.get_enemy_units(unit)
            if not enemies:
                continue

            nearest_enemy = min(
                enemies,
                key=lambda e: unit.position.distance_to(e.position)
            )

            # Calculate desired movement
            # For MVP, use simple aggressive behavior
            behavior = MovementBehavior.AGGRESSIVE
            velocity = self.movement_system.calculate_movement(
                unit=unit,
                nearest_enemy=nearest_enemy,
                behavior=behavior,
                max_speed=self.config.default_max_speed,
                time_step=self.config.time_step
            )

            if velocity.magnitude() == 0:
                continue

            # Calculate new position
            old_position = unit.position
            new_position = self.movement_system.apply_movement(
                unit=unit,
                velocity=velocity,
                time_step=self.config.time_step
            )

            # Check for collisions
            other_units = [u for u in units if u.unit_id != unit.unit_id]
            if self.movement_system.check_collision(unit, new_position, other_units):
                # Log collision
                self.event_log.log(
                    timestamp=self.state.time_elapsed,
                    turn=self.state.turn,
                    event_type=EventType.COLLISION,
                    unit_id=unit.unit_id,
                    attempted_position={'x': new_position.x, 'y': new_position.y}
                )
                continue

            # Apply movement
            distance = old_position.distance_to(new_position)
            unit.position = new_position
            unit.velocity = velocity

            # Log movement
            if distance > 0.01:  # Only log meaningful movement
                self.event_log.log(
                    timestamp=self.state.time_elapsed,
                    turn=self.state.turn,
                    event_type=EventType.MOVEMENT,
                    unit_id=unit.unit_id,
                    old_position=old_position.to_dict(),
                    new_position=new_position.to_dict(),
                    distance=distance
                )

    def _process_targeting_phase(self) -> None:
        """Process targeting for all weapons."""
        units = sorted(
            self.state.get_active_units(),
            key=lambda u: u.unit_id
        )

        for unit in units:
            enemies = self.state.get_enemy_units(unit)
            if not enemies:
                continue

            # For each component that can attack
            for comp_state in sorted(
                unit.component_states,
                key=lambda c: c.component_id
            ):
                if comp_state.is_destroyed:
                    continue

                # Check if weapon can fire
                if comp_state.cooldown_remaining > 0:
                    comp_state.cooldown_remaining -= self.config.time_step
                    continue

                # Find valid targets
                targets = self.targeting_system.find_targets_for_weapon(
                    attacker=unit,
                    weapon_range=self.config.default_weapon_range,
                    enemies=enemies
                )

                if not targets:
                    continue

                # Select best target
                target = self.targeting_system.select_target(
                    targets=targets,
                    priority=TargetingPriority.CLOSEST,
                    attacker_pos=unit.position
                )

                if target:
                    comp_state.current_target_id = f"{target.unit_id}:{target.component_id}"

                    # Log targeting
                    self.event_log.log(
                        timestamp=self.state.time_elapsed,
                        turn=self.state.turn,
                        event_type=EventType.TARGET_ACQUIRED,
                        unit_id=unit.unit_id,
                        weapon_id=comp_state.component_id,
                        target_unit_id=target.unit_id,
                        target_component_id=target.component_id,
                        range=unit.position.distance_to(target.position)
                    )

    def _process_combat_phase(self) -> None:
        """Process all weapon attacks."""
        units = sorted(
            self.state.get_active_units(),
            key=lambda u: u.unit_id
        )

        for unit in units:
            for comp_state in sorted(
                unit.component_states,
                key=lambda c: c.component_id
            ):
                if comp_state.is_destroyed:
                    continue

                if not comp_state.current_target_id:
                    continue

                # Parse target ID
                try:
                    target_unit_id, target_comp_id = comp_state.current_target_id.split(':')
                except ValueError:
                    continue

                # Get target
                target_unit = self.state.get_unit(target_unit_id)
                if not target_unit or not target_unit.is_active:
                    comp_state.current_target_id = None
                    continue

                target_comp = target_unit.get_component_state(target_comp_id)
                if not target_comp or target_comp.is_destroyed:
                    comp_state.current_target_id = None
                    continue

                # Create attack
                attack = Attack(
                    attacker_id=unit.unit_id,
                    weapon_id=comp_state.component_id,
                    target_unit_id=target_unit_id,
                    target_component_id=target_comp_id,
                    base_damage=self.config.default_weapon_damage,
                    damage_type=DamageType.ENERGY,  # Default for MVP
                    range_to_target=unit.position.distance_to(target_unit.position),
                    accuracy=self.config.default_weapon_accuracy
                )

                # Log weapon fired
                self.event_log.log(
                    timestamp=self.state.time_elapsed,
                    turn=self.state.turn,
                    event_type=EventType.WEAPON_FIRED,
                    attacker_id=unit.unit_id,
                    weapon_id=comp_state.component_id,
                    target_unit_id=target_unit_id,
                    target_component_id=target_comp_id
                )

                # Process attack
                result = self.damage_system.apply_damage(attack, target_comp)

                if not result['hit']:
                    # Log miss
                    self.event_log.log(
                        timestamp=self.state.time_elapsed,
                        turn=self.state.turn,
                        event_type=EventType.ATTACK_MISS,
                        attacker_id=unit.unit_id,
                        weapon_id=comp_state.component_id,
                        target_unit_id=target_unit_id
                    )
                else:
                    # Log hit
                    self.event_log.log(
                        timestamp=self.state.time_elapsed,
                        turn=self.state.turn,
                        event_type=EventType.ATTACK_HIT,
                        attacker_id=unit.unit_id,
                        weapon_id=comp_state.component_id,
                        target_unit_id=target_unit_id,
                        target_component_id=target_comp_id,
                        damage=result['damage'],
                        old_health=result['old_health'],
                        new_health=result['new_health'],
                        critical=result['critical']
                    )

                    if result['critical']:
                        self.event_log.log(
                            timestamp=self.state.time_elapsed,
                            turn=self.state.turn,
                            event_type=EventType.CRITICAL_HIT,
                            attacker_id=unit.unit_id,
                            weapon_id=comp_state.component_id,
                            target_unit_id=target_unit_id
                        )

                    # Check if component destroyed
                    if target_comp.is_destroyed:
                        self.event_log.log(
                            timestamp=self.state.time_elapsed,
                            turn=self.state.turn,
                            event_type=EventType.COMPONENT_DESTROYED,
                            unit_id=target_unit_id,
                            component_id=target_comp_id
                        )

                        # Check if unit destroyed
                        if target_unit.is_destroyed():
                            target_unit.is_active = False
                            self.event_log.log(
                                timestamp=self.state.time_elapsed,
                                turn=self.state.turn,
                                event_type=EventType.UNIT_DESTROYED,
                                unit_id=target_unit_id,
                                final_position=target_unit.position.to_dict()
                            )

                # Set weapon cooldown
                comp_state.cooldown_remaining = self.config.default_weapon_fire_rate
                comp_state.current_target_id = None

    def _cleanup_phase(self) -> None:
        """Clean up and prepare for next turn."""
        # Remove inactive units (already handled in combat phase)
        # Update any time-based effects
        # Future: Process effects, regeneration, etc.
        pass

    def check_win_conditions(self) -> Optional[str]:
        """
        Check if battle should end and determine winner.

        Returns:
            Winner team ID or None if battle continues
        """
        # Check elimination
        active_teams = set()
        for unit in self.state.units:
            if unit.is_active and not unit.is_destroyed():
                active_teams.add(unit.team)

        if len(active_teams) == 0:
            # Both sides destroyed simultaneously (rare)
            self.state.outcome = "draw"
            self.state.winner = None
            return None

        if len(active_teams) == 1:
            # One team remains
            winner = list(active_teams)[0]
            self.state.outcome = "elimination"
            self.state.winner = winner
            return winner

        # Check timeout
        if self.state.turn >= self.config.max_turns:
            self.state.outcome = "timeout"
            winner = self._determine_winner_by_health()
            self.state.winner = winner
            return winner

        if self.state.time_elapsed >= self.config.max_duration:
            self.state.outcome = "timeout"
            winner = self._determine_winner_by_health()
            self.state.winner = winner
            return winner

        return None

    def _determine_winner_by_health(self) -> Optional[str]:
        """
        Determine winner based on remaining health when timeout occurs.

        Returns:
            Team ID with most health or None for draw
        """
        team_health: Dict[str, float] = {}

        for unit in self.state.units:
            if unit.team not in team_health:
                team_health[unit.team] = 0
            team_health[unit.team] += unit.get_total_health()

        if not team_health:
            return None

        # Team with most health wins
        winner = max(team_health.items(), key=lambda x: x[1])[0]
        return winner

    def is_finished(self) -> bool:
        """
        Check if battle is over.

        Returns:
            True if battle has ended
        """
        return self.state.winner is not None
