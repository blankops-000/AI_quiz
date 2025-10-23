
// ============================================
// FILE: src/services/aiService.js
// ============================================
import api from './api';

const aiService = {
  processRequest: async (requestData) => {
    return await api.post('/ai/process', requestData);
  },

  textGeneration: async (prompt, options = {}) => {
    return await api.post('/ai/process', {
      requestType: 'text-generation',
      input: { prompt, ...options }
    });
  },

  imageAnalysis: async (imageUrl, analysisType = 'general') => {
    return await api.post('/ai/process', {
      requestType: 'image-analysis',
      input: { imageUrl, analysisType }
    });
  },

  prediction: async (data, modelType) => {
    return await api.post('/ai/process', {
      requestType: 'prediction',
      input: { data, modelType }
    });
  },

  recommendation: async (userId, context) => {
    return await api.post('/ai/process', {
      requestType: 'recommendation',
      input: { userId, context }
    });
  },

  getHistory: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString();
    return await api.get(`/ai/history${queryString ? `?${queryString}` : ''}`);
  },

  getRequestById: async (id) => {
    return await api.get(`/ai/requests/${id}`);
  }
};

export default aiService;