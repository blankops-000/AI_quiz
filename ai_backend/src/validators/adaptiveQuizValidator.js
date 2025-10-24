// ============================================
// FILE: src/validators/adaptiveQuizValidator.js
// ============================================
const { body, validationResult } = require('express-validator');
const { ApiResponse } = require('../utils/apiResponse');

const validateAdaptiveQuiz = [
  body('subject')
    .notEmpty()
    .withMessage('Subject is required')
    .isLength({ min: 2, max: 100 })
    .withMessage('Subject must be between 2 and 100 characters'),
  
  body('topic')
    .notEmpty()
    .withMessage('Topic is required')
    .isLength({ min: 2, max: 200 })
    .withMessage('Topic must be between 2 and 200 characters'),
  
  body('difficulty')
    .optional()
    .isIn(['easy', 'medium', 'hard', 'adaptive'])
    .withMessage('Difficulty must be easy, medium, hard, or adaptive'),
  
  body('numQuestions')
    .optional()
    .isInt({ min: 1, max: 50 })
    .withMessage('Number of questions must be between 1 and 50'),
  
  body('targetBloomsLevels')
    .optional()
    .isArray()
    .withMessage('Target Blooms levels must be an array'),
  
  body('targetBloomsLevels.*')
    .optional()
    .isIn(['remember', 'understand', 'apply', 'analyze', 'evaluate', 'create'])
    .withMessage('Invalid Blooms taxonomy level'),

  (req, res, next) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return ApiResponse.error(res, 'Validation failed', 400, errors.array());
    }
    next();
  }
];

const validateQuizResponse = [
  body('quizId')
    .notEmpty()
    .withMessage('Quiz ID is required')
    .isMongoId()
    .withMessage('Invalid quiz ID format'),
  
  body('questionId')
    .notEmpty()
    .withMessage('Question ID is required'),
  
  body('answer')
    .notEmpty()
    .withMessage('Answer is required'),
  
  body('responseTime')
    .optional()
    .isNumeric()
    .withMessage('Response time must be a number'),
  
  body('isAdaptive')
    .optional()
    .isBoolean()
    .withMessage('isAdaptive must be a boolean'),

  (req, res, next) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return ApiResponse.error(res, 'Validation failed', 400, errors.array());
    }
    next();
  }
];

const validateQuizCompletion = [
  body('quizId')
    .notEmpty()
    .withMessage('Quiz ID is required')
    .isMongoId()
    .withMessage('Invalid quiz ID format'),
  
  body('responses')
    .optional()
    .isArray()
    .withMessage('Responses must be an array'),

  (req, res, next) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return ApiResponse.error(res, 'Validation failed', 400, errors.array());
    }
    next();
  }
];

const validateStudentProfile = [
  body('learningStyle')
    .optional()
    .isIn(['visual', 'auditory', 'kinesthetic', 'reading', 'adaptive'])
    .withMessage('Invalid learning style'),
  
  body('preferredDifficulty')
    .optional()
    .isIn(['easy', 'medium', 'hard', 'adaptive'])
    .withMessage('Invalid preferred difficulty'),

  (req, res, next) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return ApiResponse.error(res, 'Validation failed', 400, errors.array());
    }
    next();
  }
];

module.exports = {
  validateAdaptiveQuiz,
  validateQuizResponse,
  validateQuizCompletion,
  validateStudentProfile
};