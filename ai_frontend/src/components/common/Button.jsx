// ============================================
// FILE: src/components/common/Button.jsx
// ============================================
import React from 'react';
import './Button.css';

const Button = ({ 
  children, 
  onClick, 
  type = 'button', 
  variant = 'primary',
  disabled = false,
  loading = false,
  fullWidth = false,
  ...props 
}) => {
  const classNames = `btn btn-${variant} ${fullWidth ? 'btn-full' : ''} ${loading ? 'btn-loading' : ''}`;
  
  return (
    <button
      type={type}
      className={classNames}
      onClick={onClick}
      disabled={disabled || loading}
      {...props}
    >
      {loading ? <span className="spinner-small"></span> : children}
    </button>
  );
};

export default Button;
