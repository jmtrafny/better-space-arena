/**
 * SpriteManager - Manages unit sprite rendering and health bars
 *
 * Responsibilities:
 * - Create and manage unit sprites (colored circles)
 * - Render health bars above units
 * - Handle team identification (blue/red borders)
 * - Update unit positions smoothly
 * - Animate unit destruction (fade out)
 *
 * Phase 2.1: Using simple graphics (circles) instead of texture sprites
 */

import { Container, Graphics } from 'pixi.js';

interface UnitSprite {
  container: Container;
  body: Graphics;
  healthBarBg: Graphics;
  healthBarFill: Graphics;
  border: Graphics;
  facing: Graphics;
  team: 'player' | 'enemy';
  isDestroying: boolean;
  destroyStartTime?: number;
  destroyStartAlpha?: number;
}

const UNIT_RADIUS = 30;
const BORDER_WIDTH = 2;
const HEALTH_BAR_WIDTH = 60;
const HEALTH_BAR_HEIGHT = 6;
const HEALTH_BAR_OFFSET_Y = -45; // Above the unit
const DESTROY_DURATION = 500; // 0.5 seconds in milliseconds

// Team colors
const PLAYER_COLOR = 0x3b82f6; // Blue
const ENEMY_COLOR = 0xef4444; // Red

// Health bar colors
const HEALTH_HIGH = 0x22c55e; // Green
const HEALTH_MEDIUM = 0xf59e0b; // Yellow
const HEALTH_LOW = 0xef4444; // Red
const HEALTH_BAR_BG = 0x374151; // Dark gray

export class SpriteManager {
  private worldContainer: Container;
  private units: Map<string, UnitSprite> = new Map();
  private spritePool: Container[] = [];

  constructor(worldContainer: Container) {
    this.worldContainer = worldContainer;
  }

  /**
   * Create a new unit sprite at the specified position
   */
  createUnit(id: string, team: 'player' | 'enemy', x: number, y: number): void {
    // Don't create if already exists
    if (this.units.has(id)) {
      console.warn(`Unit ${id} already exists`);
      return;
    }

    // Try to reuse from pool first
    let container = this.spritePool.pop();
    let border: Graphics;
    let body: Graphics;
    let healthBarBg: Graphics;
    let healthBarFill: Graphics;
    let facing: Graphics;

    if (container) {
      // Reuse pooled sprite
      container.visible = true;
      container.alpha = 1.0;
      container.x = x;
      container.y = y;

      // Get child graphics from pooled container
      border = container.children[0] as Graphics;
      body = container.children[1] as Graphics;
      healthBarBg = container.children[2] as Graphics;
      healthBarFill = container.children[3] as Graphics;
      facing = container.children[4] as Graphics;

      // Update colors for new team
      const color = team === 'player' ? PLAYER_COLOR : ENEMY_COLOR;
      border.clear();
      border.circle(0, 0, UNIT_RADIUS + BORDER_WIDTH);
      border.fill({ color });

      body.clear();
      body.circle(0, 0, UNIT_RADIUS);
      body.fill({ color });

      facing.clear();
      facing.moveTo(0, -40);
      facing.lineTo(-5, -30);
      facing.lineTo(5, -30);
      facing.lineTo(0, -40);
      facing.fill({ color });
    } else {
      // Create new container if pool is empty
      container = new Container();
      container.x = x;
      container.y = y;

      // Create border (outer circle)
      border = new Graphics();
      const borderColor = team === 'player' ? PLAYER_COLOR : ENEMY_COLOR;
      border.circle(0, 0, UNIT_RADIUS + BORDER_WIDTH);
      border.fill({ color: borderColor });

      // Create body (inner circle)
      body = new Graphics();
      const bodyColor = team === 'player' ? PLAYER_COLOR : ENEMY_COLOR;
      body.circle(0, 0, UNIT_RADIUS);
      body.fill({ color: bodyColor });

      // Create health bar background
      healthBarBg = new Graphics();
      healthBarBg.rect(
        -HEALTH_BAR_WIDTH / 2,
        HEALTH_BAR_OFFSET_Y,
        HEALTH_BAR_WIDTH,
        HEALTH_BAR_HEIGHT
      );
      healthBarBg.fill({ color: HEALTH_BAR_BG });

      // Create health bar fill
      healthBarFill = new Graphics();
      healthBarFill.rect(
        -HEALTH_BAR_WIDTH / 2,
        HEALTH_BAR_OFFSET_Y,
        HEALTH_BAR_WIDTH,
        HEALTH_BAR_HEIGHT
      );
      healthBarFill.fill({ color: HEALTH_HIGH });

      // Create facing indicator (small triangle pointing up)
      facing = new Graphics();
      const facingColor = team === 'player' ? PLAYER_COLOR : ENEMY_COLOR;
      facing.moveTo(0, -40);
      facing.lineTo(-5, -30);
      facing.lineTo(5, -30);
      facing.lineTo(0, -40);
      facing.fill({ color: facingColor });

      // Add to container in correct order
      container.addChild(border);
      container.addChild(body);
      container.addChild(healthBarBg);
      container.addChild(healthBarFill);
      container.addChild(facing);

      // Add container to world
      this.worldContainer.addChild(container);
    }

    // Store unit sprite data
    this.units.set(id, {
      container,
      body,
      healthBarBg,
      healthBarFill,
      border,
      facing,
      team,
      isDestroying: false,
    });
  }

  /**
   * Update unit position
   */
  updateUnitPosition(id: string, x: number, y: number): void {
    const unit = this.units.get(id);
    if (!unit) {
      console.warn(`Unit ${id} not found for position update`);
      return;
    }

    // Update position
    unit.container.x = x;
    unit.container.y = y;

    // Cull if off-screen (arena is 0-1000, with 50px buffer)
    unit.container.visible = (x >= -50 && x <= 1050 && y >= -50 && y <= 1050);
  }

  /**
   * Update unit health bar
   */
  updateUnitHealth(id: string, health: number, maxHealth: number): void {
    const unit = this.units.get(id);
    if (!unit) {
      console.warn(`Unit ${id} not found for health update`);
      return;
    }

    // Calculate health percentage
    const healthPercent = Math.max(0, Math.min(1, health / maxHealth));

    // Determine health bar color based on percentage
    let healthColor = HEALTH_HIGH;
    if (healthPercent <= 0.25) {
      healthColor = HEALTH_LOW;
    } else if (healthPercent <= 0.5) {
      healthColor = HEALTH_MEDIUM;
    }

    // Update health bar fill
    unit.healthBarFill.clear();
    unit.healthBarFill.rect(
      -HEALTH_BAR_WIDTH / 2,
      HEALTH_BAR_OFFSET_Y,
      HEALTH_BAR_WIDTH * healthPercent,
      HEALTH_BAR_HEIGHT
    );
    unit.healthBarFill.fill({ color: healthColor });
  }

  /**
   * Destroy unit with fade-out animation
   */
  destroyUnit(id: string): void {
    const unit = this.units.get(id);
    if (!unit) {
      console.warn(`Unit ${id} not found for destruction`);
      return;
    }

    // Mark as destroying and set start time
    unit.isDestroying = true;
    unit.destroyStartTime = performance.now();
    unit.destroyStartAlpha = unit.container.alpha;
  }

  /**
   * Update method to be called each frame
   * Handles destruction animations
   */
  update(_deltaTime: number): void {
    const currentTime = performance.now();
    const unitsToDelete: string[] = [];

    // Process destroying units
    this.units.forEach((unit, id) => {
      if (unit.isDestroying && unit.destroyStartTime !== undefined && unit.destroyStartAlpha !== undefined) {
        const elapsed = currentTime - unit.destroyStartTime;
        const progress = Math.min(1, elapsed / DESTROY_DURATION);

        // Ease-out cubic for smoother fade
        const easedProgress = 1 - Math.pow(1 - progress, 3);
        unit.container.alpha = unit.destroyStartAlpha * (1 - easedProgress);

        // Mark for removal when fully faded
        if (progress >= 1) {
          // Add to pool instead of destroying
          unit.container.visible = false;
          unit.container.alpha = 1.0;
          this.spritePool.push(unit.container);
          unitsToDelete.push(id);
        }
      }
    });

    // Delete marked units
    unitsToDelete.forEach(id => this.units.delete(id));
  }

  /**
   * Update unit facing direction
   */
  updateUnitFacing(id: string, targetX: number, targetY: number): void {
    const unit = this.units.get(id);
    if (!unit) return;

    const angle = Math.atan2(targetY - unit.container.y, targetX - unit.container.x);
    unit.facing.rotation = angle + Math.PI / 2; // Adjust for upward default
  }

  /**
   * Get unit position (useful for targeting)
   */
  getUnitPosition(id: string): { x: number; y: number } | null {
    const unit = this.units.get(id);
    if (!unit) return null;

    return {
      x: unit.container.x,
      y: unit.container.y,
    };
  }

  /**
   * Check if unit exists
   */
  hasUnit(id: string): boolean {
    return this.units.has(id);
  }

  /**
   * Get all unit IDs
   */
  getUnitIds(): string[] {
    return Array.from(this.units.keys());
  }

  /**
   * Clean up all units and resources
   */
  cleanup(): void {
    this.units.forEach((unit) => {
      this.worldContainer.removeChild(unit.container);
      unit.container.destroy({ children: true });
    });

    this.units.clear();

    // Clear sprite pool
    this.spritePool.forEach((container) => {
      container.destroy({ children: true });
    });
    this.spritePool = [];
  }
}
