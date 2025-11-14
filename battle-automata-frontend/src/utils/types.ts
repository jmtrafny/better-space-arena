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
  turn?: number;
  event_type?: string;
  data: Record<string, unknown>;
  // Legacy support for old format
  type?: string;
  unit_id?: string;
}

export interface BattleStatistics {
  winner: string | null;
  outcome_reason: string;
  total_turns: number;
  total_time: number;
  accuracy: number;
  total_shots_fired: number;
  total_hits: number;
  total_misses: number;
  total_critical_hits: number;
}

export interface BattleResult {
  config: Record<string, unknown>;
  statistics: BattleStatistics;
  events: BattleEvent[];
  final_state: {
    turn: number;
    time_elapsed: number;
    units: unknown[];
    winner: string | null;
    outcome: string | null;
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
