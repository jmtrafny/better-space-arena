/**
 * Interpolation utilities for smooth animation
 *
 * Converts discrete simulation events (0.1s timesteps) into smooth 60 FPS animation
 * Provides position interpolation, easing functions, and velocity-based smoothing
 */

// ============================================================================
// Types
// ============================================================================

export interface PositionKeyframe {
  time: number;
  x: number;
  y: number;
}

export interface VelocityData {
  vx: number;
  vy: number;
}

// ============================================================================
// Core Interpolation Functions
// ============================================================================

/**
 * Linear interpolation between two values
 * @param a Start value
 * @param b End value
 * @param t Interpolation factor (0-1)
 * @returns Interpolated value
 */
export function lerp(a: number, b: number, t: number): number {
  return a + (b - a) * t;
}

/**
 * Clamp a value between min and max
 */
export function clamp(value: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, value));
}

/**
 * Inverse lerp - find t given a, b, and value
 */
export function inverseLerp(a: number, b: number, value: number): number {
  if (Math.abs(b - a) < 0.0001) return 0;
  return (value - a) / (b - a);
}

// ============================================================================
// Easing Functions
// ============================================================================

/**
 * Smooth ease-in-out using smoothstep
 * @param t Input value (0-1)
 * @returns Eased value (0-1)
 */
export function easeInOut(t: number): number {
  t = clamp(t, 0, 1);
  return t * t * (3 - 2 * t);
}

/**
 * Ease-in (accelerate from zero velocity)
 */
export function easeIn(t: number): number {
  t = clamp(t, 0, 1);
  return t * t;
}

/**
 * Ease-out (decelerate to zero velocity)
 */
export function easeOut(t: number): number {
  t = clamp(t, 0, 1);
  return t * (2 - t);
}

/**
 * Cubic ease-in-out for smoother animation
 */
export function easeInOutCubic(t: number): number {
  t = clamp(t, 0, 1);
  return t < 0.5
    ? 4 * t * t * t
    : 1 - Math.pow(-2 * t + 2, 3) / 2;
}

// ============================================================================
// Position Interpolation
// ============================================================================

/**
 * Find the two keyframes that surround the current time
 * Returns indices [before, after] or [-1, -1] if not found
 */
function findKeyframeBracket(
  keyframes: PositionKeyframe[],
  currentTime: number
): [number, number] {
  if (keyframes.length === 0) return [-1, -1];
  if (keyframes.length === 1) return [0, 0];

  // Before first keyframe
  if (currentTime <= keyframes[0].time) {
    return [0, 0];
  }

  // After last keyframe
  if (currentTime >= keyframes[keyframes.length - 1].time) {
    const lastIdx = keyframes.length - 1;
    return [lastIdx, lastIdx];
  }

  // Binary search for the bracket
  let left = 0;
  let right = keyframes.length - 1;

  while (left <= right) {
    const mid = Math.floor((left + right) / 2);
    const kf = keyframes[mid];

    if (kf.time === currentTime) {
      return [mid, mid];
    } else if (kf.time < currentTime) {
      // Check if next keyframe is after currentTime
      if (mid + 1 < keyframes.length && keyframes[mid + 1].time > currentTime) {
        return [mid, mid + 1];
      }
      left = mid + 1;
    } else {
      right = mid - 1;
    }
  }

  // Fallback - should not reach here if keyframes are sorted
  return [-1, -1];
}

/**
 * Interpolate position between keyframes at a given time
 * @param keyframes Array of position keyframes (must be sorted by time)
 * @param currentTime Current animation time
 * @param useEasing Apply easing to interpolation (default: false for linear)
 * @returns Interpolated position { x, y }
 */
export function interpolatePosition(
  keyframes: PositionKeyframe[],
  currentTime: number,
  useEasing: boolean = false
): { x: number; y: number } {
  if (keyframes.length === 0) {
    return { x: 0, y: 0 };
  }

  if (keyframes.length === 1) {
    return { x: keyframes[0].x, y: keyframes[0].y };
  }

  const [beforeIdx, afterIdx] = findKeyframeBracket(keyframes, currentTime);

  if (beforeIdx === -1) {
    // Fallback to first keyframe
    return { x: keyframes[0].x, y: keyframes[0].y };
  }

  const before = keyframes[beforeIdx];
  const after = keyframes[afterIdx];

  // If same keyframe (at edges or exact match)
  if (beforeIdx === afterIdx) {
    return { x: before.x, y: before.y };
  }

  // Calculate interpolation factor
  const t = inverseLerp(before.time, after.time, currentTime);
  const easedT = useEasing ? easeInOut(t) : t;

  return {
    x: lerp(before.x, after.x, easedT),
    y: lerp(before.y, after.y, easedT),
  };
}

/**
 * Calculate velocity between two keyframes
 * @param kf1 First keyframe
 * @param kf2 Second keyframe
 * @returns Velocity in units/second { vx, vy }
 */
export function calculateVelocity(
  kf1: PositionKeyframe,
  kf2: PositionKeyframe
): VelocityData {
  const dt = kf2.time - kf1.time;

  if (dt <= 0.0001) {
    return { vx: 0, vy: 0 };
  }

  return {
    vx: (kf2.x - kf1.x) / dt,
    vy: (kf2.y - kf1.y) / dt,
  };
}

/**
 * Interpolate position with velocity-based smoothing
 * Uses velocity at keyframes for smoother trajectories
 */
export function interpolatePositionWithVelocity(
  keyframes: PositionKeyframe[],
  currentTime: number
): { x: number; y: number; velocity: VelocityData } {
  const position = interpolatePosition(keyframes, currentTime, false);

  if (keyframes.length < 2) {
    return { ...position, velocity: { vx: 0, vy: 0 } };
  }

  const [beforeIdx, afterIdx] = findKeyframeBracket(keyframes, currentTime);

  if (beforeIdx === -1 || beforeIdx === afterIdx) {
    return { ...position, velocity: { vx: 0, vy: 0 } };
  }

  const velocity = calculateVelocity(keyframes[beforeIdx], keyframes[afterIdx]);

  return { ...position, velocity };
}

/**
 * Check if keyframes are sorted by time (validation utility)
 */
export function areKeyframesSorted(keyframes: PositionKeyframe[]): boolean {
  for (let i = 1; i < keyframes.length; i++) {
    if (keyframes[i].time < keyframes[i - 1].time) {
      return false;
    }
  }
  return true;
}

/**
 * Sort keyframes by time (in-place)
 */
export function sortKeyframes(keyframes: PositionKeyframe[]): PositionKeyframe[] {
  return keyframes.sort((a, b) => a.time - b.time);
}

// ============================================================================
// Vector Math Utilities
// ============================================================================

/**
 * Calculate distance between two points
 */
export function distance(x1: number, y1: number, x2: number, y2: number): number {
  const dx = x2 - x1;
  const dy = y2 - y1;
  return Math.sqrt(dx * dx + dy * dy);
}

/**
 * Calculate angle in radians from point 1 to point 2
 */
export function angle(x1: number, y1: number, x2: number, y2: number): number {
  return Math.atan2(y2 - y1, x2 - x1);
}

/**
 * Normalize vector to unit length
 */
export function normalize(vx: number, vy: number): { x: number; y: number } {
  const mag = Math.sqrt(vx * vx + vy * vy);
  if (mag < 0.0001) {
    return { x: 0, y: 0 };
  }
  return { x: vx / mag, y: vy / mag };
}
