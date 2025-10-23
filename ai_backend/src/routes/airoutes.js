
// ============================================
// FILE: src/routes/ai.routes.js
// ============================================
const express = require('express');
const router = express.Router();
const aiController = require('../controllers/aiController');
const authMiddleware = require('../middleware/authMiddleware');
const { validateAIRequest } = require('../validators/aiValidator');

router.use(authMiddleware);

router.post('/process', validateAIRequest, aiController.processAIRequest);
router.get('/history', aiController.getAIRequestHistory);
router.get('/requests/:id', aiController.getAIRequestById);

module.exports = router;