// ============================================
// FILE: src/services/aiService.js
// ============================================
const axios = require('axios');
const logger = require('../utils/logger');

class AIService {
  constructor() {
    this.baseURL = process.env.AI_SERVICE_URL || 'http://localhost:8000/api';
    this.apiKey = process.env.AI_API_KEY;
    this.timeout = 30000; // 30 seconds
  }

  async processRequest(requestType, input) {
    try {
      logger.info(`Processing AI request: ${requestType}`);
      
      switch (requestType) {
        case 'text_analysis':
          return await this.analyzeText(input.text);
        case 'sentiment_analysis':
          return await this.analyzeSentiment(input.text);
        case 'text_generation':
          return await this.generateText(input.prompt, input.options);
        case 'quiz_generation':
          return await this.generateQuiz(input.topic, input.options);
        case 'recommendations':
          return await this.getRecommendations(input.userId, input.preferences);
        default:
          throw new Error(`Unsupported request type: ${requestType}`);
      }
    } catch (error) {
      logger.error(`AI service error: ${error.message}`);
      throw error;
    }
  }

  async analyzeText(text) {
    try {
      const response = await this.makeRequest('/analyze/text', {
        text
      });
      
      return response.data;
    } catch (error) {
      throw new Error(`Text analysis failed: ${error.message}`);
    }
  }

  async analyzeSentiment(text) {
    try {
      const response = await this.makeRequest('/analyze/sentiment', {
        text
      });
      
      return response.data;
    } catch (error) {
      throw new Error(`Sentiment analysis failed: ${error.message}`);
    }
  }

  async generateText(prompt, options = {}) {
    try {
      const response = await this.makeRequest('/generate/text', {
        prompt,
        max_length: options.maxLength || 100,
        temperature: options.temperature || 0.7
      });
      
      return response.data;
    } catch (error) {
      throw new Error(`Text generation failed: ${error.message}`);
    }
  }

  async generateQuiz(topic, options = {}) {
    try {
      const response = await this.makeRequest('/generate/quiz', {
        topic,
        num_questions: options.numQuestions || 5,
        difficulty: options.difficulty || 'medium'
      });
      
      return response.data;
    } catch (error) {
      throw new Error(`Quiz generation failed: ${error.message}`);
    }
  }

  async getRecommendations(userId, preferences = {}) {
    try {
      const response = await this.makeRequest('/recommendations', {
        user_id: userId,
        preferences,
        limit: preferences.limit || 10
      });
      
      return response.data;
    } catch (error) {
      throw new Error(`Recommendations failed: ${error.message}`);
    }
  }

  async makeRequest(endpoint, data) {
    try {
      const config = {
        method: 'POST',
        url: `${this.baseURL}${endpoint}`,
        data,
        timeout: this.timeout,
        headers: {
          'Content-Type': 'application/json'
        }
      };

      if (this.apiKey) {
        config.headers['Authorization'] = `Bearer ${this.apiKey}`;
      }

      const response = await axios(config);
      
      if (!response.data.success) {
        throw new Error(response.data.message || 'AI service request failed');
      }
      
      return response.data;
    } catch (error) {
      if (error.response) {
        throw new Error(error.response.data.message || 'AI service error');
      } else if (error.request) {
        throw new Error('AI service unavailable');
      } else {
        throw error;
      }
    }
  }

  async healthCheck() {
    try {
      const response = await axios.get(`${this.baseURL.replace('/api', '')}/health`, {
        timeout: 5000
      });
      
      return response.data;
    } catch (error) {
      throw new Error('AI service health check failed');
    }
  }
}

module.exports = new AIService();