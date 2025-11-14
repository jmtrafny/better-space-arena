import React, { useEffect, useRef, useState } from 'react';
import type { BattleEvent } from '../../utils/types';

export interface EventLogProps {
  events: BattleEvent[];
  maxHeight?: string;
  autoScroll?: boolean;
}

type EventFilter = 'all' | 'damage' | 'movement' | 'abilities' | 'other';

export default function EventLog({
  events,
  maxHeight = '400px',
  autoScroll = true
}: EventLogProps) {
  const [filter, setFilter] = useState<EventFilter>('all');
  const logEndRef = useRef<HTMLDivElement>(null);
  const logContainerRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new events arrive (within container only)
  useEffect(() => {
    if (autoScroll && logContainerRef.current) {
      logContainerRef.current.scrollTop = logContainerRef.current.scrollHeight;
    }
  }, [events, autoScroll]);

  const filterEvent = (event: BattleEvent): boolean => {
    if (filter === 'all') return true;

    const eventType = (event.type || event.event_type || '').toLowerCase();

    switch (filter) {
      case 'damage':
        return eventType.includes('damage') || eventType.includes('hit') || eventType.includes('destroy');
      case 'movement':
        return eventType.includes('move') || eventType.includes('position');
      case 'abilities':
        return eventType.includes('ability') || eventType.includes('skill') || eventType.includes('special');
      case 'other':
        return !eventType.includes('damage') &&
               !eventType.includes('hit') &&
               !eventType.includes('move') &&
               !eventType.includes('ability');
      default:
        return true;
    }
  };

  const getEventColor = (eventType: string): string => {
    const type = (eventType || '').toLowerCase();

    if (type.includes('damage') || type.includes('destroy')) return '#ef4444';
    if (type.includes('heal') || type.includes('repair')) return '#22c55e';
    if (type.includes('move') || type.includes('position')) return '#3b82f6';
    if (type.includes('ability') || type.includes('special')) return '#a855f7';
    if (type.includes('spawn') || type.includes('init')) return '#10b981';

    return '#6b7280';
  };

  const filteredEvents = events.filter(filterEvent);

  const containerStyles: React.CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    backgroundColor: '#1f2937',
    borderRadius: '0.5rem',
    boxShadow: '0 1px 3px rgba(0, 0, 0, 0.3)',
    border: '1px solid #374151',
    overflow: 'hidden',
  };

  const headerStyles: React.CSSProperties = {
    padding: '1rem',
    backgroundColor: '#111827',
    borderBottom: '1px solid #374151',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  };

  const titleStyles: React.CSSProperties = {
    margin: 0,
    fontSize: '1.125rem',
    fontWeight: 600,
    color: '#e5e5e5',
  };

  const filterContainerStyles: React.CSSProperties = {
    display: 'flex',
    gap: '0.5rem',
  };

  const getFilterButtonStyles = (isActive: boolean): React.CSSProperties => ({
    padding: '0.25rem 0.75rem',
    fontSize: '0.875rem',
    border: '1px solid #4b5563',
    borderRadius: '0.375rem',
    backgroundColor: isActive ? '#3b82f6' : '#374151',
    color: isActive ? '#ffffff' : '#9ca3af',
    cursor: 'pointer',
    transition: 'all 0.2s',
  });

  const logContainerStyles: React.CSSProperties = {
    maxHeight,
    overflowY: 'auto',
    padding: '1rem',
    display: 'flex',
    flexDirection: 'column',
    gap: '0.5rem',
  };

  const eventItemStyles = (eventType: string): React.CSSProperties => ({
    padding: '0.75rem',
    backgroundColor: '#111827',
    borderLeft: `4px solid ${getEventColor(eventType)}`,
    borderRadius: '0.25rem',
    fontSize: '0.875rem',
  });

  const eventHeaderStyles: React.CSSProperties = {
    display: 'flex',
    justifyContent: 'space-between',
    marginBottom: '0.25rem',
  };

  const eventTypeStyles = (eventType: string): React.CSSProperties => ({
    fontWeight: 600,
    color: getEventColor(eventType),
  });

  const timestampStyles: React.CSSProperties = {
    color: '#6b7280',
    fontSize: '0.75rem',
  };

  const eventDataStyles: React.CSSProperties = {
    color: '#9ca3af',
    fontFamily: 'monospace',
    fontSize: '0.8rem',
  };

  const emptyStateStyles: React.CSSProperties = {
    textAlign: 'center',
    padding: '2rem',
    color: '#9ca3af',
  };

  return (
    <div style={containerStyles}>
      <div style={headerStyles}>
        <h3 style={titleStyles}>
          Event Log ({filteredEvents.length})
        </h3>
        <div style={filterContainerStyles}>
          <button
            style={getFilterButtonStyles(filter === 'all')}
            onClick={() => setFilter('all')}
          >
            All
          </button>
          <button
            style={getFilterButtonStyles(filter === 'damage')}
            onClick={() => setFilter('damage')}
          >
            Damage
          </button>
          <button
            style={getFilterButtonStyles(filter === 'movement')}
            onClick={() => setFilter('movement')}
          >
            Movement
          </button>
          <button
            style={getFilterButtonStyles(filter === 'abilities')}
            onClick={() => setFilter('abilities')}
          >
            Abilities
          </button>
          <button
            style={getFilterButtonStyles(filter === 'other')}
            onClick={() => setFilter('other')}
          >
            Other
          </button>
        </div>
      </div>

      <div ref={logContainerRef} style={logContainerStyles}>
        {filteredEvents.length === 0 ? (
          <div style={emptyStateStyles}>
            {events.length === 0 ? 'No events yet' : 'No events match the current filter'}
          </div>
        ) : (
          filteredEvents.map((event, index) => {
            const eventType = (event as any).event_type || event.type || 'unknown';
            const eventData = event.data || {};
            return (
              <div key={index} style={eventItemStyles(eventType)}>
                <div style={eventHeaderStyles}>
                  <span style={eventTypeStyles(eventType)}>
                    {eventType}
                    {event.unit_id && ` - ${event.unit_id}`}
                  </span>
                  <span style={timestampStyles}>
                    {event.timestamp.toFixed(2)}s
                  </span>
                </div>
                {Object.keys(eventData).length > 0 && (
                  <div style={eventDataStyles}>
                    {JSON.stringify(eventData)}
                  </div>
                )}
              </div>
            );
          })
        )}
        <div ref={logEndRef} />
      </div>
    </div>
  );
}
