/**
 * State Management - Centralized export for all Zustand stores
 *
 * This file provides a single entry point for importing stores throughout the application.
 */

// ============================================================================
// Store Exports
// ============================================================================

export { useBattleStore } from './battleStore';
export type { BattleState, BattleStatus } from './battleStore';

export { useThemeStore, initializeTheme } from './themeStore';
export type { ThemeState, ThemeMode } from './themeStore';

export { useUnitStore, createEmptyUnit, cloneUnit } from './unitStore';
export type { UnitState, UnitLibraryEntry } from './unitStore';

// ============================================================================
// Store Utilities
// ============================================================================

// Import stores for use in utility functions
import { useBattleStore } from './battleStore';
import { useThemeStore, initializeTheme } from './themeStore';
import { useUnitStore } from './unitStore';

/**
 * Reset all stores to initial state
 * Useful for testing or logout scenarios
 */
export const resetAllStores = () => {
  useBattleStore.getState().resetBattle();
  useUnitStore.getState().clearCurrentUnit();
  // Note: Theme store is intentionally not reset to preserve user preference
  console.log('All stores reset (except theme)');
};

/**
 * Get all store states (for debugging)
 */
export const getAllStoreStates = () => {
  return {
    battle: useBattleStore.getState(),
    theme: useThemeStore.getState(),
    unit: useUnitStore.getState(),
  };
};

/**
 * Initialize all stores
 * Call this once at application startup
 */
export const initializeStores = async () => {
  console.log('Initializing stores...');

  // Initialize theme (applies theme to document)
  initializeTheme();

  // Battle engine initialization is lazy (happens on first battle)
  // Units are loaded from localStorage automatically by zustand persist

  console.log('Stores initialized successfully');
};
