import { useEffect, useState, useRef } from 'react';
import { Link } from 'react-router-dom';
import { useBattleStore } from '../state';
import { pyodideLoader } from '../engine/pyodide-loader';
import BattleViewer, { type BattleViewerRef } from '../components/battle/BattleViewer';
import BattleControls from '../components/battle/BattleControls';
import EventLog from '../components/battle/EventLog';
import type { BattleState as ViewerBattleState, UnitState } from '../components/battle/BattleViewer';
import { BattleAnimator } from '../game/BattleAnimator';

export default function Battle() {
  // Get battle store state and actions
  const {
    status,
    result,
    error,
    loadingProgress,
    winner,
    duration,
    events,
    startBattle,
    setLoadingProgress,
  } = useBattleStore();

  const [playbackSpeed, setPlaybackSpeed] = useState(1.0);
  const [battleAnimator, setBattleAnimator] = useState<BattleAnimator | null>(null);
  const [currentTime, setCurrentTime] = useState(0);
  const [totalDuration, setTotalDuration] = useState(0);
  const [currentEventIndex, setCurrentEventIndex] = useState<number | undefined>(undefined);
  const [animatorState, setAnimatorState] = useState<'idle' | 'running' | 'paused' | 'completed'>('idle');

  const viewerRef = useRef<BattleViewerRef>(null);

  // Subscribe to Pyodide loading state
  useEffect(() => {
    const unsubscribe = pyodideLoader.onStateChange((state) => {
      setLoadingProgress(state.progress);
    });

    return () => {
      unsubscribe();
    };
  }, [setLoadingProgress]);

  // Get BattleAnimator from viewer after it initializes
  useEffect(() => {
    const timer = setInterval(() => {
      if (viewerRef.current && !battleAnimator) {
        const animator = viewerRef.current.getBattleAnimator();
        if (animator) {
          setBattleAnimator(animator);
          clearInterval(timer);
        }
      }
    }, 100);

    return () => clearInterval(timer);
  }, [battleAnimator]);

  // Load battle into animator when result arrives
  useEffect(() => {
    if (result && battleAnimator && status === 'completed') {
      console.log('Loading battle into animator');
      battleAnimator.loadBattle(result);
      setTotalDuration(battleAnimator.getTotalDuration());
      setCurrentTime(0);
      setAnimatorState('paused');
    }
  }, [result, battleAnimator, status]);

  // Update playback state periodically during animation
  useEffect(() => {
    if (!battleAnimator) return;

    const interval = setInterval(() => {
      const state = battleAnimator.getState();
      setAnimatorState(state as any);
      setCurrentTime(battleAnimator.getCurrentTime());

      // Calculate current event index based on time
      if (result?.events) {
        const idx = result.events.findIndex(e => e.timestamp > battleAnimator.getCurrentTime());
        setCurrentEventIndex(idx > 0 ? idx - 1 : 0);
      }
    }, 50); // Update UI at ~20fps

    return () => clearInterval(interval);
  }, [battleAnimator, result]);

  const handleRunBattle = async () => {
    // Use actual unit definitions from Python engine
    // These units will be loaded from data/themes/space-ships/units/
    const unit1 = {
      id: 'fighter_mk1',
      name: 'Fighter Mk1',
      theme: 'space-ships',
      layout: { size: [10, 10] as [number, number] },
      components: [
        { type: 'laser_cannon_mk1', position: [5, 2] as [number, number], facing: '0' },
        { type: 'laser_cannon_mk1', position: [4, 2] as [number, number], facing: '0' },
        { type: 'light_armor_mk1', position: [5, 5] as [number, number], facing: '0' },
        { type: 'fusion_reactor_small', position: [5, 5] as [number, number], facing: '0' },
        { type: 'ion_engine_mk1', position: [5, 8] as [number, number], facing: '180' },
      ],
      resources: { power: 200, weight_limit: 500 },
    };

    const unit2 = {
      id: 'tank_mk1',
      name: 'Tank Mk1',
      theme: 'space-ships',
      layout: { size: [12, 12] as [number, number] },
      components: [
        { type: 'laser_cannon_mk1', position: [6, 2] as [number, number], facing: '0' },
        { type: 'light_armor_mk1', position: [6, 4] as [number, number], facing: '0' },
        { type: 'light_armor_mk1', position: [6, 6] as [number, number], facing: '0' },
        { type: 'light_armor_mk1', position: [6, 8] as [number, number], facing: '0' },
        { type: 'fusion_reactor_small', position: [6, 6] as [number, number], facing: '0' },
        { type: 'ion_engine_mk1', position: [6, 10] as [number, number], facing: '180' },
      ],
      resources: { power: 200, weight_limit: 800 },
    };

    const config = {
      seed: 12345,
      arena_size: [1000, 1000] as [number, number],
      max_duration: 60.0,
      time_step: 0.1,
    };

    await startBattle(unit1, unit2, config);
  };

  const isLoading = status === 'initializing';

  // Convert battle store state to viewer state
  const viewerBattleState: ViewerBattleState = {
    currentTurn: events.length,
    maxTurns: Math.floor((60.0 / 0.1)), // max_duration / time_step
    units: result ? convertResultToUnits(result) : [],
    status: status === 'initializing' ? 'idle' :
            status === 'running' ? 'running' :
            status === 'paused' ? 'paused' :
            status === 'completed' ? 'completed' : 'idle',
    winner: winner || null,
  };

  // Helper to convert battle result to unit states
  function convertResultToUnits(battleResult: typeof result): UnitState[] {
    if (!battleResult?.final_state) return [];

    const units: UnitState[] = [];

    // Extract unit data from final_state
    // final_state.units is a list of unit dicts from Python
    if (battleResult.final_state.units && Array.isArray(battleResult.final_state.units)) {
      battleResult.final_state.units.forEach((unit: any) => {
        const totalHealth = unit.total_health || 0;
        const maxHealth = unit.components?.reduce((sum: number, c: any) => sum + (c.max_health || 0), 0) || 100;

        units.push({
          id: unit.unit_id,
          name: unit.unit_id === 'unit_1' ? 'Fighter Mk1' : 'Tank Mk1',
          health: totalHealth,
          maxHealth: maxHealth,
          position: unit.position ? [unit.position.x, unit.position.y] : [0, 0],
          team: unit.team === 'team_a' ? 'player' : 'enemy',
          status: unit.is_destroyed ? 'destroyed' :
                  totalHealth < maxHealth * 0.5 ? 'damaged' : 'active',
        });
      });
    }

    // If no units found, create fallback based on winner
    if (units.length === 0) {
      units.push(
        {
          id: 'unit_1',
          name: 'Fighter Mk1',
          health: winner === 'team_a' ? 80 : 0,
          maxHealth: 300,
          position: [100, 500],
          team: 'player',
          status: winner === 'team_a' ? 'active' : 'destroyed',
        },
        {
          id: 'unit_2',
          name: 'Tank Mk1',
          health: winner === 'team_b' ? 100 : 0,
          maxHealth: 300,
          position: [900, 500],
          team: 'enemy',
          status: winner === 'team_b' ? 'active' : 'destroyed',
        }
      );
    }

    return units;
  }

  return (
    <div style={{ padding: '2rem', minHeight: '100vh' }}>
      <div style={{ maxWidth: '1400px', margin: '0 auto' }}>
        <div style={{ marginBottom: '2rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h1 style={{ margin: 0, marginBottom: '0.5rem' }}>Battle Simulator</h1>
            <p style={{ margin: 0, color: '#6b7280' }}>Full battle visualization with Python engine integration</p>
          </div>
          <Link to="/">
            <button style={{
              padding: '0.5rem 1rem',
              borderRadius: '0.375rem',
              border: '1px solid #4b5563',
              backgroundColor: '#374151',
              color: '#e5e5e5',
              cursor: 'pointer'
            }}>
              ← Back to Home
            </button>
          </Link>
        </div>

        {isLoading && (
          <div style={{ marginBottom: '2rem', padding: '1rem', background: '#1e3a8a', border: '1px solid #3b82f6', borderRadius: '0.5rem' }}>
            <p style={{ margin: 0, marginBottom: '0.5rem', fontWeight: 600, color: '#e5e5e5' }}>Loading Pyodide... {loadingProgress}%</p>
            <progress value={loadingProgress} max={100} style={{ width: '100%', height: '8px' }} />
          </div>
        )}

        {error && (
          <div style={{ marginBottom: '2rem', padding: '1rem', background: '#7f1d1d', border: '1px solid #ef4444', color: '#fca5a5', borderRadius: '0.5rem' }}>
            <strong>Error:</strong> {error}
          </div>
        )}

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 400px', gap: '2rem', marginBottom: '2rem' }}>
          <div>
            <BattleViewer
              ref={viewerRef}
              battleState={viewerBattleState}
              onUnitClick={(unitId) => console.log('Unit clicked:', unitId)}
            />
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <BattleControls
              status={status === 'completed' && result ? animatorState : status as any}
              speed={playbackSpeed}
              onPlay={() => {
                if (status !== 'completed') {
                  // Run the battle simulation
                  handleRunBattle();
                } else if (battleAnimator) {
                  // Battle already complete, just play animation
                  battleAnimator.play();
                }
              }}
              onPause={() => battleAnimator?.pause()}
              onStep={() => battleAnimator?.stepForward()}
              onReset={() => {
                battleAnimator?.stop();
                setCurrentTime(0);
                setCurrentEventIndex(0);
              }}
              onSpeedChange={(speed) => {
                setPlaybackSpeed(speed);
                battleAnimator?.setSpeed(speed);
              }}
              onSeek={(time) => battleAnimator?.seekTo(time)}
              onStepForward={() => battleAnimator?.stepForward()}
              onStepBackward={() => battleAnimator?.stepBackward()}
              currentTime={currentTime}
              totalDuration={totalDuration}
              currentTurn={events.length}
              totalTurns={600}
              isLoading={isLoading}
            />

            {status === 'completed' && result && (
              <div style={{ padding: '1rem', background: '#064e3b', border: '1px solid #22c55e', borderRadius: '0.5rem' }}>
                <h3 style={{ margin: 0, marginBottom: '0.5rem', color: '#e5e5e5' }}>Battle Complete</h3>
                <p style={{ margin: 0, color: '#d1d5db' }}><strong>Winner:</strong> {winner || 'Draw'}</p>
                <p style={{ margin: 0, color: '#d1d5db' }}><strong>Duration:</strong> {duration.toFixed(2)}s</p>
              </div>
            )}
          </div>
        </div>

        <div>
          <EventLog
            events={events}
            maxHeight="400px"
            currentEventIndex={currentEventIndex}
            onEventClick={(index) => {
              if (result?.events && result.events[index]) {
                battleAnimator?.seekTo(result.events[index].timestamp);
              }
            }}
          />
        </div>
      </div>
    </div>
  );
}
