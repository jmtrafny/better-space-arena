import React from 'react';

/**
 * BattleViewer Component
 *
 * Main container for battle visualization
 * Currently shows a placeholder for PixiJS canvas (Phase 2)
 * Displays battle state information like current turn, units, and health bars
 */

export interface UnitState {
  id: string;
  name: string;
  health: number;
  maxHealth: number;
  position: [number, number];
  team: 'player' | 'enemy';
  status?: 'active' | 'damaged' | 'destroyed';
}

export interface BattleState {
  currentTurn: number;
  maxTurns: number;
  units: UnitState[];
  status: 'idle' | 'running' | 'paused' | 'completed';
  winner?: string | null;
}

export interface BattleViewerProps {
  battleState: BattleState;
  onUnitClick?: (unitId: string) => void;
  width?: string;
  height?: string;
}

export default function BattleViewer({
  battleState,
  onUnitClick,
  width = '100%',
  height = '600px'
}: BattleViewerProps) {
  const containerStyles: React.CSSProperties = {
    width,
    height,
    backgroundColor: '#1f2937',
    borderRadius: '0.5rem',
    overflow: 'hidden',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
    display: 'flex',
    flexDirection: 'column',
  };

  const headerStyles: React.CSSProperties = {
    padding: '1rem',
    backgroundColor: '#111827',
    borderBottom: '2px solid #374151',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  };

  const titleStyles: React.CSSProperties = {
    margin: 0,
    fontSize: '1.125rem',
    fontWeight: 600,
    color: '#f9fafb',
  };

  const turnDisplayStyles: React.CSSProperties = {
    fontSize: '0.875rem',
    color: '#9ca3af',
    fontFamily: 'monospace',
  };

  const canvasPlaceholderStyles: React.CSSProperties = {
    flex: 1,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#0f172a',
    position: 'relative',
    minHeight: '400px',
  };

  const placeholderTextStyles: React.CSSProperties = {
    color: '#6b7280',
    fontSize: '1rem',
    fontStyle: 'italic',
  };

  const unitsOverlayStyles: React.CSSProperties = {
    position: 'absolute',
    top: '1rem',
    right: '1rem',
    display: 'flex',
    flexDirection: 'column',
    gap: '0.5rem',
    maxWidth: '250px',
  };

  const getStatusColor = (status: string): string => {
    switch (status) {
      case 'active':
        return '#22c55e';
      case 'damaged':
        return '#f59e0b';
      case 'destroyed':
        return '#ef4444';
      default:
        return '#6b7280';
    }
  };

  const getTeamColor = (team: 'player' | 'enemy'): string => {
    return team === 'player' ? '#3b82f6' : '#ef4444';
  };

  const renderUnitCard = (unit: UnitState) => {
    const healthPercentage = (unit.health / unit.maxHealth) * 100;
    const status = unit.status || 'active';

    const cardStyles: React.CSSProperties = {
      backgroundColor: 'rgba(17, 24, 39, 0.9)',
      border: `2px solid ${getTeamColor(unit.team)}`,
      borderRadius: '0.375rem',
      padding: '0.75rem',
      cursor: onUnitClick ? 'pointer' : 'default',
      transition: 'all 0.2s',
    };

    const unitNameStyles: React.CSSProperties = {
      margin: 0,
      fontSize: '0.875rem',
      fontWeight: 600,
      color: '#f9fafb',
      marginBottom: '0.5rem',
    };

    const healthBarContainerStyles: React.CSSProperties = {
      height: '8px',
      backgroundColor: '#374151',
      borderRadius: '4px',
      overflow: 'hidden',
      marginBottom: '0.25rem',
    };

    const healthBarFillStyles: React.CSSProperties = {
      height: '100%',
      width: `${healthPercentage}%`,
      backgroundColor: getStatusColor(status),
      transition: 'width 0.3s',
    };

    const healthTextStyles: React.CSSProperties = {
      fontSize: '0.75rem',
      color: '#9ca3af',
      fontFamily: 'monospace',
    };

    return (
      <div
        key={unit.id}
        style={cardStyles}
        onClick={() => onUnitClick?.(unit.id)}
      >
        <p style={unitNameStyles}>{unit.name}</p>
        <div style={healthBarContainerStyles}>
          <div style={healthBarFillStyles} />
        </div>
        <p style={healthTextStyles}>
          HP: {unit.health}/{unit.maxHealth}
        </p>
      </div>
    );
  };

  const statusBadgeStyles: React.CSSProperties = {
    padding: '0.25rem 0.75rem',
    borderRadius: '0.25rem',
    fontSize: '0.875rem',
    fontWeight: 600,
    backgroundColor: battleState.status === 'running' ? '#22c55e' :
                     battleState.status === 'paused' ? '#f59e0b' :
                     battleState.status === 'completed' ? '#3b82f6' : '#6b7280',
    color: '#ffffff',
  };

  return (
    <div style={containerStyles}>
      <div style={headerStyles}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <h2 style={titleStyles}>Battle Arena</h2>
          <span style={statusBadgeStyles}>
            {battleState.status.toUpperCase()}
          </span>
        </div>
        <div style={turnDisplayStyles}>
          Turn: {battleState.currentTurn} / {battleState.maxTurns}
        </div>
      </div>

      <div style={canvasPlaceholderStyles}>
        <p style={placeholderTextStyles}>
          PixiJS Canvas Placeholder (Phase 2)
        </p>

        <div style={unitsOverlayStyles}>
          {battleState.units
            .filter(u => u.status !== 'destroyed')
            .map(renderUnitCard)}
        </div>
      </div>

      {battleState.status === 'completed' && battleState.winner && (
        <div style={{
          padding: '1rem',
          backgroundColor: '#065f46',
          color: '#ffffff',
          textAlign: 'center',
          fontWeight: 600,
        }}>
          Winner: {battleState.winner}
        </div>
      )}
    </div>
  );
}
