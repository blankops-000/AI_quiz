
// ============================================
// FILE: src/validators/aiValidator.js
// ============================================
const { body, param } = require('express-validator');
const validate = require('../middleware/validation.middleware');

exports.validateAIRequest = [
  body('requestType')
    .notEmpty()
    .withMessage('Request type is required')
    .isIn(['text-generation', 'image-analysis', 'prediction', 'recommendation', 'other'])
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
