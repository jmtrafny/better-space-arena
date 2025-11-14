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

## 🎯 PHASE 2: Cross-Platform Graphical Interface

**Status:** PLANNING PHASE

### Objective

Design and implement a cross-platform graphical interface that can be built and deployed as:
- **Progressive Web App (PWA)** - Works in browsers, installable
- **Android App** - Native Android application
- **iOS App** - Native iPhone/iPad application

All three platforms share the same codebase and use the existing Python engine as the backend.

### Key Requirements

**1. Architecture Constraints**
- **Reuse:** Must leverage existing Python Battle Automata Engine
- **Separation:** Graphics layer completely independent of simulation core
- **Theme Support:** Different themes can use different graphics/assets
- **Deterministic:** Graphics render from event log (replay capability)

**2. Cross-Platform Build**
- **Single Codebase:** One frontend codebase for all platforms
- **Platform-Specific Builds:** Different build scripts for PWA/Android/iOS
- **Native Performance:** Smooth 60 FPS rendering on all platforms
- **Offline Capable:** PWA and native apps work without network

**3. Graphics Features**
- **Real-Time Rendering:** Smooth visualization of battles
- **Battle Replay:** Replay any battle from event log
- **Interactive:** Pan, zoom, pause, speed controls
- **Theme Assets:** Load sprites, animations per theme
- **Unit Builder UI:** Visual component placement
- **Battle Viewer:** Watch simulations in real-time

**4. Theme Extensibility**
- **Asset System:** Each theme provides its own graphics
- **Sprite Sheets:** Component sprites, animations, effects
- **Audio:** Optional sound effects per theme
- **UI Themes:** Theme-specific colors, fonts, icons
- **Fallbacks:** Default graphics if theme assets missing

### Technical Stack Options

**Frontend (Choose One):**

**Option A: React Native + Web** (Recommended)
- **Framework:** React Native (mobile) + React (web)
- **Shared Code:** ~95% code sharing
- **Rendering:** React Native Skia for 2D graphics
- **Build Outputs:**
  - PWA: React web app with service worker
  - Android: React Native APK
  - iOS: React Native IPA

**Option B: Flutter**
- **Framework:** Flutter (all platforms)
- **Shared Code:** 100% Dart code
- **Rendering:** Flutter's Skia engine
- **Build Outputs:**
  - PWA: Flutter web
  - Android: Flutter APK
  - iOS: Flutter IPA

**Option C: Capacitor + Web Canvas**
- **Framework:** Web technologies (React/Vue/Svelte)
- **Rendering:** HTML5 Canvas or WebGL
- **Wrapper:** Capacitor for native builds
- **Build Outputs:**
  - PWA: Standard web app
  - Android/iOS: Capacitor wrapped web app

**Backend Integration:**

**Strategy 1: Hybrid API** (Recommended for multiplayer)
- Python FastAPI backend
- RESTful API + WebSocket for real-time
- Backend runs battles (authoritative server)
- Frontend renders results

**Strategy 2: Client-Side** (Recommended for offline)
- WebAssembly Python (Pyodide)
- Battle simulation runs in browser
- No server required
- Fully offline

**Strategy 3: Dual Mode**
- Client-side for single player
- Server-side for multiplayer/tournaments
- Best of both worlds

### Architecture Diagram

```
┌────────────────────────────────────────────────────┐
│              Frontend (Cross-Platform)             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │   PWA    │  │ Android  │  │   iOS    │         │
│  │  (Web)   │  │  (APK)   │  │  (IPA)   │         │
│  └─────┬────┘  └─────┬────┘  └─────┬────┘         │
│        │             │             │               │
│        └─────────────┴─────────────┘               │
│                     │                              │
│         ┌───────────▼────────────┐                 │
│         │  Shared UI Components  │                 │
│         │  - Battle Renderer     │                 │
│         │  - Unit Builder UI     │                 │
│         │  - Theme Asset Loader  │                 │
│         └───────────┬────────────┘                 │
└─────────────────────┼──────────────────────────────┘
                      │
          ┌───────────▼───────────┐
          │   API Layer (HTTP)    │
          │   - REST endpoints    │
          │   - WebSocket stream  │
          └───────────┬───────────┘
                      │
┌─────────────────────▼──────────────────────────────┐
│         Python Backend (FastAPI)                   │
│  ┌──────────────────────────────────────┐          │
│  │  Battle Automata Engine (Existing)   │          │
│  │  - Component System                  │          │
│  │  - Unit Builder                      │          │
│  │  - Battle Simulator                  │          │
│  │  - Event Logger                      │          │
│  └──────────────────────────────────────┘          │
└────────────────────────────────────────────────────┘
```

### Theme Asset Structure

```
data/themes/space-ships/
├── theme.yaml                  # Existing metadata
├── components/                 # Existing component YAML
├── units/                      # Existing unit YAML
└── assets/                     # NEW: Graphics assets
    ├── sprites/
    │   ├── components/
    │   │   ├── laser_cannon.png
    │   │   ├── armor_plate.png
    │   │   └── ...
    │   ├── units/
    │   │   ├── fighter.png
    │   │   └── ...
    │   └── effects/
    │       ├── laser_beam.png
    │       ├── explosion.png
    │       └── ...
    ├── animations/
    │   ├── laser_fire.json      # Animation definitions
    │   ├── explosion.json
    │   └── ...
    ├── audio/                   # Optional
    │   ├── laser_shot.mp3
    │   ├── explosion.mp3
    │   └── ...
    └── ui/                      # Theme UI assets
        ├── background.png
        ├── button_style.json
        └── colors.json
```

### Build Scripts Structure

```
battle-automata-frontend/
├── src/                        # Shared source code
│   ├── components/            # UI components
│   ├── game/                  # Game rendering
│   │   ├── BattleRenderer.tsx
│   │   ├── ThemeLoader.tsx
│   │   └── AssetManager.tsx
│   ├── api/                   # Backend API client
│   └── state/                 # State management
├── android/                   # Android-specific
│   └── build.gradle
├── ios/                       # iOS-specific
│   └── Podfile
├── public/                    # PWA assets
│   ├── manifest.json
│   └── service-worker.js
├── scripts/
│   ├── build-pwa.sh          # Build PWA
│   ├── build-android.sh      # Build Android APK
│   └── build-ios.sh          # Build iOS IPA
├── package.json
└── README.md
```

### Next Steps for Agent

**The agent should plan and architect:**

1. **Technology Stack Decision**
   - Choose frontend framework (React Native, Flutter, or Capacitor)
   - Choose rendering approach (Canvas, WebGL, or native)
   - Choose backend integration strategy (API, WASM, or dual)
   - Justify choices based on requirements

2. **Graphics Architecture**
   - Design battle rendering system
   - Design asset loading and caching
   - Design theme asset structure
   - Design animation system
   - Plan for 60 FPS performance

3. **Cross-Platform Strategy**
   - How to share code between platforms
   - Platform-specific adaptations needed
   - Build pipeline for each platform
   - Testing strategy per platform

4. **Backend Integration**
   - API design (if using FastAPI)
   - WebSocket protocol for real-time battles
   - State synchronization strategy
   - Offline mode (if applicable)

5. **Asset Management**
   - Asset loading from theme directories
   - Sprite sheet management
   - Animation definitions
   - Audio integration
   - Asset bundling for production

6. **UI/UX Design**
   - Battle viewer interface
   - Unit builder interface
   - Component library browser
   - Battle replay controls
   - Touch-friendly mobile UI

7. **Build System**
   - Build scripts for each platform
   - Asset pipeline
   - Code splitting and optimization
   - Distribution strategy

**Deliverables Expected:**

- Complete architecture document for graphical layer
- Technology stack recommendations with justification
- Detailed component architecture
- API specifications (if backend required)
- Theme asset schema and examples
- Build pipeline design
- Cross-platform compatibility strategy
- Performance optimization plan
- Implementation roadmap with phases

**Invoke the orchestrator or architect to begin planning the graphical interface layer.**

---

**Ready to make it visual? Let's design the cross-platform graphics layer!** 🎮
