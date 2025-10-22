
// ============================================
// FILE: src/models/AIRequest.js
// ============================================
const mongoose = require('mongoose');

const aiRequestSchema = new mongoose.Schema({
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  requestType: {
    type: String,
    enum: ['text-generation', 'image-analysis', 'prediction', 'recommendation', 'other'],
    required: true
  },
  input: {
    type: mongoose.Schema.Types.Mixed,
    required: true
  },
  output: {
    type: mongoose.Schema.Types.Mixed,
    default: null
  },
  status: {
    type: String,
    enum: ['pending', 'processing', 'completed', 'failed'],
    default: 'pending'
  },
  error: {
    type: String,
    default: null
  },
  processingTime: {
    type: Number,
    default: null
  },
  metadata: {
    type: mongoose.Schema.Types.Mixed,
    default: {}
  }
}, {
  timestamps: true
});

module.exports = mongoose.model('AIRequest', aiRequestSchema);