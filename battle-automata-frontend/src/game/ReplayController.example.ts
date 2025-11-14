/**
 * ReplayController Integration Example
 *
 * Shows how to integrate ReplayController with BattleRenderer
 * for smooth battle replay animation
 */

import { ReplayController, BattleEvent } from './ReplayController';
import { BattleRenderer } from './BattleRenderer';
import { interpolatePosition, PositionKeyframe } from './interpolation';

/**
 * Example: Integrate ReplayController with BattleRenderer
 *
 * This demonstrates the typical usage pattern for Phase 2 synthesis:
 * 1. Load battle events from battle engine
 * 2. Create ReplayController
 * 3. Set up event handlers to update sprites
 * 4. Connect to render loop
 */
export class BattleReplayManager {
  private controller: ReplayController;
  private renderer: BattleRenderer;
  private animationFrameId: number | null = null;
  private lastFrameTime: number = 0;

  // Unit position tracking for interpolation
  private unitPositions: Map<string, PositionKeyframe[]> = new Map();

  constructor(events: BattleEvent[], renderer: BattleRenderer) {
    this.controller = new ReplayController(events);
    this.renderer = renderer;

    // Set up event callbacks
    this.setupEventHandlers();

    // Build position keyframes for smooth movement
    this.buildPositionKeyframes(events);
  }

  /**
   * Extract position keyframes from move events for each unit
   */
  private buildPositionKeyframes(events: BattleEvent[]): void {
    events.forEach(event => {
      if (event.event_type === 'move' && event.data.unit_id) {
        const unitId = event.data.unit_id as string;
        const position = event.data.position as [number, number];

        if (!this.unitPositions.has(unitId)) {
          this.unitPositions.set(unitId, []);
        }

        this.unitPositions.get(unitId)!.push({
          time: event.timestamp,
          x: position[0],
          y: position[1],
        });
      }
    });

    console.log(`Built position keyframes for ${this.unitPositions.size} units`);
  }

  /**
   * Set up event handlers to respond to battle events
   */
  private setupEventHandlers(): void {
    this.controller.onEvent((event) => {
      console.log(`[${event.timestamp.toFixed(2)}s] ${event.event_type}`, event.data);

      // Handle different event types
      switch (event.event_type) {
        case 'battle_start':
          this.handleBattleStart(event);
          break;
        case 'move':
          this.handleMove(event);
          break;
        case 'attack':
          this.handleAttack(event);
          break;
        case 'damage':
          this.handleDamage(event);
          break;
        case 'destroy':
          this.handleDestroy(event);
          break;
        case 'battle_end':
          this.handleBattleEnd(event);
          break;
      }
    });
  }

  /**
   * Event handlers (to be implemented with Track A sprite system)
   */
  private handleBattleStart(event: BattleEvent): void {
    console.log('Battle starting:', event.data.message);
    // TODO: Initialize unit sprites
  }

  private handleMove(event: BattleEvent): void {
    const unitId = event.data.unit_id as string;
    const position = event.data.position as [number, number];
    console.log(`Unit ${unitId} moves to (${position[0]}, ${position[1]})`);
    // TODO: Update sprite position (will be interpolated in render loop)
  }

  private handleAttack(event: BattleEvent): void {
    const attackerId = event.data.attacker_id as string;
    const targetId = event.data.target_id as string;
    const weapon = event.data.weapon as string;
    console.log(`${attackerId} attacks ${targetId} with ${weapon}`);
    // TODO: Trigger weapon effect animation
  }

  private handleDamage(event: BattleEvent): void {
    const targetId = event.data.target_id as string;
    const damage = event.data.damage as number;
    const hit = event.data.hit as boolean;
    console.log(`${targetId} takes ${damage} damage (hit: ${hit})`);
    // TODO: Show damage number, update health bar
  }

  private handleDestroy(event: BattleEvent): void {
    const unitId = event.data.unit_id as string;
    console.log(`${unitId} destroyed!`);
    // TODO: Play destruction animation, remove sprite
  }

  private handleBattleEnd(event: BattleEvent): void {
    const winner = event.data.winner as string;
    console.log(`Battle ended, winner: ${winner}`);
    // TODO: Show victory screen
  }

  /**
   * Start replay playback
   */
  play(): void {
    this.controller.play();
    this.startRenderLoop();
  }

  /**
   * Pause replay playback
   */
  pause(): void {
    this.controller.pause();
  }

  /**
   * Stop replay and reset
   */
  stop(): void {
    this.controller.stop();
    this.stopRenderLoop();
  }

  /**
   * Set playback speed
   */
  setSpeed(speed: number): void {
    this.controller.setSpeed(speed);
  }

  /**
   * Seek to specific time
   */
  seekTo(time: number): void {
    this.controller.seekTo(time);
  }

  /**
   * Start the animation render loop
   */
  private startRenderLoop(): void {
    if (this.animationFrameId !== null) return;

    this.lastFrameTime = performance.now();

    const animate = (currentTime: number) => {
      // Calculate delta time in seconds
      const deltaTime = (currentTime - this.lastFrameTime) / 1000;
      this.lastFrameTime = currentTime;

      // Update replay controller
      this.controller.update(deltaTime);

      // Update sprite positions with interpolation
      this.updateSpritePositions();

      // Continue loop if playing
      if (this.controller.getState() === 'playing') {
        this.animationFrameId = requestAnimationFrame(animate);
      } else {
        this.animationFrameId = null;
      }
    };

    this.animationFrameId = requestAnimationFrame(animate);
  }

  /**
   * Stop the render loop
   */
  private stopRenderLoop(): void {
    if (this.animationFrameId !== null) {
      cancelAnimationFrame(this.animationFrameId);
      this.animationFrameId = null;
    }
  }

  /**
   * Update sprite positions using interpolation
   * This runs every frame for smooth movement between events
   */
  private updateSpritePositions(): void {
    const currentTime = this.controller.getCurrentTime();

    // Update each unit's position
    this.unitPositions.forEach((keyframes, unitId) => {
      const interpolatedPos = interpolatePosition(keyframes, currentTime);

      // TODO Phase 2 synthesis: Update sprite position
      // Example: this.spriteManager.updateUnitPosition(unitId, interpolatedPos.x, interpolatedPos.y);

      // For now, just log (remove in production)
      // console.log(`Unit ${unitId} at (${interpolatedPos.x.toFixed(1)}, ${interpolatedPos.y.toFixed(1)})`);
    });
  }

  /**
   * Get current playback state
   */
  getPlaybackInfo() {
    return {
      state: this.controller.getState(),
      currentTime: this.controller.getCurrentTime(),
      totalDuration: this.controller.getTotalDuration(),
      progress: this.controller.getProgress(),
      speed: this.controller.getSpeed(),
    };
  }

  /**
   * Clean up resources
   */
  cleanup(): void {
    this.stopRenderLoop();
    this.controller.cleanup();
    this.unitPositions.clear();
  }
}

/**
 * Example usage:
 *
 * // Get battle result from engine
 * const battleResult = await battleEngine.simulateBattle(unit1, unit2);
 *
 * // Create renderer
 * const renderer = new BattleRenderer();
 * await renderer.init(container);
 *
 * // Create replay manager
 * const replayManager = new BattleReplayManager(battleResult.events, renderer);
 *
 * // Control playback
 * replayManager.play();
 * replayManager.setSpeed(2.0);
 * replayManager.pause();
 * replayManager.seekTo(10.0);
 * replayManager.play();
 *
 * // Get status
 * const info = replayManager.getPlaybackInfo();
 * console.log(info);
 *
 * // Cleanup when done
 * replayManager.cleanup();
 * renderer.cleanup();
 */
