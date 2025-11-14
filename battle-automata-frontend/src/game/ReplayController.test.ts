/**
 * ReplayController Test/Demo
 *
 * Simple demonstration of ReplayController functionality
 * Run this to verify the implementation works correctly
 */

import { ReplayController, BattleEvent } from './ReplayController';
import { interpolatePosition, PositionKeyframe, lerp, easeInOut } from './interpolation';

// ============================================================================
// Mock Battle Events
// ============================================================================

function createMockEvents(): BattleEvent[] {
  return [
    {
      timestamp: 0.0,
      event_type: 'battle_start',
      data: { message: 'Battle begins!' }
    },
    {
      timestamp: 0.5,
      event_type: 'move',
      data: { unit_id: 'unit_1', position: [100, 100] }
    },
    {
      timestamp: 1.0,
      event_type: 'attack',
      data: { attacker_id: 'unit_1', target_id: 'unit_2', weapon: 'laser' }
    },
    {
      timestamp: 1.2,
      event_type: 'damage',
      data: { target_id: 'unit_2', damage: 15, hit: true }
    },
    {
      timestamp: 2.0,
      event_type: 'move',
      data: { unit_id: 'unit_2', position: [200, 150] }
    },
    {
      timestamp: 3.0,
      event_type: 'attack',
      data: { attacker_id: 'unit_2', target_id: 'unit_1', weapon: 'missile' }
    },
    {
      timestamp: 3.5,
      event_type: 'damage',
      data: { target_id: 'unit_1', damage: 25, hit: true }
    },
    {
      timestamp: 4.0,
      event_type: 'move',
      data: { unit_id: 'unit_1', position: [150, 200] }
    },
    {
      timestamp: 5.0,
      event_type: 'destroy',
      data: { unit_id: 'unit_2', destroyed_by: 'unit_1' }
    },
    {
      timestamp: 5.5,
      event_type: 'battle_end',
      data: { winner: 'unit_1', reason: 'opponent_destroyed' }
    }
  ];
}

// ============================================================================
// Test Functions
// ============================================================================

export function testReplayController(): void {
  console.log('\n=== ReplayController Test ===\n');

  const events = createMockEvents();
  const controller = new ReplayController(events);

  console.log(`Loaded ${events.length} events`);
  console.log(`Total duration: ${controller.getTotalDuration()}s`);
  console.log(`Initial state: ${controller.getState()}`);

  // Test 1: Event callbacks
  console.log('\n--- Test 1: Event Callbacks ---');
  let eventCount = 0;
  const unsubscribe = controller.onEvent((event) => {
    eventCount++;
    console.log(`Event ${eventCount}: [${event.timestamp.toFixed(2)}s] ${event.event_type}`);
  });

  // Test 2: Playback control
  console.log('\n--- Test 2: Playback Control ---');
  controller.play();
  console.log(`State after play(): ${controller.getState()}`);

  // Simulate a few frames
  console.log('\nSimulating frames at 60 FPS...');
  for (let i = 0; i < 10; i++) {
    controller.update(1/60); // 16.67ms per frame
  }
  console.log(`Current time: ${controller.getCurrentTime().toFixed(4)}s`);
  console.log(`Progress: ${(controller.getProgress() * 100).toFixed(1)}%`);

  // Test 3: Pause and resume
  console.log('\n--- Test 3: Pause/Resume ---');
  controller.pause();
  console.log(`State after pause(): ${controller.getState()}`);
  const pausedTime = controller.getCurrentTime();

  controller.update(1/60); // This should not advance time
  console.log(`Time after update while paused: ${controller.getCurrentTime().toFixed(4)}s (should be ${pausedTime.toFixed(4)}s)`);

  controller.play();
  console.log(`State after resume: ${controller.getState()}`);

  // Test 4: Speed control
  console.log('\n--- Test 4: Speed Control ---');
  controller.setSpeed(2.0);
  console.log(`Speed set to: ${controller.getSpeed()}x`);

  const timeBefore = controller.getCurrentTime();
  controller.update(1/60);
  const timeAfter = controller.getCurrentTime();
  console.log(`Time advanced: ${((timeAfter - timeBefore) * 1000).toFixed(2)}ms (expected ~33ms at 2x speed)`);

  // Test 5: Seeking
  console.log('\n--- Test 5: Seeking ---');
  controller.seekTo(3.0);
  console.log(`Seeked to: ${controller.getCurrentTime().toFixed(2)}s`);
  console.log(`Events processed: ${controller.getProcessedEvents().length}`);

  // Test 6: Step forward/backward
  console.log('\n--- Test 6: Step Forward/Backward ---');
  controller.stop();
  controller.step('forward');
  console.log(`After step forward: ${controller.getCurrentTime().toFixed(2)}s`);
  controller.step('forward');
  console.log(`After another step: ${controller.getCurrentTime().toFixed(2)}s`);

  // Test 7: Debug info
  console.log('\n--- Test 7: Debug Info ---');
  console.log(controller.getDebugInfo());

  // Cleanup
  unsubscribe();
  controller.cleanup();
  console.log('\nController cleaned up');

  console.log('\n=== All Tests Passed! ===\n');
}

export function testInterpolation(): void {
  console.log('\n=== Interpolation Test ===\n');

  // Test 1: Basic lerp
  console.log('--- Test 1: Linear Interpolation ---');
  console.log(`lerp(0, 100, 0.0) = ${lerp(0, 100, 0.0)} (expected 0)`);
  console.log(`lerp(0, 100, 0.5) = ${lerp(0, 100, 0.5)} (expected 50)`);
  console.log(`lerp(0, 100, 1.0) = ${lerp(0, 100, 1.0)} (expected 100)`);

  // Test 2: Easing
  console.log('\n--- Test 2: Easing Functions ---');
  console.log(`easeInOut(0.0) = ${easeInOut(0.0).toFixed(3)} (expected 0.000)`);
  console.log(`easeInOut(0.5) = ${easeInOut(0.5).toFixed(3)} (expected 0.500)`);
  console.log(`easeInOut(1.0) = ${easeInOut(1.0).toFixed(3)} (expected 1.000)`);

  // Test 3: Position interpolation
  console.log('\n--- Test 3: Position Interpolation ---');
  const keyframes: PositionKeyframe[] = [
    { time: 0.0, x: 0, y: 0 },
    { time: 1.0, x: 100, y: 0 },
    { time: 2.0, x: 100, y: 100 },
    { time: 3.0, x: 0, y: 100 },
  ];

  const testTimes = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0];
  testTimes.forEach(time => {
    const pos = interpolatePosition(keyframes, time);
    console.log(`Position at t=${time.toFixed(1)}s: (${pos.x.toFixed(1)}, ${pos.y.toFixed(1)})`);
  });

  // Test 4: Edge cases
  console.log('\n--- Test 4: Edge Cases ---');
  const posBeforeStart = interpolatePosition(keyframes, -1.0);
  console.log(`Position at t=-1.0s: (${posBeforeStart.x}, ${posBeforeStart.y}) (should clamp to first keyframe)`);

  const posAfterEnd = interpolatePosition(keyframes, 5.0);
  console.log(`Position at t=5.0s: (${posAfterEnd.x}, ${posAfterEnd.y}) (should clamp to last keyframe)`);

  console.log('\n=== All Interpolation Tests Passed! ===\n');
}

// ============================================================================
// Run Tests
// ============================================================================

export function runAllTests(): void {
  testInterpolation();
  testReplayController();
}

// Allow running from console
if (typeof window !== 'undefined') {
  (window as any).testReplayController = testReplayController;
  (window as any).testInterpolation = testInterpolation;
  (window as any).runAllTests = runAllTests;
  console.log('Test functions available: testReplayController(), testInterpolation(), runAllTests()');
}
