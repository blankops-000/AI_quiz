const User = require('../models/User');
const jwtConfig = require('../config/jwt');
const { ApiResponse } = require('../utils/apiResponse');

exports.createTestUser = async (req, res) => {
  try {
    // Create test user
    const testUser = await User.create({
      name: 'Test User',
      email: 'test@example.com',
      password: 'password123'
    });

    // Generate token
    const token = jwtConfig.generateToken({ id: testUser._id, role: testUser.role });

    res.status(201).json(
      ApiResponse.success({ 
        user: { 
          id: testUser._id, 
          name: testUser.name, 
          email: testUser.email 
        }, 
        token 
      }, 'Test user created successfully')
    );
  } catch (error) {
    if (error.code === 11000) {
      // User already exists, just login
      const existingUser = await User.findOne({ email: 'test@example.com' });
      const token = jwtConfig.generateToken({ id: existingUser._id, role: existingUser.role });
      
      res.status(200).json(
        ApiResponse.success({ 
          user: { 
            id: existingUser._id, 
            name: existingUser.name, 
            email: existingUser.email 
          }, 
          token 
        }, 'Test user already exists, logged in')
      );
    } else {
      res.status(500).json(ApiResponse.error('Failed to create test user'));
    }
  }
};