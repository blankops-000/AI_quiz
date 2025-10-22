
// ============================================
// FILE: src/controllers/aiController.js
// ============================================
const AIRequest = require('../models/AIRequest');
const aiService = require('../services/aiService');
const { ApiResponse } = require('../utils/apiResponse');
const logger = require('../utils/logger');

exports.processAIRequest = async (req, res, next) => {
  try {
    const { requestType, input } = req.body;
    
    // Create AI request record
    const aiRequest = await AIRequest.create({
      userId: req.user.id,
      requestType,
      input,
      status: 'processing'
    });

    const startTime = Date.now();

    try {
      // Process AI request
      const result = await aiService.processRequest(requestType, input);
      
      const processingTime = Date.now() - startTime;

      // Update AI request record
      aiRequest.output = result;
      aiRequest.status = 'completed';
      aiRequest.processingTime = processingTime;
      await aiRequest.save();

      logger.info(`AI request completed: ${aiRequest._id} in ${processingTime}ms`);

      res.status(200).json(
        ApiResponse.success({
          requestId: aiRequest._id,
          result,
          processingTime
        }, 'AI request processed successfully')
      );
    } catch (aiError) {
      // Update AI request with error
      aiRequest.status = 'failed';
      aiRequest.error = aiError.message;
      await aiRequest.save();

      throw aiError;
    }
  } catch (error) {
    logger.error(`AI request failed: ${error.message}`);
    next(error);
  }
};

exports.getAIRequestHistory = async (req, res, next) => {
  try {
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 10;
    const skip = (page - 1) * limit;

    const requests = await AIRequest.find({ userId: req.user.id })
      .limit(limit)
      .skip(skip)
      .sort({ createdAt: -1 });

    const total = await AIRequest.countDocuments({ userId: req.user.id });

    res.status(200).json(
      ApiResponse.success({
        requests,
        pagination: {
          page,
          limit,
          total,
          pages: Math.ceil(total / limit)
        }
      }, 'AI request history retrieved successfully')
    );
  } catch (error) {
    next(error);
  }
};

exports.getAIRequestById = async (req, res, next) => {
  try {
    const aiRequest = await AIRequest.findById(req.params.id);
    
    if (!aiRequest) {
      return res.status(404).json(
        ApiResponse.error('AI request not found')
      );
    }

    // Check if user owns the request
    if (aiRequest.userId.toString() !== req.user.id && req.user.role !== 'admin') {
      return res.status(403).json(
        ApiResponse.error('Not authorized to view this request')
      );
    }

    res.status(200).json(
      ApiResponse.success({ aiRequest }, 'AI request retrieved successfully')
    );
  } catch (error) {
    next(error);
  }
};
