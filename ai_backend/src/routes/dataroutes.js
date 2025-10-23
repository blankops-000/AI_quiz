
// ============================================
// FILE: src/routes/data.routes.js
// ============================================
const express = require('express');
const router = express.Router();
const dataController = require('../controllers/dataController');
const authMiddleware = require('../middleware/authMiddleware');
const { validatePost } = require('../validators/dataValidator');

router.get('/posts', dataController.getAllPosts);
router.get('/posts/:id', dataController.getPostById);

router.use(authMiddleware);

router.post('/posts', validatePost, dataController.createPost);
router.put('/posts/:id', validatePost, dataController.updatePost);
router.delete('/posts/:id', dataController.deletePost);
router.post('/posts/:id/like', dataController.likePost);

module.exports = router;
