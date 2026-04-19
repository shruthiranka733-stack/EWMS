'use client';

import { useEffect, useState, ReactNode } from 'react';
import { AlertCircle, X } from 'lucide-react';
import './error-boundary.css';

export default function ErrorBoundary({ children }: { children: ReactNode }) {
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const handleError = (event: ErrorEvent) => setError(event.error);
    window.addEventListener('error', handleError);
    return () => window.removeEventListener('error', handleError);
  }, []);

  if (error) {
    return (
      <div className="error-boundary">
        <div className="error-card">
          <div className="error-header">
            <AlertCircle size={24} color="var(--danger)" />
            <h2>Something went wrong</h2>
            <button className="error-close" onClick={() => setError(null)}>
              <X size={20} />
            </button>
          </div>
          <p className="error-message">{error.message}</p>
          <button
            className="error-retry"
            onClick={() => { setError(null); window.location.reload(); }}
          >
            Try again
          </button>
        </div>
      </div>
    );
  }

  return <>{children}</>;
}
