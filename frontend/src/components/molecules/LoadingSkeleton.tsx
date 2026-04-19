'use client';

import './loading-skeleton.css';

export default function LoadingSkeleton() {
  return (
    <div className="skeleton-container">
      <div className="skeleton-header" />
      <div className="skeleton-cards">
        <div className="skeleton-card" />
        <div className="skeleton-card" />
        <div className="skeleton-card" />
        <div className="skeleton-card" />
      </div>
      <div className="skeleton-list">
        <div className="skeleton-item" />
        <div className="skeleton-item" />
        <div className="skeleton-item" />
      </div>
    </div>
  );
}
