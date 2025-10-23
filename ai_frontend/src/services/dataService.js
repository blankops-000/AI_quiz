
// ============================================
// FILE: src/services/dataService.js
// ============================================
import api from './api';

const dataService = {
  // Posts
  getAllPosts: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString();
    const response = await api.get(`/data/posts${queryString ? `?${queryString}` : ''}`);
    return response.data; // Extract data from backend response structure
  },

  getPostById: async (id) => {
    const response = await api.get(`/data/posts/${id}`);
    return response.data;
  },

  createPost: async (postData) => {
    const response = await api.post('/data/posts', postData);
    return response.data;
  },

  updatePost: async (id, postData) => {
    const response = await api.put(`/data/posts/${id}`, postData);
    return response.data;
  },

  deletePost: async (id) => {
    const response = await api.delete(`/data/posts/${id}`);
    return response;
  },

  likePost: async (id) => {
    const response = await api.post(`/data/posts/${id}/like`);
    return response.data;
  }
};

export default dataService;