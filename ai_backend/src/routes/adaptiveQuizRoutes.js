// ============================================
// FILE: src/routes/adaptiveQuizRoutes.js
// ============================================
const express = require('express');
const adaptiveQuizController = require('../controllers/adaptiveQuizController');
const authMiddleware = require('../middleware/authMiddleware');
const { validateAdaptiveQuiz, validateQuizResponse } = require('../validators/adaptiveQuizValidator');
const rateLimiterMiddleware = require('../middleware/rateLimitermiddleware');

const router = express.Router();

// Apply authentication middleware to all routes
router.use(authMiddleware);

// Apply rate limiting
router.use(rateLimiterMiddleware);

/**
 * @route   POST /api/adaptive-quiz/generate
 * @desc    Generate adaptive quiz based on student profile
 * @access  Private
 */
router.post('/generate', validateAdaptiveQuiz, adaptiveQuizController.generateAdaptiveQuiz);

/**
 * @route   POST /api/adaptive-quiz/response
 * @desc    Process student response and adapt quiz
 * @access  Private
 */
router.post('/response', validateQuizResponse, adaptiveQuizController.processQuizResponse);

/**
 * @route   POST /api/adaptive-quiz/complete
 * @desc    Complete quiz and get performance analysis
 * @access  Private
 */
router.post('/complete', adaptiveQuizController.completeQuiz);

/**
 * @route   GET /api/adaptive-quiz/profile
 * @desc    Get student learning profile
 * @access  Private
 */
router.get('/profile', adaptiveQuizController.getStudentProfile);

/**
 * @route   GET /api/adaptive-quiz/analytics/:quizId
 * @desc    Get quiz analytics for educators
 * @access  Private (Quiz creator or admin)
 */
router.get('/analytics/:quizId', adaptiveQuizController.getQuizAnalytics);

module.exports = router;