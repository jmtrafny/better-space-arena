/**
 * Theme Store - Zustand store for theme state management
 *
 * Manages theme state (light/dark mode) with localStorage persistence
 */

import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

// ============================================================================
// Types
// ============================================================================

export type ThemeMode = 'light' | 'dark';

export interface ThemeState {
  // Theme state
  mode: ThemeMode;

  // Actions
  toggleTheme: () => void;
  setTheme: (mode: ThemeMode) => void;
}

// ============================================================================
// Helpers
// ============================================================================

/**
 * Get system theme preference
 */
const getSystemTheme = (): ThemeMode => {
  if (typeof window === 'undefined') {
    return 'dark';
  }

  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  return prefersDark ? 'dark' : 'light';
};

/**
 * Apply theme to document
 */
const applyThemeToDocument = (mode: ThemeMode) => {
  if (typeof document === 'undefined') {
    return;
  }

  // Update document class for CSS theming
  document.documentElement.classList.remove('light', 'dark');
  document.documentElement.classList.add(mode);

  // Update data attribute for compatibility
  document.documentElement.setAttribute('data-theme', mode);

  console.log(`Theme applied: ${mode}`);
};

// ============================================================================
// Store
// ============================================================================

export const useThemeStore = create<ThemeState>()(
  persist(
    (set, get) => ({
      // Initial state - defaults to system preference
      mode: getSystemTheme(),

      // Actions
      toggleTheme: () => {
        const currentMode = get().mode;
        const newMode: ThemeMode = currentMode === 'light' ? 'dark' : 'light';

        set({ mode: newMode });
        applyThemeToDocument(newMode);

        console.log(`Theme toggled: ${currentMode} -> ${newMode}`);
      },

      setTheme: (mode: ThemeMode) => {
        set({ mode });
        applyThemeToDocument(mode);

        console.log(`Theme set: ${mode}`);
      },
    }),
    {
      name: 'battle-automata-theme',
      storage: createJSONStorage(() => localStorage),
      // Apply theme when hydrated from storage
      onRehydrateStorage: () => (state) => {
        if (state) {
          applyThemeToDocument(state.mode);
        }
      },
    }
  )
);

// ============================================================================
// Initialization
// ============================================================================

/**
 * Initialize theme on app load
 * Call this in your main app entry point
 */
export const initializeTheme = () => {
  const currentTheme = useThemeStore.getState().mode;
  applyThemeToDocument(currentTheme);

  // Listen for system theme changes
  if (typeof window !== 'undefined') {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

    const handleSystemThemeChange = (e: MediaQueryListEvent) => {
      // Only update if user hasn't manually set a preference
      const hasManualPreference = localStorage.getItem('battle-automata-theme');
      if (!hasManualPreference) {
        const newTheme: ThemeMode = e.matches ? 'dark' : 'light';
        useThemeStore.getState().setTheme(newTheme);
      }
    };

    mediaQuery.addEventListener('change', handleSystemThemeChange);

    console.log('Theme initialization complete');
  }
};
