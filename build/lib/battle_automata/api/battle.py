"""Public Battle API - main entry point for simulations."""

from dataclasses import dataclass, field
from typing import Optional, Iterator, Dict, Any, List
import json

from ..core.state import (
    BattleState, UnitState, ComponentState,
    Position, Vector2D, Battlefield
)
from ..core.events import EventLogger, Event, EventType
from ..core.simulation import SimulationEngine, SimulationConfig


@dataclass
class BattleConfig:
    """
    Configuration for battle simulation.

    Defines all parameters for running a battle.
    """

    # Random seed for determinism
    seed: int

    # Time parameters
    time_step: float = 0.1  # seconds per turn
    max_duration: float = 300.0  # seconds
    max_turns: int = 3000

    # Arena
    arena_width: float = 1000.0
    arena_height: float = 1000.0

    # Starting positions
    unit1_position: tuple[float, float] = (100.0, 500.0)
    unit2_position: tuple[float, float] = (900.0, 500.0)

    # Win conditions
    timeout_is_draw: bool = False  # If False, most health wins on timeout


@dataclass
class BattleStatistics:
    """Battle statistics and metrics."""

    winner: Optional[str]
    outcome_reason: str  # "elimination", "timeout", "draw"
    total_turns: int
    total_time: float

    # Per-unit stats
    unit_stats: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    # Combat stats
    total_shots_fired: int = 0
    total_hits: int = 0
    total_misses: int = 0
    total_critical_hits: int = 0

    def get_accuracy(self) -> float:
        """Calculate overall accuracy."""
        if self.total_shots_fired == 0:
            return 0.0
        return self.total_hits / self.total_shots_fired


@dataclass
class BattleResult:
    """
    Complete battle result.

    Contains winner, events, statistics, and final state.
    """

    config: BattleConfig
    statistics: BattleStatistics
    events: List[Event]
    final_state: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON export."""
        return {
            'config': {
                'seed': self.config.seed,
                'time_step': self.config.time_step,
                'max_duration': self.config.max_duration,
                'arena_width': self.config.arena_width,
                'arena_height': self.config.arena_height,
            },
            'statistics': {
                'winner': self.statistics.winner,
                'outcome_reason': self.statistics.outcome_reason,
                'total_turns': self.statistics.total_turns,
                'total_time': self.statistics.total_time,
                'accuracy': self.statistics.get_accuracy(),
                'total_shots_fired': self.statistics.total_shots_fired,
                'total_hits': self.statistics.total_hits,
                'total_misses': self.statistics.total_misses,
                'total_critical_hits': self.statistics.total_critical_hits,
            },
            'events': [e.to_dict() for e in self.events],
            'final_state': self.final_state,
        }

    def save(self, filepath: str) -> None:
        """Save result to JSON file."""
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    def get_winner_name(self) -> Optional[str]:
        """Get name of winning team."""
        return self.statistics.winner

    def print_summary(self) -> str:
        """Generate human-readable summary."""
        winner = self.get_winner_name() or "DRAW"

        summary = f"""
=== Battle Result ===
Winner: {winner}
Reason: {self.statistics.outcome_reason}

Duration: {self.statistics.total_time:.1f}s ({self.statistics.total_turns} turns)
Accuracy: {self.statistics.get_accuracy():.1%}

Combat Stats:
  Shots Fired: {self.statistics.total_shots_fired}
  Hits: {self.statistics.total_hits}
  Misses: {self.statistics.total_misses}
  Critical Hits: {self.statistics.total_critical_hits}
"""
        return summary


@dataclass
class BattleStep:
    """Single step in step-by-step simulation."""

    turn: int
    time: float
    state: Dict[str, Any]
    events: List[Event]
    is_finished: bool
    result: Optional[BattleResult] = None


class Battle:
    """
    A battle between units.

    Main entry point for battle simulation.

    Example:
        >>> config = BattleConfig(seed=42)
        >>> battle = Battle(config)
        >>> result = battle.simulate()
        >>> print(f"Winner: {result.statistics.winner}")
    """

    def __init__(self, config: Optional[BattleConfig] = None):
        """
        Initialize battle.

        Args:
            config: Battle configuration (uses default if None)
        """
        self.config = config or BattleConfig(seed=42)
        self.state: Optional[BattleState] = None
        self.engine: Optional[SimulationEngine] = None
        self.event_log: Optional[EventLogger] = None

    def _initialize_battle(self) -> None:
        """Initialize battle state and engine."""
        # Create battlefield
        battlefield = Battlefield(
            width=self.config.arena_width,
            height=self.config.arena_height
        )

        # Create battle state
        self.state = BattleState(
            battlefield=battlefield,
            seed=self.config.seed,
            units=[]
        )

        # Create simplified units for MVP
        # Unit 1
        unit1_pos = Position(*self.config.unit1_position)
        unit1 = UnitState(
            unit_id="unit_1",
            team="team_a",
            position=unit1_pos,
            facing=0.0,
            component_states=[
                ComponentState(
                    component_id="weapon_1",
                    health=100.0,
                    max_health=100.0
                ),
                ComponentState(
                    component_id="armor_1",
                    health=200.0,
                    max_health=200.0
                )
            ]
        )

        # Unit 2
        unit2_pos = Position(*self.config.unit2_position)
        unit2 = UnitState(
            unit_id="unit_2",
            team="team_b",
            position=unit2_pos,
            facing=3.14159,  # Face opposite direction
            component_states=[
                ComponentState(
                    component_id="weapon_2",
                    health=100.0,
                    max_health=100.0
                ),
                ComponentState(
                    component_id="armor_2",
                    health=200.0,
                    max_health=200.0
                )
            ]
        )

        self.state.units = [unit1, unit2]

        # Create event logger
        self.event_log = EventLogger()

        # Create simulation engine
        sim_config = SimulationConfig(
            time_step=self.config.time_step,
            max_turns=self.config.max_turns,
            max_duration=self.config.max_duration
        )

        self.engine = SimulationEngine(
            state=self.state,
            config=sim_config,
            event_logger=self.event_log
        )

        # Log battle start
        self.event_log.log(
            timestamp=0.0,
            turn=0,
            event_type=EventType.BATTLE_START,
            seed=self.config.seed,
            battlefield={'width': battlefield.width, 'height': battlefield.height}
        )

    def simulate(self) -> BattleResult:
        """
        Run complete battle simulation.

        Returns:
            BattleResult with winner, events, and statistics
        """
        # Initialize
        self._initialize_battle()

        # Run simulation
        while not self.engine.is_finished():
            self.engine.execute_turn()

            # Check win conditions
            winner = self.engine.check_win_conditions()
            if winner is not None or self.state.is_finished():
                break

        # Log battle end
        self.event_log.log(
            timestamp=self.state.time_elapsed,
            turn=self.state.turn,
            event_type=EventType.BATTLE_END,
            winner=self.state.winner,
            outcome=self.state.outcome
        )

        # Calculate statistics
        statistics = self._calculate_statistics()

        # Create result
        return BattleResult(
            config=self.config,
            statistics=statistics,
            events=self.event_log.events,
            final_state=self.state.snapshot()
        )

    def simulate_step_by_step(self) -> Iterator[BattleStep]:
        """
        Simulate battle step-by-step for visualization.

        Yields:
            BattleStep for each turn
        """
        # Initialize
        self._initialize_battle()

        # Yield initial state
        yield BattleStep(
            turn=0,
            time=0.0,
            state=self.state.snapshot(),
            events=[],
            is_finished=False
        )

        # Run simulation
        while not self.engine.is_finished():
            turn_start = self.state.turn

            self.engine.execute_turn()

            # Get events for this turn
            turn_events = self.event_log.get_events_in_range(
                self.state.turn,
                self.state.turn
            )

            # Check win conditions
            winner = self.engine.check_win_conditions()

            yield BattleStep(
                turn=self.state.turn,
                time=self.state.time_elapsed,
                state=self.state.snapshot(),
                events=turn_events,
                is_finished=self.engine.is_finished()
            )

            if winner is not None or self.state.is_finished():
                break

        # Log battle end
        self.event_log.log(
            timestamp=self.state.time_elapsed,
            turn=self.state.turn,
            event_type=EventType.BATTLE_END,
            winner=self.state.winner,
            outcome=self.state.outcome
        )

        # Final step with result
        statistics = self._calculate_statistics()
        result = BattleResult(
            config=self.config,
            statistics=statistics,
            events=self.event_log.events,
            final_state=self.state.snapshot()
        )

        yield BattleStep(
            turn=self.state.turn,
            time=self.state.time_elapsed,
            state=self.state.snapshot(),
            events=[],
            is_finished=True,
            result=result
        )

    def get_state(self) -> Optional[Dict[str, Any]]:
        """
        Get current battle state.

        Returns:
            Current battle state snapshot or None if not initialized
        """
        if self.state is None:
            return None
        return self.state.snapshot()

    def reset(self) -> None:
        """Reset battle to initial state."""
        self.state = None
        self.engine = None
        self.event_log = None

    def _calculate_statistics(self) -> BattleStatistics:
        """Calculate battle statistics from events."""
        # Count combat events
        shots_fired = self.event_log.count_events(EventType.WEAPON_FIRED)
        hits = self.event_log.count_events(EventType.ATTACK_HIT)
        misses = self.event_log.count_events(EventType.ATTACK_MISS)
        crits = self.event_log.count_events(EventType.CRITICAL_HIT)

        # Per-unit stats
        unit_stats = {}
        for unit in self.state.units:
            unit_stats[unit.unit_id] = {
                'final_health': unit.get_total_health(),
                'destroyed': unit.is_destroyed(),
                'team': unit.team
            }

        return BattleStatistics(
            winner=self.state.winner,
            outcome_reason=self.state.outcome or "unknown",
            total_turns=self.state.turn,
            total_time=self.state.time_elapsed,
            unit_stats=unit_stats,
            total_shots_fired=shots_fired,
            total_hits=hits,
            total_misses=misses,
            total_critical_hits=crits
        )
