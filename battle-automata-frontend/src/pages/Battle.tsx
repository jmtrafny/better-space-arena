import { useState } from 'react';
import { Link } from 'react-router-dom';
import { battleEngine } from '../engine/battle-engine-wasm';
import { pyodideLoader } from '../engine/pyodide-loader';
import type { BattleResult } from '../utils/types';

export default function Battle() {
  const [loading, setLoading] = useState(false);
  const [loadingProgress, setLoadingProgress] = useState(0);
  const [result, setResult] = useState<BattleResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Subscribe to Pyodide loading state
  const handleRunBattle = async () => {
    setLoading(true);
    setError(null);
    setResult(null);

    // Subscribe to loading progress
    const unsubscribe = pyodideLoader.onStateChange((state) => {
      setLoadingProgress(state.progress);
      if (state.error) {
        setError(state.error);
      }
    });

    try {
      console.log('Initializing Battle Engine...');

      // Mock units for testing
      const unit1 = {
        id: 'fighter',
        name: 'Light Fighter',
        theme: 'space-ships',
        layout: { size: [10, 10] as [number, number] },
        components: [],
        resources: { power: 100, weight_limit: 500 },
      };

      const unit2 = {
        id: 'tank',
        name: 'Heavy Tank',
        theme: 'space-ships',
        layout: { size: [10, 10] as [number, number] },
        components: [],
        resources: { power: 100, weight_limit: 500 },
      };

      const config = {
        seed: 12345,
        arena_size: [1000, 1000] as [number, number],
        max_duration: 60.0,
        time_step: 0.1,
      };

      console.log('Running battle simulation...');
      const battleResult = await battleEngine.simulateBattle(unit1, unit2, config);

      console.log('Battle complete:', battleResult);
      setResult(battleResult);
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : String(err);
      setError(errorMsg);
      console.error('Battle simulation failed:', err);
    } finally {
      setLoading(false);
      unsubscribe();
    }
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Battle Viewer</h1>
      <p>Test Pyodide integration and battle simulation</p>

      <div style={{ marginTop: '2rem' }}>
        <button onClick={handleRunBattle} disabled={loading}>
          {loading ? 'Loading...' : 'Run Test Battle'}
        </button>

        {loading && (
          <div style={{ marginTop: '1rem' }}>
            <p>Loading Pyodide... {loadingProgress}%</p>
            <progress value={loadingProgress} max={100} style={{ width: '300px' }} />
          </div>
        )}

        {error && (
          <div style={{ marginTop: '1rem', padding: '1rem', background: '#fee', color: '#c00' }}>
            <strong>Error:</strong> {error}
          </div>
        )}

        {result && (
          <div style={{ marginTop: '1rem', padding: '1rem', background: '#efe' }}>
            <h2>Battle Result</h2>
            <p>
              <strong>Winner:</strong> {result.winner || 'Draw'}
            </p>
            <p>
              <strong>Duration:</strong> {result.duration.toFixed(1)}s
            </p>
            <p>
              <strong>Events:</strong> {result.events.length}
            </p>
            <details>
              <summary>Full Result (JSON)</summary>
              <pre style={{ fontSize: '12px', overflow: 'auto' }}>
                {JSON.stringify(result, null, 2)}
              </pre>
            </details>
          </div>
        )}
      </div>

      <div style={{ marginTop: '2rem' }}>
        <Link to="/">
          <button>← Back to Home</button>
        </Link>
      </div>
    </div>
  );
}
