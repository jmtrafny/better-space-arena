# Phase 2: Cross-Platform Graphical Interface - Implementation Checklist

**Status:** Ready for Implementation ✅
**Architecture:** Approved
**Start Date:** TBD
**Estimated Duration:** 3 weekends (~40 hours)

---

## Pre-Implementation Setup

### ☐ Development Environment

- [ ] **Node.js 20+** installed (`node --version`)
- [ ] **npm** installed (`npm --version`)
- [ ] **Git** configured
- [ ] **VS Code** (or preferred editor) with extensions:
  - [ ] ESLint
  - [ ] Prettier
  - [ ] Tailwind CSS IntelliSense
  - [ ] TypeScript and JavaScript Language Features

### ☐ Optional (Mobile Development)

**For Android:**
- [ ] **Android Studio** installed
- [ ] **Java JDK 17** installed
- [ ] Android SDK (API 33+)
- [ ] Android emulator or physical device

**For iOS (macOS only):**
- [ ] **Xcode 15+** installed
- [ ] **CocoaPods** installed (`sudo gem install cocoapods`)
- [ ] iOS Simulator or physical device
- [ ] Apple Developer account (for device testing)

---

## Weekend 1: Foundation & Core Integration (8-12 hours)

### ☐ Project Initialization (1 hour)

```bash
# Create project
npm create vite@latest battle-automata-frontend -- --template react-ts
cd battle-automata-frontend

# Install dependencies
npm install
npm install pyodide zustand pixi.js @capacitor/core axios
npm install -D @types/node tailwindcss postcss autoprefixer
```

- [ ] Project created successfully
- [ ] Dependencies installed
- [ ] Dev server runs (`npm run dev`)
- [ ] TypeScript compiles without errors

### ☐ Project Structure Setup (1 hour)

Create directory structure:

```
src/
├── components/
│   ├── battle/
│   ├── builder/
│   └── ui/
├── engine/
│   ├── pyodide-loader.ts
│   └── battle-engine-wasm.ts
├── game/
│   ├── BattleRenderer.ts
│   ├── AssetLoader.ts
│   ├── AnimationEngine.ts
│   └── CameraController.ts
├── state/
│   ├── battleStore.ts
│   ├── themeStore.ts
│   └── unitStore.ts
├── utils/
│   └── types.ts
├── App.tsx
└── main.tsx
```

- [ ] Directory structure created
- [ ] Tailwind CSS configured (`npx tailwindcss init -p`)
- [ ] Vite config updated if needed
- [ ] ESLint and Prettier configured

### ☐ Pyodide Integration (3-4 hours)

**File: `src/engine/pyodide-loader.ts`**

```typescript
import { loadPyodide, PyodideInterface } from 'pyodide';

let pyodideInstance: PyodideInterface | null = null;

export async function initPyodide(): Promise<PyodideInterface> {
  if (pyodideInstance) return pyodideInstance;

  console.log('Loading Pyodide...');
  pyodideInstance = await loadPyodide({
    indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.25.0/full/',
  });

  console.log('Pyodide loaded successfully');
  return pyodideInstance;
}
```

**File: `src/engine/battle-engine-wasm.ts`**

```typescript
export class BattleEngineWASM {
  private pyodide: PyodideInterface | null = null;
  private initialized = false;

  async init(): Promise<void> {
    if (this.initialized) return;

    this.pyodide = await initPyodide();

    // Load Battle Automata Engine wheel
    await this.loadEngine();

    this.initialized = true;
  }

  private async loadEngine(): Promise<void> {
    // TODO: Package Python engine as wheel and load it
    // For now, test with simple Python code
    await this.pyodide!.runPythonAsync(`
      print("Python engine loaded!")
    `);
  }

  async simulateBattle(unit1: any, unit2: any, seed: number): Promise<any> {
    this.ensureInitialized();

    // TODO: Call actual Battle Automata Engine
    const result = await this.pyodide!.runPythonAsync(`
      # Placeholder - replace with actual engine call
      {'winner': 'team_a', 'turns': 100}
    `);

    return result.toJs();
  }

  private ensureInitialized(): void {
    if (!this.initialized || !this.pyodide) {
      throw new Error('BattleEngineWASM not initialized. Call init() first.');
    }
  }
}

export const battleEngine = new BattleEngineWASM();
```

**Tasks:**
- [ ] Pyodide loader created
- [ ] BattleEngineWASM wrapper created
- [ ] Test Pyodide initialization in browser console
- [ ] Package Python engine as wheel (`.whl` file)
- [ ] Load wheel in Pyodide
- [ ] Test calling Python engine from TypeScript

**Package Python Engine:**
```bash
# In project root
cd src
python -m build
# Creates dist/battle_automata-1.0.0-py3-none-any.whl

# Copy to frontend public folder
cp dist/*.whl ../battle-automata-frontend/public/
```

### ☐ Basic UI Structure (2 hours)

**Install React Router:**
```bash
npm install react-router-dom
```

**File: `src/App.tsx`**

```tsx
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-900 text-white">
        <nav className="bg-gray-800 p-4">
          <div className="flex gap-4">
            <Link to="/" className="hover:text-blue-400">Home</Link>
            <Link to="/battle" className="hover:text-blue-400">Battle</Link>
            <Link to="/builder" className="hover:text-blue-400">Builder</Link>
          </div>
        </nav>

        <Routes>
          <Route path="/" element={<HomeScreen />} />
          <Route path="/battle" element={<BattleScreen />} />
          <Route path="/builder" element={<BuilderScreen />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

function HomeScreen() {
  return (
    <div className="p-8">
      <h1 className="text-4xl font-bold mb-4">Battle Automata</h1>
      <p>Welcome to the Battle Automata Engine</p>
    </div>
  );
}

function BattleScreen() {
  return <div className="p-8">Battle Viewer (Coming Soon)</div>;
}

function BuilderScreen() {
  return <div className="p-8">Unit Builder (Coming Soon)</div>;
}

export default App;
```

**Tasks:**
- [ ] React Router installed
- [ ] Navigation working
- [ ] Three screens created (Home, Battle, Builder)
- [ ] Basic styling with Tailwind

### ☐ State Management (1 hour)

**File: `src/state/battleStore.ts`**

```typescript
import { create } from 'zustand';

interface BattleResult {
  winner: string;
  turns: number;
  events: any[];
}

interface BattleState {
  currentBattle: BattleResult | null;
  isLoading: boolean;
  error: string | null;

  startBattle: (unit1: any, unit2: any, seed?: number) => Promise<void>;
  clearBattle: () => void;
}

export const useBattleStore = create<BattleState>((set) => ({
  currentBattle: null,
  isLoading: false,
  error: null,

  startBattle: async (unit1, unit2, seed = Date.now()) => {
    set({ isLoading: true, error: null });

    try {
      const { battleEngine } = await import('../engine/battle-engine-wasm');
      await battleEngine.init();

      const result = await battleEngine.simulateBattle(unit1, unit2, seed);

      set({ currentBattle: result, isLoading: false });
    } catch (error) {
      set({ error: String(error), isLoading: false });
    }
  },

  clearBattle: () => set({ currentBattle: null })
}));
```

**Tasks:**
- [ ] Zustand store created
- [ ] Battle state managed
- [ ] Error handling implemented

### ☐ First Battle Simulation (2-3 hours)

**Update `BattleScreen` to run battle:**

```tsx
import { useEffect } from 'react';
import { useBattleStore } from '../state/battleStore';

function BattleScreen() {
  const { currentBattle, isLoading, error, startBattle } = useBattleStore();

  useEffect(() => {
    // Auto-run test battle on mount
    startBattle({ id: 'unit1' }, { id: 'unit2' }, 42);
  }, []);

  if (isLoading) {
    return (
      <div className="p-8">
        <div className="text-center">
          <div className="text-xl mb-2">Loading Pyodide...</div>
          <div className="text-gray-400">This may take a few seconds on first load</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-8">
        <div className="bg-red-900 text-white p-4 rounded">
          Error: {error}
        </div>
      </div>
    );
  }

  if (!currentBattle) {
    return <div className="p-8">No battle loaded</div>;
  }

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Battle Result</h1>
      <div className="bg-gray-800 p-4 rounded">
        <div className="mb-2">Winner: {currentBattle.winner}</div>
        <div className="mb-2">Turns: {currentBattle.turns}</div>
        <div className="mb-2">Events: {currentBattle.events?.length || 0}</div>
      </div>
    </div>
  );
}
```

**Tasks:**
- [ ] Battle can be triggered from UI
- [ ] Loading state shown during Pyodide initialization
- [ ] Battle result displayed (text-based for now)
- [ ] Errors handled gracefully
- [ ] Determinism verified (same seed = same result)

### ☐ Weekend 1 Deliverable

**Success Criteria:**
- [ ] Web app runs at `localhost:5173`
- [ ] Python engine loads in browser (via Pyodide)
- [ ] Can simulate a battle and display result
- [ ] Navigation between screens works
- [ ] No console errors

**Demo:**
- Take screenshot of battle result
- Verify in browser DevTools that Pyodide loaded
- Test determinism (run same battle twice, verify identical result)

---

## Weekend 2: Graphics Layer (12-16 hours)

### ☐ PixiJS Integration (2-3 hours)

**File: `src/game/BattleRenderer.ts`**

```typescript
import { Application, Container, Sprite } from 'pixi.js';

export class BattleRenderer {
  private app: Application;
  private stage: Container;

  async init(canvas: HTMLCanvasElement): Promise<void> {
    this.app = new Application({
      view: canvas,
      width: 1920,
      height: 1080,
      resolution: window.devicePixelRatio || 1,
      autoDensity: true,
      backgroundColor: 0x001122,
      antialias: true
    });

    this.stage = this.app.stage;

    // Start render loop
    this.app.ticker.add(() => this.render());
  }

  render(): void {
    // Rendering logic (60 FPS)
  }

  cleanup(): void {
    this.app.destroy();
  }
}
```

**Create React component:**

```tsx
// src/components/battle/BattleCanvas.tsx
import { useEffect, useRef } from 'react';
import { BattleRenderer } from '../../game/BattleRenderer';

export function BattleCanvas() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const rendererRef = useRef<BattleRenderer | null>(null);

  useEffect(() => {
    if (!canvasRef.current) return;

    const renderer = new BattleRenderer();
    renderer.init(canvasRef.current);
    rendererRef.current = renderer;

    return () => {
      renderer.cleanup();
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className="w-full h-full"
    />
  );
}
```

**Tasks:**
- [ ] PixiJS installed
- [ ] BattleRenderer class created
- [ ] Canvas component created
- [ ] Black canvas renders at 60 FPS
- [ ] FPS counter displayed (for debugging)

### ☐ Asset Loading (3-4 hours)

**File: `src/game/AssetLoader.ts`**

```typescript
import { Assets, Texture } from 'pixi.js';

interface ThemeManifest {
  theme_id: string;
  sprites: Record<string, string>;
}

export class AssetLoader {
  private cache: Map<string, Texture> = new Map();

  async loadTheme(themeId: string): Promise<void> {
    // Load manifest
    const manifestUrl = `/themes/${themeId}/assets/manifest.json`;
    const response = await fetch(manifestUrl);
    const manifest: ThemeManifest = await response.json();

    // Load sprites
    for (const [key, path] of Object.entries(manifest.sprites)) {
      const texture = await Assets.load(`/themes/${themeId}/assets/${path}`);
      this.cache.set(key, texture);
    }
  }

  getTexture(key: string): Texture | null {
    return this.cache.get(key) || null;
  }
}

export const assetLoader = new AssetLoader();
```

**Create test assets:**

```bash
# In Python project: data/themes/space-ships/
mkdir -p assets/sprites/components
mkdir -p assets/sprites/effects

# Create manifest.json
cat > assets/manifest.json << 'EOF'
{
  "theme_id": "space-ships",
  "sprites": {
    "laser_cannon": "sprites/components/laser_cannon.png",
    "laser_beam": "sprites/effects/laser_beam.png"
  }
}
EOF

# Add placeholder images (or create real ones)
# For testing, can use simple colored squares
```

**Tasks:**
- [ ] AssetLoader class created
- [ ] Theme manifest schema defined
- [ ] Test assets created (placeholders OK)
- [ ] Assets load successfully
- [ ] Cached for performance

### ☐ Animation System (4-5 hours)

**File: `src/game/AnimationEngine.ts`**

```typescript
export abstract class Animation {
  constructor(
    public startTime: number,
    public duration: number,
    public priority: number = 0
  ) {}

  abstract update(currentTime: number, deltaTime: number): void;
  abstract render(ctx: any): void;

  isFinished(currentTime: number): boolean {
    return currentTime >= this.startTime + this.duration;
  }
}

export class AnimationEngine {
  private activeAnimations: Animation[] = [];

  add(animation: Animation): void {
    this.activeAnimations.push(animation);
  }

  update(currentTime: number, deltaTime: number): void {
    // Update and remove finished animations
    this.activeAnimations = this.activeAnimations.filter(anim => {
      anim.update(currentTime, deltaTime);
      return !anim.isFinished(currentTime);
    });
  }

  renderAll(ctx: any): void {
    // Sort by priority
    const sorted = [...this.activeAnimations].sort((a, b) => a.priority - b.priority);

    // Render each animation
    for (const anim of sorted) {
      anim.render(ctx);
    }
  }
}
```

**Implement specific animations:**

```typescript
// src/game/animations/ProjectileAnimation.ts
export class ProjectileAnimation extends Animation {
  constructor(
    startTime: number,
    private startX: number,
    private startY: number,
    private endX: number,
    private endY: number,
    travelTime: number
  ) {
    super(startTime, travelTime, 5);
  }

  update(currentTime: number, deltaTime: number): void {
    // Nothing to update
  }

  render(ctx: Container): void {
    const progress = (currentTime - this.startTime) / this.duration;
    const x = lerp(this.startX, this.endX, progress);
    const y = lerp(this.startY, this.endY, progress);

    // Draw laser beam (simple line for now)
    // TODO: Use sprite
  }
}
```

**Tasks:**
- [ ] Animation base class created
- [ ] AnimationEngine manages animation lifecycle
- [ ] Projectile animation implemented
- [ ] Explosion animation implemented
- [ ] Smooth interpolation between 0.1s sim steps

### ☐ Camera Controls (2-3 hours)

**File: `src/game/CameraController.ts`**

```typescript
export class CameraController {
  public x: number = 500;
  public y: number = 500;
  public zoom: number = 1.0;

  private targetX: number = 500;
  private targetY: number = 500;
  private targetZoom: number = 1.0;

  update(deltaTime: number): void {
    // Smooth interpolation
    this.x = lerp(this.x, this.targetX, 0.1);
    this.y = lerp(this.y, this.targetY, 0.1);
    this.zoom = lerp(this.zoom, this.targetZoom, 0.1);
  }

  panTo(x: number, y: number): void {
    this.targetX = x;
    this.targetY = y;
  }

  zoomIn(): void {
    this.targetZoom = Math.min(3.0, this.targetZoom * 1.2);
  }

  zoomOut(): void {
    this.targetZoom = Math.max(0.3, this.targetZoom / 1.2);
  }

  applyTransform(container: Container): void {
    container.position.set(
      window.innerWidth / 2 - this.x * this.zoom,
      window.innerHeight / 2 - this.y * this.zoom
    );
    container.scale.set(this.zoom);
  }
}
```

**Add mouse controls:**

```typescript
// In BattleRenderer.ts
private isDragging = false;
private lastMouseX = 0;
private lastMouseY = 0;

setupControls(canvas: HTMLCanvasElement): void {
  canvas.addEventListener('mousedown', (e) => {
    this.isDragging = true;
    this.lastMouseX = e.clientX;
    this.lastMouseY = e.clientY;
  });

  canvas.addEventListener('mousemove', (e) => {
    if (!this.isDragging) return;

    const dx = e.clientX - this.lastMouseX;
    const dy = e.clientY - this.lastMouseY;

    this.camera.panTo(
      this.camera.x - dx / this.camera.zoom,
      this.camera.y - dy / this.camera.zoom
    );

    this.lastMouseX = e.clientX;
    this.lastMouseY = e.clientY;
  });

  canvas.addEventListener('mouseup', () => {
    this.isDragging = false;
  });

  canvas.addEventListener('wheel', (e) => {
    e.preventDefault();
    if (e.deltaY < 0) {
      this.camera.zoomIn();
    } else {
      this.camera.zoomOut();
    }
  });
}
```

**Tasks:**
- [ ] Camera class created
- [ ] Pan with mouse drag
- [ ] Zoom with mouse wheel
- [ ] Auto-frame units at battle start
- [ ] Smooth camera transitions

### ☐ Battle Replay Controls (2-3 hours)

**Create UI component:**

```tsx
// src/components/battle/BattleControls.tsx
interface Props {
  isPlaying: boolean;
  playbackSpeed: number;
  onTogglePlay: () => void;
  onStop: () => void;
  onSetSpeed: (speed: number) => void;
}

export function BattleControls({
  isPlaying,
  playbackSpeed,
  onTogglePlay,
  onStop,
  onSetSpeed
}: Props) {
  return (
    <div className="bg-gray-800 p-4 flex items-center gap-4">
      {/* Play/Pause button */}
      <button
        onClick={onTogglePlay}
        className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded"
      >
        {isPlaying ? '⏸ Pause' : '▶ Play'}
      </button>

      {/* Stop button */}
      <button
        onClick={onStop}
        className="bg-red-600 hover:bg-red-700 px-4 py-2 rounded"
      >
        ⏹ Stop
      </button>

      {/* Speed controls */}
      <div className="flex gap-2">
        {[0.5, 1, 2, 4].map(speed => (
          <button
            key={speed}
            onClick={() => onSetSpeed(speed)}
            className={`px-3 py-1 rounded ${
              playbackSpeed === speed
                ? 'bg-blue-600'
                : 'bg-gray-700 hover:bg-gray-600'
            }`}
          >
            {speed}x
          </button>
        ))}
      </div>
    </div>
  );
}
```

**Tasks:**
- [ ] Play/pause functionality
- [ ] Stop (reset to start)
- [ ] Speed controls (0.5x, 1x, 2x, 4x)
- [ ] Timeline scrubber (optional for Weekend 2)

### ☐ Weekend 2 Deliverable

**Success Criteria:**
- [ ] Battle animates smoothly at 60 FPS
- [ ] Units move across the screen
- [ ] Lasers fire from unit to unit
- [ ] Explosions play when units are destroyed
- [ ] Camera can pan and zoom
- [ ] Replay controls work (play/pause/speed)

**Demo:**
- Record 10-second video of animated battle
- Verify 60 FPS in browser performance tools
- Show camera controls working
- Show replay controls working

---

## Weekend 3: Polish & Mobile (12-16 hours)

### ☐ Unit Builder UI (4-5 hours)

**File: `src/components/builder/UnitBuilder.tsx`**

```tsx
export function UnitBuilder() {
  const [selectedComponent, setSelectedComponent] = useState<string | null>(null);

  return (
    <div className="h-screen flex">
      {/* Component Palette */}
      <div className="w-64 bg-gray-800 p-4 overflow-y-auto">
        <h2 className="text-xl font-bold mb-4">Components</h2>
        <ComponentPalette onSelect={setSelectedComponent} />
      </div>

      {/* Grid Editor */}
      <div className="flex-1 p-4">
        <GridEditor selectedComponent={selectedComponent} />
      </div>

      {/* Resource Monitor */}
      <div className="w-64 bg-gray-800 p-4">
        <h2 className="text-xl font-bold mb-4">Resources</h2>
        <ResourceMonitor />
      </div>
    </div>
  );
}
```

**Tasks:**
- [ ] Component palette displays available components
- [ ] Grid editor allows placing components
- [ ] Drag-and-drop functionality
- [ ] Resource constraints shown (power, weight, slots)
- [ ] Unit validation
- [ ] Save/load units

### ☐ Offline Support (2-3 hours)

**Install PWA plugin:**

```bash
npm install -D vite-plugin-pwa
```

**Configure Vite:**

```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { VitePWA } from 'vite-plugin-pwa';

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      manifest: {
        name: 'Battle Automata',
        short_name: 'BattleAuto',
        description: 'Build units and simulate battles',
        theme_color: '#1a1a1a',
        icons: [
          {
            src: '/icon-192.png',
            sizes: '192x192',
            type: 'image/png'
          },
          {
            src: '/icon-512.png',
            sizes: '512x512',
            type: 'image/png'
          }
        ]
      }
    })
  ]
});
```

**Tasks:**
- [ ] Vite PWA plugin installed
- [ ] Manifest.json configured
- [ ] Service worker generated
- [ ] App works offline
- [ ] Install prompt appears on mobile

### ☐ Capacitor Setup (2-3 hours)

```bash
# Install Capacitor
npm install @capacitor/cli @capacitor/core
npx cap init

# Add platforms
npx cap add android
npx cap add ios  # macOS only
```

**Configure:**

```typescript
// capacitor.config.ts
import { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.battleautomata.app',
  appName: 'Battle Automata',
  webDir: 'dist',
  server: {
    androidScheme: 'https'
  }
};

export default config;
```

**Tasks:**
- [ ] Capacitor initialized
- [ ] Android platform added
- [ ] iOS platform added (if on macOS)
- [ ] Config file created

### ☐ Build Scripts (1-2 hours)

**File: `scripts/build-web.sh`**

```bash
#!/bin/bash
set -e

echo "🌐 Building PWA..."
npm run build

echo "✅ PWA build complete: dist/"
```

**File: `scripts/build-android.sh`**

```bash
#!/bin/bash
set -e

echo "🤖 Building Android app..."

# Build web bundle
npm run build

# Sync to Android
npx cap sync android

# Build APK
cd android
./gradlew assembleDebug

echo "✅ APK: android/app/build/outputs/apk/debug/app-debug.apk"
```

**File: `scripts/build-ios.sh`** (macOS only)

```bash
#!/bin/bash
set -e

echo "🍎 Building iOS app..."

# Build web bundle
npm run build

# Sync to iOS
npx cap sync ios

echo "✅ iOS project ready"
echo "Open ios/App/App.xcworkspace in Xcode to build"
```

**Update package.json:**

```json
{
  "scripts": {
    "build:web": "./scripts/build-web.sh",
    "build:android": "./scripts/build-android.sh",
    "build:ios": "./scripts/build-ios.sh"
  }
}
```

**Tasks:**
- [ ] Build scripts created
- [ ] Made executable (`chmod +x scripts/*.sh`)
- [ ] PWA builds successfully
- [ ] Android APK builds successfully
- [ ] iOS project opens in Xcode (if on macOS)

### ☐ Performance Optimization (2-3 hours)

**Implement optimizations:**

```typescript
// Sprite batching
class SpriteBatcher {
  private batches: Map<string, Sprite[]> = new Map();

  add(sprite: Sprite, key: string): void {
    if (!this.batches.has(key)) {
      this.batches.set(key, []);
    }
    this.batches.get(key)!.push(sprite);
  }

  render(): void {
    for (const [key, sprites] of this.batches) {
      // Render all sprites with same texture in one batch
      for (const sprite of sprites) {
        sprite.render();
      }
    }
    this.batches.clear();
  }
}

// Object pooling
class ParticlePool {
  private pool: Particle[] = [];

  acquire(): Particle {
    return this.pool.pop() || new Particle();
  }

  release(particle: Particle): void {
    particle.reset();
    this.pool.push(particle);
  }
}

// Quality settings
interface GraphicsQuality {
  particles: boolean;
  shadows: boolean;
  targetFPS: 30 | 60;
}

const QUALITY_PRESETS: Record<string, GraphicsQuality> = {
  low: { particles: false, shadows: false, targetFPS: 30 },
  medium: { particles: true, shadows: false, targetFPS: 60 },
  high: { particles: true, shadows: true, targetFPS: 60 }
};
```

**Tasks:**
- [ ] Sprite batching implemented
- [ ] Object pooling for particles
- [ ] Quality settings (low/medium/high)
- [ ] Code splitting (lazy load routes)
- [ ] Bundle size < 1MB (excluding Pyodide)

### ☐ Deploy PWA (1-2 hours)

**Option 1: Netlify**

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Deploy
npm run build
netlify deploy --prod --dir=dist
```

**Option 2: Vercel**

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod
```

**Tasks:**
- [ ] Production build created
- [ ] Deployed to Netlify or Vercel
- [ ] Custom domain configured (optional)
- [ ] HTTPS enabled
- [ ] Service worker working
- [ ] App installable on mobile

### ☐ Weekend 3 Deliverable

**Success Criteria:**
- [ ] PWA deployed and accessible online
- [ ] Unit builder UI functional
- [ ] App works offline
- [ ] Android APK builds
- [ ] iOS project ready (if on macOS)
- [ ] 60 FPS on desktop, 30-60 FPS on mobile
- [ ] Bundle size optimized

**Demo:**
- Install PWA on phone
- Build custom unit
- Simulate battle
- Show offline functionality
- Test on Android device (APK)

---

## Final Checklist

### ☐ Code Quality

- [ ] TypeScript strict mode enabled
- [ ] ESLint configured and passing
- [ ] Prettier configured
- [ ] No console errors in production build
- [ ] Code commented where needed

### ☐ Testing

- [ ] Unit tests for core logic (optional but recommended)
- [ ] Manual testing on Chrome, Firefox, Safari
- [ ] Manual testing on Android device
- [ ] Manual testing on iOS device (if possible)
- [ ] Determinism verified (same seed = same result)

### ☐ Documentation

- [ ] README.md with setup instructions
- [ ] Build instructions
- [ ] Deployment guide
- [ ] Architecture diagrams (if needed)

### ☐ Performance

- [ ] Lighthouse score > 90 (PWA)
- [ ] 60 FPS on desktop
- [ ] 30+ FPS on mid-range mobile (2020+)
- [ ] Initial load < 5s (after cache)

### ☐ Deployment

- [ ] PWA live at public URL
- [ ] Android APK available for download
- [ ] iOS IPA ready for TestFlight (optional)

---

## Success Metrics

**Phase 2 Complete When:**

✅ PWA:
- Loads in < 5s (after Pyodide cache)
- Works offline
- Installable
- 60 FPS battles

✅ Android:
- APK builds
- Runs on Android 7+
- 60 FPS on mid-range devices

✅ iOS:
- IPA builds (macOS)
- Runs on iOS 13+
- 60 FPS on iPhone 8+

✅ Features:
- Battle viewer with animations
- Replay controls
- Unit builder
- Theme assets load
- Offline-capable

---

## Troubleshooting

### Pyodide Issues

**Problem:** Pyodide fails to load
**Solution:**
- Check browser console for errors
- Verify CDN URL is correct
- Try local Pyodide copy if CDN blocked

**Problem:** Python wheel not loading
**Solution:**
- Verify wheel file path
- Check wheel is in `public/` folder
- Ensure wheel is compatible (pure Python, no C extensions)

### Performance Issues

**Problem:** Low FPS on mobile
**Solution:**
- Enable quality settings (low/medium)
- Reduce particle effects
- Implement LOD system
- Profile with browser DevTools

### Build Issues

**Problem:** Android build fails
**Solution:**
- Check Java version (need JDK 17)
- Run `./gradlew clean` in `android/`
- Check Android SDK installation

**Problem:** iOS build fails
**Solution:**
- Run `pod install` in `ios/App/`
- Check Xcode version (need 15+)
- Verify provisioning profile

---

## Resources

**Documentation:**
- [Pyodide Docs](https://pyodide.org/) - Python in WebAssembly
- [PixiJS Guide](https://pixijs.io/guides/) - 2D rendering
- [Capacitor Docs](https://capacitorjs.com/docs) - Native wrapping
- [Zustand Docs](https://zustand-demo.pmnd.rs/) - State management

**Architecture:**
- `docs/phase2/README.md` - Architecture overview
- `prompt.md` - Complete implementation guide

**Support:**
- GitHub Issues for questions
- Browser DevTools for debugging
- React DevTools extension

---

**Good luck building the graphical interface!** 🚀

Remember: Start with Weekend 1 (Pyodide integration) before moving to graphics. Each weekend builds on the previous one.
