import React from 'react';
import { Link, useLocation } from 'react-router-dom';

export interface LayoutProps {
  children: React.ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  const location = useLocation();

  const headerStyles: React.CSSProperties = {
    backgroundColor: '#1f2937',
    color: '#ffffff',
    padding: '1rem 2rem',
    boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
  };

  const navStyles: React.CSSProperties = {
    display: 'flex',
    gap: '2rem',
    alignItems: 'center',
  };

  const titleStyles: React.CSSProperties = {
    margin: 0,
    fontSize: '1.5rem',
    fontWeight: 700,
  };

  const linksContainerStyles: React.CSSProperties = {
    display: 'flex',
    gap: '1.5rem',
    marginLeft: 'auto',
  };

  const getLinkStyles = (isActive: boolean): React.CSSProperties => ({
    color: isActive ? '#60a5fa' : '#d1d5db',
    textDecoration: 'none',
    fontWeight: 500,
    transition: 'color 0.2s',
  });

  const contentStyles: React.CSSProperties = {
    minHeight: 'calc(100vh - 64px)',
    backgroundColor: '#f9fafb',
  };

  return (
    <div>
      <header style={headerStyles}>
        <nav style={navStyles}>
          <h1 style={titleStyles}>Battle Automata</h1>
          <div style={linksContainerStyles}>
            <Link to="/" style={getLinkStyles(location.pathname === '/')}>
              Home
            </Link>
            <Link to="/builder" style={getLinkStyles(location.pathname === '/builder')}>
              Builder
            </Link>
            <Link to="/battle" style={getLinkStyles(location.pathname === '/battle')}>
              Battle
            </Link>
          </div>
        </nav>
      </header>
      <main style={contentStyles}>
        {children}
      </main>
    </div>
  );
}
