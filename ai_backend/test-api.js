const axios = require('axios');

const BASE_URL = 'http://localhost:5000/api';

async function testAIEndpoints() {
  console.log('Testing AI Endpoints...\n');

  try {
    // Test health check
    console.log('1. Testing health check...');
    const healthResponse = await axios.get(`${BASE_URL}/ai/health`);
    console.log('✓ Health check passed:', healthResponse.data);

    // Test text analysis
    console.log('\n2. Testing text analysis...');
    const textAnalysisResponse = await axios.post(`${BASE_URL}/ai/process`, {
      requestType: 'text-analysis',
      input: { text: 'This is a positive test message!' }
    });
    console.log('✓ Text analysis passed:', textAnalysisResponse.data);

    // Test quiz generation
    console.log('\n3. Testing quiz generation...');
    const quizResponse = await axios.post(`${BASE_URL}/ai/process`, {
      requestType: 'quiz-generation',
      input: { 
        topic: 'Science',
        options: { numQuestions: 3, difficulty: 'medium' }
      }
    });
    console.log('✓ Quiz generation passed:', quizResponse.data);

    // Test sentiment analysis
    console.log('\n4. Testing sentiment analysis...');
    const sentimentResponse = await axios.post(`${BASE_URL}/ai/process`, {
      requestType: 'sentiment-analysis',
      input: { text: 'I love this application!' }
    });
    console.log('✓ Sentiment analysis passed:', sentimentResponse.data);

    console.log('\n🎉 All AI endpoints are working correctly!');

  } catch (error) {
    console.error('❌ Test failed:', error.response?.data || error.message);
  }
}

testAIEndpoints();