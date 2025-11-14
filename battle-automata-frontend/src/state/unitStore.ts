/**
 * Unit Store - Zustand store for unit library management
 *
 * Manages unit definitions, unit library, and persistence
 */

import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import type { Unit } from '../utils/types';

// ============================================================================
// Types
// ============================================================================

export interface UnitLibraryEntry {
  id: string;
  unit: Unit;
  createdAt: number;
  updatedAt: number;
  description?: string;
  tags?: string[];
}

export interface UnitState {
  // Unit library
  units: Record<string, UnitLibraryEntry>;

  // Current working unit (for builder)
  currentUnit: Unit | null;

  // Actions
  addUnit: (unit: Unit, description?: string, tags?: string[]) => void;
  removeUnit: (unitId: string) => void;
  updateUnit: (unitId: string, unit: Unit, description?: string, tags?: string[]) => void;
  loadUnit: (unitId: string) => void;
  clearCurrentUnit: () => void;
  setCurrentUnit: (unit: Unit) => void;
  getUnit: (unitId: string) => UnitLibraryEntry | undefined;
  getAllUnits: () => UnitLibraryEntry[];
  searchUnits: (query: string) => UnitLibraryEntry[];
  duplicateUnit: (unitId: string, newName: string) => void;
  exportUnit: (unitId: string) => string;
  importUnit: (jsonData: string) => void;
}

// ============================================================================
// Helpers
// ============================================================================

/**
 * Generate a unique ID for a unit
 */
const generateUnitId = (name: string): string => {
  const timestamp = Date.now();
  const sanitized = name.toLowerCase().replace(/[^a-z0-9]/g, '_');
  return `${sanitized}_${timestamp}`;
};

/**
 * Validate unit data
 */
const validateUnit = (unit: Unit): boolean => {
  if (!unit.id || !unit.name || !unit.theme) {
    return false;
  }
  if (!unit.layout || !unit.layout.size || unit.layout.size.length !== 2) {
    return false;
  }
  if (!unit.resources || typeof unit.resources.power !== 'number' || typeof unit.resources.weight_limit !== 'number') {
    return false;
  }
  if (!Array.isArray(unit.components)) {
    return false;
  }
  return true;
};

// ============================================================================
// Store
// ============================================================================

export const useUnitStore = create<UnitState>()(
  persist(
    (set, get) => ({
      // Initial state
      units: {},
      currentUnit: null,

      // Actions
      addUnit: (unit: Unit, description?: string, tags?: string[]) => {
        // Validate unit
        if (!validateUnit(unit)) {
          console.error('Invalid unit data:', unit);
          throw new Error('Invalid unit data');
        }

        const now = Date.now();
        const entry: UnitLibraryEntry = {
          id: unit.id,
          unit,
          createdAt: now,
          updatedAt: now,
          description,
          tags: tags || [],
        };

        set((state) => ({
          units: {
            ...state.units,
            [unit.id]: entry,
          },
        }));

        console.log(`Unit added: ${unit.name} (${unit.id})`);
      },

      removeUnit: (unitId: string) => {
        set((state) => {
          const { [unitId]: removed, ...remainingUnits } = state.units;

          // Clear current unit if it's the one being removed
          const newCurrentUnit = state.currentUnit?.id === unitId ? null : state.currentUnit;

          return {
            units: remainingUnits,
            currentUnit: newCurrentUnit,
          };
        });

        console.log(`Unit removed: ${unitId}`);
      },

      updateUnit: (unitId: string, unit: Unit, description?: string, tags?: string[]) => {
        // Validate unit
        if (!validateUnit(unit)) {
          console.error('Invalid unit data:', unit);
          throw new Error('Invalid unit data');
        }

        set((state) => {
          const existingEntry = state.units[unitId];

          if (!existingEntry) {
            console.error(`Unit not found: ${unitId}`);
            return state;
          }

          const updatedEntry: UnitLibraryEntry = {
            ...existingEntry,
            unit,
            updatedAt: Date.now(),
            description: description !== undefined ? description : existingEntry.description,
            tags: tags !== undefined ? tags : existingEntry.tags,
          };

          return {
            units: {
              ...state.units,
              [unitId]: updatedEntry,
            },
            // Update current unit if it's the one being updated
            currentUnit: state.currentUnit?.id === unitId ? unit : state.currentUnit,
          };
        });

        console.log(`Unit updated: ${unit.name} (${unitId})`);
      },

      loadUnit: (unitId: string) => {
        const state = get();
        const entry = state.units[unitId];

        if (!entry) {
          console.error(`Unit not found: ${unitId}`);
          return;
        }

        set({ currentUnit: entry.unit });
        console.log(`Unit loaded: ${entry.unit.name} (${unitId})`);
      },

      clearCurrentUnit: () => {
        set({ currentUnit: null });
        console.log('Current unit cleared');
      },

      setCurrentUnit: (unit: Unit) => {
        // Validate unit
        if (!validateUnit(unit)) {
          console.error('Invalid unit data:', unit);
          throw new Error('Invalid unit data');
        }

        set({ currentUnit: unit });
        console.log(`Current unit set: ${unit.name}`);
      },

      getUnit: (unitId: string) => {
        const state = get();
        return state.units[unitId];
      },

      getAllUnits: () => {
        const state = get();
        return Object.values(state.units).sort((a, b) => b.updatedAt - a.updatedAt);
      },

      searchUnits: (query: string) => {
        const state = get();
        const lowerQuery = query.toLowerCase();

        return Object.values(state.units).filter((entry) => {
          const nameMatch = entry.unit.name.toLowerCase().includes(lowerQuery);
          const descMatch = entry.description?.toLowerCase().includes(lowerQuery);
          const tagMatch = entry.tags?.some((tag) => tag.toLowerCase().includes(lowerQuery));
          const themeMatch = entry.unit.theme.toLowerCase().includes(lowerQuery);

          return nameMatch || descMatch || tagMatch || themeMatch;
        }).sort((a, b) => b.updatedAt - a.updatedAt);
      },

      duplicateUnit: (unitId: string, newName: string) => {
        const state = get();
        const entry = state.units[unitId];

        if (!entry) {
          console.error(`Unit not found: ${unitId}`);
          return;
        }

        const newUnit: Unit = {
          ...entry.unit,
          id: generateUnitId(newName),
          name: newName,
        };

        get().addUnit(
          newUnit,
          entry.description ? `Copy of ${entry.description}` : undefined,
          entry.tags
        );

        console.log(`Unit duplicated: ${entry.unit.name} -> ${newName}`);
      },

      exportUnit: (unitId: string) => {
        const state = get();
        const entry = state.units[unitId];

        if (!entry) {
          console.error(`Unit not found: ${unitId}`);
          throw new Error(`Unit not found: ${unitId}`);
        }

        const exportData = {
          version: '1.0',
          exported_at: new Date().toISOString(),
          unit: entry.unit,
          metadata: {
            description: entry.description,
            tags: entry.tags,
          },
        };

        return JSON.stringify(exportData, null, 2);
      },

      importUnit: (jsonData: string) => {
        try {
          const data = JSON.parse(jsonData);

          if (!data.unit) {
            throw new Error('Invalid import data: missing unit');
          }

          const unit: Unit = data.unit;

          // Validate unit
          if (!validateUnit(unit)) {
            throw new Error('Invalid unit data in import');
          }

          // Generate new ID if unit already exists
          const state = get();
          let finalUnit = unit;

          if (state.units[unit.id]) {
            finalUnit = {
              ...unit,
              id: generateUnitId(unit.name),
            };
            console.log(`Unit ID conflict, generated new ID: ${finalUnit.id}`);
          }

          get().addUnit(
            finalUnit,
            data.metadata?.description,
            data.metadata?.tags
          );

          console.log(`Unit imported: ${finalUnit.name} (${finalUnit.id})`);
        } catch (error) {
          console.error('Failed to import unit:', error);
          throw new Error(`Failed to import unit: ${error instanceof Error ? error.message : String(error)}`);
        }
      },
    }),
    {
      name: 'battle-automata-units',
      storage: createJSONStorage(() => localStorage),
    }
  )
);

// ============================================================================
// Utility Functions
// ============================================================================

/**
 * Create a default empty unit
 */
export const createEmptyUnit = (name: string = 'New Unit', theme: string = 'space-ships'): Unit => {
  return {
    id: generateUnitId(name),
    name,
    theme,
    layout: {
      size: [10, 10],
    },
    components: [],
    resources: {
      power: 100,
      weight_limit: 500,
    },
  };
};

/**
 * Clone a unit with a new ID
 */
export const cloneUnit = (unit: Unit, newName?: string): Unit => {
  const name = newName || `${unit.name} (Copy)`;
  return {
    ...unit,
    id: generateUnitId(name),
    name,
  };
};
