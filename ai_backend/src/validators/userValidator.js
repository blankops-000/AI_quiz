
// ============================================
// FILE: src/validators/userValidator.js
// ============================================
const { body, param } = require('express-validator');
const validate = require('../middleware/validationmiddleware');

exports.validateUserId = [
  param('id')
    .isMongoId()
    .withMessage('Invalid user ID'),
  
  validate
];

exports.validateUserUpdate = [
  body('username')
    .optional()
    .trim()
    .isLength({ min: 3, max: 30 })
    .withMessage('Username must be between 3 and 30 characters'),
  
  body('email')
    .optional()
    .trim()
    .isEmail()
    .withMessage('Please provide a valid email')
    .normalizeEmail(),
  
  body('avatar')
    .optional()
    .isURL()
    .withMessage('Avatar must be a valid URL'),
  
  validate
];
