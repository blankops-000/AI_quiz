
// ============================================
// FILE: src/validators/aiValidator.js
// ============================================
const { body, param } = require('express-validator');
const validate = require('../middleware/validationmiddleware');

exports.validateAIRequest = [
  body('requestType')
    .notEmpty()
    .withMessage('Request type is required')
    .isIn(['text-analysis', 'sentiment-analysis', 'quiz-generation', 'text-generation', 'image-analysis', 'prediction', 'recommendation', 'other'])
    .withMessage('Invalid request type'),
  
  body('input')
    .notEmpty()
    .withMessage('Input is required')
    .isObject()
    .withMessage('Input must be an object'),
  
  validate
];

exports.validateRequestId = [
  param('id')
    .isMongoId()
    .withMessage('Invalid request ID'),
  
  validate
];
