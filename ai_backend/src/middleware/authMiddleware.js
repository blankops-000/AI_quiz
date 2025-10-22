
// ============================================
// FILE: src/middleware/auth.middleware.js
// ============================================
const jwtConfig = require('../config/jwt');
const User = require('../models/User');
const { ApiResponse } = require('../utils/apiResponse');

const authMiddleware = async (req, res, next) => {
  try {
    let token;

    // Check for token in Authorization header
    if (req.headers.authorization && req.headers.authorization.startsWith('Bearer')) {
      token = req.headers.authorization.split(' ')[1];
    }

    if (!token) {
      return res.status(401).json(
        ApiResponse.error('Not authorized, no token provided')
      );
    }

    try {
      // Verify token
      const decoded = jwtConfig.verifyToken(token);
      
      // Get user from token
      req.user = await User.findById(decoded.id).select('-password');
      
      if (!req.user) {
        return res.status(401).json(
          ApiResponse.error('User not found')
        );
      }

      if (!req.user.isActive) {
        return res.status(403).json(
          ApiResponse.error('Account is deactivated')
        );
      }

      next();
    } catch (error) {
      return res.status(401).json(
        ApiResponse.error('Not authorized, token invalid or expired')
      );
    }
  } catch (error) {
    next(error);
  }
};

const authorize = (...roles) => {
  return (req, res, next) => {
    if (!roles.includes(req.user.role)) {
      return res.status(403).json(
        ApiResponse.error(`User role '${req.user.role}' is not authorized to access this route`)
      );
    }
    next();
  };
};

module.exports = authMiddleware;
module.exports.authorize = authorize;