// ============================================
// FILE: src/models/Quiz.js
// ============================================
const mongoose = require('mongoose');

const questionSchema = new mongoose.Schema({
  questionText: { type: String, required: true },
  questionType: {
    type: String,
    enum: ['multiple-choice', 'true-false', 'short-answer', 'coding', 'essay'],
    default: 'multiple-choice'
  },
  options: [{
    text: String,
    isCorrect: Boolean
  }],
  correctAnswer: String,
  explanation: String,
  // IRT parameters
  difficulty: { type: Number, required: true, min: -4, max: 4 }, // b parameter
  discrimination: { type: Number, default: 1, min: 0.1, max: 3 }, // a parameter
  guessing: { type: Number, default: 0, min: 0, max: 1 }, // c parameter
  // Bloom's Taxonomy classification
  bloomsLevel: {
    type: String,
    enum: ['remember', 'understand', 'apply', 'analyze', 'evaluate', 'create'],
    required: true
  },
  cognitiveComplexity: { type: Number, min: 1, max: 6 }, // 1=remember, 6=create
  // Subject and topic tagging
  subject: { type: String, required: true },
  topic: { type: String, required: true },
  subtopics: [String],
  keywords: [String],
  // Performance tracking
  timesAsked: { type: Number, default: 0 },
  correctResponses: { type: Number, default: 0 },
  averageResponseTime: { type: Number, default: 0 }
});

const quizSchema = new mongoose.Schema({
  title: { type: String, required: true },
  description: String,
  subject: { type: String, required: true },
  createdBy: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  // Quiz configuration
  isAdaptive: { type: Boolean, default: true },
  initialDifficulty: {
    type: String,
    enum: ['easy', 'medium', 'hard'],
    default: 'medium'
  },
  targetBloomsLevels: [{
    level: {
      type: String,
      enum: ['remember', 'understand', 'apply', 'analyze', 'evaluate', 'create']
    },
    weight: { type: Number, min: 0, max: 1 }
  }],
  // Question pool
  questions: [questionSchema],
  questionPool: [questionSchema], // Additional questions for adaptive selection
  // Quiz settings
  timeLimit: { type: Number, default: 0 }, // 0 = no limit
  maxQuestions: { type: Number, default: 10 },
  passingScore: { type: Number, default: 70 },
  allowRetakes: { type: Boolean, default: true },
  showCorrectAnswers: { type: Boolean, default: true },
  // Adaptive parameters
  adaptiveSettings: {
    terminationCriteria: {
      type: String,
      enum: ['fixed-length', 'standard-error', 'confidence-interval'],
      default: 'fixed-length'
    },
    standardErrorThreshold: { type: Number, default: 0.3 },
    confidenceLevel: { type: Number, default: 0.95 },
    minQuestions: { type: Number, default: 5 },
    maxQuestions: { type: Number, default: 20 }
  },
  // Analytics
  analytics: {
    totalAttempts: { type: Number, default: 0 },
    averageScore: { type: Number, default: 0 },
    averageTime: { type: Number, default: 0 },
    difficultyDistribution: {
      easy: { type: Number, default: 0 },
      medium: { type: Number, default: 0 },
      hard: { type: Number, default: 0 }
    }
  },
  isActive: { type: Boolean, default: true }
}, {
  timestamps: true
});

// Calculate question difficulty distribution
quizSchema.methods.getDifficultyDistribution = function() {
  const distribution = { easy: 0, medium: 0, hard: 0 };
  this.questions.forEach(q => {
    if (q.difficulty < -1) distribution.easy++;
    else if (q.difficulty > 1) distribution.hard++;
    else distribution.medium++;
  });
  return distribution;
};

// Get questions by Bloom's level
quizSchema.methods.getQuestionsByBloomsLevel = function(level) {
  return this.questions.filter(q => q.bloomsLevel === level);
};

// Calculate quiz complexity score
quizSchema.methods.getComplexityScore = function() {
  const totalComplexity = this.questions.reduce((sum, q) => sum + q.cognitiveComplexity, 0);
  return totalComplexity / this.questions.length;
};

module.exports = mongoose.model('Quiz', quizSchema);