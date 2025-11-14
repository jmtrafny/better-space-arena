"""Movement system - movement calculations and AI behaviors."""

from enum import Enum
from typing import Optional

from ..core.state import UnitState, Position, Vector2D, Battlefield


class MovementBehavior(str, Enum):
    """AI movement behavior types."""

    AGGRESSIVE = "aggressive"  # Move toward enemy
    DEFENSIVE = "defensive"  # Maintain distance
    KITING = "kiting"  # Stay at optimal range
    STATIONARY = "stationary"  # Don't move


class MovementSystem:
    """
    Handles all movement-related calculations.

    For MVP, implements simple movement without complex physics.
    Future enhancements can add acceleration, turning rates, etc.
    """

    def __init__(self, battlefield: Battlefield):
        """
        Initialize movement system.

        Args:
            battlefield: Battlefield dimensions
        """
        self.battlefield = battlefield

    def calculate_movement(
        self,
        unit: UnitState,
        nearest_enemy: Optional[UnitState],
        behavior: MovementBehavior,
        max_speed: float,
        time_step: float
    ) -> Vector2D:
        """
        Determine unit's movement direction and speed.

        Args:
            unit: Unit to move
            nearest_enemy: Nearest enemy unit (or None)
            behavior: Movement behavior
            max_speed: Maximum movement speed (m/s)
            time_step: Time step (seconds)

        Returns:
            Movement vector for this turn
        """
        if behavior == MovementBehavior.STATIONARY:
            return Vector2D.zero()

        if nearest_enemy is None:
            return Vector2D.zero()

        # Calculate direction to enemy
        direction = (nearest_enemy.position - unit.position).normalized()

        if behavior == MovementBehavior.AGGRESSIVE:
            # Move directly toward enemy
            return direction * max_speed

        elif behavior == MovementBehavior.DEFENSIVE:
            # Move away from enemy
            return -direction * max_speed

        elif behavior == MovementBehavior.KITING:
            # Maintain optimal distance (60% of max range)
            # For MVP, use simplified logic
            distance = unit.position.distance_to(nearest_enemy.position)
            optimal_distance = 80.0  # meters (could be weapon-dependent)

            if distance < optimal_distance * 0.8:
                # Too close - move away
                return -direction * max_speed
            elif distance > optimal_distance * 1.2:
                # Too far - move closer
                return direction * max_speed
            else:
                # Good distance - orbit (perpendicular movement)
                perpendicular = Vector2D(-direction.y, direction.x)
                return perpendicular * (max_speed * 0.5)

        return Vector2D.zero()

    def apply_movement(
        self,
        unit: UnitState,
        velocity: Vector2D,
        time_step: float
    ) -> Position:
        """
        Calculate new position given velocity and time step.

        Args:
            unit: Unit to move
            velocity: Velocity vector
            time_step: Time step (seconds)

        Returns:
            New position (clamped to battlefield)
        """
        displacement = velocity * time_step
        new_position = unit.position + displacement

        # Clamp to battlefield bounds
        return self.battlefield.clamp(new_position)

    def check_collision(
        self,
        unit: UnitState,
        new_position: Position,
        other_units: list[UnitState],
        collision_radius: float = 5.0
    ) -> bool:
        """
        Check if movement would result in collision.

        Args:
            unit: Unit attempting to move
            new_position: Proposed new position
            other_units: Other units in the battle
            collision_radius: Minimum distance between units

        Returns:
            True if collision detected
        """
        for other_unit in other_units:
            if other_unit.unit_id == unit.unit_id:
                continue

            distance = new_position.distance_to(other_unit.position)
            if distance < collision_radius:
                return True  # Collision detected

        return False
