# Phase 2: Cross-Platform Graphical Interface - Architecture

**Status:** APPROVED ✅ → READY FOR IMPLEMENTATION
**Date:** 2025-11-13
**Orchestration Pattern:** Hybrid (Parallel research → Sequential synthesis)

---

## Overview

This directory contains the complete technical architecture for Phase 2 of the Battle Automata Engine, which adds a cross-platform graphical interface on top of the existing Python CLI engine (Phase 1).

**Goal:** Build PWA, Android, and iOS applications from a single TypeScript/React codebase that provides:
- 60 FPS battle visualization with PixiJS
- Client-side Python simulation via Pyodide (WebAssembly)
- Visual unit builder interface
- Battle replay system with VCR controls
- Theme-based asset loading
- Offline-first architecture

---

## Architecture Documents

These comprehensive documents were created by 4 parallel architecture agents, each researching a specific aspect of the system:

### 1. Frontend Technology Stack Analysis
**Focus:** Technology comparison and selection rationale
**Agent:** Frontend Technology Architect

**Key Findings:**
- **Recommended:** Capacitor + Vite/React + PixiJS
- **Why:** 95%+ code sharing, weekend viable, best PWA quality, $0 hosting costs
- **Comparison:** React Native vs Flutter vs Capacitor (detailed matrix)
- **Code Sharing:** 100% shared web codebase, wrapped for native

**Deliverable Summary:**
- Technology comparison across 3 options
- Pros/cons analysis with scoring
- Justification for Capacitor choice
- Implementation path and risk factors

---

### 2. Graphics Rendering Architecture
**Focus:** Canvas rendering, animation system, 60 FPS strategy
**Agent:** Graphics Rendering Architect

**Key Findings:**
- **Rendering:** HTML5 Canvas 2D with PixiJS v7
- **Animation:** Event-driven interpolation (0.1s sim steps → 60 FPS)
- **Performance:** Sprite batching, culling, LOD, object pooling
- **Replay:** VCR controls with timeline scrubber

**Technical Highlights:**
- Layer-based rendering (background → units → effects → UI)
- Camera system (pan, zoom, auto-frame)
- Smooth interpolation between discrete simulation timesteps
- Theme asset loading with sprite sheets and caching
- Deterministic replay from event logs

**Deliverable Summary:**
- Complete rendering pipeline specification
- Animation engine design
- Asset management system
- Performance optimization strategies
- Battle replay architecture

---

### 3. Backend Integration Strategy
**Focus:** Pyodide WASM integration, TypeScript wrappers
**Agent:** Backend Integration Architect

**Key Findings:**
- **Strategy:** Pyodide (Client-Side WebAssembly)
- **Why:** Perfect fit for existing Python engine, offline-first, zero server costs
- **Integration:** TypeScript wrapper for type-safe Python calls
- **Future:** Optional FastAPI server for multiplayer (Phase 3+)

**Technical Highlights:**
- Python engine runs entirely in browser via Pyodide
- Type-safe TypeScript adapter with Zod validation
- Offline-capable (no network required for core features)
- Deterministic battles preserved (same seed = same result)
- State management with Zustand

**Deliverable Summary:**
- Pyodide integration architecture
- TypeScript-Python bridge design
- Data serialization schemas
- State management strategy
- Offline support implementation

---

### 4. Cross-Platform Build System Design
**Focus:** Build scripts, CI/CD, deployment strategies
**Agent:** Build System Architect

**Key Findings:**
- **Approach:** Single web codebase → 3 platform builds
- **Tools:** Vite (bundler), Capacitor CLI (native wrapper)
- **Deployment:** Netlify/Vercel (PWA), Google Play (Android), App Store (iOS)
- **CI/CD:** GitHub Actions with parallel builds

**Technical Highlights:**
- Build scripts for PWA, Android, iOS
- Asset pipeline (icon generation, optimization, sprite sheets)
- Platform-specific configurations (minimal ~5% code)
- Automated CI/CD pipeline
- Deployment strategies per platform

**Deliverable Summary:**
- Complete project structure
- Build script specifications
- Asset processing pipeline
- CI/CD configuration
- Platform-specific considerations

---

## Approved Technology Stack

| Layer | Technology | Justification |
|-------|-----------|---------------|
| **Frontend** | React + TypeScript | Industry standard, massive ecosystem |
| **Bundler** | Vite | Blazing fast dev, optimized prod builds |
| **Graphics** | PixiJS v7 | 60 FPS 2D, battle-tested game engine |
| **Backend** | Pyodide (WASM) | Runs Python engine client-side, offline-first |
| **State** | Zustand | Lightweight, TypeScript-first |
| **Styling** | Tailwind CSS | Responsive, touch-friendly |
| **Native** | Capacitor 5 | Modern web-to-native bridge |
| **Hosting** | Netlify/Vercel | Free tier, global CDN, HTTPS |

---

## Implementation Roadmap

### Weekend 1: Foundation & Core Integration (8-12 hours)
**Goal:** Python engine running in browser with basic UI

**Tasks:**
1. Initialize Vite + React + TypeScript project
2. Set up Pyodide integration and load Python engine
3. Create basic UI structure (React Router, Zustand)
4. Implement first battle simulation (text-based result)

**Deliverable:** Working web app that runs Python battles in browser

---

### Weekend 2: Graphics Layer (12-16 hours)
**Goal:** Animated battle visualization at 60 FPS

**Tasks:**
1. Integrate PixiJS for 2D rendering
2. Implement asset loading from theme manifests
3. Build animation system (interpolation, events → animations)
4. Implement camera controls (pan, zoom, follow)
5. Add battle replay controls (play/pause/speed/seek)

**Deliverable:** Full battle animation with replay controls

---

### Weekend 3: Polish & Mobile (12-16 hours)
**Goal:** Production PWA + mobile app builds

**Tasks:**
1. Build Unit Builder UI (drag-and-drop components)
2. Add offline support (Service Worker, caching)
3. Set up Capacitor and configure Android/iOS builds
4. Create build scripts for all platforms
5. Performance optimization (batching, pooling, quality settings)
6. Deploy PWA to Netlify/Vercel

**Deliverable:** Production PWA + Android/iOS apps

---

## Architecture Decisions

### Why Capacitor + React + PixiJS + Pyodide?

**1. Weekend Viable (Critical)**
- Familiar web stack (React, TypeScript)
- No new language to learn (vs Flutter/Dart)
- Fast setup and iteration
- Single codebase for all platforms

**2. Code Sharing (95%+)**
- 100% shared web application
- Platform-specific code only for native APIs (~5%)
- Maintain three apps from one codebase

**3. Graphics Performance**
- PixiJS delivers 60 FPS 2D sprite rendering
- WebGL hardware acceleration
- Battle-tested in production games
- Perfect for turn-based visualization

**4. Backend Reuse**
- Existing Python engine (82/82 tests passing)
- No rewrite needed
- Pyodide runs Python in browser
- Deterministic battles preserved

**5. Operating Costs**
- $0/month for PWA hosting (Netlify/Vercel free tier)
- No backend servers required
- Client-side simulation (offline-first)

---

## Success Criteria

**Phase 2 is complete when:**

✅ **PWA:**
- Loads in < 5 seconds (after first visit)
- Battles render at 60 FPS
- Works fully offline
- Installable on mobile home screen

✅ **Android:**
- APK builds successfully
- Runs on Android 7+ devices
- 60 FPS on mid-range devices (2020+)
- Passes Google Play policy checks

✅ **iOS:**
- IPA builds successfully (macOS required)
- Runs on iOS 13+ devices
- 60 FPS on iPhone 8 and newer
- Passes App Store review guidelines

✅ **Features:**
- Battle viewer with smooth animations
- Replay controls (play/pause/speed/seek)
- Unit builder with drag-and-drop
- Theme asset loading
- Offline-capable

---

## Key Metrics

**Development:**
- Estimated time: 3 weekends (~40 hours)
- Code reuse: 95%+ across platforms
- Test coverage target: 80%+ (unit + integration)

**Performance:**
- Initial load: < 5s (after Pyodide cache)
- Battle rendering: 60 FPS target
- Bundle size: < 1MB (excluding Pyodide ~15MB, cached)
- Offline capability: 100% core features

**Operating Costs:**
- PWA hosting: $0/month
- CDN: $0/month
- Backend: $0/month (client-side only)

---

## Risk Mitigation

### Medium Risks:
1. **Pyodide bundle size (~15MB)**
   - Mitigation: CDN caching, loading progress, splash screen

2. **Mobile WebView performance**
   - Mitigation: LOD system, quality settings, 30 FPS fallback

### Low Risks:
3. **iOS App Store review**
   - Mitigation: Follow guidelines, add native features, clear value prop

4. **Memory leaks in long battles**
   - Mitigation: Object pooling, GC optimization, state cache limits

---

## Next Steps

**To begin implementation:**

1. Create new directory: `battle-automata-frontend/`
2. Run: `npm create vite@latest battle-automata-frontend -- --template react-ts`
3. Follow Weekend 1 roadmap (see `prompt.md` for detailed tasks)
4. Reference architecture documents for implementation guidance

**Resources:**
- [prompt.md](../../prompt.md) - Complete Phase 2 implementation instructions
- [Pyodide Docs](https://pyodide.org/) - Python in WebAssembly
- [PixiJS Examples](https://pixijs.io/examples/) - 2D rendering
- [Capacitor Guides](https://capacitorjs.com/docs) - Native wrapping

---

## Architecture Process

**Pattern Used:** Hybrid Workflow
- **Phase 1:** Parallel research (4 agents launched simultaneously)
- **Phase 2:** Sequential synthesis (coherent architecture created)

**Agents Involved:**
1. Frontend Technology Architect
2. Graphics Rendering Architect
3. Backend Integration Architect
4. Build System Architect

**Time Saved:** ~2-3 hours via parallelism vs sequential approach

**Quality:** Comprehensive, production-ready architecture documents totaling ~50,000 words

---

**Architecture approved and ready for implementation!** 🚀

See [prompt.md](../../prompt.md) for step-by-step implementation guide.
