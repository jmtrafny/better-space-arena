# Battle Automata Engine - Frontend

Cross-platform graphical interface for the Battle Automata Engine.

## Tech Stack

- **Frontend:** React 18 + TypeScript
- **Build Tool:** Vite
- **Graphics:** PixiJS (to be integrated)
- **Backend:** Pyodide (Python via WebAssembly)
- **State:** Zustand
- **Routing:** React Router
- **Styling:** CSS (Tailwind to be added)

## Project Structure

```
src/
├── components/       # React UI components
│   ├── battle/      # Battle viewer components
│   ├── builder/     # Unit builder components
│   └── ui/          # Shared UI components
├── game/            # PixiJS rendering (to be implemented)
├── engine/          # Pyodide integration (to be implemented)
├── state/           # Zustand stores (to be implemented)
├── utils/           # Utility functions
└── pages/           # Route pages
    ├── Home.tsx     # Landing page
    ├── Battle.tsx   # Battle viewer
    └── Builder.tsx  # Unit builder
```

## Getting Started

### Install Dependencies

```bash
npm install
```

### Run Development Server

```bash
npm run dev
```

Opens at http://localhost:5173

### Build for Production

```bash
npm run build
```

### Preview Production Build

```bash
npm run preview
```

## Development Status

### ✅ Phase 1.1 Complete: Project Initialization

- [x] Vite + React + TypeScript project initialized
- [x] Dependencies installed (pyodide, zustand, pixi.js, react-router-dom)
- [x] Project structure created
- [x] TypeScript strict mode configured
- [x] ESLint + Prettier set up
- [x] Dev server runs successfully
- [x] Basic routing implemented

### ⏳ Next: Phase 1.2 - Pyodide Integration

Integrate Python Battle Automata Engine via WebAssembly.

## Routes

- `/` - Home page with navigation
- `/battle` - Battle viewer and simulation
- `/builder` - Unit builder interface

## Dependencies

### Runtime

- `react` - UI framework
- `react-dom` - React DOM bindings
- `react-router-dom` - Client-side routing
- `zustand` - State management
- `pixi.js` - 2D graphics rendering
- `pyodide` - Python in WebAssembly

### Development

- `vite` - Build tool and dev server
- `typescript` - Type safety
- `eslint` - Code linting
- `prettier` - Code formatting
- `@types/*` - TypeScript type definitions

## Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Configuration

### TypeScript

- **Target:** ES2020
- **Strict Mode:** Enabled
- **Module:** ESNext
- **JSX:** react-jsx

### ESLint

- React Hooks rules enabled
- Prettier integration
- TypeScript rules
- Warnings for `any` type

### Prettier

- Single quotes
- 2 space indentation
- Semicolons enabled
- 100 character line width
- ES5 trailing commas

## Next Steps

1. Integrate Pyodide and load Python engine
2. Implement Zustand state management
3. Add PixiJS battle renderer
4. Build unit builder UI
5. Add offline support (PWA)
6. Configure Capacitor for mobile

---

**Phase 2 Status:** Weekend 1 - Foundation & Core Integration (In Progress)
