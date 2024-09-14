import React from 'react';
import './Header.css';

function Header() {
  return (
    <header className="app-header">
      <div className="header-container">
        <div className="logo-container">
          <img src="/ee.png" alt="Project Logo" className="logo" />
          <h1 className="app-title">InQGen</h1>
        </div>
        <nav className="nav-links">
          <a href="#get-started" className="nav-link">Get Started</a>
          <a href="#about-us" className="nav-link">About Us</a>
        </nav>
      </div>
    </header>
  );
}

export default Header;
