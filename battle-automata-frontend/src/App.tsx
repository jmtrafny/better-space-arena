import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Battle from './pages/Battle';
import BattleDemo from './pages/BattleDemo';
import Builder from './pages/Builder';
import TestDeterminism from './pages/TestDeterminism';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/battle" element={<Battle />} />
        <Route path="/battle-demo" element={<BattleDemo />} />
        <Route path="/test-determinism" element={<TestDeterminism />} />
        <Route path="/builder" element={<Builder />} />
      </Routes>
    </Router>
  );
}

export default App;
