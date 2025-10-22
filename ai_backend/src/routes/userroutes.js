// ============================================
// FILE: src/routes/user.routes.js
// ============================================
const express = require('express');
const router = express.Router();
const userController = require('../controllers/userController');
const authMiddleware = require('../middleware/auth.middleware');
const { authorize } = require('../middleware/auth.middleware');

router.use(authMiddleware);

router.get('/', authorize('admin'), userController.getAllUsers);
router.get('/:id', userController.getUserById);
router.put('/profile', userController.updateUser);
router.delete('/:id', authorize('admin'), userController.deleteUser);

module.exports = router;