import React from 'react';
import Button from '../ui/Button';

/**
 * BattleControls Component
 *
 * Provides control interface for battle playback
 * - Play/Pause/Step/Reset buttons
 * - Speed control slider
 * - Battle status display
 */

export type BattleControlStatus = 'idle' | 'running' | 'paused' | 'completed';

export interface BattleControlsProps {
  status: BattleControlStatus;
  speed: number;
  onPlay: () => void;
  onPause: () => void;
  onStep: () => void;
  onReset: () => void;
  onSpeedChange: (speed: number) => void;
  currentTurn?: number;
  totalTurns?: number;
  isLoading?: boolean;
}

export default function BattleControls({
  status,
  speed,
  onPlay,
  onPause,
  onStep,
  onReset,
  onSpeedChange,
  currentTurn = 0,
  totalTurns = 100,
  isLoading = false
}: BattleControlsProps) {
  const containerStyles: React.CSSProperties = {
    backgroundColor: '#1f2937',
    borderRadius: '0.5rem',
    boxShadow: '0 1px 3px rgba(0, 0, 0, 0.3)',
    border: '1px solid #374151',
    padding: '1.5rem',
    display: 'flex',
    flexDirection: 'column',
    gap: '1.5rem',
  };

  const sectionStyles: React.CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    gap: '0.75rem',
  };

  const labelStyles: React.CSSProperties = {
    fontSize: '0.875rem',
    fontWeight: 600,
    color: '#9ca3af',
    textTransform: 'uppercase',
    letterSpacing: '0.05em',
  };

  const buttonsContainerStyles: React.CSSProperties = {
    display: 'flex',
    gap: '0.75rem',
    flexWrap: 'wrap',
  };

  const sliderContainerStyles: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    gap: '1rem',
  };

  const sliderStyles: React.CSSProperties = {
    flex: 1,
    height: '6px',
    borderRadius: '3px',
    outline: 'none',
    WebkitAppearance: 'none',
  };

  const speedDisplayStyles: React.CSSProperties = {
    minWidth: '60px',
    textAlign: 'right',
    fontSize: '0.875rem',
    fontWeight: 600,
    color: '#e5e5e5',
    fontFamily: 'monospace',
  };

  const statusDisplayStyles: React.CSSProperties = {
    display: 'flex',
    justifyContent: 'space-between',
    padding: '0.75rem',
    backgroundColor: '#111827',
    borderRadius: '0.375rem',
    fontSize: '0.875rem',
  };

  const statusItemStyles: React.CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    gap: '0.25rem',
  };

  const statusLabelStyles: React.CSSProperties = {
    fontSize: '0.75rem',
    color: '#6b7280',
    textTransform: 'uppercase',
  };

  const statusValueStyles: React.CSSProperties = {
    fontSize: '1rem',
    fontWeight: 600,
    color: '#e5e5e5',
    fontFamily: 'monospace',
  };

  const getStatusColor = (currentStatus: BattleControlStatus): string => {
    switch (currentStatus) {
      case 'running':
        return '#22c55e';
      case 'paused':
        return '#f59e0b';
      case 'completed':
        return '#3b82f6';
      case 'idle':
      default:
        return '#6b7280';
    }
  };

  const statusBadgeStyles: React.CSSProperties = {
    display: 'inline-block',
    padding: '0.25rem 0.75rem',
    borderRadius: '0.25rem',
    fontSize: '0.875rem',
    fontWeight: 600,
    backgroundColor: getStatusColor(status),
    color: '#ffffff',
  };

  const canPlay = status === 'idle' || status === 'paused';
  const canPause = status === 'running';
  const canStep = status !== 'running';
  const canReset = status !== 'idle';

  const progressPercentage = totalTurns > 0 ? (currentTurn / totalTurns) * 100 : 0;

  const progressBarContainerStyles: React.CSSProperties = {
    height: '8px',
    backgroundColor: '#374151',
    borderRadius: '4px',
    overflow: 'hidden',
  };

  const progressBarFillStyles: React.CSSProperties = {
    height: '100%',
    width: `${progressPercentage}%`,
    backgroundColor: '#3b82f6',
    transition: 'width 0.3s',
  };

  return (
    <div style={containerStyles}>
      {/* Status Display */}
      <div style={sectionStyles}>
        <span style={labelStyles}>Battle Status</span>
        <div style={statusDisplayStyles}>
          <div style={statusItemStyles}>
            <span style={statusLabelStyles}>Status</span>
            <span style={statusBadgeStyles}>{status.toUpperCase()}</span>
          </div>
          <div style={statusItemStyles}>
            <span style={statusLabelStyles}>Turn</span>
            <span style={statusValueStyles}>
              {currentTurn} / {totalTurns}
            </span>
          </div>
          <div style={statusItemStyles}>
            <span style={statusLabelStyles}>Progress</span>
            <span style={statusValueStyles}>{progressPercentage.toFixed(0)}%</span>
          </div>
        </div>
        <div style={progressBarContainerStyles}>
          <div style={progressBarFillStyles} />
        </div>
      </div>

      {/* Playback Controls */}
      <div style={sectionStyles}>
        <span style={labelStyles}>Playback Controls</span>
        <div style={buttonsContainerStyles}>
          <Button
            variant="primary"
            onClick={onPlay}
            disabled={!canPlay || isLoading}
            loading={isLoading && canPlay}
          >
            Play
          </Button>
          <Button
            variant="secondary"
            onClick={onPause}
            disabled={!canPause || isLoading}
          >
            Pause
          </Button>
          <Button
            variant="secondary"
            onClick={onStep}
            disabled={!canStep || isLoading}
          >
            Step
          </Button>
          <Button
            variant="danger"
            onClick={onReset}
            disabled={!canReset || isLoading}
          >
            Reset
          </Button>
        </div>
      </div>

      {/* Speed Control */}
      <div style={sectionStyles}>
        <span style={labelStyles}>Playback Speed</span>
        <div style={sliderContainerStyles}>
          <input
            type="range"
            min="0.25"
            max="4"
            step="0.25"
            value={speed}
            onChange={(e) => onSpeedChange(parseFloat(e.target.value))}
            disabled={isLoading}
            style={sliderStyles}
          />
          <span style={speedDisplayStyles}>{speed.toFixed(2)}x</span>
        </div>
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          fontSize: '0.75rem',
          color: '#6b7280',
        }}>
          <span>0.25x</span>
          <span>1x</span>
          <span>2x</span>
          <span>4x</span>
        </div>
      </div>
    </div>
  );
}
