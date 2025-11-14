/**
 * BattleRenderer - PixiJS-based battle visualization engine
 *
 * Responsibilities:
 * - Initialize and manage PixiJS Application
 * - Render 60 FPS animation loop
 * - Handle canvas resizing
 * - Manage camera/viewport for 1000x1000 arena
 * - Provide clean lifecycle (init/cleanup)
 *
 * Phase 1: Foundation only (grid, borders, test scene)
 * Phase 2: Sprite rendering and weapon effects
 */

import { Application, Container, Graphics, Text, TextStyle } from 'pixi.js';
import { SpriteManager } from './SpriteManager';
import { WeaponEffects } from './effects/WeaponEffects';
import { BattleAnimator } from './BattleAnimator';
import type { BattleResult } from '../utils/types';

export interface BattleRendererConfig {
  arenaWidth: number;
  arenaHeight: number;
  backgroundColor: number;
  showDebugInfo: boolean;
}

const DEFAULT_CONFIG: BattleRendererConfig = {
  arenaWidth: 1000,
  arenaHeight: 1000,
  backgroundColor: 0x001122, // Dark blue matching theme
  showDebugInfo: true, // Show FPS counter and debug grid
};

export class BattleRenderer {
  private app: Application | null = null;
  private container: HTMLElement | null = null;
  private config: BattleRendererConfig;

  // Rendering layers
  private worldContainer: Container | null = null;
  private debugContainer: Container | null = null;

  // Phase 2: Sprite and effects managers
  private spriteManager: SpriteManager | null = null;
  private weaponEffects: WeaponEffects | null = null;
  private battleAnimator: BattleAnimator | null = null;

  // Debug elements
  private fpsText: Text | null = null;
  private lastFrameTime: number = 0;
  private frameCount: number = 0;
  private fps: number = 60;

  // Camera properties (will be used in Phase 2)
  private zoom: number = 1.0;

  // Test scene state (Phase 2 demo)
  private testLastWeaponTime: number = 0;
  private testHealthDecrement: number = 0;

  constructor(config: Partial<BattleRendererConfig> = {}) {
    this.config = { ...DEFAULT_CONFIG, ...config };
  }

  /**
   * Initialize the PixiJS application and set up rendering
   */
  async init(container: HTMLElement): Promise<void> {
    this.container = container;

    // Create PixiJS Application
    this.app = new Application();

    await this.app.init({
      width: container.clientWidth,
      height: container.clientHeight,
      backgroundColor: this.config.backgroundColor,
      antialias: true,
      resolution: window.devicePixelRatio || 1,
      autoDensity: true,
    });

    // Append canvas to container
    container.appendChild(this.app.canvas);

    // Create rendering layers
    this.worldContainer = new Container();
    this.debugContainer = new Container();

    this.app.stage.addChild(this.worldContainer);
    this.app.stage.addChild(this.debugContainer);

    // Initialize Phase 2 managers
    this.spriteManager = new SpriteManager(this.worldContainer);
    this.weaponEffects = new WeaponEffects(this.worldContainer);
    this.battleAnimator = new BattleAnimator(this.spriteManager, this.weaponEffects);

    // Set up test scene (Phase 1 grid only - units now controlled by BattleAnimator)
    this.createTestScene();

    // Set up FPS counter
    if (this.config.showDebugInfo) {
      this.createFPSCounter();
    }

    // Start render loop
    this.app.ticker.add(() => this.render());

    // Handle window resize
    window.addEventListener('resize', this.handleResize);

    // Initial camera setup
    this.updateCamera();

    console.log('BattleRenderer initialized at', this.app.canvas.width, 'x', this.app.canvas.height);
  }

  /**
   * Main render loop (called at 60 FPS by PixiJS ticker)
   */
  private render(): void {
    const deltaTime = this.app?.ticker.deltaMS || 0;

    // Update FPS counter
    if (this.config.showDebugInfo && this.fpsText) {
      this.frameCount++;
      const currentTime = performance.now();

      if (currentTime - this.lastFrameTime >= 1000) {
        this.fps = Math.round((this.frameCount * 1000) / (currentTime - this.lastFrameTime));
        this.fpsText.text = `FPS: ${this.fps}`;
        this.frameCount = 0;
        this.lastFrameTime = currentTime;
      }
    }

    // Phase 2: Update battle animator (which updates sprites and effects)
    if (this.battleAnimator) {
      this.battleAnimator.update(deltaTime);
    } else {
      // Fallback: direct updates if no animator
      if (this.spriteManager) {
        this.spriteManager.update(deltaTime);
      }
      if (this.weaponEffects) {
        this.weaponEffects.update(deltaTime);
      }
    }

    // Phase 3: Test scene disabled - battles now controlled by BattleAnimator
    // this.updateTestScene();
  }

  /**
   * Create test scene with grid, borders, and center marker
   */
  private createTestScene(): void {
    if (!this.worldContainer) return;

    const graphics = new Graphics();

    // Draw arena border with glow effect
    graphics.rect(0, 0, this.config.arenaWidth, this.config.arenaHeight);
    graphics.stroke({ width: 4, color: 0x3b82f6, alpha: 0.5 }); // Outer glow
    graphics.stroke({ width: 2, color: 0x60a5fa }); // Inner border

    // Draw enhanced grid with depth (thicker at 250px intervals)
    for (let x = 0; x <= this.config.arenaWidth; x += 50) {
      const isThick = x % 250 === 0;
      graphics.moveTo(x, 0);
      graphics.lineTo(x, this.config.arenaHeight);
      graphics.stroke({
        width: isThick ? 2 : 1,
        color: 0x374151,
        alpha: isThick ? 0.5 : 0.2,
      });
    }

    for (let y = 0; y <= this.config.arenaHeight; y += 50) {
      const isThick = y % 250 === 0;
      graphics.moveTo(0, y);
      graphics.lineTo(this.config.arenaWidth, y);
      graphics.stroke({
        width: isThick ? 2 : 1,
        color: 0x374151,
        alpha: isThick ? 0.5 : 0.2,
      });
    }

    // Draw center crosshair
    const centerX = this.config.arenaWidth / 2;
    const centerY = this.config.arenaHeight / 2;
    const crosshairSize = 50;

    graphics.moveTo(centerX - crosshairSize, centerY);
    graphics.lineTo(centerX + crosshairSize, centerY);
    graphics.moveTo(centerX, centerY - crosshairSize);
    graphics.lineTo(centerX, centerY + crosshairSize);
    graphics.stroke({ width: 2, color: 0x22c55e }); // Green crosshair

    // Draw center circle
    graphics.circle(centerX, centerY, 10);
    graphics.fill({ color: 0x22c55e, alpha: 0.5 });
    graphics.stroke({ width: 2, color: 0x22c55e });

    this.worldContainer.addChild(graphics);

    // Add corner labels
    this.addCornerLabels();

    // Phase 3: Test units disabled - units now created by BattleAnimator
    // this.createTestUnits();
  }

  /**
   * Create test units for Phase 2 demonstration
   */
  private createTestUnits(): void {
    if (!this.spriteManager) return;

    // Create player unit (blue) on the left
    this.spriteManager.createUnit('player1', 'player', 200, 500);

    // Create enemy unit (red) on the right
    this.spriteManager.createUnit('enemy1', 'enemy', 800, 500);

    // Initialize with full health
    this.spriteManager.updateUnitHealth('player1', 100, 100);
    this.spriteManager.updateUnitHealth('enemy1', 100, 100);

    console.log('Test units created');
  }

  /**
   * Update test scene animations (Phase 2 demo)
   */
  private updateTestScene(): void {
    if (!this.spriteManager || !this.weaponEffects) return;

    const currentTime = performance.now();

    // Trigger weapon effect every 2 seconds
    if (currentTime - this.testLastWeaponTime >= 2000) {
      const playerPos = this.spriteManager.getUnitPosition('player1');
      const enemyPos = this.spriteManager.getUnitPosition('enemy1');

      if (playerPos && enemyPos) {
        // Alternate between player shooting and enemy shooting
        const playerShoots = Math.random() > 0.5;
        const fromPos = playerShoots ? playerPos : enemyPos;
        const toPos = playerShoots ? enemyPos : playerPos;
        const targetId = playerShoots ? 'enemy1' : 'player1';

        // Random hit/miss (70% hit chance)
        const isHit = Math.random() > 0.3;
        const isCritical = isHit && Math.random() > 0.7; // 30% of hits are critical

        // Show laser beam
        this.weaponEffects.showLaserBeam(fromPos.x, fromPos.y, toPos.x, toPos.y, isHit);

        // Show hit or miss effect
        if (isHit) {
          this.weaponEffects.showHitEffect(toPos.x, toPos.y, isCritical);

          // Damage the target
          const damage = isCritical ? 25 : 15;
          this.testHealthDecrement += damage;
          const currentHealth = Math.max(0, 100 - this.testHealthDecrement);
          this.spriteManager.updateUnitHealth(targetId, currentHealth, 100);

          // Destroy unit if health reaches 0
          if (currentHealth <= 0) {
            this.spriteManager.destroyUnit(targetId);
            console.log(`Unit ${targetId} destroyed`);
          }
        } else {
          this.weaponEffects.showMissEffect(toPos.x, toPos.y);
        }
      }

      this.testLastWeaponTime = currentTime;
    }
  }

  /**
   * Add text labels at arena corners for debugging
   */
  private addCornerLabels(): void {
    if (!this.worldContainer) return;

    const labelStyle = new TextStyle({
      fontFamily: 'monospace',
      fontSize: 14,
      fill: 0x9ca3af,
    });

    const corners = [
      { pos: [10, 10], text: '(0, 0)' },
      { pos: [this.config.arenaWidth - 60, 10], text: `(${this.config.arenaWidth}, 0)` },
      { pos: [10, this.config.arenaHeight - 30], text: `(0, ${this.config.arenaHeight})` },
      { pos: [this.config.arenaWidth - 110, this.config.arenaHeight - 30], text: `(${this.config.arenaWidth}, ${this.config.arenaHeight})` },
    ];

    corners.forEach(({ pos, text }) => {
      const label = new Text({ text, style: labelStyle });
      label.x = pos[0];
      label.y = pos[1];
      this.worldContainer!.addChild(label);
    });
  }

  /**
   * Create FPS counter display
   */
  private createFPSCounter(): void {
    if (!this.debugContainer) return;

    const fpsStyle = new TextStyle({
      fontFamily: 'monospace',
      fontSize: 16,
      fill: 0x22c55e,
      fontWeight: 'bold',
    });

    this.fpsText = new Text({ text: 'FPS: 60', style: fpsStyle });
    this.fpsText.x = 10;
    this.fpsText.y = 10;

    this.debugContainer.addChild(this.fpsText);

    this.lastFrameTime = performance.now();
  }

  /**
   * Update camera transform to center arena in viewport
   */
  private updateCamera(): void {
    if (!this.worldContainer || !this.app) return;

    const canvasWidth = this.app.canvas.width / this.app.renderer.resolution;
    const canvasHeight = this.app.canvas.height / this.app.renderer.resolution;

    // Center the arena in the canvas
    const offsetX = (canvasWidth - this.config.arenaWidth * this.zoom) / 2;
    const offsetY = (canvasHeight - this.config.arenaHeight * this.zoom) / 2;

    this.worldContainer.x = offsetX;
    this.worldContainer.y = offsetY;
    this.worldContainer.scale.set(this.zoom);
  }

  /**
   * Handle canvas resize
   */
  private handleResize = (): void => {
    this.resize();
  };

  /**
   * Resize canvas to match container
   */
  resize(): void {
    if (!this.app || !this.container) return;

    const width = this.container.clientWidth;
    const height = this.container.clientHeight;

    this.app.renderer.resize(width, height);
    this.updateCamera();

    console.log('BattleRenderer resized to', width, 'x', height);
  }

  /**
   * Set camera zoom level
   */
  setZoom(zoom: number): void {
    this.zoom = Math.max(0.1, Math.min(3.0, zoom));
    this.updateCamera();
  }

  /**
   * Pan camera to position (Phase 2)
   */
  panTo(_x: number, _y: number): void {
    // Will be implemented in Phase 2
    this.updateCamera();
  }

  /**
   * Public API: Get sprite manager for external use
   */
  getSpriteManager(): SpriteManager | null {
    return this.spriteManager;
  }

  /**
   * Public API: Get weapon effects manager for external use
   */
  getWeaponEffects(): WeaponEffects | null {
    return this.weaponEffects;
  }

  /**
   * Public API: Get battle animator for external use
   */
  getBattleAnimator(): BattleAnimator | null {
    return this.battleAnimator;
  }

  /**
   * Public API: Load and start playing a battle
   */
  loadAndPlayBattle(battleResult: BattleResult): void {
    if (!this.battleAnimator) {
      console.error('BattleRenderer: BattleAnimator not initialized');
      return;
    }

    this.battleAnimator.loadBattle(battleResult);
    this.battleAnimator.play();
  }

  /**
   * Clean up resources and destroy PixiJS app
   */
  cleanup(): void {
    // Clean up Phase 2 managers
    if (this.battleAnimator) {
      this.battleAnimator.cleanup();
      this.battleAnimator = null;
    }
    if (this.spriteManager) {
      this.spriteManager.cleanup();
      this.spriteManager = null;
    }
    if (this.weaponEffects) {
      this.weaponEffects.cleanup();
      this.weaponEffects = null;
    }

    if (this.app) {
      window.removeEventListener('resize', this.handleResize);
      this.app.destroy(true, { children: true, texture: true });
      this.app = null;
    }

    this.worldContainer = null;
    this.debugContainer = null;
    this.fpsText = null;
    this.container = null;

    console.log('BattleRenderer cleaned up');
  }
}
