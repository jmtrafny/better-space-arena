/**
 * Battle Engine WASM - TypeScript wrapper for Python Battle Automata Engine
 *
 * Provides type-safe TypeScript interface to Python engine running in Pyodide
 */

import { pyodideLoader } from './pyodide-loader';
import type {
  BattleResult,
  BattleConfig,
  Unit,
  Component,
  ThemeMetadata,
} from '../utils/types';

export class BattleEngineWASM {
  private initialized = false;

  /**
   * Initialize the engine (loads Pyodide and installs Python package)
   */
  async init(): Promise<void> {
    if (this.initialized) {
      return;
    }

    console.log('Initializing Battle Engine WASM...');

    // Load Pyodide
    await pyodideLoader.init();

    // Install Battle Automata wheel
    // Wheel is served from /wheels/ directory
    const wheelUrl = '/wheels/battle_automata-0.1.0-py3-none-any.whl';

    console.log(`Installing Battle Automata from ${wheelUrl}...`);

    await pyodideLoader.installPackage(wheelUrl);

    // Verify installation
    await pyodideLoader.runPython(`
      import battle_automata
      print(f"Battle Automata Engine v{battle_automata.__version__} loaded")
    `);

    this.initialized = true;
    console.log('Battle Engine WASM initialized successfully');
  }

  /**
   * Simulate a battle between two units
   */
  async simulateBattle(
    unit1: Unit,
    unit2: Unit,
    config?: BattleConfig
  ): Promise<BattleResult> {
    await this.init();

    const pyodide = pyodideLoader.getPyodide();

    // Pass units and config to Python
    pyodide.globals.set('unit1_json', JSON.stringify(unit1));
    pyodide.globals.set('unit2_json', JSON.stringify(unit2));
    pyodide.globals.set('config_json', JSON.stringify(config || {}));

    // Run battle simulation in Python
    const resultPy = await pyodideLoader.runPythonAsync(`
      import json
      from battle_automata.api.battle import Battle, BattleConfig

      # Parse inputs
      unit1_data = json.loads(unit1_json)
      unit2_data = json.loads(unit2_json)
      config_data = json.loads(config_json)

      # Create battle config
      arena_size = config_data.get('arena_size', [1000, 1000])
      battle_config = BattleConfig(
        seed=config_data.get('seed', 12345),
        arena_width=arena_size[0],
        arena_height=arena_size[1],
        max_duration=config_data.get('max_duration', 60.0),
        time_step=config_data.get('time_step', 0.1)
      )

      # Create and run battle
      battle = Battle(config=battle_config)
      result = battle.simulate()

      # Convert result to dictionary for JavaScript
      result_dict = result.to_dict()
      result_dict
    `);

    // Convert Python result to JavaScript
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const result = (resultPy as any).toJs({ dict_converter: Object.fromEntries });

    return result as BattleResult;
  }

  /**
   * Load components from theme
   */
  async loadComponents(themeName: string): Promise<Component[]> {
    await this.init();

    const pyodide = pyodideLoader.getPyodide();
    pyodide.globals.set('theme_name', themeName);

    const componentsPy = await pyodideLoader.runPythonAsync(`
      from battle_automata.utils.theme import ThemeLoader
      from battle_automata.core.registry import ComponentRegistry
      import json

      # Load theme
      theme_loader = ThemeLoader()
      registry = ComponentRegistry()

      # TODO: Implement theme loading
      # For now, return mock components
      [
        {
          'id': 'laser_cannon_mk1',
          'name': 'Laser Cannon Mk1',
          'type': 'offensive',
          'category': 'weapon',
          'stats': {
            'damage': 50,
            'range': 100,
            'fire_rate': 1.0,
            'accuracy': 0.85
          },
          'resources': {
            'power_draw': 20,
            'weight': 50,
            'slots': 1
          }
        },
        {
          'id': 'armor_plate',
          'name': 'Armor Plate',
          'type': 'defensive',
          'category': 'armor',
          'stats': {
            'armor': 100
          },
          'resources': {
            'power_draw': 0,
            'weight': 30,
            'slots': 1
          }
        }
      ]
    `);

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const components = (componentsPy as any).toJs({ dict_converter: Object.fromEntries });
    return components as Component[];
  }

  /**
   * Load theme metadata
   */
  async loadTheme(themeName: string): Promise<ThemeMetadata> {
    await this.init();

    const pyodide = pyodideLoader.getPyodide();
    pyodide.globals.set('theme_name', themeName);

    const themePy = await pyodideLoader.runPythonAsync(`
      # TODO: Implement theme loading
      # For now, return mock metadata
      {
        'id': 'space-ships',
        'name': 'Space Ships',
        'description': 'Spaceship combat theme',
        'version': '0.1.0'
      }
    `);

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const theme = (themePy as any).toJs({ dict_converter: Object.fromEntries });
    return theme as ThemeMetadata;
  }

  /**
   * Check if engine is initialized
   */
  isInitialized(): boolean {
    return this.initialized;
  }
}

// Singleton instance
export const battleEngine = new BattleEngineWASM();
