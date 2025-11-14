/**
 * Battle Store - Zustand store for battle state management
 *
 * Manages battle state, actions, and integration with BattleEngineWASM
 */

import { create } from 'zustand';
import { battleEngine } from '../engine/battle-engine-wasm';
import type { BattleResult, BattleEvent, BattleConfig, Unit } from '../utils/types';

// ============================================================================
// Types
// ============================================================================

export type BattleStatus = 'idle' | 'initializing' | 'running' | 'paused' | 'completed' | 'error';

export interface BattleState {
  // Battle state
  status: BattleStatus;
  currentTurn: number;
  winner: string | null;
  duration: number;
  error: string | null;

  // Battle configuration
  config: BattleConfig | null;
  unit1: Unit | null;
  unit2: Unit | null;

  // Battle history
  events: BattleEvent[];
  result: BattleResult | null;

  // Loading state
  isEngineInitialized: boolean;
  loadingProgress: number;

  // Actions
  initializeEngine: () => Promise<void>;
  startBattle: (unit1: Unit, unit2: Unit, config?: BattleConfig) => Promise<void>;
  pauseBattle: () => void;
  resumeBattle: () => void;
  resetBattle: () => void;
  stepForward: () => void;
  setLoadingProgress: (progress: number) => void;
  setError: (error: string | null) => void;
}

// ============================================================================
// Store
// ============================================================================

export const useBattleStore = create<BattleState>((set, get) => ({
  // Initial state
  status: 'idle',
  currentTurn: 0,
  winner: null,
  duration: 0,
  error: null,

  config: null,
  unit1: null,
  unit2: null,

  events: [],
  result: null,

  isEngineInitialized: false,
  loadingProgress: 0,

  // Actions
  initializeEngine: async () => {
    const state = get();
    if (state.isEngineInitialized) {
      return;
    }

    try {
      set({ status: 'initializing', error: null, loadingProgress: 0 });

      await battleEngine.init();

      set({
        isEngineInitialized: true,
        status: 'idle',
        loadingProgress: 100
      });

      console.log('Battle engine initialized successfully');
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      set({
        status: 'error',
        error: errorMsg,
        isEngineInitialized: false
      });
      console.error('Failed to initialize battle engine:', error);
    }
  },

  startBattle: async (unit1: Unit, unit2: Unit, config?: BattleConfig) => {
    const state = get();

    // Reset any previous battle state
    set({
      status: 'initializing',
      error: null,
      currentTurn: 0,
      winner: null,
      duration: 0,
      events: [],
      result: null,
      unit1,
      unit2,
      config: config || null,
    });

    try {
      // Ensure engine is initialized
      if (!state.isEngineInitialized) {
        await get().initializeEngine();
      }

      // Start battle
      set({ status: 'running' });
      console.log('Starting battle simulation...');

      const battleResult = await battleEngine.simulateBattle(unit1, unit2, config);

      // Update state with results
      // BattleResult structure: { config, statistics, events, final_state }
      set({
        status: 'completed',
        result: battleResult,
        winner: battleResult.statistics?.winner || null,
        duration: battleResult.statistics?.total_time || 0,
        events: battleResult.events || [],
        currentTurn: battleResult.events?.length || 0,
      });

      console.log('Battle completed:', battleResult);
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      set({
        status: 'error',
        error: errorMsg
      });
      console.error('Battle simulation failed:', error);
    }
  },

  pauseBattle: () => {
    const state = get();
    if (state.status === 'running') {
      set({ status: 'paused' });
      console.log('Battle paused');
    }
  },

  resumeBattle: () => {
    const state = get();
    if (state.status === 'paused') {
      set({ status: 'running' });
      console.log('Battle resumed');
    }
  },

  resetBattle: () => {
    set({
      status: 'idle',
      currentTurn: 0,
      winner: null,
      duration: 0,
      error: null,
      config: null,
      unit1: null,
      unit2: null,
      events: [],
      result: null,
    });
    console.log('Battle reset');
  },

  stepForward: () => {
    const state = get();
    if (state.status === 'paused' && state.currentTurn < state.events.length) {
      set({ currentTurn: state.currentTurn + 1 });
      console.log(`Stepped to turn ${state.currentTurn + 1}`);
    }
  },

  setLoadingProgress: (progress: number) => {
    set({ loadingProgress: progress });
  },

  setError: (error: string | null) => {
    set({ error });
  },
}));
