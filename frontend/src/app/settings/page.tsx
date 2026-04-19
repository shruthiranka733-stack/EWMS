'use client';

export default function SettingsPage() {
  return (
    <>
      <h1 className="page-title">Settings</h1>
      <p className="page-subtitle">Manage your preferences and organization</p>

      <div className="card" style={{ maxWidth: 600 }}>
        <p className="card-title" style={{ fontSize: 'var(--t-md)', marginBottom: 'var(--s-6)' }}>
          User Preferences
        </p>

        <div style={{ display: 'grid', gap: 'var(--s-5)' }}>
          <label style={{ display: 'flex', alignItems: 'center', gap: 'var(--s-3)', cursor: 'pointer' }}>
            <input type="checkbox" defaultChecked />
            <span>
              <strong style={{ display: 'block', fontSize: 'var(--t-sm)' }}>Email Notifications</strong>
              <span style={{ fontSize: 'var(--t-xs)', color: 'var(--fg-muted)' }}>
                Receive email alerts for critical shipments
              </span>
            </span>
          </label>

          <label style={{ display: 'flex', alignItems: 'center', gap: 'var(--s-3)', cursor: 'pointer' }}>
            <input type="checkbox" />
            <span>
              <strong style={{ display: 'block', fontSize: 'var(--t-sm)' }}>SMS Alerts</strong>
              <span style={{ fontSize: 'var(--t-xs)', color: 'var(--fg-muted)' }}>
                Receive SMS for D&amp;D risk alerts
              </span>
            </span>
          </label>
        </div>

        <button className="btn btn-primary" style={{ marginTop: 'var(--s-6)' }}>
          Save Preferences
        </button>
      </div>
    </>
  );
}
