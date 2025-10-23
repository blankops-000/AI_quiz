const User = require('../models/User');
const jwtConfig = require('../config/jwt');

const createTestUser = async () => {
  try {
    // Create a test user
    const testUser = await User.create({
      name: 'Test User',
      email: 'test@example.com',
      password: 'password123'
    });

    // Generate token
    const token = jwtConfig.generateToken({ id: testUser._id });
    
    console.log('Test User Created:');
    console.log('ID:', testUser._id);
    console.log('Token:', token);
    
    return { user: testUser, token };
  } catch (error) {
    console.error('Error creating test user:', error.message);
  }
};

module.exports = { createTestUser };