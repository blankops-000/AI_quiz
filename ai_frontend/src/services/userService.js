
// ============================================
// FILE: src/services/userService.js
// ============================================
import api from './api';

const userService = {
  getAllUsers: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString();
    return await api.get(`/users${queryString ? `?${queryString}` : ''}`);
  },

  getUserById: async (id) => {
    return await api.get(`/users/${id}`);
  },

  updateProfile: async (userData) => {
    return await api.put('/users/profile', userData);
  },

  deleteUser: async (id) => {
    return await api.delete(`/users/${id}`);
  }
};

export default userService;