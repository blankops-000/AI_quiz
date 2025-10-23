
// ============================================
// FILE: src/services/dataService.js
// ============================================
import api from './api';

const dataService = {
  // Posts
  getAllPosts: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString();
    return await api.get(`/data/posts${queryString ? `?${queryString}` : ''}`);
  },

  getPostById: async (id) => {
    return await api.get(`/data/posts/${id}`);
  },

  createPost: async (postData) => {
    return await api.post('/data/posts', postData);
  },

  updatePost: async (id, postData) => {
    return await api.put(`/data/posts/${id}`, postData);
  },

  deletePost: async (id) => {
    return await api.delete(`/data/posts/${id}`);
  },

  likePost: async (id) => {
    return await api.post(`/data/posts/${id}/like`);
  }
};

export default dataService;