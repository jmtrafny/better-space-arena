import { useState } from 'react';
import BattleViewer from '../components/battle/BattleViewer';
import BattleControls from '../components/battle/BattleControls';
import EventLog from '../components/battle/EventLog';
import type { BattleState } from '../components/battle/BattleViewer';
import type { BattleControlStatus } from '../components/battle/BattleControls';
import type { BattleEvent } from '../utils/types';

/**
 * BattleDemo Page
 *
 * Demonstrates all Phase 1.3 UI components working together
 * This page shows the components with mock data before state management is integrated
 */

export default function BattleDemo() {
  const [speed, setSpeed] = useState(1);
  const [status, setStatus] = useState<BattleControlStatus>('idle');
  const [currentTurn, setCurrentTurn] = useState(0);

  // Mock battle state
  const battleState: BattleState = {
    currentTurn,
    maxTurns: 100,
    status,
    units: [
      {
        id: 'player-1',
        name: 'Light Fighter',
        health: 75,
        maxHealth: 100,
        position: [100, 200],
        team: 'player',
        status: 'active',
      },
      {
        id: 'player-2',
        name: 'Heavy Tank',
        health: 150,
        maxHealth: 200,
        position: [150, 250],
        team: 'player',
        status: 'damaged',
      },
      {
        id: 'enemy-1',
        name: 'Scout',
        health: 40,
        maxHealth: 80,
        position: [800, 300],
        team: 'enemy',
        status: 'damaged',
      },
      {
        id: 'enemy-2',
        name: 'Destroyer',
        health: 120,
        maxHealth: 180,
        position: [850, 350],
        team: 'enemy',
        status: 'active',
      },
    ],
  };

  // Mock events
  const events: BattleEvent[] = [
    {
      timestamp: 0,
      type: 'battle_start',
      data: { arena_size: [1000, 1000] },
    },
    {
      timestamp: 0.5,
      type: 'unit_spawn',
      unit_id: 'player-1',
      data: { position: [100, 200] },
    },
    {
      timestamp: 0.5,
      type: 'unit_spawn',
      unit_id: 'player-2',
      data: { position: [150, 250] },
    },
    {
      timestamp: 0.5,
      type: 'unit_spawn',
      unit_id: 'enemy-1',
      data: { position: [800, 300] },
    },
    {
      timestamp: 0.5,
      type: 'unit_spawn',
      unit_id: 'enemy-2',
      data: { position: [850, 350] },
    },
    {
      timestamp: 1.2,
      type: 'unit_move',
      unit_id: 'player-1',
      data: { from: [100, 200], to: [120, 210] },
    },
    {
      timestamp: 2.1,
      type: 'weapon_fire',
      unit_id: 'player-1',
      data: { target: 'enemy-1', weapon: 'laser' },
    },
    {
      timestamp: 2.15,
      type: 'damage_dealt',
      unit_id: 'enemy-1',
      data: { damage: 25, source: 'player-1' },
    },
    {
      timestamp: 3.5,
      type: 'ability_used',
      unit_id: 'player-2',
      data: { ability: 'shield_boost', duration: 5 },
    },
    {
      timestamp: 4.2,
      type: 'unit_move',
      unit_id: 'enemy-2',
      data: { from: [850, 350], to: [820, 340] },
    },
  ];

  const handlePlay = () => {
    setStatus('running');
    console.log('Play button clicked');
  };

  const handlePause = () => {
    setStatus('paused');
    console.log('Pause button clicked');
  };

  const handleStep = () => {
    setCurrentTurn((prev) => Math.min(prev + 1, 100));
    console.log('Step button clicked');
  };

  const handleReset = () => {
    setStatus('idle');
    setCurrentTurn(0);
    console.log('Reset button clicked');
  };

  const handleSpeedChange = (newSpeed: number) => {
    setSpeed(newSpeed);
    console.log('Speed changed to:', newSpeed);
  };

  const handleUnitClick = (unitId: string) => {
    console.log('Unit clicked:', unitId);
  };

  const containerStyles: React.CSSProperties = {
    display: 'grid',
    gridTemplateColumns: '1fr 350px',
    gap: '1.5rem',
    padding: '1.5rem',
    backgroundColor: '#f9fafb',
    minHeight: '100vh',
  };

  const mainColumnStyles: React.CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    gap: '1.5rem',
  };

  const sidebarStyles: React.CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    gap: '1.5rem',
  };

  const headerStyles: React.CSSProperties = {
    backgroundColor: '#ffffff',
    padding: '1.5rem',
    borderRadius: '0.5rem',
    boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
  };

  const titleStyles: React.CSSProperties = {
    margin: 0,
    fontSize: '1.875rem',
    fontWeight: 700,
    color: '#111827',
  };

  const subtitleStyles: React.CSSProperties = {
    margin: '0.5rem 0 0 0',
    fontSize: '1rem',
    color: '#6b7280',
  };

  return (
    <div style={containerStyles}>
      <div style={mainColumnStyles}>
        <div style={headerStyles}>
          <h1 style={titleStyles}>Battle Automata - Component Demo</h1>
          <p style={subtitleStyles}>
            Phase 1.3: UI Components (Before State Management Integration)
          </p>
        </div>

        <BattleViewer
          battleState={battleState}
          onUnitClick={handleUnitClick}
          height="600px"
        />

        <EventLog events={events} maxHeight="300px" />
      </div>

      <div style={sidebarStyles}>
        <BattleControls
          status={status}
          speed={speed}
          onPlay={handlePlay}
          onPause={handlePause}
          onStep={handleStep}
          onReset={handleReset}
          onSpeedChange={handleSpeedChange}
          currentTurn={currentTurn}
          totalTurns={100}
        />
      </div>
    </div>
  );
}
