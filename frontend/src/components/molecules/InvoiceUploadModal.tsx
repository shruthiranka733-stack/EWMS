'use client';

import { useState } from 'react';
import { useAppStore } from '@/store/appStore';
import { invoiceAPI } from '@/services/api';
import { Upload, AlertCircle, X } from 'lucide-react';
import './upload-modal.css';

interface InvoiceUploadModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSuccess?: () => void;
}

export default function InvoiceUploadModal({
  open,
  onOpenChange,
  onSuccess,
}: InvoiceUploadModalProps) {
  const user = useAppStore((state) => state.user);
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [dragActive, setDragActive] = useState(false);

  const handleUpload = async () => {
    if (!file || !user) return;

    setUploading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('org_id', user.org_id);

      await invoiceAPI.upload(formData);

      onOpenChange(false);
      setFile(null);
      onSuccess?.();
    } catch (err: unknown) {
      const message =
        err instanceof Error
          ? err.message
          : (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail ?? 'Upload failed';
      setError(message);
    } finally {
      setUploading(false);
    }
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(e.type === 'dragenter' || e.type === 'dragover');
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files?.[0]) {
      setFile(e.dataTransfer.files[0]);
      setError(null);
    }
  };

  if (!open) return null;

  return (
    <div className="modal-overlay" onClick={() => onOpenChange(false)}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Upload Sales Invoice</h2>
          <button className="modal-close" onClick={() => onOpenChange(false)}>
            <X size={20} />
          </button>
        </div>

        <p className="modal-description">
          Upload a PDF or image of your sales invoice. We'll extract data automatically.
        </p>

        {error && (
          <div className="error-alert">
            <AlertCircle size={16} />
            <span>{error}</span>
          </div>
        )}

        <div
          className={`file-drop-zone${dragActive ? ' active' : ''}${file ? ' has-file' : ''}`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          {!file ? (
            <>
              <Upload size={32} className="upload-icon" />
              <p className="drop-text">Drag and drop your file here, or click to select</p>
              <input
                type="file"
                accept=".pdf,.jpg,.jpeg,.png"
                onChange={(e) => {
                  if (e.target.files?.[0]) {
                    setFile(e.target.files[0]);
                    setError(null);
                  }
                }}
                className="file-input"
              />
            </>
          ) : (
            <>
              <p className="file-name">{file.name}</p>
              <p className="file-size">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
              <button className="change-file-btn" onClick={() => setFile(null)}>
                Change file
              </button>
            </>
          )}
        </div>

        <div className="modal-actions">
          <button
            className="btn-secondary"
            onClick={() => onOpenChange(false)}
            disabled={uploading}
          >
            Cancel
          </button>
          <button
            className="btn-primary"
            onClick={handleUpload}
            disabled={!file || uploading}
          >
            {uploading ? 'Uploading...' : 'Upload'}
          </button>
        </div>
      </div>
    </div>
  );
}
