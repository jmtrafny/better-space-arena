/**
 * ReplayController - Event playback state machine for battle replay
 *
 * Converts discrete battle events (0.1s timesteps) into smooth 60 FPS animation
 * Manages playback state, speed control, timeline scrubbing, and event callbacks
 */

// ============================================================================
// Types
// ============================================================================

export interface BattleEvent {
  timestamp: number;
  turn?: number;
  event_type?: string;
  type?: string; // legacy support
  data: Record<string, unknown>;
}

export type PlaybackState = 'stopped' | 'playing' | 'paused' | 'completed';

export type EventCallback = (event: BattleEvent) => void;

interface EventIndex {
  event: BattleEvent;
  index: number;
  processed: boolean;
}

// ============================================================================
// ReplayController
// ============================================================================

export class ReplayController {
  private events: BattleEvent[] = [];
  private eventIndices: EventIndex[] = [];
  private state: PlaybackState = 'stopped';
  private currentTime: number = 0;
  private playbackSpeed: number = 1.0;
  private totalDuration: number = 0;
  private callbacks: EventCallback[] = [];

  // Event processing
  private nextEventIndex: number = 0;
  private lastProcessedIndex: number = -1;

  // Time accumulation
  private accumulatedDeltaTime: number = 0;

  /**
   * Create a new ReplayController with battle events
   * @param events Array of battle events (will be sorted by timestamp)
   */
  constructor(events: BattleEvent[]) {
    this.setEvents(events);
  }

  // ============================================================================
  // Public API - Playback Control
  // ============================================================================

  /**
   * Start or resume playback
   */
  play(): void {
    if (this.state === 'completed') {
      // Restart from beginning if completed
      this.stop();
    }

    if (this.state !== 'playing') {
      this.state = 'playing';
      console.log(`[ReplayController] Playing at ${this.playbackSpeed}x speed`);
    }
  }

  /**
   * Pause playback
   */
  pause(): void {
    if (this.state === 'playing') {
      this.state = 'paused';
      console.log('[ReplayController] Paused at', this.currentTime.toFixed(2), 's');
    }
  }

  /**
   * Stop playback and reset to beginning
   */
  stop(): void {
    this.state = 'stopped';
    this.currentTime = 0;
    this.nextEventIndex = 0;
    this.lastProcessedIndex = -1;
    this.accumulatedDeltaTime = 0;
    this.resetProcessedFlags();
    console.log('[ReplayController] Stopped');
  }

  /**
   * Step forward or backward by one event
   * @param direction 'forward' or 'backward'
   */
  step(direction: 'forward' | 'backward'): void {
    const wasPaused = this.state === 'paused' || this.state === 'stopped';

    if (direction === 'forward') {
      if (this.nextEventIndex < this.events.length) {
        const event = this.events[this.nextEventIndex];
        this.currentTime = event.timestamp;
        this.processEventsUpToTime(this.currentTime);

        if (wasPaused) {
          this.state = 'paused';
        }
      }
    } else {
      // Step backward
      if (this.nextEventIndex > 0) {
        const prevIndex = this.nextEventIndex - 2;
        if (prevIndex >= 0) {
          const event = this.events[prevIndex];
          this.seekTo(event.timestamp);
        } else {
          this.seekTo(0);
        }

        if (wasPaused) {
          this.state = 'paused';
        }
      }
    }
  }

  /**
   * Set playback speed multiplier
   * @param speed Speed multiplier (e.g., 0.5, 1.0, 2.0, 4.0)
   */
  setSpeed(speed: number): void {
    this.playbackSpeed = Math.max(0.1, Math.min(10.0, speed));
    console.log(`[ReplayController] Speed set to ${this.playbackSpeed}x`);
  }

  /**
   * Seek to a specific time in the replay
   * @param time Target time in seconds
   */
  seekTo(time: number): void {
    const clampedTime = Math.max(0, Math.min(this.totalDuration, time));
    this.currentTime = clampedTime;

    // Reset event processing
    this.nextEventIndex = 0;
    this.lastProcessedIndex = -1;
    this.resetProcessedFlags();

    // Process all events up to the target time
    this.processEventsUpToTime(clampedTime, true);

    // Update state
    if (clampedTime >= this.totalDuration) {
      this.state = 'completed';
    } else if (this.state === 'completed') {
      this.state = 'paused';
    }

    console.log('[ReplayController] Seeked to', clampedTime.toFixed(2), 's');
  }

  // ============================================================================
  // Public API - State Queries
  // ============================================================================

  /**
   * Get current playback time
   */
  getCurrentTime(): number {
    return this.currentTime;
  }

  /**
   * Get total duration of the replay
   */
  getTotalDuration(): number {
    return this.totalDuration;
  }

  /**
   * Get current playback state
   */
  getState(): PlaybackState {
    return this.state;
  }

  /**
   * Get current playback speed
   */
  getSpeed(): number {
    return this.playbackSpeed;
  }

  /**
   * Get progress as a fraction (0-1)
   */
  getProgress(): number {
    if (this.totalDuration <= 0) return 0;
    return Math.min(1.0, this.currentTime / this.totalDuration);
  }

  /**
   * Get all events
   */
  getEvents(): BattleEvent[] {
    return [...this.events];
  }

  /**
   * Get events that have been processed up to current time
   */
  getProcessedEvents(): BattleEvent[] {
    return this.events.filter((_, idx) =>
      this.eventIndices[idx]?.processed || false
    );
  }

  // ============================================================================
  // Public API - Event Callbacks
  // ============================================================================

  /**
   * Register a callback to be fired when events occur
   * @param callback Function to call with each event
   * @returns Unsubscribe function
   */
  onEvent(callback: EventCallback): () => void {
    this.callbacks.push(callback);

    // Return unsubscribe function
    return () => {
      const index = this.callbacks.indexOf(callback);
      if (index !== -1) {
        this.callbacks.splice(index, 1);
      }
    };
  }

  // ============================================================================
  // Public API - Update Loop
  // ============================================================================

  /**
   * Update the replay controller (call each frame)
   * @param deltaTime Time elapsed since last update (in seconds)
   */
  update(deltaTime: number): void {
    if (this.state !== 'playing') {
      return;
    }

    // Accumulate delta time (helps with variable frame rates)
    this.accumulatedDeltaTime += deltaTime * this.playbackSpeed;

    // Update current time (small steps for stability)
    const maxStep = 1.0; // Max 1 second per frame
    const step = Math.min(this.accumulatedDeltaTime, maxStep);

    this.currentTime += step;
    this.accumulatedDeltaTime -= step;

    // Process events up to current time
    this.processEventsUpToTime(this.currentTime);

    // Check if replay is completed
    if (this.currentTime >= this.totalDuration) {
      this.currentTime = this.totalDuration;
      this.state = 'completed';
      console.log('[ReplayController] Playback completed');
    }
  }

  // ============================================================================
  // Public API - Lifecycle
  // ============================================================================

  /**
   * Clean up resources
   */
  cleanup(): void {
    this.callbacks = [];
    this.events = [];
    this.eventIndices = [];
    this.state = 'stopped';
    console.log('[ReplayController] Cleaned up');
  }

  // ============================================================================
  // Private Methods - Event Management
  // ============================================================================

  /**
   * Set events and prepare for playback
   */
  private setEvents(events: BattleEvent[]): void {
    // Sort events by timestamp
    this.events = [...events].sort((a, b) => a.timestamp - b.timestamp);

    // Create event indices
    this.eventIndices = this.events.map((event, index) => ({
      event,
      index,
      processed: false,
    }));

    // Calculate total duration
    if (this.events.length > 0) {
      this.totalDuration = this.events[this.events.length - 1].timestamp;
    } else {
      this.totalDuration = 0;
    }

    console.log(
      `[ReplayController] Loaded ${this.events.length} events, duration: ${this.totalDuration.toFixed(2)}s`
    );
  }

  /**
   * Process all events up to a given time
   */
  private processEventsUpToTime(time: number, isSeeking: boolean = false): void {
    while (this.nextEventIndex < this.events.length) {
      const event = this.events[this.nextEventIndex];

      if (event.timestamp > time) {
        break;
      }

      // Mark as processed
      this.eventIndices[this.nextEventIndex].processed = true;
      this.lastProcessedIndex = this.nextEventIndex;
      this.nextEventIndex++;

      // Fire callbacks (skip during seeking for performance)
      if (!isSeeking) {
        this.fireEventCallbacks(event);
      }
    }

    // If seeking, fire one callback for the last processed event
    if (isSeeking && this.lastProcessedIndex >= 0) {
      const lastEvent = this.events[this.lastProcessedIndex];
      this.fireEventCallbacks(lastEvent);
    }
  }

  /**
   * Fire all registered callbacks for an event
   */
  private fireEventCallbacks(event: BattleEvent): void {
    for (const callback of this.callbacks) {
      try {
        callback(event);
      } catch (error) {
        console.error('[ReplayController] Error in event callback:', error);
      }
    }
  }

  /**
   * Reset all processed flags
   */
  private resetProcessedFlags(): void {
    for (const index of this.eventIndices) {
      index.processed = false;
    }
  }

  // ============================================================================
  // Private Methods - Binary Search (optimized for future use)
  // ============================================================================

  /**
   * Find the index of the first event at or after the given time
   * Uses binary search for O(log n) performance
   * Note: Currently unused but kept for future optimization
   */
  private _findEventIndexAtTime(time: number): number {
    if (this.events.length === 0) return 0;
    if (time <= this.events[0].timestamp) return 0;
    if (time >= this.events[this.events.length - 1].timestamp) {
      return this.events.length;
    }

    let left = 0;
    let right = this.events.length - 1;

    while (left < right) {
      const mid = Math.floor((left + right) / 2);
      const event = this.events[mid];

      if (event.timestamp < time) {
        left = mid + 1;
      } else {
        right = mid;
      }
    }

    return left;
  }

  // ============================================================================
  // Utility Methods
  // ============================================================================

  /**
   * Get debug information about current state
   */
  getDebugInfo(): Record<string, unknown> {
    return {
      state: this.state,
      currentTime: this.currentTime.toFixed(2),
      totalDuration: this.totalDuration.toFixed(2),
      progress: (this.getProgress() * 100).toFixed(1) + '%',
      playbackSpeed: this.playbackSpeed + 'x',
      nextEventIndex: this.nextEventIndex,
      totalEvents: this.events.length,
      processedEvents: this.eventIndices.filter(e => e.processed).length,
    };
  }

  /**
   * Format time as MM:SS
   */
  static formatTime(seconds: number): string {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }
}
