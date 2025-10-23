
// ============================================
// FILE: src/middleware/validation.middleware.js
// ============================================
const { validationResult } = require('express-validator');
const { ApiResponse } = require('../utils/apiResponse');

const validate = (req, res, next) => {
  const errors = validationResult(req);
  
  if (!errors.isEmpty()) {
    console.log('Validation errors:', errors.array());
    console.log('Request body:', req.body);
    return res.status(400).json(
      ApiResponse.error('Validation failed', 400, errors.array())
    );
  }
  
  next();
};

module.exports = validate;