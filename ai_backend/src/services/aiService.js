
// ============================================
// FILE: src/services/aiService.js
// ============================================
const axios = require('axios');
const logger = require('../utils/logger');

const AI_SERVICE_URL = process.env.AI_SERVICE_URL || 'http://localhost:8000/api';
const AI_API_KEY = process.env.AI_API_KEY;

class AIService {
  async processRequest(requestType, input) {
    try {
      const response = await axios.post(`${AI_SERVICE_URL}/process`, {
        type: requestType,
        data: input
      }, {
        headers: {
          'Authorization': `Bearer ${AI_API_KEY}`,
          'Content-Type': 'application/json'
        },
        timeout: 60000 // 60 seconds
      });

      return response.data;
    } catch (error) {
      logger.error(`AI Service Error: ${error.message}`);
      
      if (error.response) {
        throw new Error(`AI Service responded with error: ${error.response.data.message || error.response.statusText}`);
      } else if (error.request) {
        throw new Error('AI Service is not responding');
      } else {
        throw new Error(`AI Service request failed: ${error.message}`);
      }
    }
  }

  async textGeneration(prompt, options = {}) {
    return await this.processRequest('text-generation', { prompt, ...options });
  }

  async imageAnalysis(imageUrl, analysisType = 'general') {
    return await this.processRequest('image-analysis', { imageUrl, analysisType });
  }

  async prediction(data, modelType) {
    return await this.processRequest('prediction', { data, modelType });
  }

  async recommendation(userId, context) {
    return await this.processRequest('recommendation', { userId, context });
  }
}

module.exports = new AIService();
