const request = require('supertest');
const app = require('../src/app');

describe('AI Endpoints', () => {
  
  test('GET /api/ai/health should return health status', async () => {
    const response = await request(app)
      .get('/api/ai/health')
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.backend_status).toBe('healthy');
  });

  test('POST /api/ai/process should handle text analysis', async () => {
    const response = await request(app)
      .post('/api/ai/process')
      .send({
        requestType: 'text-analysis',
        input: { text: 'This is a test text' }
      })
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.result).toBeDefined();
  });

  test('POST /api/ai/process should handle quiz generation', async () => {
    const response = await request(app)
      .post('/api/ai/process')
      .send({
        requestType: 'quiz-generation',
        input: { 
          topic: 'Science',
          options: { numQuestions: 5, difficulty: 'medium' }
        }
      })
      .expect(200);
    
    expect(response.body.success).toBe(true);
    expect(response.body.data.result.questions).toBeDefined();
  });

  test('POST /api/ai/process should validate request type', async () => {
    const response = await request(app)
      .post('/api/ai/process')
      .send({
        requestType: 'invalid-type',
        input: { text: 'test' }
      })
      .expect(400);
    
    expect(response.body.success).toBe(false);
  });

});