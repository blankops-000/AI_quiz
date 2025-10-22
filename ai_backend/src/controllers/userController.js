
// ============================================
// FILE: src/controllers/userController.js
// ============================================
const User = require('../models/User');
const { ApiResponse } = require('../utils/apiResponse');

exports.getAllUsers = async (req, res, next) => {
  try {
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 10;
    const skip = (page - 1) * limit;

    const users = await User.find()
      .select('-password')
      .limit(limit)
      .skip(skip)
      .sort({ createdAt: -1 });

    const total = await User.countDocuments();

    res.status(200).json(
      ApiResponse.success({
        users,
        pagination: {
          page,
          limit,
          total,
          pages: Math.ceil(total / limit)
        }
      }, 'Users retrieved successfully')
    );
  } catch (error) {
    next(error);
  }
};

exports.getUserById = async (req, res, next) => {
  try {
    const user = await User.findById(req.params.id).select('-password');
    
    if (!user) {
      return res.status(404).json(
        ApiResponse.error('User not found')
      );
    }

    res.status(200).json(
      ApiResponse.success({ user }, 'User retrieved successfully')
    );
  } catch (error) {
    next(error);
  }
};

exports.updateUser = async (req, res, next) => {
  try {
    const { username, email, avatar } = req.body;
    
    const user = await User.findByIdAndUpdate(
      req.user.id,
      { username, email, avatar },
      { new: true, runValidators: true }
    );

    if (!user) {
      return res.status(404).json(
        ApiResponse.error('User not found')
      );
    }

    res.status(200).json(
      ApiResponse.success({ user }, 'User updated successfully')
    );
  } catch (error) {
    next(error);
  }
};

exports.deleteUser = async (req, res, next) => {
  try {
    const user = await User.findByIdAndDelete(req.params.id);
    
    if (!user) {
      return res.status(404).json(
        ApiResponse.error('User not found')
      );
    }

    res.status(200).json(
      ApiResponse.success(null, 'User deleted successfully')
    );
  } catch (error) {
    next(error);
  }
};