const jwtConfig = require('../config/jwt');
const User = require('../models/User');

const optionalAuthMiddleware = async (req, res, next) => {
  try {
    let token;

    // Check for token in Authorization header
    if (req.headers.authorization && req.headers.authorization.startsWith('Bearer')) {
      token = req.headers.authorization.split(' ')[1];
    }

    if (token) {
      try {
        // Verify token
        const decoded = jwtConfig.verifyToken(token);
        
        // Get user from token
        req.user = await User.findById(decoded.id).select('-password');
      } catch (error) {
        // Token invalid, but continue without user
        req.user = null;
      }
    } else {
      // No token provided, continue without user
      req.user = null;
    }

    next();
  } catch (error) {
    // Continue even if there's an error
    req.user = null;
    next();
  }
};

module.exports = optionalAuthMiddleware;