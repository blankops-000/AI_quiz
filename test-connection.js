// Simple test script to verify frontend-backend connection
const axios = require('axios');

const API_URL = 'http://localhost:5000/api';

async function testConnection() {
  console.log('Testing backend connection...');
  
  try {
    // Test health endpoint
    const healthResponse = await axios.get('http://localhost:5000/health');
    console.log('✅ Health check:', healthResponse.data);
    
    // Test posts endpoint (should work without auth)
    const postsResponse = await axios.get(`${API_URL}/data/posts`);
    console.log('✅ Posts endpoint:', postsResponse.data);
    
    console.log('\n🎉 Backend is running and accessible!');
  } catch (error) {
    console.error('❌ Connection failed:', error.message);
    if (error.response) {
      console.error('Response status:', error.response.status);
      console.error('Response data:', error.response.data);
    }
  }
}

testConnection();