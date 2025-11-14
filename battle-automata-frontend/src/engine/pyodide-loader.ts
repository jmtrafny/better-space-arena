/**
 * Pyodide Loader - Initializes and manages Pyodide WebAssembly runtime
 *
 * Loads Python interpreter in browser and provides utilities for:
 * - Lazy initialization (only load when needed)
 * - Progress tracking during load
 * - Error handling
 * - Package installation
 */

import { loadPyodide, PyodideInterface } from 'pyodide';

export type LoadingState = 'idle' | 'loading' | 'ready' | 'error';

export interface PyodideLoaderState {
  state: LoadingState;
  progress: number; // 0-100
  error: string | null;
}

class PyodideLoader {
  private pyodide: PyodideInterface | null = null;
  private loadPromise: Promise<PyodideInterface> | null = null;
  private state: PyodideLoaderState = {
    state: 'idle',
    progress: 0,
    error: null,
  };
  private stateListeners: Array<(state: PyodideLoaderState) => void> = [];

  /**
   * Get current loading state
   */
  getState(): PyodideLoaderState {
    return { ...this.state };
  }

  /**
   * Subscribe to state changes
   */
  onStateChange(listener: (state: PyodideLoaderState) => void): () => void {
    this.stateListeners.push(listener);
    // Return unsubscribe function
    return () => {
      this.stateListeners = this.stateListeners.filter((l) => l !== listener);
    };
  }

  /**
   * Update state and notify listeners
   */
  private setState(updates: Partial<PyodideLoaderState>) {
    this.state = { ...this.state, ...updates };
    this.stateListeners.forEach((listener) => listener(this.state));
  }

  /**
   * Initialize Pyodide (lazy load)
   * Subsequent calls return the same instance
   */
  async init(): Promise<PyodideInterface> {
    // Already initialized
    if (this.pyodide) {
      return this.pyodide;
    }

    // Already loading
    if (this.loadPromise) {
      return this.loadPromise;
    }

    // Start loading
    this.setState({ state: 'loading', progress: 0, error: null });

    this.loadPromise = this.load();

    try {
      this.pyodide = await this.loadPromise;
      this.setState({ state: 'ready', progress: 100, error: null });
      return this.pyodide;
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      this.setState({ state: 'error', progress: 0, error: errorMsg });
      this.loadPromise = null;
      throw error;
    }
  }

  /**
   * Internal load implementation
   */
  private async load(): Promise<PyodideInterface> {
    try {
      // Load Pyodide from CDN
      // Using version 0.29.0 (matches installed package)
      this.setState({ progress: 10 });

      const pyodide = await loadPyodide({
        indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.29.0/full/',
      });

      this.setState({ progress: 60 });

      // Install micropip for package installation
      await pyodide.loadPackage('micropip');

      this.setState({ progress: 80 });

      console.log('Pyodide loaded successfully');
      console.log('Python version:', pyodide.runPython('import sys; sys.version'));

      return pyodide;
    } catch (error) {
      console.error('Failed to load Pyodide:', error);
      throw error;
    }
  }

  /**
   * Install Python package from PyPI or wheel URL
   */
  async installPackage(packageName: string): Promise<void> {
    const pyodide = await this.init();

    try {
      await pyodide.runPythonAsync(`
        import micropip
        await micropip.install('${packageName}')
      `);
      console.log(`Package installed: ${packageName}`);
    } catch (error) {
      console.error(`Failed to install package ${packageName}:`, error);
      throw error;
    }
  }

  /**
   * Run Python code
   */
  async runPython(code: string): Promise<unknown> {
    const pyodide = await this.init();
    return pyodide.runPython(code);
  }

  /**
   * Run async Python code
   */
  async runPythonAsync(code: string): Promise<unknown> {
    const pyodide = await this.init();
    return pyodide.runPythonAsync(code);
  }

  /**
   * Get Pyodide instance (must be initialized first)
   */
  getPyodide(): PyodideInterface {
    if (!this.pyodide) {
      throw new Error('Pyodide not initialized. Call init() first.');
    }
    return this.pyodide;
  }

  /**
   * Check if Pyodide is ready
   */
  isReady(): boolean {
    return this.state.state === 'ready';
  }
}

// Singleton instance
export const pyodideLoader = new PyodideLoader();

// Export for testing/advanced usage
export { PyodideLoader };
