/**
 * WeaponEffects - Manages weapon visual effects
 *
 * Responsibilities:
 * - Render laser beam effects between shooter and target
 * - Show hit/miss indicators
 * - Display critical hit effects
 * - Manage effect lifecycles and animations
 *
 * Phase 2.1: Simple graphics-based effects
 */

import { Container, Graphics } from 'pixi.js';

interface LaserBeam {
  graphics: Graphics;
  startTime: number;
  duration: number;
}

interface HitEffect {
  graphics: Graphics;
  startTime: number;
  duration: number;
  initialRadius: number;
  maxRadius: number;
  isCritical: boolean;
}

interface MissEffect {
  graphics: Graphics;
  startTime: number;
  duration: number;
}

interface Particle {
  graphics: Graphics;
  x: number;
  y: number;
  vx: number;
  vy: number;
  startTime: number;
  duration: number;
}

// Effect colors
const LASER_HIT_COLOR = 0x00ffff; // Cyan
const LASER_MISS_COLOR = 0x6b7280; // Gray
const HIT_COLOR = 0xfbbf24; // Yellow
const CRITICAL_HIT_COLOR = 0xf97316; // Orange
const MISS_COLOR = 0x6b7280; // Gray

// Effect durations (milliseconds)
const LASER_DURATION = 200; // 0.2 seconds
const HIT_DURATION = 300; // 0.3 seconds
const MISS_DURATION = 200; // 0.2 seconds

// Effect properties
const LASER_WIDTH = 3;
const HIT_INITIAL_RADIUS = 5;
const HIT_MAX_RADIUS = 20;
const CRITICAL_HIT_INITIAL_RADIUS = 8;
const CRITICAL_HIT_MAX_RADIUS = 30;
const MISS_RADIUS = 10;

export class WeaponEffects {
  private worldContainer: Container;
  private laserBeams: LaserBeam[] = [];
  private hitEffects: HitEffect[] = [];
  private missEffects: MissEffect[] = [];
  private particles: Particle[] = [];

  constructor(worldContainer: Container) {
    this.worldContainer = worldContainer;
  }

  /**
   * Show laser beam from shooter to target
   */
  showLaserBeam(fromX: number, fromY: number, toX: number, toY: number, hit: boolean): void {
    const graphics = new Graphics();

    // Draw laser line
    const color = hit ? LASER_HIT_COLOR : LASER_MISS_COLOR;
    graphics.moveTo(fromX, fromY);
    graphics.lineTo(toX, toY);
    graphics.stroke({ width: LASER_WIDTH, color, alpha: 0.8 });

    // Add optional glow effect for hits
    if (hit) {
      graphics.moveTo(fromX, fromY);
      graphics.lineTo(toX, toY);
      graphics.stroke({ width: LASER_WIDTH + 2, color, alpha: 0.3 });
    }

    this.worldContainer.addChild(graphics);

    this.laserBeams.push({
      graphics,
      startTime: performance.now(),
      duration: LASER_DURATION,
    });
  }

  /**
   * Show hit effect at impact point
   */
  showHitEffect(x: number, y: number, critical: boolean): void {
    const graphics = new Graphics();
    const color = critical ? CRITICAL_HIT_COLOR : HIT_COLOR;
    const initialRadius = critical ? CRITICAL_HIT_INITIAL_RADIUS : HIT_INITIAL_RADIUS;
    const maxRadius = critical ? CRITICAL_HIT_MAX_RADIUS : HIT_MAX_RADIUS;

    // Draw initial hit circle
    graphics.circle(x, y, initialRadius);
    graphics.fill({ color, alpha: 0.8 });

    // Add outer glow
    graphics.circle(x, y, initialRadius * 1.5);
    graphics.fill({ color, alpha: 0.3 });

    this.worldContainer.addChild(graphics);

    this.hitEffects.push({
      graphics,
      startTime: performance.now(),
      duration: HIT_DURATION,
      initialRadius,
      maxRadius,
      isCritical: critical,
    });
  }

  /**
   * Show miss effect at target position
   */
  showMissEffect(x: number, y: number): void {
    const graphics = new Graphics();

    // Draw subtle miss puff
    graphics.circle(x, y, MISS_RADIUS);
    graphics.fill({ color: MISS_COLOR, alpha: 0.4 });

    // Add smaller inner circle
    graphics.circle(x, y, MISS_RADIUS * 0.6);
    graphics.fill({ color: MISS_COLOR, alpha: 0.2 });

    this.worldContainer.addChild(graphics);

    this.missEffects.push({
      graphics,
      startTime: performance.now(),
      duration: MISS_DURATION,
    });
  }

  /**
   * Show destruction effect with particle explosion
   */
  showDestructionEffect(x: number, y: number): void {
    const particleCount = 8;

    for (let i = 0; i < particleCount; i++) {
      const angle = (i / particleCount) * Math.PI * 2;
      const speed = 50 + Math.random() * 50;

      const particle = new Graphics();
      particle.circle(0, 0, 3);
      particle.fill({ color: 0xf97316 }); // Orange

      this.worldContainer.addChild(particle);

      this.particles.push({
        graphics: particle,
        x,
        y,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed,
        startTime: performance.now(),
        duration: 0.5,
      });
    }
  }

  /**
   * Update method to be called each frame
   * Handles effect animations and cleanup
   */
  update(deltaTime: number): void {
    const currentTime = performance.now();

    // Update laser beams (filter out finished)
    this.laserBeams = this.laserBeams.filter((beam) => {
      const elapsed = (currentTime - beam.startTime) / 1000;

      if (elapsed >= beam.duration / 1000) {
        this.worldContainer.removeChild(beam.graphics);
        beam.graphics.destroy();
        return false; // Remove from array
      }

      // Update alpha
      beam.graphics.alpha = Math.max(0, 1 - (elapsed / (beam.duration / 1000)));
      return true; // Keep in array
    });

    // Update hit effects (filter out finished)
    this.hitEffects = this.hitEffects.filter((effect) => {
      const elapsed = (currentTime - effect.startTime) / 1000;

      if (elapsed >= effect.duration / 1000) {
        this.worldContainer.removeChild(effect.graphics);
        effect.graphics.destroy();
        return false; // Remove from array
      }

      const progress = elapsed / (effect.duration / 1000);

      // Expand and fade out
      const currentRadius = effect.initialRadius + (effect.maxRadius - effect.initialRadius) * progress;
      const alpha = 1 - progress;

      // Redraw expanding circle
      effect.graphics.clear();
      const color = effect.isCritical ? CRITICAL_HIT_COLOR : HIT_COLOR;

      // Main expanding circle
      effect.graphics.circle(0, 0, currentRadius);
      effect.graphics.fill({ color, alpha: alpha * 0.6 });

      // Outer glow
      effect.graphics.circle(0, 0, currentRadius * 1.5);
      effect.graphics.fill({ color, alpha: alpha * 0.2 });

      // Add particle spray for critical hits
      if (effect.isCritical && progress < 0.5) {
        this.drawCriticalParticles(effect.graphics, currentRadius, alpha);
      }

      return true; // Keep in array
    });

    // Update miss effects (filter out finished)
    this.missEffects = this.missEffects.filter((effect) => {
      const elapsed = (currentTime - effect.startTime) / 1000;

      if (elapsed >= effect.duration / 1000) {
        this.worldContainer.removeChild(effect.graphics);
        effect.graphics.destroy();
        return false; // Remove from array
      }

      // Update alpha
      effect.graphics.alpha = Math.max(0, 1 - (elapsed / (effect.duration / 1000)));
      return true; // Keep in array
    });

    // Update particles with physics
    this.particles = this.particles.filter((p) => {
      const elapsed = (currentTime - p.startTime) / 1000;

      if (elapsed >= p.duration) {
        this.worldContainer.removeChild(p.graphics);
        p.graphics.destroy();
        return false; // Remove from array
      }

      // Physics with gravity
      p.x += p.vx * (deltaTime / 1000);
      p.y += p.vy * (deltaTime / 1000);
      p.vy += 200 * (deltaTime / 1000); // Gravity

      p.graphics.x = p.x;
      p.graphics.y = p.y;
      p.graphics.alpha = 1 - (elapsed / p.duration);

      return true; // Keep in array
    });
  }

  /**
   * Draw particle spray effect for critical hits
   */
  private drawCriticalParticles(graphics: Graphics, radius: number, alpha: number): void {
    const particleCount = 8;
    const particleSize = 3;

    for (let i = 0; i < particleCount; i++) {
      const angle = (i / particleCount) * Math.PI * 2;
      const distance = radius * 1.2;
      const x = Math.cos(angle) * distance;
      const y = Math.sin(angle) * distance;

      graphics.circle(x, y, particleSize);
      graphics.fill({ color: CRITICAL_HIT_COLOR, alpha: alpha * 0.8 });
    }
  }

  /**
   * Get count of active effects (for debugging)
   */
  getActiveEffectCount(): number {
    return this.laserBeams.length + this.hitEffects.length + this.missEffects.length + this.particles.length;
  }

  /**
   * Clean up all effects and resources
   */
  cleanup(): void {
    // Clean up laser beams
    this.laserBeams.forEach((beam) => {
      this.worldContainer.removeChild(beam.graphics);
      beam.graphics.destroy();
    });
    this.laserBeams = [];

    // Clean up hit effects
    this.hitEffects.forEach((effect) => {
      this.worldContainer.removeChild(effect.graphics);
      effect.graphics.destroy();
    });
    this.hitEffects = [];

    // Clean up miss effects
    this.missEffects.forEach((effect) => {
      this.worldContainer.removeChild(effect.graphics);
      effect.graphics.destroy();
    });
    this.missEffects = [];

    // Clean up particles
    this.particles.forEach((particle) => {
      this.worldContainer.removeChild(particle.graphics);
      particle.graphics.destroy();
    });
    this.particles = [];
  }
}
