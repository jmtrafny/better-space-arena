"""Example battle simulation demonstrating the Battle Automata Engine."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from battle_automata.api.battle import Battle, BattleConfig


def run_simple_battle():
    """Run a simple battle with default configuration."""
    print("=" * 60)
    print("BATTLE AUTOMATA ENGINE - Example Battle")
    print("=" * 60)
    print()

    # Create battle configuration
    config = BattleConfig(
        seed=42,
        max_turns=1000,
        max_duration=100.0,
        arena_width=1000.0,
        arena_height=1000.0,
        unit1_position=(100.0, 500.0),
        unit2_position=(900.0, 500.0)
    )

    print(f"Configuration:")
    print(f"  Seed: {config.seed}")
    print(f"  Max Turns: {config.max_turns}")
    print(f"  Max Duration: {config.max_duration}s")
    print(f"  Arena: {config.arena_width}x{config.arena_height}m")
    print(f"  Starting positions: {config.unit1_position} vs {config.unit2_position}")
    print()

    # Create and run battle
    print("Running simulation...")
    battle = Battle(config)
    result = battle.simulate()

    # Display results
    print()
    print(result.print_summary())

    # Display sample events
    print("\nSample Events (first 10):")
    for i, event in enumerate(result.events[:10]):
        print(f"  {event}")

    print()
    print(f"Total events logged: {len(result.events)}")

    # Save result
    output_file = "battle_result.json"
    result.save(output_file)
    print(f"\nFull results saved to: {output_file}")

    return result


def run_multiple_battles_with_different_seeds():
    """Run multiple battles with different seeds to demonstrate variability."""
    print("\n" + "=" * 60)
    print("MULTIPLE BATTLE COMPARISON")
    print("=" * 60)
    print()

    seeds = [42, 123, 456, 789, 1000]
    results = []

    for seed in seeds:
        config = BattleConfig(seed=seed, max_turns=500)
        battle = Battle(config)
        result = battle.simulate()
        results.append((seed, result))

        print(f"Seed {seed:4d}: Winner={result.statistics.winner}, "
              f"Turns={result.statistics.total_turns:3d}, "
              f"Hits={result.statistics.total_hits:3d}, "
              f"Accuracy={result.statistics.get_accuracy():.1%}")

    # Count wins
    team_a_wins = sum(1 for _, r in results if r.statistics.winner == "team_a")
    team_b_wins = sum(1 for _, r in results if r.statistics.winner == "team_b")

    print()
    print(f"Win Distribution:")
    print(f"  Team A: {team_a_wins} wins")
    print(f"  Team B: {team_b_wins} wins")


def demonstrate_determinism():
    """Demonstrate that same seed produces identical results."""
    print("\n" + "=" * 60)
    print("DETERMINISM DEMONSTRATION")
    print("=" * 60)
    print()

    seed = 12345
    print(f"Running same battle 5 times with seed={seed}...")
    print()

    results = []
    for i in range(5):
        config = BattleConfig(seed=seed, max_turns=500)
        battle = Battle(config)
        result = battle.simulate()
        results.append(result)

        print(f"Run {i+1}: Winner={result.statistics.winner}, "
              f"Turns={result.statistics.total_turns}, "
              f"Hits={result.statistics.total_hits}, "
              f"Events={len(result.events)}")

    # Verify all identical
    reference = results[0]
    all_identical = all(
        r.statistics.winner == reference.statistics.winner and
        r.statistics.total_turns == reference.statistics.total_turns and
        r.statistics.total_hits == reference.statistics.total_hits and
        len(r.events) == len(reference.events)
        for r in results
    )

    print()
    if all_identical:
        print("VERIFIED: All 5 runs produced IDENTICAL results!")
        print("  Same seed = Same battle = Perfect determinism")
    else:
        print("ERROR: Results differ (determinism broken)")


def demonstrate_step_by_step():
    """Demonstrate step-by-step simulation for visualization."""
    print("\n" + "=" * 60)
    print("STEP-BY-STEP SIMULATION")
    print("=" * 60)
    print()

    config = BattleConfig(seed=42, max_turns=20)  # Short battle for demo
    battle = Battle(config)

    print("Running battle step-by-step (showing every 5th turn)...")
    print()

    for step in battle.simulate_step_by_step():
        if step.turn % 5 == 0 or step.is_finished:
            print(f"Turn {step.turn:3d} @ {step.time:5.1f}s: "
                  f"{len(step.events)} events this turn")

            # Show unit positions from state
            if 'units' in step.state:
                for unit in step.state['units']:
                    pos = unit['position']
                    health = unit['total_health']
                    print(f"  {unit['unit_id']}: pos=({pos['x']:.0f}, {pos['y']:.0f}), "
                          f"health={health:.0f}")

        if step.is_finished:
            print()
            print(f"Battle finished!")
            if step.result:
                print(f"Winner: {step.result.statistics.winner}")
            break


if __name__ == '__main__':
    # Run example demonstrations
    result = run_simple_battle()
    run_multiple_battles_with_different_seeds()
    demonstrate_determinism()
    demonstrate_step_by_step()

    print("\n" + "=" * 60)
    print("Examples complete!")
    print("=" * 60)
