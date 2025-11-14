"""Deterministic random number generator for reproducible simulations."""

import random
from typing import Any, Dict, List, TypeVar


T = TypeVar('T')


class SeededRandom:
    """
    Deterministic random number generator.

    Uses Python's Mersenne Twister (MT19937) for reproducibility across platforms.
    All randomness in the simulation MUST go through this class to ensure determinism.
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

        Returns:
            Random float
        """
        self.call_count += 1
        return self.rng.random()

    def randint(self, a: int, b: int) -> int:
        """
        Generate random integer in [a, b].

        Args:
            a: Minimum value (inclusive)
            b: Maximum value (inclusive)

        Returns:
            Random integer
        """
        self.call_count += 1
        return self.rng.randint(a, b)

    def uniform(self, a: float, b: float) -> float:
        """
        Generate random float in [a, b].

        Args:
            a: Minimum value
            b: Maximum value

        Returns:
            Random float
        """
        self.call_count += 1
        return self.rng.uniform(a, b)

    def choice(self, sequence: List[T]) -> T:
        """
        Choose random element from sequence.

        Args:
            sequence: Non-empty sequence

        Returns:
            Random element

        Raises:
            IndexError: If sequence is empty
        """
        self.call_count += 1
        return self.rng.choice(sequence)

    def shuffle(self, sequence: List[T]) -> None:
        """
        Shuffle sequence in-place.

        Args:
            sequence: List to shuffle
        """
        self.call_count += 1
        self.rng.shuffle(sequence)

    def get_state(self) -> Dict[str, Any]:
        """
        Get current RNG state for serialization.

        Returns:
            State dictionary
        """
        return {
            'seed': self.seed,
            'call_count': self.call_count,
            'state': self.rng.getstate()
        }

    def set_state(self, state: Dict[str, Any]) -> None:
        """
        Restore RNG state from serialization.

        Args:
            state: State dictionary from get_state()
        """
        self.seed = state['seed']
        self.call_count = state['call_count']
        self.rng.setstate(state['state'])

    def __repr__(self) -> str:
        """String representation."""
        return f"SeededRandom(seed={self.seed}, calls={self.call_count})"
