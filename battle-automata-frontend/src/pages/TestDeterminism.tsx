/**
 * Determinism Test Page
 *
 * Tests that battles with the same seed produce identical results
 */

import { useState } from 'react';
import { battleEngine } from '../engine/battle-engine-wasm';
import type { Unit, BattleConfig } from '../utils/types';

export default function TestDeterminism() {
  const [testing, setTesting] = useState(false);
  const [results, setResults] = useState<string[]>([]);

  const testUnit1: Unit = {
    id: 'fighter_mk1',
    name: 'Fighter Mk1',
    theme: 'space-ships',
    layout: { size: [10, 10] },
    components: [
      { type: 'laser_cannon_mk1', position: [5, 2], facing: '0' },
      { type: 'laser_cannon_mk1', position: [4, 2], facing: '0' },
      { type: 'light_armor_mk1', position: [5, 5], facing: '0' },
      { type: 'fusion_reactor_small', position: [5, 5], facing: '0' },
      { type: 'ion_engine_mk1', position: [5, 8], facing: '180' },
    ],
    resources: { power: 200, weight_limit: 500 },
  };

  const testUnit2: Unit = {
    id: 'tank_mk1',
    name: 'Tank Mk1',
    theme: 'space-ships',
    layout: { size: [12, 12] },
    components: [
      { type: 'laser_cannon_mk1', position: [6, 2], facing: '0' },
      { type: 'light_armor_mk1', position: [6, 4], facing: '0' },
      { type: 'light_armor_mk1', position: [6, 6], facing: '0' },
      { type: 'light_armor_mk1', position: [6, 8], facing: '0' },
      { type: 'fusion_reactor_small', position: [6, 6], facing: '0' },
      { type: 'ion_engine_mk1', position: [6, 10], facing: '180' },
    ],
    resources: { power: 200, weight_limit: 800 },
  };

  const runDeterminismTest = async () => {
    setTesting(true);
    setResults(['Starting determinism test...']);

    try {
      const config: BattleConfig = {
        seed: 42424242, // Fixed seed for determinism
        arena_size: [1000, 1000],
        max_duration: 60.0,
        time_step: 0.1,
      };

      // Run 3 battles with the same seed
      const battles: typeof battleEngine.simulateBattle extends (...args: any[]) => Promise<infer R> ? R[] : never = [];
      for (let i = 0; i < 3; i++) {
        setResults(prev => [...prev, `\nRun ${i + 1}: Starting battle...`]);
        const result = await battleEngine.simulateBattle(testUnit1, testUnit2, config);
        battles.push(result);
        setResults(prev => [...prev,
          `Run ${i + 1} Complete:`,
          `  Winner: ${result.statistics.winner}`,
          `  Duration: ${result.statistics.total_time.toFixed(3)}s`,
          `  Total Turns: ${result.statistics.total_turns}`,
          `  Events: ${result.events.length}`,
          `  Shots Fired: ${result.statistics.total_shots_fired}`,
          `  Hits: ${result.statistics.total_hits}`,
        ]);
      }

      // Compare results
      setResults(prev => [...prev, '\n=== Determinism Check ===']);

      const allMatch = battles.every((battle, i) => {
        if (i === 0) return true;
        return (
          battle.statistics.winner === battles[0].statistics.winner &&
          battle.statistics.total_time === battles[0].statistics.total_time &&
          battle.statistics.total_turns === battles[0].statistics.total_turns &&
          battle.events.length === battles[0].events.length &&
          battle.statistics.total_shots_fired === battles[0].statistics.total_shots_fired
        );
      });

      if (allMatch) {
        setResults(prev => [...prev,
          '✅ DETERMINISM TEST PASSED',
          'All 3 battles produced identical results!',
        ]);
      } else {
        setResults(prev => [...prev,
          '❌ DETERMINISM TEST FAILED',
          'Battles produced different results with same seed',
        ]);
      }

    } catch (error) {
      setResults(prev => [...prev,
        `❌ ERROR: ${error instanceof Error ? error.message : String(error)}`
      ]);
    } finally {
      setTesting(false);
    }
  };

  return (
    <div style={{ padding: '2rem', maxWidth: '900px', margin: '0 auto', minHeight: '100vh' }}>
      <h1 style={{ color: '#e5e5e5' }}>Determinism Test</h1>
      <p style={{ color: '#9ca3af' }}>Tests that battles with the same seed produce identical results</p>

      <button
        onClick={runDeterminismTest}
        disabled={testing}
        style={{
          padding: '0.75rem 1.5rem',
          fontSize: '1rem',
          backgroundColor: testing ? '#ccc' : '#3b82f6',
          color: 'white',
          border: 'none',
          borderRadius: '0.375rem',
          cursor: testing ? 'default' : 'pointer',
          marginTop: '1rem',
        }}
      >
        {testing ? 'Running Tests...' : 'Run Determinism Test (3 Battles)'}
      </button>

      {results.length > 0 && (
        <pre style={{
          marginTop: '2rem',
          padding: '1rem',
          backgroundColor: '#1e1e1e',
          color: '#d4d4d4',
          borderRadius: '0.5rem',
          overflow: 'auto',
          fontSize: '0.875rem',
          lineHeight: 1.6,
        }}>
          {results.join('\n')}
        </pre>
      )}
    </div>
  );
}
