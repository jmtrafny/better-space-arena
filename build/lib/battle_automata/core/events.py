"""Battle event system for complete observability and replay."""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional
import json


class EventType(str, Enum):
    """All possible event types in a battle simulation."""

    # Battle lifecycle
    BATTLE_START = "battle_start"
    BATTLE_END = "battle_end"
    TURN_START = "turn_start"
    TURN_END = "turn_end"

    # Movement
    MOVEMENT = "movement"
    COLLISION = "collision"

    # Targeting
    TARGET_ACQUIRED = "target_acquired"
    TARGET_LOST = "target_lost"

    # Combat
    WEAPON_FIRED = "weapon_fired"
    ATTACK_HIT = "attack_hit"
    ATTACK_MISS = "attack_miss"
    CRITICAL_HIT = "critical_hit"

    # Damage
    DAMAGE_DEALT = "damage_dealt"
    SHIELD_HIT = "shield_hit"
    ARMOR_HIT = "armor_hit"

    # Destruction
    COMPONENT_DAMAGED = "component_damaged"
    COMPONENT_DESTROYED = "component_destroyed"
    UNIT_DESTROYED = "unit_destroyed"

    # Effects
    EFFECT_APPLIED = "effect_applied"
    EFFECT_EXPIRED = "effect_expired"

    # Other
    TIMEOUT = "timeout"


@dataclass
class Event:
    """
    Immutable event representing something that happened during simulation.

    All events contain complete information about what happened at a specific
    point in time, enabling perfect replay and analysis.
    """

    timestamp: float  # Simulation time in seconds
    turn: int  # Turn number
    event_type: EventType
    data: Dict[str, Any]  # Event-specific data

    def to_dict(self) -> Dict[str, Any]:
        """Serialize event to dictionary for JSON export."""
        return {
            'timestamp': self.timestamp,
            'turn': self.turn,
            'event_type': self.event_type.value,
            'data': self.data
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> 'Event':
        """Deserialize event from dictionary."""
        return cls(
            timestamp=d['timestamp'],
            turn=d['turn'],
            event_type=EventType(d['event_type']),
            data=d['data']
        )

    def __str__(self) -> str:
        """Human-readable event representation."""
        return f"[T{self.turn} @ {self.timestamp:.2f}s] {self.event_type.value}: {self.data}"


class EventLogger:
    """
    Records all events during simulation.

    Features:
    - Append-only event log
    - Fast serialization to JSON
    - Query capabilities by type
    - Replay support
    """

    def __init__(self):
        self.events: List[Event] = []
        self._event_index: Dict[EventType, List[int]] = {}

    def log_event(self, event: Event) -> None:
        """
        Add event to log.

        Args:
            event: Event to log
        """
        event_id = len(self.events)
        self.events.append(event)

        # Update index for fast queries
        if event.event_type not in self._event_index:
            self._event_index[event.event_type] = []
        self._event_index[event.event_type].append(event_id)

    def log(
        self,
        timestamp: float,
        turn: int,
        event_type: EventType,
        **data
    ) -> None:
        """
        Convenience method to log an event.

        Args:
            timestamp: Simulation time
            turn: Turn number
            event_type: Type of event
            **data: Event data as keyword arguments
        """
        event = Event(
            timestamp=timestamp,
            turn=turn,
            event_type=event_type,
            data=data
        )
        self.log_event(event)

    def get_events(
        self,
        event_type: Optional[EventType] = None
    ) -> List[Event]:
        """
        Get events, optionally filtered by type.

        Args:
            event_type: If specified, only return events of this type

        Returns:
            List of events
        """
        if event_type is None:
            return self.events.copy()

        if event_type not in self._event_index:
            return []

        indices = self._event_index[event_type]
        return [self.events[i] for i in indices]

    def get_events_in_range(
        self,
        start_turn: int,
        end_turn: int
    ) -> List[Event]:
        """
        Get events within turn range.

        Args:
            start_turn: Start turn (inclusive)
            end_turn: End turn (inclusive)

        Returns:
            Events in the specified turn range
        """
        return [
            e for e in self.events
            if start_turn <= e.turn <= end_turn
        ]

    def count_events(self, event_type: Optional[EventType] = None) -> int:
        """
        Count events, optionally filtered by type.

        Args:
            event_type: If specified, only count events of this type

        Returns:
            Event count
        """
        if event_type is None:
            return len(self.events)
        return len(self._event_index.get(event_type, []))

    def serialize(self) -> Dict[str, Any]:
        """
        Serialize entire log to dictionary.

        Returns:
            Dictionary with events and metadata
        """
        return {
            'events': [e.to_dict() for e in self.events],
            'count': len(self.events),
            'event_types': {
                et.value: self.count_events(et)
                for et in EventType
                if self.count_events(et) > 0
            }
        }

    def export_json(self, filepath: str) -> None:
        """
        Export log to JSON file.

        Args:
            filepath: Path to output file
        """
        with open(filepath, 'w') as f:
            json.dump(self.serialize(), f, indent=2)

    def clear(self) -> None:
        """Clear all events from the log."""
        self.events.clear()
        self._event_index.clear()

    def __len__(self) -> int:
        """Return number of logged events."""
        return len(self.events)

    def __iter__(self):
        """Iterate over events."""
        return iter(self.events)
