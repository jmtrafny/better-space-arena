"""Targeting system - target selection, line of sight, and weapon arcs."""

from enum import Enum
from typing import List, Optional
from dataclasses import dataclass

from ..core.state import UnitState, ComponentState, Position


class TargetingPriority(str, Enum):
    """How weapon selects targets."""

    CLOSEST = "closest"
    WEAKEST = "weakest"
    STRONGEST = "strongest"
    RANDOM = "random"


@dataclass
class Target:
    """Target descriptor."""

    unit_id: str
    component_id: str
    position: Position
    health: float


class TargetingSystem:
    """
    Handles target acquisition and line of sight.

    For MVP, implements simple targeting without obstacles.
    Future enhancements can add terrain, stealth, etc.
    """

    def has_line_of_sight(
        self,
        from_pos: Position,
        to_pos: Position
    ) -> bool:
        """
        Check if there's a clear line of sight between two positions.

        For MVP: Always true if in range
        Future: Raycasting for obstacles

        Args:
            from_pos: Starting position
            to_pos: Target position

        Returns:
            True if line of sight exists
        """
        # MVP: No obstacles
        return True

    def is_in_range(
        self,
        attacker_pos: Position,
        target_pos: Position,
        weapon_range: float
    ) -> bool:
        """
        Check if target is within weapon range.

        Args:
            attacker_pos: Attacker position
            target_pos: Target position
            weapon_range: Maximum weapon range

        Returns:
            True if target is in range
        """
        distance = attacker_pos.distance_to(target_pos)
        return distance <= weapon_range

    def find_targets_for_weapon(
        self,
        attacker: UnitState,
        weapon_range: float,
        enemies: List[UnitState]
    ) -> List[Target]:
        """
        Find all valid targets for a weapon.

        Args:
            attacker: Attacking unit
            weapon_range: Maximum weapon range
            enemies: List of enemy units

        Returns:
            List of valid targets sorted deterministically
        """
        potential_targets = []

        for enemy in enemies:
            # Check if enemy is in range
            distance = attacker.position.distance_to(enemy.position)
            if distance > weapon_range:
                continue

            # Check line of sight
            if not self.has_line_of_sight(attacker.position, enemy.position):
                continue

            # Add all components as potential targets
            for component_state in enemy.component_states:
                if component_state.is_destroyed:
                    continue

                potential_targets.append(Target(
                    unit_id=enemy.unit_id,
                    component_id=component_state.component_id,
                    position=enemy.position,  # Simplified: use unit position
                    health=component_state.health
                ))

        # Sort deterministically (by unit ID, then component ID)
        return sorted(
            potential_targets,
            key=lambda t: (t.unit_id, t.component_id)
        )

    def select_target(
        self,
        targets: List[Target],
        priority: TargetingPriority,
        attacker_pos: Position
    ) -> Optional[Target]:
        """
        Select best target based on targeting priority.

        Args:
            targets: List of valid targets
            priority: Targeting priority
            attacker_pos: Attacker position

        Returns:
            Selected target or None if no targets
        """
        if not targets:
            return None

        if priority == TargetingPriority.CLOSEST:
            return min(
                targets,
                key=lambda t: attacker_pos.distance_to(t.position)
            )

        elif priority == TargetingPriority.WEAKEST:
            return min(targets, key=lambda t: t.health)

        elif priority == TargetingPriority.STRONGEST:
            return max(targets, key=lambda t: t.health)

        else:  # RANDOM or default
            # First target (deterministic)
            return targets[0]
