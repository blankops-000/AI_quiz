
// ============================================
// FILE: src/routes/ai.routes.js
// ============================================
const express = require('express');
const router = express.Router();
const aiController = require('../controllers/aiController');
const authMiddleware = require('../middleware/authMiddleware');
const optionalAuthMiddleware = require('../middleware/optionalAuthMiddleware');
const { validateAIRequest } = require('../validators/aiValidator');

// Health check endpoint (no auth required)
router.get('/health', aiController.healthCheck);

// Test endpoint to create user and get token
const testController = require('../controllers/testController');
router.post('/test-token', testController.createTestUser);

// AI process endpoint (optional auth)
router.post('/process', optionalAuthMiddleware, aiController.processAIRequest);

router.use(authMiddleware);
router.get('/history', aiController.getAIRequestHistory);
router.get('/requests/:id', aiController.getAIRequestById);

module.exports = router;