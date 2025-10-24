// ============================================
// FILE: src/models/StudentProfile.js
// ============================================
const mongoose = require('mongoose');

const studentProfileSchema = new mongoose.Schema({
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true,
    unique: true
  },
  // IRT-based ability estimation
  abilityLevel: {
    type: Number,
    default: 0, // Theta parameter in IRT
    min: -4,
    max: 4
  },
  // Bloom's Taxonomy progression tracking
  bloomsLevels: {
    remember: { type: Number, default: 0, min: 0, max: 1 },
    understand: { type: Number, default: 0, min: 0, max: 1 },
    apply: { type: Number, default: 0, min: 0, max: 1 },
    analyze: { type: Number, default: 0, min: 0, max: 1 },
    evaluate: { type: Number, default: 0, min: 0, max: 1 },
    create: { type: Number, default: 0, min: 0, max: 1 }
  },
  // Subject-specific performance
  subjectPerformance: [{
    subject: { type: String, required: true },
    abilityLevel: { type: Number, default: 0 },
    bloomsProgress: {
      remember: { type: Number, default: 0 },
      understand: { type: Number, default: 0 },
      apply: { type: Number, default: 0 },
      analyze: { type: Number, default: 0 },
      evaluate: { type: Number, default: 0 },
      create: { type: Number, default: 0 }
    },
    lastUpdated: { type: Date, default: Date.now }
  }],
  // Learning preferences
  learningStyle: {
    type: String,
    enum: ['visual', 'auditory', 'kinesthetic', 'reading'],
    default: 'visual'
  },
  preferredDifficulty: {
    type: String,
    enum: ['easy', 'medium', 'hard', 'adaptive'],
    default: 'adaptive'
  },
  // Performance metrics
  totalQuizzesTaken: { type: Number, default: 0 },
  averageScore: { type: Number, default: 0 },
  improvementRate: { type: Number, default: 0 },
  streakCount: { type: Number, default: 0 },
  // Adaptive learning parameters
  adaptiveSettings: {
    minDifficulty: { type: Number, default: 0.2 },
    maxDifficulty: { type: Number, default: 0.8 },
    adaptationRate: { type: Number, default: 0.1 },
    confidenceThreshold: { type: Number, default: 0.7 }
  }
}, {
  timestamps: true
});

// Calculate overall proficiency
studentProfileSchema.methods.calculateOverallProficiency = function() {
  const bloomsValues = Object.values(this.bloomsLevels);
  return bloomsValues.reduce((sum, val) => sum + val, 0) / bloomsValues.length;
};

// Update ability level based on performance
studentProfileSchema.methods.updateAbilityLevel = function(correct, difficulty) {
  const learningRate = 0.1;
  const expected = 1 / (1 + Math.exp(-(this.abilityLevel - difficulty)));
  this.abilityLevel += learningRate * (correct - expected);
  this.abilityLevel = Math.max(-4, Math.min(4, this.abilityLevel));
};

module.exports = mongoose.model('StudentProfile', studentProfileSchema);