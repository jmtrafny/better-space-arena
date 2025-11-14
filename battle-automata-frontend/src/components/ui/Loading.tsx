import React from 'react';

export interface LoadingProps {
  text?: string;
  size?: 'small' | 'medium' | 'large';
}

export default function Loading({ text, size = 'medium' }: LoadingProps) {
  const sizeMap = {
    small: '1.5rem',
    medium: '3rem',
    large: '5rem',
  };

  const spinnerSize = sizeMap[size];

  const containerStyles: React.CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '1rem',
    padding: '2rem',
  };

  const spinnerStyles: React.CSSProperties = {
    width: spinnerSize,
    height: spinnerSize,
    border: '4px solid #e5e7eb',
    borderTopColor: '#3b82f6',
    borderRadius: '50%',
    animation: 'spin 0.8s linear infinite',
  };

  const textStyles: React.CSSProperties = {
    fontSize: '1rem',
    color: '#6b7280',
    fontWeight: 500,
  };

  return (
    <div style={containerStyles}>
      <div style={spinnerStyles} />
      {text && <p style={textStyles}>{text}</p>}
    </div>
  );
}
