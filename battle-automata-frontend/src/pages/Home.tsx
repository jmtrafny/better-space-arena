import { Link } from 'react-router-dom';

export default function Home() {
  return (
    <div style={{ padding: '2rem' }}>
      <h1>Battle Automata Engine</h1>
      <p>Welcome to the Battle Automata Engine - A theme-agnostic battle simulation system</p>

      <div style={{ marginTop: '2rem', display: 'flex', gap: '1rem' }}>
        <Link to="/battle">
          <button>Run Battle</button>
        </Link>
        <Link to="/builder">
          <button>Unit Builder</button>
        </Link>
      </div>
    </div>
  );
}
