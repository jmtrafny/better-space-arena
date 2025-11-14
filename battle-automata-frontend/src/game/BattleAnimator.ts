/**
 * BattleAnimator - Synthesizes ReplayController + SpriteManager + WeaponEffects
 *
 * This is the SYNTHESIS layer for Phase 2 - combining:
 * - Track A: Sprite rendering (SpriteManager, WeaponEffects)
 * - Track B: Animation timing (ReplayController, interpolation)
 *
 * Responsibilities:
 * - Connect battle events to visual effects
 * - Interpolate unit positions between events
 * - Trigger weapon effects at correct times
 * - Update health bars based on damage events
 * - Coordinate smooth 60 FPS animation from discrete 0.1s events
 */

import { SpriteManager } from './SpriteManager';
import { WeaponEffects } from './effects/WeaponEffects';
import { ReplayController, BattleEvent } from './ReplayController';
import { interpolatePosition, PositionKeyframe } from './interpolation';
import type { BattleResult } from '../utils/types';

interface UnitData {
  id: string;
  team: 'player' | 'enemy';
  positionKeyframes: PositionKeyframe[];
  maxHealth: number;
  currentHealth: number;
}

export class BattleAnimator {
  private replayController: ReplayController | null = null;
  private spriteManager: SpriteManager;
  private weaponEffects: WeaponEffects;

  private units: Map<string, UnitData> = new Map();
  private isAnimating: boolean = false;

  // Performance profiling
  private lastProfileTime: number = 0;
  private frameTimings: number[] = [];

  constructor(
    spriteManager: SpriteManager,
    weaponEffects: WeaponEffects
  ) {
    this.spriteManager = spriteManager;
    this.weaponEffects = weaponEffects;
  }

  /**
   * Load battle data and prepare for animation
   */
  loadBattle(battleResult: BattleResult): void {
    console.log('BattleAnimator: Loading battle with', battleResult.events.length, 'events');

    // Create ReplayController with events
    this.replayController = new ReplayController(battleResult.events);

    // Extract unit data from battle result
    this.extractUnits(battleResult);

    // Set up event callbacks
    this.setupEventHandlers();

    console.log('BattleAnimator: Battle loaded, units:', this.units.size);
  }

  /**
   * Extract unit data and position keyframes from battle events
   */
  private extractUnits(battleResult: BattleResult): void {
    this.units.clear();

    // Get initial unit data from final_state
    if (battleResult.final_state?.units && Array.isArray(battleResult.final_state.units)) {
      battleResult.final_state.units.forEach((unit: any) => {
        const unitId = unit.unit_id || unit.id;
        const team = unit.team === 'team_a' ? 'player' : 'enemy';
        const maxHealth = unit.components?.reduce((sum: number, c: any) => sum + (c.max_health || 0), 0) || 100;

        this.units.set(unitId, {
          id: unitId,
          team,
          positionKeyframes: [],
          maxHealth,
          currentHealth: maxHealth,
        });
      });
    }

    // Build position keyframes from events
    battleResult.events.forEach(event => {
      const eventType = (event.event_type || event.type || '').toLowerCase();

      if (eventType === 'move' || eventType === 'position_update') {
        const unitId = (event.data as any).unit_id;
        const position = (event.data as any).position;

        if (unitId && position) {
          const unitData = this.units.get(unitId);
          if (unitData) {
            unitData.positionKeyframes.push({
              time: event.timestamp,
              x: position.x || position[0] || 0,
              y: position.y || position[1] || 0,
            });
          }
        }
      }
    });

    // Create sprites for all units
    this.units.forEach((unitData, unitId) => {
      // Get initial position (first keyframe or default)
      const initialPos = unitData.positionKeyframes[0] || { x: 500, y: 500 };

      this.spriteManager.createUnit(
        unitId,
        unitData.team,
        initialPos.x,
        initialPos.y
      );

      this.spriteManager.updateUnitHealth(
        unitId,
        unitData.currentHealth,
        unitData.maxHealth
      );

      console.log(`Created unit ${unitId} at (${initialPos.x}, ${initialPos.y})`);
    });
  }

  /**
   * Set up event handlers for battle events
   */
  private setupEventHandlers(): void {
    if (!this.replayController) return;

    this.replayController.onEvent((event: BattleEvent) => {
      this.handleBattleEvent(event);
    });
  }

  /**
   * Handle individual battle event
   */
  private handleBattleEvent(event: BattleEvent): void {
    const eventType = (event.event_type || event.type || '').toLowerCase();
    const data = event.data as any;

    switch (eventType) {
      case 'attack':
      case 'weapon_fire':
        this.handleAttackEvent(data);
        break;

      case 'damage':
      case 'damage_dealt':
        this.handleDamageEvent(data);
        break;

      case 'destroy':
      case 'unit_destroyed':
        this.handleDestroyEvent(data);
        break;

      case 'move':
      case 'position_update':
        // Position updates handled via interpolation in update()
        break;

      default:
        // Unknown event type, ignore
        break;
    }
  }

  /**
   * Handle weapon attack event
   */
  private handleAttackEvent(data: any): void {
    const attackerId = data.attacker_id || data.source;
    const targetId = data.target_id || data.target;
    const hit = data.hit !== false; // Default to true if not specified
    const critical = data.critical || false;

    if (!attackerId || !targetId) return;

    // Get current positions
    const attackerPos = this.getCurrentPosition(attackerId);
    const targetPos = this.getCurrentPosition(targetId);

    if (!attackerPos || !targetPos) return;

    // Show laser beam
    this.weaponEffects.showLaserBeam(
      attackerPos.x,
      attackerPos.y,
      targetPos.x,
      targetPos.y,
      hit
    );

    // Show hit/miss effect
    if (hit) {
      this.weaponEffects.showHitEffect(targetPos.x, targetPos.y, critical);
    } else {
      this.weaponEffects.showMissEffect(targetPos.x, targetPos.y);
    }
  }

  /**
   * Handle damage event
   */
  private handleDamageEvent(data: any): void {
    const unitId = data.unit_id || data.target;
    const damage = data.damage || 0;

    if (!unitId) return;

    const unitData = this.units.get(unitId);
    if (!unitData) return;

    // Update health
    unitData.currentHealth = Math.max(0, unitData.currentHealth - damage);

    // Update sprite health bar
    this.spriteManager.updateUnitHealth(
      unitId,
      unitData.currentHealth,
      unitData.maxHealth
    );
  }

  /**
   * Handle unit destroy event
   */
  private handleDestroyEvent(data: any): void {
    const unitId = data.unit_id || data.target;

    if (!unitId) return;

    const unitData = this.units.get(unitId);
    if (!unitData) return;

    // Set health to 0
    unitData.currentHealth = 0;

    // Get unit position for effect
    const pos = this.getCurrentPosition(unitId);
    if (pos) {
      // Show explosion particles
      this.weaponEffects.showDestructionEffect(pos.x, pos.y);
    }

    // Trigger destruction animation
    this.spriteManager.destroyUnit(unitId);
  }

  /**
   * Get current interpolated position for a unit
   */
  private getCurrentPosition(unitId: string): { x: number; y: number } | null {
    if (!this.replayController) return null;

    const unitData = this.units.get(unitId);
    if (!unitData || unitData.positionKeyframes.length === 0) return null;

    const currentTime = this.replayController.getCurrentTime();

    return interpolatePosition(unitData.positionKeyframes, currentTime);
  }

  /**
   * Update animation (called every frame at ~60 FPS)
   */
  update(deltaTime: number): void {
    if (!this.replayController || !this.isAnimating) return;

    const startTime = performance.now();

    // Update replay controller
    this.replayController.update(deltaTime);

    // Update all unit positions via interpolation
    this.units.forEach((unitData, unitId) => {
      if (unitData.positionKeyframes.length > 0) {
        const pos = this.getCurrentPosition(unitId);
        if (pos) {
          this.spriteManager.updateUnitPosition(unitId, pos.x, pos.y);
        }
      }
    });

    // Update weapon effects
    this.weaponEffects.update(deltaTime);

    // Update sprite animations
    this.spriteManager.update(deltaTime);

    // Check if playback completed
    if (this.replayController.getState() === 'completed') {
      this.isAnimating = false;
      console.log('BattleAnimator: Playback completed');
    }

    // Performance profiling (development only)
    const elapsed = performance.now() - startTime;
    this.frameTimings.push(elapsed);

    if (startTime - this.lastProfileTime > 5000) {
      const avg = this.frameTimings.reduce((a, b) => a + b, 0) / this.frameTimings.length;
      const max = Math.max(...this.frameTimings);
      console.log(
        `BattleAnimator performance: avg ${avg.toFixed(2)}ms, max ${max.toFixed(2)}ms (target: <16ms for 60fps)`
      );
      this.frameTimings = [];
      this.lastProfileTime = startTime;
    }
  }

  /**
   * Start playing the battle animation
   */
  play(): void {
    if (!this.replayController) {
      console.warn('BattleAnimator: No battle loaded');
      return;
    }

    this.isAnimating = true;
    this.replayController.play();
    console.log('BattleAnimator: Playing');
  }

  /**
   * Pause the battle animation
   */
  pause(): void {
    if (!this.replayController) return;

    this.isAnimating = false;
    this.replayController.pause();
    console.log('BattleAnimator: Paused');
  }

  /**
   * Stop and reset the battle animation
   */
  stop(): void {
    if (!this.replayController) return;

    this.isAnimating = false;
    this.replayController.stop();
    console.log('BattleAnimator: Stopped');
  }

  /**
   * Step forward one event
   */
  stepForward(): void {
    if (!this.replayController) return;

    this.replayController.step('forward');
  }

  /**
   * Step backward one event
   */
  stepBackward(): void {
    if (!this.replayController) return;

    this.replayController.step('backward');
  }

  /**
   * Set playback speed (0.5x, 1x, 2x, 4x, etc.)
   */
  setSpeed(speed: number): void {
    if (!this.replayController) return;

    this.replayController.setSpeed(speed);
  }

  /**
   * Seek to specific time in the battle
   */
  seekTo(time: number): void {
    if (!this.replayController) return;

    this.replayController.seekTo(time);
  }

  /**
   * Get current playback time
   */
  getCurrentTime(): number {
    return this.replayController?.getCurrentTime() || 0;
  }

  /**
   * Get total battle duration
   */
  getTotalDuration(): number {
    return this.replayController?.getTotalDuration() || 0;
  }

  /**
   * Get current playback state
   */
  getState(): string {
    return this.replayController?.getState() || 'stopped';
  }

  /**
   * Get playback progress (0-1)
   */
  getProgress(): number {
    return this.replayController?.getProgress() || 0;
  }

  /**
   * Clean up resources
   */
  cleanup(): void {
    this.isAnimating = false;
    this.units.clear();
    this.replayController?.cleanup();
    this.replayController = null;
    console.log('BattleAnimator: Cleaned up');
  }
}
