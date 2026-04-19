'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useAppStore } from '@/store/appStore';
import { Bell, User, Menu, X } from 'lucide-react';
import '../styles/navbar.css';

export default function NavigationBar() {
  const user = useAppStore((state) => state.user);
  const [menuOpen, setMenuOpen] = useState(false);

  const navItems = [
    { label: 'Dashboard', href: '/dashboard' },
    { label: 'Shipment', href: '/shipments' },
    { label: 'D&D Risk', href: '/dd-risk' },
    { label: 'Analytics', href: '/analytics' },
    { label: 'Adv. Analytics', href: '/analytics/advanced' },
    { label: 'HITL Review', href: '/hitl-review' },
  ];

  return (
    <nav className="navbar">
      <div className="navbar-container">
        {/* Left: Logo */}
        <Link href="/" className="navbar-logo">
          <div className="logo-icon"></div>
          <span>Dashboard</span>
        </Link>

        {/* Center: Nav Items (Desktop) */}
        <div className="navbar-menu">
          {navItems.map((item) => (
            <Link key={item.href} href={item.href} className="nav-item">
              {item.label}
            </Link>
          ))}
        </div>

        {/* Right: Icons + User */}
        <div className="navbar-right">
          <input
            type="text"
            placeholder="Search"
            className="navbar-search"
          />
          <button className="navbar-icon-btn">
            <Bell size={20} />
            <span className="notification-dot"></span>
          </button>
          <button className="user-avatar">
            <User size={16} />
          </button>
          <button
            className="mobile-menu-btn"
            onClick={() => setMenuOpen(!menuOpen)}
          >
            {menuOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {menuOpen && (
        <div className="navbar-mobile-menu">
          {navItems.map((item) => (
            <Link key={item.href} href={item.href} className="mobile-nav-item">
              {item.label}
            </Link>
          ))}
        </div>
      )}
    </nav>
  );
}
