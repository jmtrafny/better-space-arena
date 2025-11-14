# Phase 2 Integration Guide: Track A + Track B

This guide shows how to integrate Track A (Sprite System) and Track B (Animation Timing System) to create the complete battle replay visualization.

## Quick Start

```typescript
import { BattleRenderer } from './game/BattleRenderer';
import { ReplayController } from './game/ReplayController';
import { interpolatePosition } from './game/interpolation';
import { BattleEvent } from './utils/types';

// 1. Initialize renderer
const container = document.getElementById('battle-canvas')!;
const renderer = new BattleRenderer();
await renderer.init(container);

// 2. Get sprite and effects managers from renderer
const spriteManager = renderer.getSpriteManager();
const weaponEffects = renderer.getWeaponEffects();

// 3. Load battle events from engine
const battleResult = await battleEngine.simulateBattle(unit1, unit2);
const events: BattleEvent[] = battleResult.events;

// 4. Create replay controller
const controller = new ReplayController(events);

// 5. Set up event handlers
controller.onEvent(event => {
  handleBattleEvent(event, spriteManager, weaponEffects);
});

// 6. Create position keyframes for smooth movement
const unitKeyframes = extractPositionKeyframes(events);

// 7. Start animation loop
function animate() {
  const deltaTime = 1/60; // 16.67ms

  // Update replay controller
  controller.update(deltaTime);

  // Interpolate unit positions
  const currentTime = controller.getCurrentTime();
  updateUnitPositions(unitKeyframes, currentTime, spriteManager);

  requestAnimationFrame(animate);
}

// 8. Start playback
controller.play();
animate();
```

## Integration Components

### 1. Position Keyframe Extraction

Extract position data from move events for smooth interpolation:

```typescript
import { PositionKeyframe } from './game/interpolation';

function extractPositionKeyframes(
  events: BattleEvent[]
): Map<string, PositionKeyframe[]> {
  const keyframes = new Map<string, PositionKeyframe[]>();

  events.forEach(event => {
    if (event.event_type === 'move' && event.data.unit_id) {
      const unitId = event.data.unit_id as string;
      const position = event.data.position as [number, number];

      if (!keyframes.has(unitId)) {
        keyframes.set(unitId, []);
      }

      keyframes.get(unitId)!.push({
        time: event.timestamp,
        x: position[0],
        y: position[1]
      });
    }
  });

  return keyframes;
}
```

### 2. Event Handler Integration

Connect replay events to sprite updates:

```typescript
function handleBattleEvent(
  event: BattleEvent,
  spriteManager: SpriteManager | null,
  weaponEffects: WeaponEffects | null
): void {
  if (!spriteManager || !weaponEffects) return;

  switch (event.event_type) {
    case 'battle_start':
      handleBattleStart(event, spriteManager);
      break;

    case 'move':
      // Movement is handled by interpolation in render loop
      break;

    case 'attack':
      handleAttack(event, spriteManager, weaponEffects);
      break;

    case 'damage':
      handleDamage(event, spriteManager, weaponEffects);
      break;

    case 'destroy':
      handleDestroy(event, spriteManager);
      break;

    case 'battle_end':
      handleBattleEnd(event);
      break;
  }
}

function handleBattleStart(
  event: BattleEvent,
  spriteManager: SpriteManager
): void {
  // Create initial units
  const units = event.data.units as Array<{
    id: string;
    team: string;
    position: [number, number];
    health: number;
  }>;

  units.forEach(unit => {
    const team = unit.team === 'player' ? 'player' : 'enemy';
    spriteManager.createUnit(
      unit.id,
      team,
      unit.position[0],
      unit.position[1]
    );
    spriteManager.updateUnitHealth(unit.id, unit.health, 100);
  });
}

function handleAttack(
  event: BattleEvent,
  spriteManager: SpriteManager,
  weaponEffects: WeaponEffects
): void {
  const attackerId = event.data.attacker_id as string;
  const targetId = event.data.target_id as string;

  const attackerPos = spriteManager.getUnitPosition(attackerId);
  const targetPos = spriteManager.getUnitPosition(targetId);

  if (attackerPos && targetPos) {
    // Show weapon fire animation
    weaponEffects.showLaserBeam(
      attackerPos.x,
      attackerPos.y,
      targetPos.x,
      targetPos.y,
      true // will be updated on damage event
    );
  }
}

function handleDamage(
  event: BattleEvent,
  spriteManager: SpriteManager,
  weaponEffects: WeaponEffects
): void {
  const targetId = event.data.target_id as string;
  const damage = event.data.damage as number;
  const hit = event.data.hit as boolean;
  const critical = event.data.critical || false;

  const targetPos = spriteManager.getUnitPosition(targetId);
  if (!targetPos) return;

  if (hit) {
    // Show hit effect
    weaponEffects.showHitEffect(targetPos.x, targetPos.y, critical);

    // Update health bar
    const currentHealth = event.data.current_health as number;
    const maxHealth = event.data.max_health as number;
    spriteManager.updateUnitHealth(targetId, currentHealth, maxHealth);
  } else {
    // Show miss effect
    weaponEffects.showMissEffect(targetPos.x, targetPos.y);
  }
}

function handleDestroy(
  event: BattleEvent,
  spriteManager: SpriteManager
): void {
  const unitId = event.data.unit_id as string;
  spriteManager.destroyUnit(unitId);
}

function handleBattleEnd(event: BattleEvent): void {
  const winner = event.data.winner as string;
  console.log(`Battle ended. Winner: ${winner}`);
  // Show victory screen, etc.
}
```

### 3. Position Interpolation in Render Loop

Update sprite positions smoothly between events:

```typescript
function updateUnitPositions(
  keyframes: Map<string, PositionKeyframe[]>,
  currentTime: number,
  spriteManager: SpriteManager | null
): void {
  if (!spriteManager) return;

  keyframes.forEach((unitKeyframes, unitId) => {
    const pos = interpolatePosition(unitKeyframes, currentTime);
    spriteManager.updateUnitPosition(unitId, pos.x, pos.y);
  });
}
```

### 4. Complete Integration Example

```typescript
export class BattleReplayIntegration {
  private renderer: BattleRenderer;
  private controller: ReplayController;
  private unitKeyframes: Map<string, PositionKeyframe[]>;
  private animationFrameId: number | null = null;

  constructor(
    renderer: BattleRenderer,
    events: BattleEvent[]
  ) {
    this.renderer = renderer;
    this.controller = new ReplayController(events);
    this.unitKeyframes = extractPositionKeyframes(events);

    this.setupEventHandlers();
  }

  private setupEventHandlers(): void {
    const spriteManager = this.renderer.getSpriteManager();
    const weaponEffects = this.renderer.getWeaponEffects();

    this.controller.onEvent(event => {
      handleBattleEvent(event, spriteManager, weaponEffects);
    });
  }

  play(): void {
    this.controller.play();
    this.startAnimationLoop();
  }

  pause(): void {
    this.controller.pause();
  }

  stop(): void {
    this.controller.stop();
    this.stopAnimationLoop();
  }

  setSpeed(speed: number): void {
    this.controller.setSpeed(speed);
  }

  seekTo(time: number): void {
    this.controller.seekTo(time);
  }

  private startAnimationLoop(): void {
    if (this.animationFrameId !== null) return;

    let lastTime = performance.now();

    const animate = (currentTime: number) => {
      const deltaTime = (currentTime - lastTime) / 1000;
      lastTime = currentTime;

      // Update replay controller
      this.controller.update(deltaTime);

      // Interpolate positions
      const replayTime = this.controller.getCurrentTime();
      updateUnitPositions(
        this.unitKeyframes,
        replayTime,
        this.renderer.getSpriteManager()
      );

      // Continue if playing
      if (this.controller.getState() === 'playing') {
        this.animationFrameId = requestAnimationFrame(animate);
      }
    };

    this.animationFrameId = requestAnimationFrame(animate);
  }

  private stopAnimationLoop(): void {
    if (this.animationFrameId !== null) {
      cancelAnimationFrame(this.animationFrameId);
      this.animationFrameId = null;
    }
  }

  getPlaybackInfo() {
    return {
      state: this.controller.getState(),
      time: this.controller.getCurrentTime(),
      duration: this.controller.getTotalDuration(),
      progress: this.controller.getProgress(),
      speed: this.controller.getSpeed()
    };
  }

  cleanup(): void {
    this.stopAnimationLoop();
    this.controller.cleanup();
    this.unitKeyframes.clear();
  }
}
```

## Usage in Application

```typescript
// In your battle view component
async function startBattleReplay(battleResult: BattleResult) {
  // Create renderer
  const container = document.getElementById('battle-canvas')!;
  const renderer = new BattleRenderer({
    showDebugInfo: true,
    arenaWidth: 1000,
    arenaHeight: 1000
  });
  await renderer.init(container);

  // Create replay integration
  const replay = new BattleReplayIntegration(
    renderer,
    battleResult.events
  );

  // Set up UI controls
  document.getElementById('play-btn')!.onclick = () => replay.play();
  document.getElementById('pause-btn')!.onclick = () => replay.pause();
  document.getElementById('stop-btn')!.onclick = () => replay.stop();

  document.getElementById('speed-2x')!.onclick = () => replay.setSpeed(2);
  document.getElementById('speed-4x')!.onclick = () => replay.setSpeed(4);

  const timeline = document.getElementById('timeline') as HTMLInputElement;
  timeline.max = String(replay.getPlaybackInfo().duration);
  timeline.oninput = () => replay.seekTo(Number(timeline.value));

  // Update UI periodically
  setInterval(() => {
    const info = replay.getPlaybackInfo();
    document.getElementById('time')!.textContent =
      `${info.time.toFixed(1)}s / ${info.duration.toFixed(1)}s`;
    timeline.value = String(info.time);
  }, 100);

  // Start playback
  replay.play();
}
```

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     BattleReplayIntegration                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────┐         ┌──────────────────┐        │
│  │ ReplayController │         │  BattleRenderer  │        │
│  │   (Track B)      │         │   (Track A)      │        │
│  ├──────────────────┤         ├──────────────────┤        │
│  │ • Event stream   │         │ • SpriteManager  │        │
│  │ • Playback state │────────▶│ • WeaponEffects  │        │
│  │ • Time management│         │ • PixiJS app     │        │
│  │ • Event callbacks│         └──────────────────┘        │
│  └──────────────────┘                  │                   │
│           │                            │                   │
│           ▼                            ▼                   │
│  ┌──────────────────┐         ┌──────────────────┐        │
│  │  Interpolation   │────────▶│   60 FPS Render  │        │
│  │   (Track B)      │         │      Loop        │        │
│  ├──────────────────┤         └──────────────────┘        │
│  │ • Position lerp  │                  │                   │
│  │ • Easing         │                  ▼                   │
│  │ • Keyframes      │         ┌──────────────────┐        │
│  └──────────────────┘         │   PixiJS Canvas  │        │
│                               └──────────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

## File Checklist

### Track A (Sprite System)
- [x] `BattleRenderer.ts` - PixiJS foundation
- [x] `SpriteManager.ts` - Unit sprites
- [x] `WeaponEffects.ts` - Weapon animations

### Track B (Animation Timing)
- [x] `interpolation.ts` - Position interpolation
- [x] `ReplayController.ts` - Event playback
- [x] `ReplayController.test.ts` - Tests
- [x] `ReplayController.example.ts` - Examples

### Integration
- [x] `PHASE2_INTEGRATION.md` - This guide
- [ ] Create `BattleReplayIntegration.ts` (optional wrapper)

## Next Steps

1. ✅ Verify both Track A and Track B compile
2. ✅ Run Track B tests to verify functionality
3. Create integration wrapper class (BattleReplayIntegration)
4. Test with real battle events from Python engine
5. Add UI controls (play, pause, speed, timeline)
6. Fine-tune animation timing and effects
7. Add polish (smooth camera follow, zoom controls)

## Success Criteria

✅ Sprites move smoothly between event positions (60 FPS)
✅ Weapon effects trigger at correct times
✅ Health bars update on damage events
✅ Unit destruction animations play correctly
✅ Playback controls work (play, pause, speed, seek)
✅ No visual jitter or timing issues
✅ Performance is stable with 1500+ events

---

**Status:** Ready for integration testing
**Last Updated:** 2025-11-14
