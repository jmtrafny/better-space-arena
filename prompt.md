# Battle Automata Engine - Project Requirements

## Project Vision

Create a **theme-agnostic engine for automata simulation of battles** inspired by the mobile game "Space Arena". The engine should enable users to build combat units from modular components, then simulate deterministic battles between these automata.

## Inspiration: Space Arena

Space Arena is a mobile game with an engaging gameplay loop:
- Players build spaceships by placing components (weapons, armor, shields, engines) on a grid
- Ships fight autonomously in deterministic, automated battles
- Combat outcome is determined by ship design, not player skill during battle
- The simulation is reproducible given the same starting conditions

## Core Concept

The fundamental idea is:
1. **Build** an automaton using standard parts and layouts
2. **Simulate** an engagement against another automaton
3. **Watch** the deterministic battle unfold
4. **Iterate** on design based on results

This concept can be applied to various themes:
- Space ships (the inspiration)
- Armadas and fleets (space or water)
- Mech robots (Pacific Rim style)
- Army/navy/airforce wargame scenarios
- Fantasy armies
- Custom themes

## Project Goals

### Primary Goals (Weekend MVP)

1. **Theme-Agnostic Engine**
   - Core simulation logic independent of visual theme
   - Data-driven component and unit definitions
   - Easy to swap themes without code changes

2. **Component-Based Unit Building**
   - Units are built from modular components
   - Components have types: offensive, defensive, mobility, support
   - Components interact based on defined rules
   - Resource constraints (power, weight, slots, etc.)

3. **Deterministic Combat Simulation**
   - Battles are reproducible with same inputs
   - Automated AI behavior based on component placement
   - Turn-based simulation with small time steps
   - Complete battle history logging for replay

4. **Working Demo**
   - At least one complete theme (recommend: space ships)
   - 10+ component types across categories
   - Ability to define units via JSON/YAML
   - CLI tool to run battles
   - Basic visualization of results (can be text-based)

### Secondary Goals (Nice to Have)

- Multiple themes included
- Web-based unit builder UI
- Visual battle replay
- AI opponent with preset designs
- Balance analysis tools
- Save/load battle scenarios

## Technical Requirements

### Core Systems

1. **Data Model**
   - Component schema (properties, types, effects)
   - Unit schema (layout, component slots)
   - Battle configuration schema
   - Theme definition schema

2. **Component System**
   - Load components from configuration files
   - Validate component data
   - Component type classification
   - Effect and stat system

3. **Unit Builder**
   - Assemble units from components
   - Validate component placement rules
   - Check resource constraints
   - Serialize/deserialize units

4. **Combat Simulation**
   - Position and facing mechanics
   - Movement and pathfinding
   - Targeting and line of sight
   - Damage calculation
   - Component destruction
   - Win condition detection

5. **Battle Engine**
   - Initialize battle from configuration
   - Execute simulation loop
   - Process actions (move, attack, abilities)
   - Update state deterministically
   - Log events for replay
   - Output results

### Technology Stack

**Recommended:**
- **Language**: Python 3.10+ (rapid prototyping, good libraries)
  - Alternative: TypeScript/Node.js
- **Data Format**: JSON or YAML for all configurations
- **Testing**: pytest or similar
- **CLI**: argparse or click
- **Optional UI**: Flask/FastAPI for web, or simple terminal UI

**Must Support:**
- Running battles from command line
- Configuration via files (no hardcoded game data)
- Deterministic random number generation (seeded)
- Output to various formats (JSON, text, CSV)

### Project Structure

```
better-space-arena/
├── src/
│   ├── core/
│   │   ├── component.py      # Component system
│   │   ├── unit.py           # Unit building
│   │   ├── battle.py         # Battle simulation
│   │   └── engine.py         # Simulation engine
│   ├── mechanics/
│   │   ├── movement.py       # Movement logic
│   │   ├── targeting.py      # Targeting systems
│   │   ├── damage.py         # Damage calculation
│   │   └── effects.py        # Status effects
│   ├── utils/
│   │   ├── loader.py         # Data loading
│   │   ├── validator.py      # Schema validation
│   │   └── logger.py         # Event logging
│   └── cli.py                # Command-line interface
├── data/
│   ├── themes/
│   │   └── space-ships/
│   │       ├── components/   # Component definitions
│   │       ├── units/        # Preset units
│   │       └── theme.yaml    # Theme metadata
│   └── battles/              # Battle scenarios
├── tests/
│   ├── test_components.py
│   ├── test_units.py
│   ├── test_combat.py
│   └── test_determinism.py
├── docs/
│   ├── GETTING_STARTED.md
│   ├── USER_GUIDE.md
│   ├── DEVELOPER_GUIDE.md
│   └── API_REFERENCE.md
├── examples/
│   └── simple_battle.py
├── README.md
├── requirements.txt
└── setup.py
```

## Key Features

### 1. Component System

Components are the building blocks:

**Component Types:**
- **Offensive**: Weapons, turrets, missiles
- **Defensive**: Armor plating, shields, point defense
- **Mobility**: Engines, thrusters, maneuvering jets
- **Support**: Power generators, sensors, repair systems

**Component Properties:**
- Core stats (damage, armor, speed, etc.)
- Resource costs (power draw, weight, slots)
- Special effects (splash damage, armor piercing, etc.)
- Targeting preferences (closest, strongest, weakest)
- Activation rules (range, cooldown, conditions)

### 2. Unit Building

Units are assemblies of components:

**Features:**
- Grid-based or slot-based layout
- Component placement with facing direction
- Resource constraints (total power, weight limits)
- Compatibility rules (dependencies, conflicts)
- Validation before battle

### 3. Battle Simulation

Deterministic, turn-based combat:

**Simulation Loop:**
1. Initialize battle state (positions, health, etc.)
2. For each time step (e.g., 0.1 second ticks):
   - Process movement for each unit
   - Process targeting for each weapon
   - Apply damage and effects
   - Remove destroyed components
   - Check win conditions
3. Log all events for replay
4. Return battle results

**Combat Mechanics:**
- 2D positional arena (recommend: 100x100 grid)
- Facing direction affects weapon arcs
- Distance affects weapon effectiveness
- Line of sight for targeting
- Component damage reduces effectiveness
- Unit destroyed when core components gone

### 4. Determinism

Critical for debugging and fairness:

- Same input always produces same output
- Seeded random number generation
- No external dependencies during simulation
- Complete event log for replay
- State snapshots at each step

### 5. Extensibility

Easy to add new content:

- New components via JSON files
- New themes via directory structure
- Custom mechanics via plugin system (future)
- Mod-friendly architecture

## Scope and Constraints

### Weekend Timeline

This is a weekend project, so scope must be realistic:

**Day 1: Core Architecture**
- Set up project structure
- Implement data models
- Create component and unit systems
- Build basic simulation engine

**Day 2: Polish and Demo**
- Complete combat mechanics
- Add example theme with components
- Create CLI tool
- Write tests
- Basic documentation

### MVP Scope

**In Scope:**
- One complete theme (space ships recommended)
- 10-15 component types
- Simple 2D positioning
- Turn-based simulation
- CLI interface
- Text-based output
- Basic tests

**Out of Scope (for MVP):**
- Graphics and animations
- Real-time combat
- Multiplayer networking
- AI opponents
- Progression system
- Multiple themes
- Web UI
- Mobile app

### Success Criteria

The MVP is successful if:

1. ✅ You can define components in JSON
2. ✅ You can build units from components
3. ✅ You can run battles from CLI
4. ✅ Battles are deterministic
5. ✅ Results clearly show winner and battle log
6. ✅ Easy to add new components
7. ✅ Code is tested and documented
8. ✅ Someone else could create a new theme

## Example Usage (Target UX)

### Defining a Component

```yaml
# data/themes/space-ships/components/laser_cannon.yaml
name: "Laser Cannon Mk1"
type: offensive
category: weapon

stats:
  damage: 50
  range: 100
  fire_rate: 1.0  # shots per second
  accuracy: 0.85

resources:
  power_draw: 20
  weight: 50
  slots: 1

special:
  damage_type: energy
  armor_piercing: 0.3
```

### Building a Unit

```yaml
# data/themes/space-ships/units/fighter.yaml
name: "Light Fighter"
theme: space-ships

layout:
  size: [10, 10]  # grid size

components:
  - type: laser_cannon
    position: [5, 2]
    facing: forward

  - type: armor_plate
    position: [5, 5]

  - type: engine
    position: [5, 8]
    facing: rear

resources:
  power: 100
  weight_limit: 500
```

### Running a Battle

```bash
# CLI usage
$ battle-sim simulate data/units/fighter.yaml data/units/tank.yaml

Battle: Fighter vs Tank
Seed: 12345

Turn 1: Fighter moves forward (45, 30)
Turn 1: Tank rotates to face Fighter
Turn 2: Fighter fires Laser Cannon -> Tank [HIT] 50 damage to armor
Turn 2: Tank fires Heavy Cannon -> Fighter [MISS]
Turn 3: Fighter fires Laser Cannon -> Tank [HIT] 50 damage to armor
...
Turn 25: Tank destroyed

Winner: Fighter
Duration: 2.5 seconds
Damage Dealt: Fighter: 450, Tank: 200
```

## Development Approach

### Multi-Agent Workflow

Use the multi-agent system:

1. **Orchestrator** initiates and coordinates
2. **Project Manager** breaks down tasks and tracks progress
3. **Architect** designs the system architecture
4. **Developer** implements features
5. **QA Tester** validates and finds bugs
6. **Documentation** creates comprehensive docs

### Human Validation Gates

Pause for human approval at:
1. ✋ After project plan created
2. ✋ After architecture designed
3. ✋ After each major feature (demo)
4. ✋ Before final delivery

### Iterative Development

Build in iterations:
- **Iteration 1**: Core data structures and loading
- **Iteration 2**: Component and unit building
- **Iteration 3**: Basic simulation and combat
- **Iteration 4**: Polish, testing, documentation

## Questions to Consider

### Design Decisions

1. **2D or 3D positioning?**
   - Recommend: 2D for MVP

2. **Grid-based or free positioning?**
   - Recommend: Grid-based for simplicity

3. **Turn-based or real-time?**
   - Recommend: Turn-based with small time steps (0.1s)

4. **How to handle randomness?**
   - Use seeded RNG for determinism
   - Minimize randomness in MVP

5. **How detailed should damage be?**
   - Component-level damage
   - Track health per component

6. **How to balance components?**
   - Out of scope for MVP
   - Provide framework for future balancing

### Technical Decisions

1. **Python or TypeScript?**
   - Recommend: Python for speed of development

2. **JSON or YAML?**
   - Either works; YAML more readable

3. **Testing framework?**
   - pytest for Python, jest for TypeScript

4. **How to validate data?**
   - JSON Schema or pydantic

5. **How to visualize battles?**
   - Text output for MVP
   - Plan for visual replay later

## Additional Context

### Space Arena Research

From research, Space Arena features:
- Automated deterministic battles
- Component-based ship design
- Weapon types: Ballistics, Missiles, Lasers
- Defense types: Armor, Shields
- Systems: Engines, Power, Sensors
- Strategic placement of components matters
- Emergent complexity from simple rules

### Similar Games

Other games in this space:
- **Gratuitous Space Battles**: Fleet combat simulation
- **From the Depths**: Vehicle construction and combat
- **TABS**: Physics-based battle simulation
- **Automation**: Car design and racing

### Why This Is Interesting

1. **Design challenge**: Building an effective automaton
2. **Emergent gameplay**: Complex behavior from simple rules
3. **Replayability**: Iterate on designs
4. **Moddability**: Easy to extend and customize
5. **Fair**: Skill in design, not reflexes
6. **Educational**: Learn system design

## Success Metrics

By end of weekend, we should have:

- ✅ Complete, working simulation engine
- ✅ At least one theme with 10+ components
- ✅ CLI tool for running battles
- ✅ Deterministic, reproducible battles
- ✅ Test coverage for core logic
- ✅ Documentation for users and developers
- ✅ Example battles and unit designs
- ✅ Clear path for future expansion

---

## ✅ PHASE 1 COMPLETE: CLI Engine MVP

**Status:** COMPLETED ✓

### What Was Built

The core Battle Automata Engine has been fully implemented with the following systems:

**1. Component System** (✅ Complete)
- Pydantic schemas for validation (weapons, armor, shields, engines, power)
- Frozen dataclasses for runtime performance
- YAML loading pipeline with comprehensive error handling
- Component registry with filtering and discovery
- 8 working example components
- **20/20 tests passing**

**2. Unit Builder** (✅ Complete)
- Fluent builder pattern API (chainable methods)
- Resource constraint validation (power, weight, slots)
- Component dependency checking
- 3-layer validation system (schema, business rules, resources)
- 3 example units (fighter, tank, scout)
- **43/43 tests passing**

**3. Battle Simulator** (✅ Complete)
- Fixed 0.1s timestep simulation (deterministic)
- Seeded RNG for reproducibility
- 5-phase turn execution (movement → targeting → combat → cleanup → win conditions)
- Complete event logging for replay
- Step-by-step execution mode (graphics-ready)
- **11/11 determinism tests passing**

**4. Data Loader & CLI** (✅ Complete)
- Engine facade for simple API
- Theme loading system
- Click-based CLI with 12+ commands
- Rich terminal output formatting
- **8/8 integration tests passing**

### Architecture Highlights

- **Total:** ~2,500+ lines of production code, 82/82 tests passing (100%)
- **Determinism:** Verified - same seed produces identical battles
- **Graphics-Ready:** Step-by-step mode, complete event logs, state snapshots
- **Extensible:** Theme plugin system, data-driven components
- **Production Quality:** Type hints, validation, comprehensive error handling

### Files Delivered

**Source Code:**
- `src/battle_automata/` - Complete engine implementation
- `data/themes/space-ships/` - Example theme with 8 components, 3 units
- `tests/` - 82 comprehensive tests
- `docs/` - Architecture and implementation documentation

**Documentation:**
- Data Model Architecture (106KB)
- Simulation Engine Architecture (complete specs)
- API Design (all interfaces)
- Project Structure (build system)
- Implementation reports for all systems

---

## ✅ PHASE 1 COMPLETE: Web Frontend Foundation

**Status:** COMPLETE ✅
**Started:** 2025-11-13
**Completed:** 2025-11-14
**Total Time:** ~10-12 hours (under budget!)

### What Was Delivered

**Complete Battle Automata Web Application:**
- 🎯 Python engine running in browser via Pyodide WebAssembly
- 🎯 Full battle simulation (600 turns, 1534 events, deterministic)
- 🎯 React + TypeScript UI with dark theme
- 🎯 State management with Zustand stores
- 🎯 Event log with filtering and color coding
- 🎯 Battle controls (foundation for Phase 2 animation)
- 🎯 Type-safe Python ↔ TypeScript integration
- 🎯 82/82 Python engine tests passing
- 🎯 All Human Gate #1 validation tests passing

**Code Statistics:**
- **Frontend:** ~2,778 lines (UI components + state + engine wrapper)
- **Python Engine:** ~2,500 lines (from Phase 1)
- **Tests:** 82 passing (100% coverage of core systems)
- **Bundle Size:** 279.9 KB (89.7 KB gzipped)

**Key Files Delivered:**
- `battle-automata-frontend/` - Complete React application
- `public/wheels/battle_automata-0.1.0-py3-none-any.whl` - Python engine (52KB)
- 6 React components, 3 Zustand stores, TypeScript wrapper
- Full dark theme, routing, error handling

---

## 🎯 PHASE 2: Visual Battle Animation (PixiJS)

**Status:** READY TO START 🚀
**Next:** Weekend 2 - Graphics Layer
**Goal:** Animated battle visualization at 60 FPS

### Progress Tracker

**Weekend 1: Foundation & Core Integration - ✅ COMPLETE**
- ✅ Phase 1.1: Project Initialization (1h) - COMPLETE
  - Vite + React + TypeScript project initialized
  - All dependencies installed (pyodide, zustand, pixi.js, react-router-dom)
  - Project structure created (8 directories)
  - TypeScript strict mode configured
  - ESLint + Prettier configured
  - Dev server tested successfully
- ✅ Phase 1.2: Pyodide Integration (3h) - COMPLETE & VERIFIED
  - Pyodide loader with progress tracking (155 lines)
  - Battle Automata Engine packaged as Python wheel (52KB)
  - TypeScript wrapper for Python engine (185 lines)
  - TypeScript type definitions (100 lines)
  - Interactive test UI with progress bar
  - Version mismatch fixed (0.25.0 → 0.29.0)
  - BattleConfig parameters fixed (arena_size → arena_width/height)
  - **✅ VERIFIED: Python engine executes successfully in browser!**
- ✅ Phase 1.3: UI Structure (2-3h) - COMPLETE
  - BattleViewer.tsx (227 lines) - unit display with health bars
  - BattleControls.tsx (258 lines) - play/pause/reset controls
  - EventLog.tsx (218 lines) - event filtering, color coding, auto-scroll
  - Button.tsx (73 lines) - reusable button component
  - Loading.tsx (47 lines) - loading spinner
  - Layout.tsx (71 lines) - navigation layout
  - BattleDemo.tsx (221 lines) - component integration demo
  - **Total: 894 lines of UI components**
- ✅ Phase 1.4: State Management (2-3h) - COMPLETE
  - battleStore.ts (198 lines) - battle state, engine integration
  - themeStore.ts (129 lines) - dark/light theme with localStorage
  - unitStore.ts (348 lines) - unit library CRUD operations
  - index.ts (65 lines) - centralized exports
  - Battle.tsx updated with store integration
  - **Total: 884 lines of state management**
- ✅ Phase 1.5: First Battle Simulation (2-3h) - COMPLETE & VERIFIED
  - Connected all UI components to battleStore
  - Real Python battle simulation (1534 events per battle)
  - Fighter Mk1 vs Tank Mk1 with actual component loadouts
  - Full event log display with filtering
  - Type-safe data flow from Python → TypeScript
  - Unit health/position extraction from battle results
  - **✅ VERIFIED: Battle completes successfully with real data!**
- ✅ Phase 1.6: Testing & Human Gate #1 (1-2h) - COMPLETE & PASSED
  - Pyodide loading integration: PASSED
  - Battle determinism test page created
  - Error handling: VERIFIED
  - Performance: 1534 events, <1s load (cached)
  - Dark theme applied (全app)
  - Auto-scroll fixed (EventLog only)
  - All UI tweaks complete
  - **✅ ALL HUMAN GATE #1 TESTS PASSED**

**Total Weekend 1 Time:** ~10-12 hours (estimated 12-16h)
**Status:** ✅ AHEAD OF SCHEDULE

### Approved Architecture Summary

The Phase 2 architecture has been designed and approved. The cross-platform graphical interface will be built using:

**Technology Stack:**
- **Frontend:** React + TypeScript + Vite
- **Graphics:** PixiJS v7 (HTML5 Canvas/WebGL)
- **Backend Integration:** Pyodide (Python via WebAssembly)
- **Native Wrapper:** Capacitor 5
- **State Management:** Zustand
- **Styling:** Tailwind CSS

**Build Targets:**
- Progressive Web App (PWA) - Netlify/Vercel hosting
- Android App (APK/AAB) - Google Play Store
- iOS App (IPA) - Apple App Store

**Key Architecture Decisions:**
- ✅ **95%+ code sharing** across all platforms (single web codebase)
- ✅ **Client-side simulation** via Pyodide (offline-first, $0 hosting costs)
- ✅ **60 FPS graphics** with PixiJS 2D rendering
- ✅ **Weekend viable** - familiar web technologies, minimal learning curve
- ✅ **Deterministic replay** - battles rendered from event logs

### Architecture Documentation

Comprehensive architecture documents are available in `docs/phase2/`:

1. **Frontend Technology Stack** - Technology comparison and selection rationale
2. **Graphics Rendering Architecture** - Canvas rendering, animation system, 60 FPS strategy
3. **Backend Integration Strategy** - Pyodide WASM integration, TypeScript wrappers
4. **Cross-Platform Build System** - Build scripts, CI/CD, deployment strategies

### Implementation Roadmap

**Weekend 1: Foundation & Core Integration (8-12 hours)**

**Goal:** Get Python engine running in browser with basic UI

**Tasks:**
1. Initialize project structure
   ```bash
   npm create vite@latest battle-automata-frontend -- --template react-ts
   cd battle-automata-frontend
   npm install pyodide zustand pixi.js @capacitor/core
   ```

2. Set up Pyodide integration
   - Create `src/engine/pyodide-loader.ts` - Load and initialize Pyodide
   - Create `src/engine/battle-engine-wasm.ts` - TypeScript wrapper for Python engine
   - Package Battle Automata Engine as Python wheel
   - Test loading engine in browser console

3. Create basic UI structure
   - Set up React Router for navigation
   - Create placeholder screens (Home, Battle, Builder)
   - Add Zustand state management
   - Test navigation flow

4. Implement first battle simulation
   - Load two preset units from Python engine
   - Call `battle.simulate()` via Pyodide
   - Display battle result (text-based for now)
   - Verify determinism (same seed = same result)

**Deliverable:** Working web app that runs Python battles in browser

---

**Weekend 2: Graphics Layer (12-16 hours)**

**Goal:** Animated battle visualization at 60 FPS

**Tasks:**
1. Integrate PixiJS
   - Create `src/game/BattleRenderer.ts` - PixiJS Application wrapper
   - Set up canvas element in React component
   - Implement basic rendering loop (60 FPS)
   - Add FPS counter for performance monitoring

2. Implement asset loading
   - Create `src/game/AssetLoader.ts` - Load theme sprites
   - Design theme asset manifest structure
   - Load first test sprites (unit, laser, explosion)
   - Implement sprite caching (IndexedDB)

3. Build animation system
   - Create `src/game/AnimationEngine.ts` - Event-driven animations
   - Implement interpolation between 0.1s simulation steps
   - Add projectile animations (laser beams)
   - Add explosion animations (sprite sheet frames)
   - Smooth unit movement

4. Implement camera controls
   - Create `src/game/CameraController.ts` - Pan, zoom, follow
   - Mouse drag to pan
   - Mouse wheel to zoom
   - Auto-frame units at battle start
   - Smooth camera transitions

5. Add battle replay controls
   - Create playback UI (play/pause/stop buttons)
   - Speed controls (0.5x, 1x, 2x, 4x)
   - Timeline scrubber for seeking
   - Frame-by-frame stepping

**Deliverable:** Full battle animation with replay controls

---

**Weekend 3: Polish & Mobile (12-16 hours)**

**Goal:** Production PWA + mobile app builds

**Tasks:**
1. Build Unit Builder UI
   - Create grid-based component placement interface
   - Drag-and-drop components from palette
   - Display resource constraints (power, weight, slots)
   - Validate unit configuration
   - Save/load custom units

2. Add offline support
   - Configure Vite PWA plugin
   - Generate service worker
   - Cache theme assets
   - Test offline functionality
   - Add install prompt for PWA

3. Set up Capacitor
   ```bash
   npm install @capacitor/cli @capacitor/core
   npx cap init
   npx cap add android
   npx cap add ios  # macOS only
   ```

4. Create build scripts
   - `scripts/build-web.sh` - Build optimized PWA
   - `scripts/build-android.sh` - Build Android APK
   - `scripts/build-ios.sh` - Build iOS IPA (macOS)
   - Test builds on all platforms

5. Performance optimization
   - Implement sprite batching
   - Add object pooling for particles
   - Optimize bundle size (code splitting)
   - Test on low-end mobile devices
   - Implement graphics quality settings

6. Deploy PWA
   - Build production bundle
   - Deploy to Netlify or Vercel
   - Configure custom domain (optional)
   - Test PWA installation

**Deliverable:** Production PWA + Android/iOS apps

---

### Theme Asset Structure (NEW)

Extend existing themes with graphics assets:

```
data/themes/space-ships/
├── theme.yaml                  # Existing metadata
├── components/                 # Existing component YAML
├── units/                      # Existing unit YAML
└── assets/                     # NEW: Graphics for frontend
    ├── manifest.json           # Asset manifest
    ├── sprites/
    │   ├── components/
    │   │   ├── laser_cannon_mk1@1x.png
    │   │   ├── laser_cannon_mk1@2x.png  # Retina
    │   │   ├── armor_plate@1x.png
    │   │   └── ...
    │   ├── units/
    │   │   ├── fighter@1x.png
    │   │   └── tank@1x.png
    │   └── effects/
    │       ├── laser_beam.png
    │       └── explosion.png
    ├── spritesheets/
    │   ├── explosions.json     # Texture atlas metadata
    │   ├── explosions.png      # Packed spritesheet
    │   └── ...
    └── audio/                   # Optional
        ├── laser_shot.mp3
        └── explosion.mp3
```

**Asset Manifest Example:**

```json
{
  "theme_id": "space-ships",
  "version": "1.0.0",
  "sprites": {
    "laser_cannon_mk1": {
      "1x": "sprites/components/laser_cannon_mk1@1x.png",
      "2x": "sprites/components/laser_cannon_mk1@2x.png"
    },
    "laser_beam": "sprites/effects/laser_beam.png"
  },
  "spritesheets": {
    "explosions": {
      "image": "spritesheets/explosions.png",
      "data": "spritesheets/explosions.json"
    }
  }
}
```

---

### Frontend Project Structure

```
battle-automata-frontend/
├── src/
│   ├── components/              # React UI components
│   │   ├── battle/
│   │   │   ├── BattleViewer.tsx
│   │   │   ├── BattleControls.tsx
│   │   │   └── EventLog.tsx
│   │   ├── builder/
│   │   │   ├── UnitBuilder.tsx
│   │   │   ├── ComponentPalette.tsx
│   │   │   └── GridEditor.tsx
│   │   └── ui/
│   │       ├── Button.tsx
│   │       └── Layout.tsx
│   ├── game/                    # PixiJS rendering
│   │   ├── BattleRenderer.ts
│   │   ├── AssetLoader.ts
│   │   ├── AnimationEngine.ts
│   │   └── CameraController.ts
│   ├── engine/                  # Pyodide integration
│   │   ├── pyodide-loader.ts
│   │   └── battle-engine-wasm.ts
│   ├── state/                   # Zustand stores
│   │   ├── battleStore.ts
│   │   ├── themeStore.ts
│   │   └── unitStore.ts
│   ├── utils/
│   │   └── types.ts             # TypeScript types
│   ├── App.tsx
│   └── main.tsx
├── public/
│   ├── manifest.json            # PWA manifest
│   └── icons/                   # App icons
├── scripts/
│   ├── build-web.sh
│   ├── build-android.sh
│   └── build-ios.sh
├── android/                     # Capacitor Android
├── ios/                         # Capacitor iOS
├── package.json
├── vite.config.ts
├── capacitor.config.ts
└── README.md
```

---

### Key Implementation Guidelines

**1. Pyodide Integration**

```typescript
// src/engine/battle-engine-wasm.ts
import { loadPyodide } from 'pyodide';

export class BattleEngineWASM {
  private pyodide: any;

  async init() {
    this.pyodide = await loadPyodide({
      indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.25.0/full/'
    });

    // Load Battle Automata Engine wheel
    await this.pyodide.loadPackage('/static/battle_automata-1.0.0-py3-none-any.whl');
  }

  async simulateBattle(unit1: any, unit2: any, seed: number) {
    const result = await this.pyodide.runPythonAsync(`
      from battle_automata.api.battle import Battle, BattleConfig

      config = BattleConfig(seed=${seed})
      battle = Battle(config)
      result = battle.simulate()
      result.to_dict()
    `);

    return result.toJs();
  }
}
```

**2. PixiJS Rendering**

```typescript
// src/game/BattleRenderer.ts
import { Application, Sprite } from 'pixi.js';

export class BattleRenderer {
  private app: Application;

  async init(canvas: HTMLCanvasElement) {
    this.app = new Application({
      view: canvas,
      width: 1920,
      height: 1080,
      backgroundColor: 0x001122
    });

    this.app.ticker.add(() => this.render());
  }

  render() {
    // 60 FPS rendering loop
  }
}
```

**3. State Management**

```typescript
// src/state/battleStore.ts
import { create } from 'zustand';

interface BattleState {
  currentBattle: BattleResult | null;
  isPlaying: boolean;
  playbackSpeed: number;

  startBattle: (unit1: any, unit2: any) => Promise<void>;
  pause: () => void;
  setSpeed: (speed: number) => void;
}

export const useBattleStore = create<BattleState>((set) => ({
  currentBattle: null,
  isPlaying: false,
  playbackSpeed: 1.0,

  startBattle: async (unit1, unit2) => {
    const result = await battleEngine.simulateBattle(unit1, unit2, Date.now());
    set({ currentBattle: result, isPlaying: true });
  },

  pause: () => set({ isPlaying: false }),
  setSpeed: (speed) => set({ playbackSpeed: speed })
}));
```

---

### Success Criteria

**Phase 2 is complete when:**

✅ **PWA:**
- Loads in < 5 seconds after first visit
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

### Next Steps

**To begin implementation:**

1. Create new directory: `battle-automata-frontend/`
2. Run: `npm create vite@latest battle-automata-frontend -- --template react-ts`
3. Follow Weekend 1 roadmap above
4. Reference architecture docs in `docs/phase2/` for detailed guidance

**Questions/Issues:**
- Phase 2 architecture documents provide detailed implementations
- Pyodide documentation: https://pyodide.org/
- PixiJS examples: https://pixijs.io/examples/
- Capacitor guides: https://capacitorjs.com/docs

---

**Let's build the graphical interface!** 🚀
