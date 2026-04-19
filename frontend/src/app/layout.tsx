'use client';

import { ReactNode, useState } from 'react';
import '@/styles/design-tokens.css';
import '@/styles/compact-design.css';
import './globals.css';
import Providers from './providers';
import Sidebar from '@/components/organisms/Sidebar';
import TopHeader from '@/components/organisms/TopHeader';

export default function RootLayout({ children }: { children: ReactNode }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <html lang="en">
      <body>
        <Providers>
          <div className="main-layout">
            <Sidebar open={sidebarOpen} onToggle={() => setSidebarOpen(!sidebarOpen)} />
            <TopHeader onMenuClick={() => setSidebarOpen(!sidebarOpen)} />
            <div className="content">{children}</div>
          </div>
        </Providers>
      </body>
    </html>
  );
}
