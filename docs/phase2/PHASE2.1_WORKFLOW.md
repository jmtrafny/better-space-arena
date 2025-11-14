# Phase 2.1: PixiJS Visual Battle System - Multi-Agent Workflow

**Project:** Battle Automata Engine - Phase 2 Frontend
**Phase:** 2.1 - PixiJS Integration for Visual Battles
**Pattern:** Hybrid Workflow (Sequential phases, parallel within phases)
**Estimated Time:** 8-12 hours
**Date:** November 14, 2025

---

## Executive Summary

Phase 2.1 adds visual animation to the Battle Automata web application using PixiJS. Currently battles complete instantly with no visual feedback. This phase will implement a replay system that animates battles frame-by-frame at 60 FPS, with full playback controls.

**Core Goal:** Transform instant battle calculation into smooth animated replay with play/pause/step controls.

---

## Pattern Selection: Hybrid Workflow

### Analysis

**Project Characteristics:**
- **Complexity:** Medium-High (PixiJS integration, animation timing, state management)
- **User Experience:** Experienced (completed Phase 1 successfully)
- **Time Constraints:** Weekend project (8-12 hours available)
- **Dependencies:** Some components independent, others tightly coupled

### Pattern Evaluation

**Sequential:**
- Simplicity: ⭐⭐⭐⭐⭐
- Speed: ⭐⭐
- Fit: Too slow for weekend timeline

**Parallel:**
- Speed: ⭐⭐⭐⭐⭐
- Complexity: ⭐⭐
- Fit: Risky - tight coupling between renderer and animation

**Hybrid:** ⭐⭐⭐⭐⭐ **CHOSEN**
- Balance: Perfect
- Best for: Clear phases with parallelizable subtasks
- Fit: Excellent - architecture phase can parallelize, integration must be sequential

**Adaptive:**
- Optimization: ⭐⭐⭐⭐⭐
- Requires: Experience (user has it!)
- Fit: Good alternative, but hybrid is simpler for this scope

### Rationale for Hybrid

✅ **Clear progression:** PixiJS setup → Sprites → Animation → Controls (4 phases)
✅ **Parallelizable work:** Sprite rendering and control UI can be built concurrently
✅ **Natural gates:** Demo working renderer before animation, demo animation before controls
✅ **Time efficient:** Save 2-3 hours via parallel sprite + UI development
✅ **Manageable risk:** Integration points are well-defined

---

## Phase Breakdown

### Phase 0: Initialization (30 minutes, Sequential)

**Owner:** Orchestrator

**Tasks:**
- Read Phase 1 summary and current codebase
- Understand existing battleStore integration
- Review PixiJS documentation requirements
- Set up task tracking
- Present high-level plan

**Deliverables:**
- Understanding of current state
- Clear task list
- No code changes yet

---

### Phase 1: PixiJS Foundation (2-3 hours, Sequential)

**Owner:** Developer Agent

**Why Sequential:** Foundation must be solid before building on it.

**Tasks:**

#### Task 1.1: Create BattleRenderer.ts (1 hour)
- Set up PixiJS Application
- Create canvas container
- Implement initialization/cleanup lifecycle
- Add resize handling
- Basic arena background rendering
- Camera/viewport setup (1000x1000 arena)

**Files:**
- `src/game/BattleRenderer.ts` (new)

#### Task 1.2: Integrate Renderer with Battle.tsx (30 min)
- Replace placeholder canvas with PixiJS renderer
- Connect to battleStore
- Handle loading/error states
- Lifecycle management (mount/unmount)

**Files:**
- `src/pages/Battle.tsx` (edit)
- `src/components/battle/BattleViewer.tsx` (edit)

#### Task 1.3: Verify Basic Rendering (30 min)
- Create simple test scene (grid, borders)
- Verify 60 FPS rendering
- Test resize behavior
- Ensure no memory leaks

**Deliverables:**
- Working PixiJS canvas integrated into React
- Clean rendering loop at 60 FPS
- No visual battles yet, just foundation

**HUMAN GATE #1:** Verify PixiJS renders and integrates cleanly

---

### Phase 2: Sprite System & Animation Loop (3-4 hours, PARALLEL)

**Why Parallel:** Sprite rendering and animation timing are independent concerns that can be built concurrently.

#### Parallel Track A: Sprite Rendering (Developer Agent)

**Task 2A.1: Create SpriteManager.ts (1.5 hours)**
- Unit sprite creation (colored circles for Phase 2.1)
- Health bar rendering above units
- Team identification (player=blue, enemy=red)
- Position updates
- Destruction effects (fade out)

**Task 2A.2: Weapon Fire Visualization (1 hour)**
- Laser beam effects between units
- Hit/miss indicators
- Critical hit visual feedback
- Projectile trails

**Files:**
- `src/game/SpriteManager.ts` (new)
- `src/game/effects/WeaponEffects.ts` (new)

**Deliverables:**
- Sprites render at correct positions
- Visual distinction between teams
- Weapon effects visible

#### Parallel Track B: Animation Timing System (Developer Agent)

**Task 2B.1: Create ReplayController.ts (2 hours)**
- Event stream parser (1534 events)
- Time interpolation (events → frames)
- Playback state machine (playing/paused/stopped)
- Frame stepping logic
- Speed control (0.5x, 1x, 2x, 4x)

**Task 2B.2: Position Interpolation (1 hour)**
- Smooth movement between event positions
- Velocity-based interpolation
- Handle instant events (damage, destruction)

**Files:**
- `src/game/ReplayController.ts` (new)
- `src/game/interpolation.ts` (new)

**Deliverables:**
- Replay controller manages event playback
- Smooth position interpolation
- Variable speed support

#### Synthesis (30 minutes)

**Owner:** Developer Agent

- Integrate SpriteManager with ReplayController
- Connect sprites to interpolated positions
- Ensure weapon effects trigger on events
- Resolve any timing conflicts
- Test full animation loop

**HUMAN GATE #2:** Demo animated battle replay (no controls yet)

---

### Phase 3: Playback Controls Integration (2-3 hours, PARALLEL)

**Why Parallel:** UI updates and state integration are independent from visualization tweaks.

#### Parallel Track A: UI Controls (Developer Agent)

**Task 3A.1: Update BattleControls.tsx (1.5 hours)**
- Connect play/pause to ReplayController
- Implement step forward/backward
- Wire up speed slider
- Add timeline scrubber
- Display current time / total time

**Files:**
- `src/components/battle/BattleControls.tsx` (edit)

**Task 3A.2: Update EventLog.tsx (30 min)**
- Highlight current event during playback
- Auto-scroll to current event
- Click event to jump to time

**Files:**
- `src/components/battle/EventLog.tsx` (edit)

**Deliverables:**
- Fully functional playback controls
- Timeline navigation works
- Event log synced with animation

#### Parallel Track B: Polish & Performance (Developer Agent)

**Task 3B.1: Performance Optimization (1 hour)**
- Sprite pooling/reuse
- Efficient event filtering
- Cull off-screen sprites
- Profile and optimize hot paths

**Task 3B.2: Visual Polish (1 hour)**
- Smooth transitions
- Better destruction effects
- Arena background details
- Unit facing direction

**Files:**
- Various refinements across game/ files

**Deliverables:**
- Consistent 60 FPS performance
- Polished visual experience

#### Synthesis (30 minutes)

**Owner:** Developer Agent

- Integrate all UI controls with replay system
- Test all playback scenarios (play/pause/step/speed)
- Verify timeline scrubbing works
- Ensure event log stays synchronized
- Fix any integration issues

**HUMAN GATE #3:** Full system test - controls + animation

---

### Phase 4: Testing & Validation (1-2 hours, PARALLEL)

**Why Parallel:** Different test areas are independent.

#### Parallel Track A: Functional Testing (QA Agent)

**Test Areas:**
- Playback controls (play, pause, reset, step)
- Speed adjustment (all speeds work correctly)
- Timeline scrubbing accuracy
- Event log synchronization
- Battle start/complete states

#### Parallel Track B: Visual Testing (QA Agent)

**Test Areas:**
- Sprite rendering accuracy
- Weapon effects visibility
- Position interpolation smoothness
- Health bar updates
- Destruction animations
- 60 FPS consistency

#### Parallel Track C: Edge Cases (QA Agent)

**Test Areas:**
- Rapid play/pause toggling
- Scrubbing to extreme positions (start/end)
- Speed changes during playback
- Window resize during battle
- Multiple battles in sequence
- Memory leak testing

**Deliverables:**
- Bug report with prioritization
- Performance metrics
- Visual quality assessment

#### Bug Fix Phase (Sequential)

**Owner:** Developer Agent

- Fix critical bugs blocking demo
- Address high-priority visual issues
- Performance fixes if needed
- Re-test after fixes

**HUMAN GATE #4:** Final validation - all features working

---

### Phase 5: Documentation (1 hour, Sequential)

**Owner:** Documentation Agent (or Developer)

**Why Sequential:** Needs complete system understanding.

**Tasks:**
- Update README with Phase 2.1 completion
- Document PixiJS architecture
- Create animation system guide
- Update PHASE1_SUMMARY with Phase 2.1 notes
- Create PHASE2.1_SUMMARY.md

**Files:**
- `docs/phase2/PHASE2.1_SUMMARY.md` (new)
- `README.md` updates
- Code documentation

**Deliverables:**
- Complete Phase 2.1 documentation
- Architecture diagrams (text-based)
- Next steps for Phase 2.2

---

## Workflow Visualization

```
Phase 0: Initialization (Orchestrator)
    ↓
Phase 1: PixiJS Foundation (Sequential - Developer)
    ├─→ Task 1.1: BattleRenderer.ts
    ├─→ Task 1.2: Integration
    └─→ Task 1.3: Verification
    ↓ [HUMAN GATE #1]

Phase 2: Sprite & Animation (PARALLEL)
    ├─→ Track A: Sprite System (Developer)
    │     ├─→ SpriteManager.ts
    │     └─→ WeaponEffects.ts
    │
    └─→ Track B: Replay System (Developer)
          ├─→ ReplayController.ts
          └─→ Interpolation
    ↓ [Synthesis]
    ↓ [HUMAN GATE #2]

Phase 3: Controls & Polish (PARALLEL)
    ├─→ Track A: UI Controls (Developer)
    │     ├─→ BattleControls.tsx
    │     └─→ EventLog.tsx
    │
    └─→ Track B: Polish (Developer)
          ├─→ Performance
          └─→ Visual effects
    ↓ [Synthesis]
    ↓ [HUMAN GATE #3]

Phase 4: Testing (PARALLEL)
    ├─→ Functional (QA)
    ├─→ Visual (QA)
    └─→ Edge Cases (QA)
    ↓ [Bug Fixes - Sequential]
    ↓ [HUMAN GATE #4]

Phase 5: Documentation (Sequential - Docs)
    └─→ Complete docs
    ↓ [DELIVERY]
```

---

## Time Estimates

| Phase | Sequential Time | Parallel Time | Time Saved |
|-------|----------------|---------------|------------|
| Phase 0: Init | 30 min | 30 min | - |
| Phase 1: Foundation | 2-3 hours | 2-3 hours | - |
| Phase 2: Sprite + Animation | 5-6 hours | 3-4 hours | **2 hours** |
| Phase 3: Controls + Polish | 4-5 hours | 2-3 hours | **2 hours** |
| Phase 4: Testing | 2-3 hours | 1-2 hours | **1 hour** |
| Phase 5: Docs | 1 hour | 1 hour | - |
| **Total** | **14-18 hours** | **9-13 hours** | **~5 hours** |

**Target:** Complete in 8-12 hours with parallel execution

---

## Success Criteria

### Phase 1 Success
✅ PixiJS canvas renders at 60 FPS
✅ No console errors or warnings
✅ Resize handling works correctly
✅ Memory usage stable

### Phase 2 Success
✅ Units appear as colored sprites
✅ Health bars display correctly
✅ Weapon effects visible
✅ Smooth movement interpolation
✅ Battle animates from start to finish

### Phase 3 Success
✅ All playback controls functional
✅ Speed adjustment works (0.5x to 4x)
✅ Timeline scrubber accurate
✅ Event log synchronized
✅ Consistent 60 FPS during playback

### Phase 4 Success
✅ All critical bugs fixed
✅ No visual glitches
✅ Performance acceptable on target hardware
✅ Edge cases handled gracefully

### Final Delivery Success
✅ Complete animated battle replay system
✅ Fully functional playback controls
✅ Professional visual quality
✅ Comprehensive documentation
✅ Ready for Phase 2.2 (advanced visuals)

---

## Risk Assessment

### High Risk Items

**Risk 1: PixiJS + React Integration**
- **Mitigation:** Use proven patterns (useEffect lifecycle), test thoroughly
- **Fallback:** Simplify integration, accept some React anti-patterns if needed

**Risk 2: Event Timing Complexity**
- **Mitigation:** Start simple (linear playback), add features incrementally
- **Fallback:** Fixed 1x speed only, step controls as backup

**Risk 3: Performance at 60 FPS**
- **Mitigation:** Profile early, optimize sprite rendering, use object pools
- **Fallback:** Reduce to 30 FPS if necessary

### Medium Risk Items

**Risk 4: Parallel Development Integration**
- **Mitigation:** Clear interface contracts, synthesis phase allocated
- **Impact:** May lose 30-60 minutes on integration issues

**Risk 5: Scope Creep**
- **Mitigation:** Strict MVP definition, defer advanced visuals to Phase 2.2
- **Impact:** Could extend timeline by 2-4 hours if not controlled

---

## Technology Stack

### New Dependencies
- **PixiJS 8.7.2** (already installed)
- **@pixi/react 7.1.2** (already installed)

### Core Files to Create
1. `src/game/BattleRenderer.ts` - PixiJS application management
2. `src/game/SpriteManager.ts` - Unit sprite rendering
3. `src/game/ReplayController.ts` - Event playback state machine
4. `src/game/interpolation.ts` - Position/state interpolation
5. `src/game/effects/WeaponEffects.ts` - Visual effects

### Files to Modify
1. `src/pages/Battle.tsx` - Integrate renderer
2. `src/components/battle/BattleViewer.tsx` - Replace placeholder canvas
3. `src/components/battle/BattleControls.tsx` - Wire up controls
4. `src/components/battle/EventLog.tsx` - Add event highlighting
5. `src/state/battleStore.ts` - Add replay state

---

## Human Validation Gates

### Gate #1: Foundation Complete
**Location:** After Phase 1
**Demo:** Show PixiJS canvas rendering cleanly
**Approval Needed:** Confirm architecture is solid before building on it

### Gate #2: Animation Working
**Location:** After Phase 2
**Demo:** Show animated battle (auto-play, no controls)
**Approval Needed:** Confirm animation quality and performance

### Gate #3: Controls Integrated
**Location:** After Phase 3
**Demo:** Show full playback control system
**Approval Needed:** Confirm UX is acceptable

### Gate #4: Final Validation
**Location:** After Phase 4
**Demo:** Complete system test, all features
**Approval Needed:** Sign-off for delivery

---

## Bootstrap Command

To start Phase 2.1 execution, run:

```
/orchestrator-v2 docs/phase2/PHASE2.1_WORKFLOW.md
```

The orchestrator will:
1. Load this workflow plan
2. Execute hybrid pattern (sequential phases, parallel within)
3. Coordinate developer and QA agents
4. Manage human validation gates
5. Track progress with TodoWrite
6. Deliver complete visual battle system

---

## Next Steps After Phase 2.1

### Phase 2.2: Advanced Visuals (Future)
- Actual unit sprites (ship graphics)
- Particle effects (explosions, shields)
- Trail effects for movement
- Camera shake on impacts
- Advanced lighting

### Phase 2.3: Unit Builder UI (Future)
- Visual unit editor
- Component drag-and-drop
- Real-time preview
- Save/load custom units

### Phase 3: Mobile Support (Future)
- Capacitor integration
- Touch controls
- Responsive layouts
- Performance optimization

---

**Document Version:** 1.0
**Created:** 2025-11-14
**Author:** Claude (Anthropic)
**Project:** Battle Automata Engine - Phase 2
