// ============================================
// FILE: src/utils/validators.js
// ============================================
export const validators = {
  email: (email) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
  },

  password: (password) => {
    // At least 6 characters, 1 uppercase, 1 lowercase, 1 number
    const re = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{6,}$/;
    return re.test(password);
  },

  username: (username) => {
    // 3-30 characters, alphanumeric and underscore only
    const re = /^[a-zA-Z0-9_]{3,30}$/;
    return re.test(username);
  },

  required: (value) => {
    return value && value.toString().trim().length > 0;
  },

  minLength: (value, min) => {
    return value && value.length >= min;
  },

  maxLength: (value, max) => {
    return value && value.length <= max;
  }
};

export default validators;
