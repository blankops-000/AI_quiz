import React, { useState, useEffect } from 'react';

const Toast = ({ message, type = 'info', duration = 3000, onClose }) => {
  const [visible, setVisible] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setVisible(false);
      setTimeout(onClose, 300);
    }, duration);

    return () => clearTimeout(timer);
  }, [duration, onClose]);

  if (!visible) return null;

  return (
    <div className={`toast toast-${type} ${visible ? 'toast-show' : 'toast-hide'}`}>
      <span>{message}</span>
      <button onClick={() => setVisible(false)} className="toast-close">×</button>
      <style jsx>{`
        .toast {
          position: fixed;
          top: 20px;
          right: 20px;
          padding: 1rem 1.5rem;
          border-radius: 4px;
          color: white;
          z-index: 1000;
          display: flex;
          align-items: center;
          gap: 1rem;
          transition: all 0.3s ease;
        }
        .toast-info { background: #007bff; }
        .toast-success { background: #28a745; }
        .toast-error { background: #dc3545; }
        .toast-warning { background: #ffc107; color: #212529; }
        .toast-show { opacity: 1; transform: translateX(0); }
        .toast-hide { opacity: 0; transform: translateX(100%); }
        .toast-close {
          background: none;
          border: none;
          color: inherit;
          font-size: 1.5rem;
          cursor: pointer;
          padding: 0;
          margin-left: auto;
        }
      `}</style>
    </div>
  );
};

export default Toast;