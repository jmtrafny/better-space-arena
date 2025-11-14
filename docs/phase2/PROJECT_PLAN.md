# Battle Automata Engine - Phase 2 Project Plan

**Version:** 1.0
**Date:** 2025-11-13
**Status:** ✅ APPROVED - IN PROGRESS
**Pattern:** Hybrid Workflow (Sequential weekends, parallel tasks within)

---

## Executive Summary

**Project:** Cross-Platform Graphical Interface for Battle Automata Engine
**Phase:** Phase 2 (Phase 1 CLI complete: 82/82 tests passing ✅)
**Timeline:** 3 weekends (~32-44 hours with parallel optimization)
**Delivery Targets:** PWA + Android + iOS apps
**Time Savings:** ~8 hours via parallel execution

---

## Success Criteria

| Platform | Criteria |
|----------|----------|
| **PWA** | < 5s load time, 60 FPS, fully offline, installable |
| **Android** | APK builds, runs on Android 7+, 60 FPS on mid-range devices |
| **iOS** | IPA builds, runs on iOS 13+, 60 FPS on iPhone 8+ |
| **Features** | Battle viewer, replay controls, unit builder, theme loading |

---

## Weekend 1: Foundation & Core Integration (8-12 hours → 9-13h net)

**Goal:** Python engine running in browser with basic UI
**Time Saved:** ~1 hour via parallel execution

### Phase 1.1: Project Initialization (Sequential) - 1-2 hours

| ID | Task | Time | Owner |
|----|------|------|-------|
| W1.1 | Initialize Vite React TypeScript project | 15m | Developer |
| W1.2 | Install dependencies (pyodide, zustand, pixi.js, @capacitor/core) | 15m | Developer |
| W1.3 | Set up project structure (src/, public/, scripts/) | 30m | Developer |
| W1.4 | Configure TypeScript (tsconfig.json, strict mode) | 15m | Developer |
| W1.5 | Set up ESLint + Prettier | 15m | Developer |

**Deliverable:** Clean project foundation

---

### Phase 1.2: Pyodide Integration (Critical Path) - 3-4 hours

**Risk:** MEDIUM (Pyodide complexity, Python wheel packaging)

| ID | Task | Time | Owner |
|----|------|------|-------|
| W1.6 | Create `src/engine/pyodide-loader.ts` | 1h | Developer |
| W1.7 | Package Battle Automata Engine as Python wheel | 1h | Developer |
| W1.8 | Create `src/engine/battle-engine-wasm.ts` (TypeScript wrapper) | 1.5h | Developer |
| W1.9 | Test Pyodide initialization in browser console | 30m | QA |
| W1.10 | Verify deterministic battle simulation | 30m | QA |

**Deliverable:** Python engine callable from TypeScript

---

### Phase 1.3 + 1.4: UI Structure + State Management (PARALLEL) - 2-3 hours

**Parallel Opportunity:** Both can run simultaneously (save ~1 hour)

#### Phase 1.3: Basic UI Structure

| ID | Task | Time | Owner |
|----|------|------|-------|
| W1.11 | Set up React Router (Home, Battle, Builder routes) | 45m | Developer |
| W1.12 | Create placeholder screens | 45m | Developer |
| W1.13 | Set up Zustand stores | 1h | Developer |
| W1.14 | Create basic layout with navigation | 30m | Developer |

#### Phase 1.4: State Management

| ID | Task | Time | Owner |
|----|------|------|-------|
| W1.15 | Create TypeScript types for battle data | 1h | Developer |
| W1.16 | Implement `battleStore.ts` with Zustand | 1h | Developer |
| W1.17 | Implement `themeStore.ts` and `unitStore.ts` | 1h | Developer |

**Deliverable:** Working navigation + type-safe state management

---

### Phase 1.5: First Battle Simulation (Integration) - 2-3 hours

| ID | Task | Time | Owner |
|----|------|------|-------|
| W1.18 | Load preset units from Python engine | 45m | Developer |
| W1.19 | Implement battle start flow | 1h | Developer |
| W1.20 | Display text-based battle result | 45m | Developer |
| W1.21 | Add loading states and error handling | 30m | Developer |

**Deliverable:** Working web app running Python battles

---

### Phase 1.6: Testing & Validation - 1-2 hours

| ID | Task | Time | Owner |
|----|------|------|-------|
| W1.22 | Integration tests for Pyodide loading | 30m | QA |
| W1.23 | Test battle determinism | 15m | QA |
| W1.24 | Test error handling | 30m | QA |
| W1.25 | Performance testing | 30m | QA |

---

### 🚦 HUMAN GATE #1: Weekend 1 Demo

**Validate:**
- Python engine runs in browser
- Battles are deterministic
- Basic UI navigation works
- Performance acceptable

---

## Weekend 2: Graphics Layer (12-16 hours net)

**Goal:** Animated battle visualization at 60 FPS
**Time Saved:** ~3-4 hours via parallel execution

### Phase 2.1: PixiJS Integration (Critical Path) - 2-3 hours

**Risk:** MEDIUM

| ID | Task | Time | Owner |
|----|------|------|-------|
| W2.1 | Create `src/game/BattleRenderer.ts` | 1h | Developer |
| W2.2 | Set up canvas in React component | 30m | Developer |
| W2.3 | Implement 60 FPS rendering loop | 1h | Developer |
| W2.4 | Add FPS counter | 15m | Developer |
| W2.5 | Test rendering performance | 15m | QA |

---

### Phase 2.2 + 2.3: Asset Loading + Animation System (PARALLEL) - 4-5 hours

**Parallel Opportunity:** Independent systems (save ~2 hours)

#### Phase 2.2: Asset Loading System

**Risk:** MEDIUM

| ID | Task | Time | Owner |
|----|------|------|-------|
| W2.6 | Create `src/game/AssetLoader.ts` | 1h | Developer |
| W2.7 | Design asset manifest JSON schema | 45m | Developer |
| W2.8 | Create placeholder sprites | 1h | Developer |
| W2.9 | Implement sprite caching (IndexedDB) | 1h | Developer |
| W2.10 | Test asset loading | 30m | QA |

#### Phase 2.3: Animation System

**Risk:** HIGH (Most complex component)

| ID | Task | Time | Owner |
|----|------|------|-------|
| W2.11 | Create `src/game/AnimationEngine.ts` | 2h | Developer |
| W2.12 | Implement interpolation (0.1s → 60 FPS) | 1.5h | Developer |
| W2.13 | Add projectile animations | 1h | Developer |
| W2.14 | Add explosion animations | 1h | Developer |
| W2.15 | Implement smooth unit movement | 1h | Developer |
| W2.16 | Test animation smoothness | 30m | QA |

---

### Phase 2.4 + 2.5: Camera + Replay Controls (PARALLEL) - 3-4 hours

**Parallel Opportunity:** Independent features (save ~1.5 hours)

#### Phase 2.4: Camera Controls

| ID | Task | Time | Owner |
|----|------|------|-------|
| W2.17 | Create `src/game/CameraController.ts` | 1h | Developer |
| W2.18 | Mouse drag to pan | 45m | Developer |
| W2.19 | Mouse wheel to zoom | 30m | Developer |
| W2.20 | Auto-frame units | 30m | Developer |
| W2.21 | Smooth camera transitions | 30m | Developer |

#### Phase 2.5: Battle Replay Controls

**Risk:** MEDIUM

| ID | Task | Time | Owner |
|----|------|------|-------|
| W2.22 | Create playback UI (play/pause/stop) | 1h | Developer |
| W2.23 | Implement speed controls (0.5x-4x) | 1h | Developer |
| W2.24 | Add timeline scrubber | 1.5h | Developer |
| W2.25 | Frame-by-frame stepping | 45m | Developer |
| W2.26 | Test replay controls | 30m | QA |

---

### Phase 2.6: Integration & Testing - 2-3 hours

**Risk:** MEDIUM (Integration bugs likely)

| ID | Task | Time | Owner |
|----|------|------|-------|
| W2.27 | Integrate all graphics systems | 1h | Developer |
| W2.28 | End-to-end testing | 30m | QA |
| W2.29 | Performance testing (60 FPS) | 45m | QA |
| W2.30 | Fix integration bugs | 1h | Developer |
| W2.31 | Write unit tests | 1h | QA |

---

### 🚦 HUMAN GATE #2: Weekend 2 Demo

**Validate:**
- 60 FPS animation
- Camera controls work
- Replay controls functional
- Animations match battle events

---

## Weekend 3: Polish & Mobile (11-15 hours net)

**Goal:** Production PWA + mobile builds
**Time Saved:** ~2-3 hours via parallel execution

### Phase 3.1 + 3.2: Unit Builder + Offline Support (PARALLEL) - 4-5 hours

**Parallel Opportunity:** Independent features (save ~2 hours)

#### Phase 3.1: Unit Builder UI

**Risk:** MEDIUM

| ID | Task | Time | Owner |
|----|------|------|-------|
| W3.1 | Grid-based component placement interface | 2h | Developer |
| W3.2 | Drag-and-drop from palette | 2h | Developer |
| W3.3 | Display resource constraints | 1h | Developer |
| W3.4 | Add unit validation | 1h | Developer |
| W3.5 | Save/load to localStorage | 1h | Developer |
| W3.6 | Test unit builder | 30m | QA |

#### Phase 3.2: Offline Support

| ID | Task | Time | Owner |
|----|------|------|-------|
| W3.7 | Configure Vite PWA plugin | 30m | Developer |
| W3.8 | Generate service worker | 1h | Developer |
| W3.9 | Configure caching strategies | 1h | Developer |
| W3.10 | Test offline functionality | 45m | QA |
| W3.11 | Add PWA install prompt | 45m | Developer |

---

### Phase 3.3: Capacitor Setup (Sequential) - 2-3 hours

**Risk:** MEDIUM

| ID | Task | Time | Owner |
|----|------|------|-------|
| W3.12 | Install Capacitor packages | 15m | Developer |
| W3.13 | Run `npx cap init` | 15m | Developer |
| W3.14 | Add Android platform | 30m | Developer |
| W3.15 | Add iOS platform (if macOS) | 30m | Developer |
| W3.16 | Configure `capacitor.config.ts` | 45m | Developer |
| W3.17 | Test sync | 15m | QA |

---

### Phase 3.4 + 3.5: Build Scripts + Performance (PARALLEL) - 3-4 hours

**Parallel Opportunity:** Independent work (save ~1.5 hours)

#### Phase 3.4: Build Scripts

| ID | Task | Time | Owner |
|----|------|------|-------|
| W3.18 | Create `scripts/build-web.sh` | 45m | Developer |
| W3.19 | Create `scripts/build-android.sh` | 45m | Developer |
| W3.20 | Create `scripts/build-ios.sh` | 45m | Developer |
| W3.21 | Test PWA build | 30m | QA |
| W3.22 | Test Android APK build | 30m | QA |

#### Phase 3.5: Performance Optimization

**Risk:** MEDIUM

| ID | Task | Time | Owner |
|----|------|------|-------|
| W3.23 | Implement sprite batching | 1h | Developer |
| W3.24 | Add object pooling | 1h | Developer |
| W3.25 | Optimize bundle size | 1h | Developer |
| W3.26 | Test on low-end mobile | 1h | QA |
| W3.27 | Graphics quality settings | 1h | Developer |

---

### Phase 3.6: Deployment (Sequential) - 2-3 hours

| ID | Task | Time | Owner |
|----|------|------|-------|
| W3.28 | Build production PWA | 15m | Developer |
| W3.29 | Deploy to Netlify/Vercel | 30m | Developer |
| W3.30 | Configure custom domain | 30m | Developer |
| W3.31 | Test PWA installation | 45m | QA |
| W3.32 | Build and test Android APK | 30m | QA |
| W3.33 | Build and test iOS IPA | 30m | QA |

---

### 🚦 HUMAN GATE #3: Final Acceptance

**Validate:**
- PWA loads < 5s, works offline
- Unit builder functional
- Performance acceptable
- Mobile builds work

---

## Critical Path & Dependencies

```
Weekend 1 (9-13h net):
Setup → Pyodide → Integration → Testing
(UI + State in parallel saves ~1h)

Weekend 2 (12-16h net):
PixiJS → (Assets ∥ Animation) → (Camera ∥ Replay) → Integration
(2 parallel phases save ~4h)

Weekend 3 (11-15h net):
(Builder ∥ Offline) → Capacitor → (Scripts ∥ Performance) → Deploy
(2 parallel phases save ~3h)

TOTAL: 32-44 hours (vs 40-52h sequential)
```

---

## Risk Assessment

### 🔴 HIGH RISK

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Pyodide bundle size kills mobile | Medium | High | CDN caching, loading screen |
| Animation system too complex | Medium | High | Simplify if needed, skip particles |
| 60 FPS not achievable | Medium | Medium | Quality settings, 30 FPS fallback |

### 🟡 MEDIUM RISK

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| PixiJS integration issues | Low | Medium | Follow React patterns carefully |
| Capacitor platform bugs | Medium | Medium | Test early, platform fallbacks |
| Asset creation bottleneck | High | Low | Use placeholders initially |
| iOS build issues | Medium | Low | Prioritize PWA + Android |

---

## Parallel Execution Strategy

### Weekend 1
- ✅ **Parallel:** UI Structure + State Management
- ❌ **Sequential:** Pyodide (critical path)

### Weekend 2
- ✅ **Parallel:** Asset Loading + Animation System
- ✅ **Parallel:** Camera Controls + Replay Controls

### Weekend 3
- ✅ **Parallel:** Unit Builder + Offline Support
- ✅ **Parallel:** Build Scripts + Performance Optimization

**Total Time Saved:** ~8 hours

---

## Deliverables Checklist

### Weekend 1
- [ ] Vite + React + TypeScript project initialized
- [ ] Pyodide loading Python engine
- [ ] Basic UI with navigation
- [ ] State management with Zustand
- [ ] First battle simulation (text-based)
- [ ] Determinism verified

### Weekend 2
- [ ] PixiJS rendering at 60 FPS
- [ ] Asset loading with caching
- [ ] Animation system
- [ ] Camera controls
- [ ] Replay controls
- [ ] Full animated battle

### Weekend 3
- [ ] Unit builder UI
- [ ] Offline support
- [ ] Capacitor configured
- [ ] Build scripts for all platforms
- [ ] Performance optimizations
- [ ] PWA deployed
- [ ] Android APK tested
- [ ] iOS IPA tested (optional)

---

## Next Steps

1. ✅ Plan approved
2. ➡️ Update documentation
3. ➡️ Begin Weekend 1, Phase 1.1 (Project Initialization)
4. ➡️ Track progress with TodoWrite

**Project Plan v1.0 - Ready for execution!** 🚀
