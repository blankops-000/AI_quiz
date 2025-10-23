
// ============================================
// FILE: src/utils/constants.js
// ============================================
export const POST_CATEGORIES = [
  { value: 'technology', label: 'Technology' },
  { value: 'business', label: 'Business' },
  { value: 'lifestyle', label: 'Lifestyle' },
  { value: 'education', label: 'Education' },
  { value: 'other', label: 'Other' }
];

export const POST_STATUS = [
  { value: 'draft', label: 'Draft' },
  { value: 'published', label: 'Published' },
  { value: 'archived', label: 'Archived' }
];

export const AI_REQUEST_TYPES = [
  { value: 'text-generation', label: 'Text Generation' },
  { value: 'image-analysis', label: 'Image Analysis' },
  { value: 'prediction', label: 'Prediction' },
  { value: 'recommendation', label: 'Recommendation' },
  { value: 'other', label: 'Other' }
];

export const USER_ROLES = [
  { value: 'user', label: 'User' },
  { value: 'admin', label: 'Admin' },
  { value: 'moderator', label: 'Moderator' }
];

export const PAGINATION_LIMITS = [5, 10, 20, 50];

export const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

export default {
  POST_CATEGORIES,
  POST_STATUS,
  AI_REQUEST_TYPES,
  USER_ROLES,
  PAGINATION_LIMITS,
  API_URL
};