import type { Metadata } from 'next';
import Providers from './providers';
import ErrorBoundary from '@/components/molecules/ErrorBoundary';
import '@/styles/design-tokens.css';
import '@/styles/responsive.css';

export const metadata: Metadata = {
  title: 'EWMS — Export Workflow Management',
  description: 'End-to-end workflow for India-to-US steel exports',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <ErrorBoundary>
          <Providers>{children}</Providers>
        </ErrorBoundary>
      </body>
    </html>
  );
}
