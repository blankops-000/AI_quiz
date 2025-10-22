
// ============================================
// FILE: src/services/authService.js
// ============================================
const User = require('../models/User');
const jwtConfig = require('../config/jwt');

class AuthService {
  async createUser(userData) {
    const user = await User.create(userData);
    const token = jwtConfig.generateToken({ id: user._id, role: user.role });
    return { user, token };
  }

  async authenticateUser(email, password) {
    const user = await User.findOne({ email }).select('+password');
    
    if (!user || !(await user.comparePassword(password))) {
      throw new Error('Invalid credentials');
    }

    if (!user.isActive) {
      throw new Error('Account is deactivated');
    }

    user.lastLogin = new Date();
    await user.save();

    const token = jwtConfig.generateToken({ id: user._id, role: user.role });
    user.password = undefined;

    return { user, token };
  }

  async changePassword(userId, currentPassword, newPassword) {
    const user = await User.findById(userId).select('+password');
    
    if (!user) {
      throw new Error('User not found');
    }

    const isMatch = await user.comparePassword(currentPassword);
    if (!isMatch) {
      throw new Error('Current password is incorrect');
    }

    user.password = newPassword;
    await user.save();

    return true;
  }
}

module.exports = new AuthService();
