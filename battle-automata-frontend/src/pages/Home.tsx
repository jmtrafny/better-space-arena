import { Link } from 'react-router-dom';

export default function Home() {
  return (
    <div style={{ padding: '2rem', minHeight: '100vh' }}>
      <h1 style={{ color: '#e5e5e5' }}>Battle Automata Engine</h1>
      <p style={{ color: '#9ca3af' }}>Welcome to the Battle Automata Engine - A theme-agnostic battle simulation system</p>

      <div style={{ marginTop: '2rem', display: 'flex', gap: '1rem' }}>
        <Link to="/battle">
          <button>Run Battle</button>
        </Link>
        <Link to="/battle-demo">
          <button>UI Component Demo</button>
        </Link>
        <Link to="/test-determinism">
          <button>Determinism Test</button>
        </Link>
        <Link to="/builder">
          <button>Unit Builder</button>
        </Link>
      </div>
    </div>
  );
}
