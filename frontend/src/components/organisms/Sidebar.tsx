'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  LayoutDashboard,
  Package,
  AlertTriangle,
  BarChart3,
  CheckSquare,
  Settings,
  X,
} from 'lucide-react';

interface SidebarProps {
  open: boolean;
  onToggle: () => void;
}

const NAV_ITEMS = [
  { label: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { label: 'Shipments', href: '/shipments', icon: Package },
  { label: 'Tasks', href: '/tasks', icon: CheckSquare },
  { label: 'D&D Risk', href: '/dd-risk', icon: AlertTriangle },
  { label: 'Analytics', href: '/analytics', icon: BarChart3 },
  { label: 'Settings', href: '/settings', icon: Settings },
];

export default function Sidebar({ open, onToggle }: SidebarProps) {
  const pathname = usePathname();

  return (
    <aside className={`sidebar ${open ? 'open' : ''}`}>
      <div className="sidebar-header">
        <div className="sidebar-logo" />
        <h2 className="sidebar-title">EWMS</h2>
        <button className="modal-close" onClick={onToggle} style={{ marginLeft: 'auto' }}>
          <X size={16} />
        </button>
      </div>

      <nav className="sidebar-nav">
        {NAV_ITEMS.map(({ label, href, icon: Icon }) => (
          <Link
            key={href}
            href={href}
            className={`nav-item ${pathname === href ? 'active' : ''}`}
            onClick={onToggle}
          >
            <Icon size={15} />
            {label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
