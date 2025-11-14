import React, { useEffect, useRef, useImperativeHandle, forwardRef } from 'react';
import { BattleRenderer } from '../../game/BattleRenderer';
import { BattleAnimator } from '../../game/BattleAnimator';

/**
 * BattleViewer Component
 *
 * Main container for battle visualization with PixiJS rendering
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

export interface BattleViewerRef {
  getBattleAnimator: () => BattleAnimator | null;
  getRenderer: () => BattleRenderer | null;
}

const BattleViewer = forwardRef<BattleViewerRef, BattleViewerProps>(({
  battleState,
  onUnitClick,
  width = '100%',
  height = '600px'
}, ref) => {
  // Refs for PixiJS integration
  const canvasContainerRef = useRef<HTMLDivElement>(null);
  const rendererRef = useRef<BattleRenderer | null>(null);

  // Expose methods via ref
  useImperativeHandle(ref, () => ({
    getBattleAnimator: () => rendererRef.current?.getBattleAnimator() || null,
    getRenderer: () => rendererRef.current,
  }));

  // Initialize PixiJS renderer
  useEffect(() => {
    let mounted = true;

    const initRenderer = async () => {
      if (!canvasContainerRef.current || !mounted) return;

      try {
        const renderer = new BattleRenderer({
          arenaWidth: 1000,
          arenaHeight: 1000,
          backgroundColor: 0x001122,
          showDebugInfo: true, // Show FPS counter in Phase 1
        });

        await renderer.init(canvasContainerRef.current);

        if (mounted) {
          rendererRef.current = renderer;
          console.log('PixiJS BattleRenderer initialized successfully');
        } else {
          renderer.cleanup();
        }
      } catch (error) {
        console.error('Failed to initialize BattleRenderer:', error);
      }
    };

    initRenderer();

    // Cleanup on unmount
    return () => {
      mounted = false;
      if (rendererRef.current) {
        rendererRef.current.cleanup();
        rendererRef.current = null;
      }
    };
  }, []); // Only run once on mount
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

  const canvasContainerStyles: React.CSSProperties = {
    flex: 1,
    position: 'relative',
    minHeight: '400px',
    backgroundColor: '#0f172a',
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

      <div ref={canvasContainerRef} style={canvasContainerStyles}>
        {/* PixiJS canvas will be injected here */}

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
});

BattleViewer.displayName = 'BattleViewer';

export default BattleViewer;
