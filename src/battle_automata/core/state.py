"""Battle state management - positions, vectors, and state tracking."""

from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict, Tuple
import math


@dataclass(frozen=True)
class Vector2D:
    """Immutable 2D vector for velocity and direction."""

    x: float
    y: float

    def magnitude(self) -> float:
        """Calculate vector magnitude (length)."""
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalized(self) -> 'Vector2D':
        """
        Return unit vector in same direction.

        Returns:
            Normalized vector (magnitude 1.0) or zero vector if magnitude is 0
        """
        mag = self.magnitude()
        if mag == 0:
            return Vector2D(0, 0)
        return Vector2D(self.x / mag, self.y / mag)

    def dot(self, other: 'Vector2D') -> float:
        """
        Dot product with another vector.

        Args:
            other: Another vector

        Returns:
            Dot product
        """
        return self.x * other.x + self.y * other.y

    def __add__(self, other: 'Vector2D') -> 'Vector2D':
        """Vector addition."""
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Vector2D') -> 'Vector2D':
        """Vector subtraction."""
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> 'Vector2D':
        """Scalar multiplication."""
        return Vector2D(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> 'Vector2D':
        """Reverse scalar multiplication."""
        return self.__mul__(scalar)

    def __neg__(self) -> 'Vector2D':
        """Negation."""
        return Vector2D(-self.x, -self.y)

    def __truediv__(self, scalar: float) -> 'Vector2D':
        """Scalar division."""
        if scalar == 0:
            raise ValueError("Cannot divide vector by zero")
        return Vector2D(self.x / scalar, self.y / scalar)

    @staticmethod
    def zero() -> 'Vector2D':
        """Return zero vector."""
        return Vector2D(0, 0)

    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary."""
        return {'x': self.x, 'y': self.y}

    @classmethod
    def from_dict(cls, d: Dict[str, float]) -> 'Vector2D':
        """Create from dictionary."""
        return cls(d['x'], d['y'])


@dataclass(frozen=True)
class Position:
    """Immutable 2D position in battlefield."""

    x: float
    y: float

    def distance_to(self, other: 'Position') -> float:
        """
        Calculate Euclidean distance to another position.

        Args:
            other: Another position

        Returns:
            Distance in meters
        """
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def __add__(self, vector: Vector2D) -> 'Position':
        """Add vector to position (translation)."""
        return Position(self.x + vector.x, self.y + vector.y)

    def __sub__(self, other: 'Position') -> Vector2D:
        """Subtract positions to get vector between them."""
        return Vector2D(self.x - other.x, self.y - other.y)

    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary."""
        return {'x': self.x, 'y': self.y}

    @classmethod
    def from_dict(cls, d: Dict[str, float]) -> 'Position':
        """Create from dictionary."""
        return cls(d['x'], d['y'])

    def to_tuple(self) -> Tuple[float, float]:
        """Convert to tuple."""
        return (self.x, self.y)


@dataclass(frozen=True)
class Battlefield:
    """Battlefield dimensions and properties."""

    width: float
    height: float

    def is_in_bounds(self, position: Position) -> bool:
        """
        Check if position is within battlefield bounds.

        Args:
            position: Position to check

        Returns:
            True if position is within bounds
        """
        return (0 <= position.x <= self.width and
                0 <= position.y <= self.height)

    def clamp(self, position: Position) -> Position:
        """
        Clamp position to battlefield bounds.

        Args:
            position: Position to clamp

        Returns:
            Position clamped to battlefield
        """
        x = max(0, min(self.width, position.x))
        y = max(0, min(self.height, position.y))
        return Position(x, y)

    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary."""
        return {'width': self.width, 'height': self.height}

    @classmethod
    def from_dict(cls, d: Dict[str, float]) -> 'Battlefield':
        """Create from dictionary."""
        return cls(d['width'], d['height'])


@dataclass
class ComponentState:
    """
    Mutable state of a component instance during battle.

    This represents the dynamic state that changes during simulation,
    separate from the immutable component definition.
    """

    component_id: str  # Reference to component definition
    health: float
    max_health: float
    is_destroyed: bool = False

    # Weapon-specific state
    cooldown_remaining: float = 0.0
    current_target_id: Optional[str] = None
    last_fire_time: float = 0.0

    # Shield-specific state
    shield_strength: float = 0.0
    max_shield_strength: float = 0.0
    time_since_last_hit: float = 0.0

    # Effects
    active_effects: List[Dict[str, Any]] = field(default_factory=list)

    def take_damage(self, amount: float) -> float:
        """
        Apply damage to component.

        Args:
            amount: Damage amount

        Returns:
            Actual damage dealt (may be less if component health is low)
        """
        if self.is_destroyed:
            return 0.0

        old_health = self.health
        self.health = max(0.0, self.health - amount)

        if self.health == 0.0:
            self.is_destroyed = True

        return old_health - self.health

    def is_functional(self) -> bool:
        """
        Check if component can function.

        Returns:
            True if component is not destroyed and has >10% health
        """
        if self.is_destroyed:
            return False
        return (self.health / self.max_health) >= 0.1

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'component_id': self.component_id,
            'health': self.health,
            'max_health': self.max_health,
            'is_destroyed': self.is_destroyed,
            'cooldown_remaining': self.cooldown_remaining,
            'current_target_id': self.current_target_id,
            'shield_strength': self.shield_strength,
        }


@dataclass
class UnitState:
    """
    Mutable state of a unit during battle.

    Tracks position, velocity, and component states.
    """

    unit_id: str
    team: str  # Team identifier

    # Position and motion
    position: Position
    facing: float  # Radians
    velocity: Vector2D = field(default_factory=Vector2D.zero)
    angular_velocity: float = 0.0

    # Component states
    component_states: List[ComponentState] = field(default_factory=list)

    # Status
    is_active: bool = True

    def get_total_health(self) -> float:
        """
        Calculate sum of all component health.

        Returns:
            Total health across all components
        """
        return sum(
            cs.health
            for cs in self.component_states
            if not cs.is_destroyed
        )

    def is_destroyed(self) -> bool:
        """
        Check if unit is destroyed.

        A unit is destroyed if all its components are destroyed.

        Returns:
            True if unit is destroyed
        """
        functional = [
            cs for cs in self.component_states
            if not cs.is_destroyed
        ]
        return len(functional) == 0

    def get_component_state(self, component_id: str) -> Optional[ComponentState]:
        """
        Get state of specific component.

        Args:
            component_id: Component identifier

        Returns:
            Component state or None if not found
        """
        for cs in self.component_states:
            if cs.component_id == component_id:
                return cs
        return None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'unit_id': self.unit_id,
            'team': self.team,
            'position': self.position.to_dict(),
            'facing': self.facing,
            'velocity': self.velocity.to_dict(),
            'total_health': self.get_total_health(),
            'is_active': self.is_active,
            'is_destroyed': self.is_destroyed(),
            'components': [cs.to_dict() for cs in self.component_states]
        }


@dataclass
class BattleState:
    """
    Complete mutable battle state at a point in time.

    This is the single source of truth for all simulation state.
    """

    # Configuration
    battlefield: Battlefield
    seed: int

    # Time tracking
    turn: int = 0
    time_elapsed: float = 0.0

    # Units
    units: List[UnitState] = field(default_factory=list)

    # Win condition
    winner: Optional[str] = None  # Team ID or None
    outcome: Optional[str] = None  # "elimination", "timeout", "draw"

    # Cached data (invalidated when state changes)
    _active_units_cache: Optional[List[UnitState]] = field(default=None, repr=False)

    def get_active_units(self) -> List[UnitState]:
        """
        Get all active (not destroyed) units.

        Returns:
            List of active unit states
        """
        if self._active_units_cache is None:
            self._active_units_cache = [
                u for u in self.units
                if u.is_active and not u.is_destroyed()
            ]
        return self._active_units_cache

    def get_unit(self, unit_id: str) -> Optional[UnitState]:
        """
        Get unit by ID.

        Args:
            unit_id: Unit identifier

        Returns:
            Unit state or None if not found
        """
        for unit in self.units:
            if unit.unit_id == unit_id:
                return unit
        return None

    def get_units_by_team(self, team: str) -> List[UnitState]:
        """
        Get all units on a team.

        Args:
            team: Team identifier

        Returns:
            List of unit states on the team
        """
        return [u for u in self.units if u.team == team]

    def get_enemy_units(self, unit: UnitState) -> List[UnitState]:
        """
        Get all enemy units for a given unit.

        Args:
            unit: Reference unit

        Returns:
            List of enemy unit states
        """
        return [
            u for u in self.get_active_units()
            if u.team != unit.team
        ]

    def invalidate_cache(self) -> None:
        """Invalidate cached derived state."""
        self._active_units_cache = None

    def snapshot(self) -> Dict[str, Any]:
        """
        Create a complete snapshot of current state.

        Returns:
            State snapshot as dictionary
        """
        return {
            'turn': self.turn,
            'time_elapsed': self.time_elapsed,
            'battlefield': self.battlefield.to_dict(),
            'units': [u.to_dict() for u in self.units],
            'winner': self.winner,
            'outcome': self.outcome
        }

    def is_finished(self) -> bool:
        """
        Check if battle is over.

        Returns:
            True if battle has ended
        """
        return self.winner is not None
