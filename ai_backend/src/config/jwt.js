
// ============================================
// FILE: src/config/jwt.js
// ============================================
const jwt = require('jsonwebtoken');

const jwtConfig = {
  secret: process.env.JWT_SECRET || 'your_jwt_secret_key_change_in_production',
  expiresIn: process.env.JWT_EXPIRE || '7d',
  
  generateToken: (payload) => {
    return jwt.sign(payload, jwtConfig.secret, {
      expiresIn: jwtConfig.expiresIn
    });
  },
  
  verifyToken: (token) => {
    try {
      return jwt.verify(token, jwtConfig.secret);
    } catch (error) {
      throw new Error('Invalid token');
    }
  }
};

module.exports = jwtConfig;