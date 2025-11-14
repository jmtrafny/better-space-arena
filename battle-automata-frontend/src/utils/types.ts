/**
 * TypeScript types for Battle Automata Engine
 *
 * Mirrors Python data structures for type safety across the JS/Python boundary
 */

// ============================================================================
// Battle Results
// ============================================================================

export interface BattleEvent {
  timestamp: number;
  type: string;
  unit_id?: string;
  data: Record<string, unknown>;
}

export interface BattleResult {
  winner: string | null;
  duration: number;
  events: BattleEvent[];
  final_state: {
    units: Record<string, unknown>;
  };
}

// ============================================================================
// Components
// ============================================================================

export interface ComponentStats {
  damage?: number;
  armor?: number;
  shield?: number;
  speed?: number;
  range?: number;
  fire_rate?: number;
  accuracy?: number;
  power_output?: number;
  [key: string]: number | undefined;
}

export interface ComponentResources {
  power_draw: number;
  weight: number;
  slots: number;
}

export interface Component {
  id: string;
  name: string;
  type: 'offensive' | 'defensive' | 'mobility' | 'support';
  category: string;
  stats: ComponentStats;
  resources: ComponentResources;
  special?: Record<string, unknown>;
}

// ============================================================================
// Units
// ============================================================================

export interface UnitLayout {
  size: [number, number];
}

export interface ComponentPlacement {
  type: string;
  position: [number, number];
  facing?: string;
}

export interface UnitResources {
  power: number;
  weight_limit: number;
}

export interface Unit {
  id: string;
  name: string;
  theme: string;
  layout: UnitLayout;
  components: ComponentPlacement[];
  resources: UnitResources;
}

// ============================================================================
// Battle Configuration
// ============================================================================

export interface BattleConfig {
  seed?: number;
  arena_size?: [number, number];
  max_duration?: number;
  time_step?: number;
}

// ============================================================================
// Theme
// ============================================================================

export interface ThemeMetadata {
  id: string;
  name: string;
  description: string;
  version: string;
}
