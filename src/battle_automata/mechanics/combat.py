"""Combat damage system - damage types, calculations, and application."""

from enum import Enum
from typing import Dict, Optional
from dataclasses import dataclass

from ..core.state import ComponentState
from ..core.rng import SeededRandom


class DamageType(str, Enum):
    """Damage type for weapons."""

    KINETIC = "kinetic"  # Ballistic weapons
    ENERGY = "energy"  # Lasers, plasma
    EXPLOSIVE = "explosive"  # Missiles, grenades
    PLASMA = "plasma"  # Plasma weapons


@dataclass
class Attack:
    """Descriptor for a single attack."""

    attacker_id: str
    weapon_id: str
    target_unit_id: str
    target_component_id: str

    # Weapon properties
    base_damage: float
    damage_type: DamageType
    range_to_target: float
    accuracy: float
    armor_piercing: float = 0.0
    critical_chance: float = 0.0
    critical_multiplier: float = 2.0


class DamageSystem:
    """
    Handles damage calculations and type effectiveness.

    Implements the rock-paper-scissors damage type system:
    - Kinetic: Strong vs armor, weak vs shields
    - Energy: Strong vs shields, weak vs armor
    - Explosive: Balanced, good vs structure
    - Plasma: Balanced across all types
    """

    # Damage type effectiveness matrix
    # [damage_type][defense_type] = multiplier
    DAMAGE_TYPE_EFFECTIVENESS: Dict[str, Dict[str, float]] = {
        'kinetic': {
            'armor': 1.0,
            'shield': 0.5,
            'structure': 1.2
        },
        'energy': {
            'armor': 0.8,
            'shield': 1.5,
            'structure': 0.9
        },
        'explosive': {
            'armor': 1.3,
            'shield': 0.7,
            'structure': 1.0
        },
        'plasma': {
            'armor': 1.1,
            'shield': 1.1,
            'structure': 1.1
        }
    }

    def __init__(self, rng: SeededRandom):
        """
        Initialize damage system.

        Args:
            rng: Seeded random number generator for deterministic damage
        """
        self.rng = rng

    def calculate_hit_chance(
        self,
        attack: Attack,
        target_component: ComponentState
    ) -> float:
        """
        Calculate probability of attack hitting target.

        Factors:
        - Base weapon accuracy
        - Range (falloff)
        - Target size/evasion (could be extended)

        Args:
            attack: Attack descriptor
            target_component: Target component state

        Returns:
            Hit probability (0.0 to 1.0)
        """
        base_accuracy = attack.accuracy

        # Range penalty (30% penalty at max range)
        # For now, assume max range is attack.range_to_target * 1.5
        max_range = attack.range_to_target * 1.5
        if max_range > 0:
            range_factor = 1.0 - (attack.range_to_target / max_range) * 0.3
        else:
            range_factor = 1.0

        # Final hit chance
        hit_chance = base_accuracy * range_factor

        # Clamp between minimum and maximum
        return max(0.05, min(0.95, hit_chance))  # 5% min, 95% max

    def roll_hit(self, attack: Attack, target_component: ComponentState) -> bool:
        """
        Roll to see if attack hits.

        Args:
            attack: Attack descriptor
            target_component: Target component state

        Returns:
            True if attack hits
        """
        hit_chance = self.calculate_hit_chance(attack, target_component)
        roll = self.rng.random()
        return roll <= hit_chance

    def roll_critical(self, attack: Attack) -> bool:
        """
        Roll to see if attack is a critical hit.

        Args:
            attack: Attack descriptor

        Returns:
            True if critical hit
        """
        if attack.critical_chance <= 0:
            return False
        roll = self.rng.random()
        return roll <= attack.critical_chance

    def calculate_damage(
        self,
        attack: Attack,
        target_component: ComponentState,
        is_critical: bool = False
    ) -> float:
        """
        Calculate final damage after all modifiers.

        Args:
            attack: Attack descriptor
            target_component: Target component state
            is_critical: Whether this is a critical hit

        Returns:
            Final damage amount
        """
        base_damage = attack.base_damage

        # Critical hit multiplier
        if is_critical:
            base_damage *= attack.critical_multiplier

        # Apply armor reduction
        # For MVP, use simplified armor calculation
        # TODO: In full implementation, get armor from component stats
        armor = 0  # Placeholder
        damage_after_armor = self._apply_armor_reduction(
            base_damage,
            armor,
            attack.armor_piercing
        )

        # Apply damage type effectiveness
        # For MVP, use neutral multiplier
        # TODO: In full implementation, get component type
        type_multiplier = 1.0  # Placeholder

        damage_after_type = damage_after_armor * type_multiplier

        # Random variance (±10%)
        variance = self.rng.uniform(0.9, 1.1)
        final_damage = damage_after_type * variance

        return max(1.0, final_damage)  # Minimum 1 damage

    def _apply_armor_reduction(
        self,
        damage: float,
        armor: float,
        armor_piercing: float
    ) -> float:
        """
        Calculate damage reduction from armor.

        Uses diminishing returns formula:
        reduction = armor / (armor + K)
        where K determines armor effectiveness curve

        Args:
            damage: Base damage
            armor: Armor value
            armor_piercing: Armor piercing (0.0 to 1.0)

        Returns:
            Damage after armor reduction
        """
        K = 100.0  # Armor constant

        # Effective armor after penetration
        effective_armor = armor * (1.0 - armor_piercing)

        # Damage reduction percentage
        if effective_armor + K > 0:
            reduction = effective_armor / (effective_armor + K)
        else:
            reduction = 0.0

        # Apply reduction
        return damage * (1.0 - reduction)

    def apply_damage(
        self,
        attack: Attack,
        target_component: ComponentState
    ) -> Dict[str, any]:
        """
        Complete damage application pipeline.

        Args:
            attack: Attack descriptor
            target_component: Target component state

        Returns:
            Dictionary with damage results:
            - hit: bool
            - critical: bool
            - damage: float
            - old_health: float
            - new_health: float
        """
        # Roll for hit
        hit = self.roll_hit(attack, target_component)
        if not hit:
            return {
                'hit': False,
                'critical': False,
                'damage': 0.0,
                'old_health': target_component.health,
                'new_health': target_component.health
            }

        # Roll for critical
        critical = self.roll_critical(attack)

        # Calculate damage
        damage = self.calculate_damage(attack, target_component, critical)

        # Apply damage
        old_health = target_component.health
        actual_damage = target_component.take_damage(damage)
        new_health = target_component.health

        return {
            'hit': True,
            'critical': critical,
            'damage': actual_damage,
            'old_health': old_health,
            'new_health': new_health
        }
