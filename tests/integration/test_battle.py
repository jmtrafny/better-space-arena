"""Integration tests for complete battle simulation."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from battle_automata.api.battle import Battle, BattleConfig
from battle_automata.core.events import EventType


def test_complete_battle_simulation():
    """Test full battle from start to finish."""
    config = BattleConfig(seed=42, max_turns=1000)
    battle = Battle(config)
    result = battle.simulate()

    # Verify battle completed
    assert result.statistics.winner is not None or result.statistics.outcome_reason == "timeout", \
        "Battle must produce a result"

    # Verify events were logged
    assert len(result.events) > 0, "Battle must generate events"

    # Verify required events exist
    battle_start = [e for e in result.events if e.event_type == EventType.BATTLE_START]
    battle_end = [e for e in result.events if e.event_type == EventType.BATTLE_END]

    assert len(battle_start) == 1, "Must have exactly one BATTLE_START event"
    assert len(battle_end) == 1, "Must have exactly one BATTLE_END event"

    # Verify statistics
    assert result.statistics.total_turns > 0, "Battle must have at least one turn"
    assert result.statistics.total_time >= 0, "Time must be non-negative"

    print(f"PASS: Complete battle simulation")
    print(f"  Winner: {result.statistics.winner}")
    print(f"  Outcome: {result.statistics.outcome_reason}")
    print(f"  Turns: {result.statistics.total_turns}")
    print(f"  Time: {result.statistics.total_time:.1f}s")
    print(f"  Events: {len(result.events)}")


def test_battle_step_by_step():
    """Test step-by-step simulation."""
    config = BattleConfig(seed=42, max_turns=20)
    battle = Battle(config)

    steps = list(battle.simulate_step_by_step())

    # Verify we got steps
    assert len(steps) > 0, "Must generate simulation steps"

    # Verify progression
    for i in range(len(steps) - 1):
        assert steps[i].turn <= steps[i + 1].turn, "Turns must increase"

    # Verify final step has result
    final_step = steps[-1]
    assert final_step.is_finished, "Final step must be marked finished"
    assert final_step.result is not None, "Final step must have result"

    print(f"PASS: Step-by-step simulation ({len(steps)} steps)")


def test_battle_with_timeout():
    """Test battle that ends due to timeout."""
    config = BattleConfig(
        seed=42,
        max_turns=10,  # Very short
        max_duration=1.0
    )
    battle = Battle(config)
    result = battle.simulate()

    # Should timeout before elimination
    assert result.statistics.outcome_reason == "timeout", \
        "Short battle should timeout"

    print(f"PASS: Timeout handling")


def test_battle_events_chronological():
    """Verify events are in chronological order."""
    config = BattleConfig(seed=42, max_turns=100)
    battle = Battle(config)
    result = battle.simulate()

    # Check timestamp ordering
    for i in range(len(result.events) - 1):
        assert result.events[i].timestamp <= result.events[i + 1].timestamp, \
            f"Event {i} timestamp out of order"

    # Check turn ordering
    for i in range(len(result.events) - 1):
        assert result.events[i].turn <= result.events[i + 1].turn, \
            f"Event {i} turn out of order"

    print(f"PASS: Events are chronologically ordered")


def test_battle_statistics_accurate():
    """Verify statistics match event counts."""
    config = BattleConfig(seed=42, max_turns=100)
    battle = Battle(config)
    result = battle.simulate()

    # Count events manually
    weapon_fired = len([e for e in result.events if e.event_type == EventType.WEAPON_FIRED])
    hits = len([e for e in result.events if e.event_type == EventType.ATTACK_HIT])
    misses = len([e for e in result.events if e.event_type == EventType.ATTACK_MISS])

    # Verify statistics match
    assert result.statistics.total_shots_fired == weapon_fired, \
        "Shots fired statistic must match events"
    assert result.statistics.total_hits == hits, \
        "Hits statistic must match events"
    assert result.statistics.total_misses == misses, \
        "Misses statistic must match events"

    print(f"PASS: Statistics match event counts")


def test_battle_final_state_valid():
    """Verify final battle state is valid."""
    config = BattleConfig(seed=42, max_turns=100)
    battle = Battle(config)
    result = battle.simulate()

    # Verify final state exists
    assert result.final_state is not None, "Must have final state"
    assert 'units' in result.final_state, "Final state must have units"
    assert 'turn' in result.final_state, "Final state must have turn"
    assert 'time_elapsed' in result.final_state, "Final state must have time"

    print(f"PASS: Final state is valid")


if __name__ == '__main__':
    print("Running integration tests...\n")

    test_complete_battle_simulation()
    test_battle_step_by_step()
    test_battle_with_timeout()
    test_battle_events_chronological()
    test_battle_statistics_accurate()
    test_battle_final_state_valid()

    print("\nAll integration tests PASSED!")
