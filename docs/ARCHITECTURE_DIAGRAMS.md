# Architecture Diagrams
## Battle Automata Engine

Visual representations of the system architecture.

---

## System Overview

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                        EXTERNAL USERS                            ┃
┃   Developers  │  CLI Users  │  API Consumers  │  Web Clients    ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
          │              │              │                │
          └──────────────┴──────────────┴────────────────┘
                                │
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┷━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                     INTERFACE LAYER                              ┃
┃  ┌───────────────┐  ┌──────────────┐  ┌────────────────────┐   ┃
┃  │  Python SDK   │  │  CLI (Click) │  │  Web API (FastAPI) │   ┃
┃  │  (Programmic) │  │  (Terminal)  │  │  (REST/WebSocket)  │   ┃
┃  └───────┬───────┘  └──────┬───────┘  └─────────┬──────────┘   ┃
┗━━━━━━━━━━┷━━━━━━━━━━━━━━━━┷━━━━━━━━━━━━━━━━━━━━┷━━━━━━━━━━━━━━┛
            │                 │                     │
            └─────────────────┴─────────────────────┘
                              │
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┷━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                      PUBLIC API LAYER                            ┃
┃  ┌──────────────┐  ┌────────────┐  ┌──────────────────────┐    ┃
┃  │  Component   │  │    Unit    │  │       Battle         │    ┃
┃  │     API      │  │    API     │  │        API           │    ┃
┃  └──────┬───────┘  └─────┬──────┘  └──────────┬───────────┘    ┃
┃  ┌──────┴────────────────┴──────────────┬─────┴──────────┐     ┃
┃  │         Theme API                    │   Engine API   │     ┃
┃  └───────────────────────────────────────┴────────────────┘     ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                              │
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┷━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                      CORE ENGINE LAYER                           ┃
┃  ┌─────────────────┐  ┌────────────────┐  ┌─────────────────┐  ┃
┃  │   Component     │  │  Unit Builder  │  │     Battle      │  ┃
┃  │     System      │  │  & Validator   │  │  Orchestrator   │  ┃
┃  └────────┬────────┘  └────────┬───────┘  └────────┬────────┘  ┃
┃  ┌────────┴──────────────────┬─┴─────────────┬─────┴────────┐  ┃
┃  │  State Manager            │  Theme Loader │ Event Logger │  ┃
┃  └───────────────────────────┴───────────────┴──────────────┘  ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                              │
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┷━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                     MECHANICS LAYER                              ┃
┃  ┌────────────┐  ┌──────────┐  ┌─────────┐  ┌──────────────┐  ┃
┃  │  Movement  │  │ Targeting│  │ Damage  │  │   Effects    │  ┃
┃  │   System   │  │  System  │  │  Calc   │  │  & Status    │  ┃
┃  └─────┬──────┘  └────┬─────┘  └────┬────┘  └──────┬───────┘  ┃
┃  ┌─────┴──────────────┴──────────────┴──────────────┴───────┐  ┃
┃  │         Collision Detection & Physics                     │  ┃
┃  └────────────────────────────────────────────────────────────┘  ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                              │
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┷━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                   INFRASTRUCTURE LAYER                           ┃
┃  ┌──────────┐  ┌───────────┐  ┌─────────┐  ┌────────────────┐ ┃
┃  │  Loader  │  │ Validator │  │ Logger  │  │  Serializer    │ ┃
┃  └────┬─────┘  └─────┬─────┘  └────┬────┘  └────────┬───────┘ ┃
┃  ┌────┴──────────────┴──────────────┴─────────────┬──┴───────┐ ┃
┃  │  Deterministic RNG  │  Geometry Utils          │ I/O      │ ┃
┃  └─────────────────────┴──────────────────────────┴──────────┘ ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                              │
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┷━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                      DATA LAYER                                  ┃
┃     YAML/JSON Files  │  Schemas  │  Themes  │  Configurations   ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

---

## Data Flow - Battle Simulation

```
START
  │
  ▼
┌────────────────────────┐
│   Load Unit Files      │ ◄─── YAML/JSON Files
│  (fighter.yaml, etc)   │
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│   Parse & Validate     │ ◄─── Schema Validation
│   (Component & Unit)   │
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│  Build Unit Objects    │
│  (Resolve Components)  │
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│  Initialize Battle     │
│  (Setup Arena, RNG)    │
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│   Simulation Loop      │ ◄──┐
│  - Process Movement    │    │
│  - Process Targeting   │    │ Loop until
│  - Apply Damage        │    │ battle ends
│  - Check Win Condition │    │
│  - Log Events          │    │
└───────────┬────────────┘    │
            │                 │
            ├─────────────────┘
            │ (Continue)
            │
            ▼
┌────────────────────────┐
│  Generate Result       │
│  (Winner, Stats, Log)  │
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│   Return/Export        │ ───► JSON/Text Output
│   (Result Object)      │
└────────────────────────┘
  │
END
```

---

## Module Dependency Graph

```
                    ┌──────────┐
                    │   CLI    │
                    └────┬─────┘
                         │
                    ┌────┴─────┐
                    │   Web    │
                    └────┬─────┘
                         │
         ┌───────────────┴───────────────┐
         │                               │
    ┌────┴─────┐                   ┌─────┴─────┐
    │   API    │                   │   Theme   │
    └────┬─────┘                   └─────┬─────┘
         │                               │
         │         ┌─────────────────────┘
         │         │
    ┌────┴─────────┴───┐
    │       Core       │
    └────┬─────────────┘
         │
    ┌────┴─────────┐
    │  Mechanics   │
    └────┬─────────┘
         │
    ┌────┴─────────┐
    │    Utils     │
    └──────────────┘
         │
    ┌────┴─────────┐
    │   stdlib     │
    └──────────────┘

Legend:
  ──► Direct dependency
  ═══ Can use (but not required)
```

---

## Component System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Component Registry                        │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │              In-Memory Cache                        │    │
│  │  { "laser_mk1": Component(...),                    │    │
│  │    "armor_plate": Component(...), ... }            │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  Methods:                                                    │
│  • register(component)                                       │
│  • get(component_id) -> Component                           │
│  • list(type=?, category=?) -> List[Component]              │
│  • load_from_directory(path)                                │
└──────────────────┬───────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│                   Component Loader                           │
│                                                              │
│  1. Find YAML/JSON files                                    │
│  2. Parse file content                                       │
│  3. Validate against schema                                 │
│  4. Create Component objects                                │
│  5. Return to registry                                      │
└──────────────────┬───────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│                 Component Definition (YAML)                  │
│                                                              │
│  id: laser_cannon_mk1                                       │
│  name: "Laser Cannon Mk1"                                   │
│  type: offensive                                            │
│  category: weapon                                           │
│  stats: { damage: 50, range: 100, ... }                    │
│  resources: { power_draw: 20, weight: 50, slots: 1 }       │
└─────────────────────────────────────────────────────────────┘
```

---

## Unit Building Flow

```
                    START
                      │
                      ▼
         ┌────────────────────────┐
         │   Create UnitBuilder   │
         │  builder = UnitBuilder │
         │    ("Fighter", theme)  │
         └───────────┬────────────┘
                     │
                     ▼
         ┌────────────────────────┐
         │    Set Layout          │
         │  .with_layout(10, 10)  │
         └───────────┬────────────┘
                     │
                     ▼
         ┌────────────────────────┐
         │   Set Resources        │
         │  .with_resources(...)  │
         └───────────┬────────────┘
                     │
                     ▼
         ┌────────────────────────┐
         │   Add Components       │──┐
         │  .add_component(...)   │  │ Repeat for
         └───────────┬────────────┘  │ each component
                     │                │
                     ├────────────────┘
                     │
                     ▼
         ┌────────────────────────┐
         │      Build Unit        │
         │     .build()           │
         └───────────┬────────────┘
                     │
                     ▼
         ┌────────────────────────┐
         │   Validate Unit        │
         │  • Check resources     │
         │  • Verify components   │
         │  • Check constraints   │
         └───────────┬────────────┘
                     │
                     ├──── Valid ────────► Unit Object
                     │
                     └── Invalid ───────► ValidationError
```

---

## Battle Simulation State Machine

```
                      [Initialize]
                           │
                           ▼
                   ┌───────────────┐
                   │  INITIALIZED  │
                   └───────┬───────┘
                           │ .simulate()
                           ▼
                   ┌───────────────┐
         ┌─────────│   RUNNING     │◄────────┐
         │         └───────┬───────┘         │
         │                 │                 │
         │                 ▼                 │
         │       ┌──────────────────┐        │
         │       │  Process Turn:   │        │
         │       │  1. Movement     │        │
         │       │  2. Targeting    │        │
         │       │  3. Damage       │        │
         │       │  4. Effects      │        │
         │       │  5. Log Events   │        │
         │       └──────────┬───────┘        │
         │                  │                │
         │                  ▼                │
         │       ┌──────────────────┐        │
         │       │  Check Win Cond  │        │
         │       └──────────┬───────┘        │
         │                  │                │
         │                  ├─ Continue ─────┘
         │                  │
         │                  ├─ Timeout
         │                  │
         │                  ├─ Unit Destroyed
         │                  │
         │                  └─ Draw
         │                  │
         │                  ▼
         │          ┌───────────────┐
         └─────────►│   FINISHED    │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │ Return Result │
                    └───────────────┘
```

---

## Theme Structure

```
themes/
│
└── space-ships/                          Theme Directory
    │
    ├── theme.yaml                        Theme Metadata
    │   • id: space-ships
    │   • name: "Space Ships"
    │   • version: "1.0.0"
    │   • description: "..."
    │
    ├── components/                       Component Directory
    │   ├── offensive/                    Component Type
    │   │   ├── laser_cannon_mk1.yaml
    │   │   ├── laser_cannon_mk2.yaml
    │   │   ├── missile_launcher.yaml
    │   │   └── ...
    │   │
    │   ├── defensive/
    │   │   ├── armor_plate_light.yaml
    │   │   ├── armor_plate_heavy.yaml
    │   │   ├── shield_generator.yaml
    │   │   └── ...
    │   │
    │   ├── mobility/
    │   │   ├── engine_basic.yaml
    │   │   ├── engine_advanced.yaml
    │   │   ├── thruster.yaml
    │   │   └── ...
    │   │
    │   └── support/
    │       ├── power_generator_small.yaml
    │       ├── power_generator_large.yaml
    │       ├── sensor_array.yaml
    │       └── ...
    │
    └── units/                            Preset Units
        ├── fighter.yaml
        ├── tank.yaml
        ├── bomber.yaml
        ├── scout.yaml
        └── ...
```

---

## CLI Command Flow

```bash
$ battle-sim battle simulate fighter.yaml tank.yaml --seed 12345
```

```
┌─────────────────────────────────────────────────────────────┐
│  1. CLI Parser (Click)                                      │
│     • Parse command: "battle simulate"                      │
│     • Extract args: fighter.yaml, tank.yaml                 │
│     • Extract options: --seed 12345                         │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  2. Command Handler                                         │
│     • Validate file paths exist                             │
│     • Initialize engine                                     │
│     • Load units from files                                 │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  3. API Call                                                │
│     battle = Battle(unit1, unit2, config={seed: 12345})     │
│     result = battle.simulate()                              │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  4. Core Engine Execution                                   │
│     • Run simulation loop                                   │
│     • Generate events                                       │
│     • Determine winner                                      │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  5. Result Formatting                                       │
│     • Format output (table, JSON, etc.)                     │
│     • Display to terminal                                   │
│     • Save to file if requested                             │
└─────────────────────────────────────────────────────────────┘
```

---

## API Integration Patterns

### Pattern 1: Library Usage

```python
┌──────────────────────────────────────────────┐
│         User Application Code                │
└─────────────────┬────────────────────────────┘
                  │
                  ▼
┌──────────────────────────────────────────────┐
│  from battle_automata.api import Engine      │
│                                              │
│  engine = Engine()                           │
│  engine.initialize()                         │
│                                              │
│  unit1 = engine.load_unit("fighter.yaml")   │
│  unit2 = engine.load_unit("tank.yaml")      │
│                                              │
│  battle = engine.create_battle(u1, u2)      │
│  result = battle.simulate()                  │
└──────────────────┬───────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────┐
│         BattleResult Object                  │
│  • winner: "fighter"                         │
│  • duration: 25.3                            │
│  • events: [...]                             │
└──────────────────────────────────────────────┘
```

### Pattern 2: Web API Usage

```
┌──────────────────────────────────────────────┐
│         HTTP Client (Browser, curl)          │
└─────────────────┬────────────────────────────┘
                  │
                  │ POST /api/battles/simulate
                  │ { "unit1": "fighter",
                  │   "unit2": "tank",
                  │   "seed": 12345 }
                  ▼
┌──────────────────────────────────────────────┐
│         FastAPI Server                       │
│                                              │
│  @app.post("/api/battles/simulate")         │
│  async def simulate_battle(...):            │
│      engine = get_engine()                   │
│      result = engine.simulate_battle(...)   │
│      return result.model_dump()             │
└──────────────────┬───────────────────────────┘
                   │
                   │ HTTP Response (JSON)
                   ▼
┌──────────────────────────────────────────────┐
│  {                                           │
│    "outcome": "unit1_victory",              │
│    "winner": "fighter",                      │
│    "duration": 25.3,                         │
│    "events": [...]                           │
│  }                                           │
└──────────────────────────────────────────────┘
```

---

## Error Handling Flow

```
                 Code Execution
                       │
                       ▼
              ┌────────────────┐
              │  Try Operation │
              └────────┬───────┘
                       │
         ┌─────────────┴─────────────┐
         │                           │
         ▼                           ▼
    ┌─────────┐              ┌──────────────┐
    │ Success │              │   Exception  │
    └────┬────┘              └──────┬───────┘
         │                          │
         │                          ▼
         │              ┌──────────────────────┐
         │              │   Catch & Classify   │
         │              └──────┬───────────────┘
         │                     │
         │        ┌────────────┼────────────┐
         │        │            │            │
         │        ▼            ▼            ▼
         │  ┌──────────┐ ┌─────────┐ ┌─────────┐
         │  │Validation│ │Component│ │ Battle  │
         │  │  Error   │ │  Error  │ │  Error  │
         │  └────┬─────┘ └────┬────┘ └────┬────┘
         │       │            │            │
         │       └────────────┴────────────┘
         │                    │
         │                    ▼
         │       ┌────────────────────────┐
         │       │  Format Error Response │
         │       │  • Error type          │
         │       │  • Message             │
         │       │  • Details             │
         │       └────────┬───────────────┘
         │                │
         │                ▼
         │       ┌────────────────────────┐
         │       │  Return to Caller      │
         │       │  (or log & exit)       │
         │       └────────────────────────┘
         │
         ▼
    ┌─────────────────┐
    │ Return Success  │
    └─────────────────┘
```

---

## Testing Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Test Pyramid                            │
│                                                              │
│                         ╱╲                                   │
│                        ╱  ╲                                  │
│                       ╱ E2E╲         Few, slow              │
│                      ╱──────╲        Full workflows         │
│                     ╱        ╲                               │
│                    ╱Integration                              │
│                   ╱────────────╲    Medium count            │
│                  ╱   Module     ╲   Module interactions     │
│                 ╱  Interactions  ╲                           │
│                ╱──────────────────╲                          │
│               ╱                    ╲                         │
│              ╱    Unit Tests        ╲  Many, fast           │
│             ╱   Individual Functions ╲ Single functions     │
│            ╱──────────────────────────╲                      │
│           ╱____________________________╲                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘

Test Structure:

tests/
├── unit/                     # Unit Tests (Most)
│   ├── test_component.py     # Component class tests
│   ├── test_unit.py          # Unit class tests
│   ├── test_mechanics.py     # Mechanics functions
│   └── test_utils.py         # Utility functions
│
├── integration/              # Integration Tests (Medium)
│   ├── test_api.py           # API integration
│   ├── test_cli.py           # CLI commands
│   ├── test_theme_loading.py# Theme system
│   └── test_battle_flow.py  # Battle workflow
│
└── e2e/                      # End-to-End Tests (Few)
    ├── test_full_battle.py   # Complete battle
    └── test_determinism.py   # Deterministic behavior
```

---

## Performance Optimization Points

```
┌─────────────────────────────────────────────────────────────┐
│                   Performance Layers                         │
│                                                              │
│  1. DATA LOADING                                            │
│     ┌────────────────────────────────────────────┐         │
│     │ • Cache parsed YAML/JSON                   │         │
│     │ • Lazy load themes                         │         │
│     │ • Reuse component registry                 │         │
│     └────────────────────────────────────────────┘         │
│                          │                                   │
│  2. OBJECT CREATION                                         │
│     ┌────────────────────────────────────────────┐         │
│     │ • Object pooling for frequent allocations  │         │
│     │ • Minimize deep copies                     │         │
│     │ • Use __slots__ for performance-critical   │         │
│     └────────────────────────────────────────────┘         │
│                          │                                   │
│  3. SIMULATION                                              │
│     ┌────────────────────────────────────────────┐         │
│     │ • Optimize hot paths (damage calc, etc)   │         │
│     │ • Use numpy for numeric operations         │         │
│     │ • Minimize branching in tight loops        │         │
│     └────────────────────────────────────────────┘         │
│                          │                                   │
│  4. PARALLEL EXECUTION                                      │
│     ┌────────────────────────────────────────────┐         │
│     │ • Multiprocessing for tournaments          │         │
│     │ • Async I/O for web server                 │         │
│     │ • Thread pool for independent operations   │         │
│     └────────────────────────────────────────────┘         │
│                                                              │
└─────────────────────────────────────────────────────────────┘

Benchmark Targets:
• Component loading: < 10ms per component
• Unit validation: < 50ms per unit
• Battle simulation: > 100 turns/second
• API response: < 100ms
```

---

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Development Environment                    │
│                                                              │
│  Developer Machine                                           │
│  ┌────────────────────────────────────────────────┐         │
│  │  • Python 3.10+ with venv                      │         │
│  │  • Install: pip install -e ".[dev]"            │         │
│  │  • Run tests: make test                        │         │
│  │  • CLI: battle-sim ...                         │         │
│  └────────────────────────────────────────────────┘         │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   CI/CD Pipeline (GitHub Actions)            │
│                                                              │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌─────────┐ │
│  │   Lint   │──►│   Test   │──►│  Build   │──►│ Publish │ │
│  │          │   │          │   │          │   │         │ │
│  │ • black  │   │ • pytest │   │ • wheel  │   │ • PyPI  │ │
│  │ • mypy   │   │ • cov    │   │ • sdist  │   │ • Docs  │ │
│  └──────────┘   └──────────┘   └──────────┘   └─────────┘ │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   Distribution                               │
│                                                              │
│  ┌──────────────────┐         ┌──────────────────┐         │
│  │      PyPI        │         │  Docker Hub      │         │
│  │  pip install     │         │  docker pull     │         │
│  │  battle-automata │         │  battle-automata │         │
│  └──────────────────┘         └──────────────────┘         │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   Production Usage                           │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │   Library    │  │  CLI Tool    │  │  Web Service    │   │
│  │  (imported)  │  │  (command)   │  │  (container)    │   │
│  └──────────────┘  └──────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## Security Boundaries

```
┌─────────────────────────────────────────────────────────────┐
│                   Untrusted Input                            │
│   User Files (YAML/JSON) │ CLI Arguments │ Web Requests     │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│              Input Validation Layer                          │
│  ┌────────────────────────────────────────────────┐         │
│  │ • Schema validation (Pydantic)                 │         │
│  │ • Path traversal prevention                    │         │
│  │ • File size limits                             │         │
│  │ • Type checking                                │         │
│  └────────────────────────────────────────────────┘         │
└──────────────────┬──────────────────────────────────────────┘
                   │ (Validated Data)
                   ▼
┌─────────────────────────────────────────────────────────────┐
│              Business Logic Layer                            │
│  ┌────────────────────────────────────────────────┐         │
│  │ • Trusted data processing                      │         │
│  │ • Safe operations only                         │         │
│  │ • Sandboxed execution (if plugins)             │         │
│  └────────────────────────────────────────────────┘         │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│              Output Sanitization                             │
│  ┌────────────────────────────────────────────────┐         │
│  │ • Safe serialization                           │         │
│  │ • XSS prevention (web)                         │         │
│  │ • Safe file writes                             │         │
│  └────────────────────────────────────────────────┘         │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
               Trusted Output
```

---

## Legend

```
┌─────────────────────────────────────────────────────────────┐
│  Symbol Guide:                                              │
│                                                              │
│  ┌────────┐    Component/Module                             │
│  │        │                                                  │
│  └────────┘                                                  │
│                                                              │
│  ──────►      Data flow / Dependency                        │
│                                                              │
│  ═══════►     Optional / Can use                            │
│                                                              │
│  │            Vertical flow                                 │
│  ▼                                                           │
│                                                              │
│  ┏━━━━━━━┓    External boundary / Layer                     │
│  ┃       ┃                                                   │
│  ┗━━━━━━━┛                                                  │
│                                                              │
│  ┌───────┬───────┐  Split flow                              │
│          │                                                   │
│                                                              │
│  ┌───────┼───────┐  Merge flow                              │
│          ▼                                                   │
└─────────────────────────────────────────────────────────────┘
```

---

**Document Version**: 1.0
**Created**: 2025-11-14
**Purpose**: Visual reference for system architecture