
// ============================================
// FILE: src/validators/dataValidator.js
// ============================================
const { body, param } = require('express-validator');
const validate = require('../middleware/validation.middleware');

exports.validatePost = [
  body('title')
    .trim()
    .notEmpty()
    .withMessage('Title is required')
    .isLength({ max: 200 })
    .withMessage('Title cannot exceed 200 characters'),
  
  body('content')
    .trim()
    .notEmpty()
    .withMessage('Content is required'),
  
  body('tags')
    .optional()
    .isArray()
    .withMessage('Tags must be an array'),
  
  body('category')
    .optional()
    .isIn(['technology', 'business', 'lifestyle', 'education', 'other'])
    .withMessage('Invalid category'),
  
  body('status')
    .optional()
    .isIn(['draft', 'published', 'archived'])
    .withMessage('Invalid status'),
  
  validate
];

exports.validatePostId = [
  param('id')
    .isMongoId()
    .withMessage('Invalid post ID'),
  
  validate
];
