import React from 'react';

const LoadingSpinner = ({ message = "Processing..." }) => (
  <div className="loading-spinner">
    <div className="spinner"></div>
    <p>{message}</p>
    <style jsx>{`
      .loading-spinner {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 2rem;
      }
      .spinner {
        width: 40px;
        height: 40px;
        border: 4px solid #f3f3f3;
        border-top: 4px solid #007bff;
        border-radius: 50%;
        animation: spin 1s linear infinite;
      }
      @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
      }
    `}</style>
  </div>
);

export default LoadingSpinner;