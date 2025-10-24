// ============================================
// FILE: src/models/QuizAttempt.js
// ============================================
const mongoose = require('mongoose');

const responseSchema = new mongoose.Schema({
  questionId: { type: mongoose.Schema.Types.ObjectId, required: true },
  questionText: String,
  userAnswer: mongoose.Schema.Types.Mixed,
  correctAnswer: mongoose.Schema.Types.Mixed,
  isCorrect: { type: Boolean, required: true },
  responseTime: { type: Number, default: 0 }, // in seconds
  difficulty: Number,
  bloomsLevel: String,
  // IRT calculations for this response
  expectedProbability: Number, // P(correct) based on IRT
  informationValue: Number, // Fisher information
  abilityEstimate: Number, // Theta estimate after this response
  standardError: Number
});

const quizAttemptSchema = new mongoose.Schema({
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  quizId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Quiz',
    required: true
  },
  // Attempt details
  attemptNumber: { type: Number, default: 1 },
  startTime: { type: Date, default: Date.now },
  endTime: Date,
  totalTime: Number, // in seconds
  // Performance metrics
  score: { type: Number, min: 0, max: 100 },
  correctAnswers: { type: Number, default: 0 },
  totalQuestions: { type: Number, default: 0 },
  // IRT-based metrics
  initialAbility: Number,
  finalAbility: Number,
  abilityChange: Number,
  standardError: Number,
  // Bloom's Taxonomy performance
  bloomsPerformance: {
    remember: { correct: { type: Number, default: 0 }, total: { type: Number, default: 0 } },
    understand: { correct: { type: Number, default: 0 }, total: { type: Number, default: 0 } },
    apply: { correct: { type: Number, default: 0 }, total: { type: Number, default: 0 } },
    analyze: { correct: { type: Number, default: 0 }, total: { type: Number, default: 0 } },
    evaluate: { correct: { type: Number, default: 0 }, total: { type: Number, default: 0 } },
    create: { correct: { type: Number, default: 0 }, total: { type: Number, default: 0 } }
  },
  // Detailed responses
  responses: [responseSchema],
  // Adaptive quiz data
  adaptiveData: {
    questionsAdministered: { type: Number, default: 0 },
    terminationReason: {
      type: String,
      enum: ['max-questions', 'standard-error', 'confidence-reached', 'time-limit']
    },
    averageDifficulty: Number,
    difficultyProgression: [Number]
  },
  // Status and completion
  status: {
    type: String,
    enum: ['in-progress', 'completed', 'abandoned', 'timed-out'],
    default: 'in-progress'
  },
  isPassed: Boolean,
  // Feedback and recommendations
  feedback: {
    strengths: [String],
    weaknesses: [String],
    recommendations: [String],
    nextSteps: [String]
  }
}, {
  timestamps: true
});

// Calculate performance by Bloom's level
quizAttemptSchema.methods.getBloomsPerformance = function() {
  const performance = {};
  Object.keys(this.bloomsPerformance).forEach(level => {
    const data = this.bloomsPerformance[level];
    performance[level] = data.total > 0 ? data.correct / data.total : 0;
  });
  return performance;
};

// Calculate ability estimate using IRT
quizAttemptSchema.methods.calculateAbilityEstimate = function() {
  if (this.responses.length === 0) return 0;
  
  // Simple maximum likelihood estimation
  let ability = 0;
  const maxIterations = 20;
  const tolerance = 0.001;
  
  for (let iter = 0; iter < maxIterations; iter++) {
    let numerator = 0;
    let denominator = 0;
    
    this.responses.forEach(response => {
      const difficulty = response.difficulty || 0;
      const discrimination = 1; // Default discrimination
      const probability = 1 / (1 + Math.exp(-discrimination * (ability - difficulty)));
      
      numerator += discrimination * (response.isCorrect ? 1 : 0) - discrimination * probability;
      denominator += discrimination * discrimination * probability * (1 - probability);
    });
    
    if (Math.abs(numerator) < tolerance) break;
    ability += numerator / denominator;
  }
  
  return Math.max(-4, Math.min(4, ability));
};

// Generate personalized feedback
quizAttemptSchema.methods.generateFeedback = function() {
  const bloomsPerf = this.getBloomsPerformance();
  const strengths = [];
  const weaknesses = [];
  const recommendations = [];
  
  Object.entries(bloomsPerf).forEach(([level, score]) => {
    if (score >= 0.8) {
      strengths.push(`Strong performance in ${level} level questions`);
    } else if (score < 0.5) {
      weaknesses.push(`Needs improvement in ${level} level questions`);
      recommendations.push(`Practice more ${level} level exercises`);
    }
  });
  
  this.feedback = { strengths, weaknesses, recommendations };
  return this.feedback;
};

module.exports = mongoose.model('QuizAttempt', quizAttemptSchema);