import { Link } from 'react-router-dom';

export default function Builder() {
  return (
    <div style={{ padding: '2rem' }}>
      <h1>Unit Builder</h1>
      <p>Design and customize your battle units here</p>

      <div style={{ marginTop: '2rem' }}>
        <Link to="/">
          <button>← Back to Home</button>
        </Link>
      </div>
    </div>
  );
}
