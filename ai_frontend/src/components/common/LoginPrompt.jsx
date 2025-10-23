import React from 'react';
import { Link } from 'react-router-dom';

const LoginPrompt = ({ message = "Please login to use AI features" }) => {
  return (
    <div className="login-prompt">
      <p>{message}</p>
      <Link to="/login" className="btn btn-primary">
        Login
      </Link>
      <Link to="/register" className="btn btn-secondary">
        Register
      </Link>
    </div>
  );
};

export default LoginPrompt;