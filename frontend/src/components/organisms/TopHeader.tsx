'use client';

import { useAppStore } from '@/store/appStore';
import { Bell, Menu } from 'lucide-react';

interface TopHeaderProps {
  onMenuClick: () => void;
}

export default function TopHeader({ onMenuClick }: TopHeaderProps) {
  const user = useAppStore((state) => state.user);

  return (
    <header className="header">
      <button className="header-menu-btn" onClick={onMenuClick} aria-label="Toggle menu">
        <Menu size={20} />
      </button>

      <div className="header-search">
        <input type="text" placeholder={`Search shipments, tasks… (${user?.name ?? ''})`} />
      </div>

      <div className="header-right">
        <button className="header-icon" aria-label="Notifications">
          <Bell size={16} />
          <span className="notification-dot" />
        </button>
      </div>
    </header>
  );
}
