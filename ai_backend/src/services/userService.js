// ============================================
// FILE: src/services/userService.js
// ============================================
const User = require('../models/User');

class UserService {
  async getAllUsers(page = 1, limit = 10, filters = {}) {
    const skip = (page - 1) * limit;
    
    const users = await User.find(filters)
      .select('-password')
      .limit(limit)
      .skip(skip)
      .sort({ createdAt: -1 });

    const total = await User.countDocuments(filters);

    return {
      users,
      pagination: {
        page,
        limit,
        total,
        pages: Math.ceil(total / limit)
      }
    };
  }

  async getUserById(userId) {
    const user = await User.findById(userId).select('-password');
    
    if (!user) {
      throw new Error('User not found');
    }

    return user;
  }

  async updateUser(userId, updateData) {
    const user = await User.findByIdAndUpdate(
      userId,
      updateData,
      { new: true, runValidators: true }
    );

    if (!user) {
      throw new Error('User not found');
    }

    return user;
  }

  async deleteUser(userId) {
    const user = await User.findByIdAndDelete(userId);
    
    if (!user) {
      throw new Error('User not found');
    }

    return true;
  }

  async deactivateUser(userId) {
    return await this.updateUser(userId, { isActive: false });
  }

  async activateUser(userId) {
    return await this.updateUser(userId, { isActive: true });
  }
}

module.exports = new UserService();