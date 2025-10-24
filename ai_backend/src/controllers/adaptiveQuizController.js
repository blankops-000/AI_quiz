// ============================================
// FILE: src/controllers/adaptiveQuizController.js
// ============================================
const Quiz = require('../models/Quiz');
const QuizAttempt = require('../models/QuizAttempt');
const StudentProfile = require('../models/StudentProfile');
const aiService = require('../services/aiService');
const { ApiResponse } = require('../utils/apiResponse');
const logger = require('../utils/logger');

class AdaptiveQuizController {
  // Generate adaptive quiz
  async generateAdaptiveQuiz(req, res) {
    try {
      const { subject, topic, difficulty = 'medium', numQuestions = 10, targetBloomsLevels } = req.body;
      const userId = req.user.id;

      // Get or create student profile
      let studentProfile = await StudentProfile.findOne({ userId });
      if (!studentProfile) {
        studentProfile = new StudentProfile({ userId });
        await studentProfile.save();
      }

      // Prepare AI service request
      const aiRequest = {
        user_id: userId,
        subject,
        topic,
        difficulty,
        num_questions: numQuestions,
        target_blooms_levels: targetBloomsLevels || ['apply', 'analyze'],
        student_profile: {
          ability_level: studentProfile.abilityLevel,
          blooms_progress: studentProfile.bloomsLevels,
          subject_abilities: studentProfile.subjectPerformance.reduce((acc, perf) => {
            acc[perf.subject] = perf.abilityLevel;
            return acc;
          }, {}),
          learning_style: studentProfile.learningStyle
        }
      };

      // Call AI service for adaptive quiz generation
      const aiResponse = await aiService.processRequest('quiz/adaptive/generate', aiRequest);

      if (!aiResponse.success) {
        return ApiResponse.error(res, 'Failed to generate adaptive quiz', 500);
      }

      // Create quiz record in database
      const quizData = aiResponse.data;
      const quiz = new Quiz({
        title: quizData.title,
        description: `Adaptive quiz for ${topic}`,
        subject,
        createdBy: userId,
        isAdaptive: true,
        initialDifficulty: difficulty,
        targetBloomsLevels: (targetBloomsLevels || []).map(level => ({
          level,
          weight: 1.0 / (targetBloomsLevels?.length || 1)
        })),
        questions: quizData.questions.map(q => ({
          questionText: q.text,
          questionType: q.type || 'multiple-choice',
          options: q.options?.map(opt => ({ text: opt, isCorrect: false })) || [],
          difficulty: q.difficulty,
          discrimination: 1.0,
          guessing: 0.25,
          bloomsLevel: q.blooms_level,
          cognitiveComplexity: this.getBloomsComplexity(q.blooms_level),
          subject,
          topic,
          keywords: [topic]
        })),
        adaptiveSettings: {
          terminationCriteria: 'fixed-length',
          minQuestions: Math.min(5, numQuestions),
          maxQuestions: numQuestions
        }
      });

      await quiz.save();

      // Update quiz data with database ID
      quizData.quiz_id = quiz._id.toString();
      quizData.database_id = quiz._id;

      return ApiResponse.success(res, quizData, 'Adaptive quiz generated successfully');

    } catch (error) {
      logger.error('Error generating adaptive quiz:', error);
      return ApiResponse.error(res, 'Internal server error', 500);
    }
  }

  // Process quiz response
  async processQuizResponse(req, res) {
    try {
      const { quizId, questionId, answer, responseTime = 0, isAdaptive = true } = req.body;
      const userId = req.user.id;

      // Find or create quiz attempt
      let quizAttempt = await QuizAttempt.findOne({ 
        userId, 
        quizId, 
        status: 'in-progress' 
      });

      if (!quizAttempt) {
        const studentProfile = await StudentProfile.findOne({ userId });
        quizAttempt = new QuizAttempt({
          userId,
          quizId,
          initialAbility: studentProfile?.abilityLevel || 0,
          status: 'in-progress'
        });
      }

      // Prepare AI service request
      const aiRequest = {
        user_id: userId,
        quiz_id: quizId,
        question_id: questionId,
        answer,
        response_time: responseTime,
        is_adaptive: isAdaptive,
        remaining_questions: req.body.remainingQuestions || []
      };

      // Process response through AI service
      const aiResponse = await aiService.processRequest('quiz/adaptive/response', aiRequest);

      if (!aiResponse.success) {
        return ApiResponse.error(res, 'Failed to process quiz response', 500);
      }

      const responseData = aiResponse.data;

      // Update quiz attempt with response
      const response = {
        questionId,
        userAnswer: answer,
        correctAnswer: responseData.correct_answer,
        isCorrect: responseData.is_correct,
        responseTime,
        difficulty: responseData.difficulty || 0,
        bloomsLevel: responseData.blooms_level || 'remember',
        expectedProbability: responseData.expected_probability,
        abilityEstimate: responseData.updated_ability
      };

      quizAttempt.responses.push(response);
      quizAttempt.totalQuestions += 1;
      if (responseData.is_correct) {
        quizAttempt.correctAnswers += 1;
      }

      // Update Bloom's performance
      const bloomsLevel = responseData.blooms_level || 'remember';
      if (quizAttempt.bloomsPerformance[bloomsLevel]) {
        quizAttempt.bloomsPerformance[bloomsLevel].total += 1;
        if (responseData.is_correct) {
          quizAttempt.bloomsPerformance[bloomsLevel].correct += 1;
        }
      }

      // Update ability estimates
      quizAttempt.finalAbility = responseData.updated_ability;
      quizAttempt.abilityChange = quizAttempt.finalAbility - quizAttempt.initialAbility;

      await quizAttempt.save();

      // Update student profile
      await this.updateStudentProfile(userId, responseData);

      return ApiResponse.success(res, {
        ...responseData,
        attempt_id: quizAttempt._id,
        current_score: quizAttempt.totalQuestions > 0 ? 
          (quizAttempt.correctAnswers / quizAttempt.totalQuestions * 100) : 0
      }, 'Response processed successfully');

    } catch (error) {
      logger.error('Error processing quiz response:', error);
      return ApiResponse.error(res, 'Internal server error', 500);
    }
  }

  // Complete quiz and analyze performance
  async completeQuiz(req, res) {
    try {
      const { quizId, responses } = req.body;
      const userId = req.user.id;

      // Find quiz attempt
      const quizAttempt = await QuizAttempt.findOne({ 
        userId, 
        quizId, 
        status: 'in-progress' 
      });

      if (!quizAttempt) {
        return ApiResponse.error(res, 'Quiz attempt not found', 404);
      }

      // Complete the attempt
      quizAttempt.endTime = new Date();
      quizAttempt.totalTime = Math.floor((quizAttempt.endTime - quizAttempt.startTime) / 1000);
      quizAttempt.score = quizAttempt.totalQuestions > 0 ? 
        (quizAttempt.correctAnswers / quizAttempt.totalQuestions * 100) : 0;
      quizAttempt.status = 'completed';
      quizAttempt.isPassed = quizAttempt.score >= 70; // Default passing score

      // Generate feedback
      quizAttempt.generateFeedback();

      await quizAttempt.save();

      // Analyze performance through AI service
      const aiRequest = {
        user_id: userId,
        responses: responses || quizAttempt.responses.map(r => ({
          question: {
            id: r.questionId,
            difficulty: r.difficulty,
            blooms_level: r.bloomsLevel
          },
          is_correct: r.isCorrect,
          response_time: r.responseTime
        }))
      };

      const analysisResponse = await aiService.processRequest('quiz/adaptive/analyze', aiRequest);

      let performanceAnalysis = {};
      if (analysisResponse.success) {
        performanceAnalysis = analysisResponse.data;
      }

      // Update quiz analytics
      await this.updateQuizAnalytics(quizId, quizAttempt);

      return ApiResponse.success(res, {
        attempt: quizAttempt,
        analysis: performanceAnalysis,
        summary: {
          score: quizAttempt.score,
          totalQuestions: quizAttempt.totalQuestions,
          correctAnswers: quizAttempt.correctAnswers,
          totalTime: quizAttempt.totalTime,
          isPassed: quizAttempt.isPassed,
          abilityChange: quizAttempt.abilityChange
        }
      }, 'Quiz completed and analyzed successfully');

    } catch (error) {
      logger.error('Error completing quiz:', error);
      return ApiResponse.error(res, 'Internal server error', 500);
    }
  }

  // Get student profile
  async getStudentProfile(req, res) {
    try {
      const userId = req.user.id;

      let studentProfile = await StudentProfile.findOne({ userId }).populate('userId', 'name email');
      
      if (!studentProfile) {
        studentProfile = new StudentProfile({ userId });
        await studentProfile.save();
        await studentProfile.populate('userId', 'name email');
      }

      // Get recent quiz attempts for additional insights
      const recentAttempts = await QuizAttempt.find({ userId })
        .sort({ createdAt: -1 })
        .limit(10)
        .populate('quizId', 'title subject');

      const profileData = {
        ...studentProfile.toObject(),
        overallProficiency: studentProfile.calculateOverallProficiency(),
        recentPerformance: recentAttempts.map(attempt => ({
          quizTitle: attempt.quizId?.title || 'Unknown Quiz',
          subject: attempt.quizId?.subject || 'Unknown',
          score: attempt.score,
          date: attempt.createdAt,
          abilityChange: attempt.abilityChange
        }))
      };

      return ApiResponse.success(res, profileData, 'Student profile retrieved successfully');

    } catch (error) {
      logger.error('Error retrieving student profile:', error);
      return ApiResponse.error(res, 'Internal server error', 500);
    }
  }

  // Get quiz analytics for educators
  async getQuizAnalytics(req, res) {
    try {
      const { quizId } = req.params;
      const userId = req.user.id;

      // Verify quiz ownership or admin access
      const quiz = await Quiz.findById(quizId);
      if (!quiz) {
        return ApiResponse.error(res, 'Quiz not found', 404);
      }

      if (quiz.createdBy.toString() !== userId && req.user.role !== 'admin') {
        return ApiResponse.error(res, 'Access denied', 403);
      }

      // Get all attempts for this quiz
      const attempts = await QuizAttempt.find({ quizId }).populate('userId', 'name email');

      // Calculate analytics
      const analytics = {
        quiz: {
          title: quiz.title,
          subject: quiz.subject,
          totalQuestions: quiz.questions.length,
          isAdaptive: quiz.isAdaptive
        },
        participation: {
          totalAttempts: attempts.length,
          uniqueStudents: new Set(attempts.map(a => a.userId.toString())).size,
          completionRate: attempts.filter(a => a.status === 'completed').length / attempts.length
        },
        performance: {
          averageScore: attempts.reduce((sum, a) => sum + (a.score || 0), 0) / attempts.length,
          passRate: attempts.filter(a => a.isPassed).length / attempts.length,
          averageTime: attempts.reduce((sum, a) => sum + (a.totalTime || 0), 0) / attempts.length
        },
        bloomsAnalysis: this.analyzeBloomsPerformance(attempts),
        difficultyAnalysis: this.analyzeDifficultyDistribution(attempts),
        studentProgress: attempts.map(attempt => ({
          studentName: attempt.userId.name,
          score: attempt.score,
          abilityChange: attempt.abilityChange,
          bloomsPerformance: attempt.getBloomsPerformance(),
          completedAt: attempt.endTime
        }))
      };

      return ApiResponse.success(res, analytics, 'Quiz analytics retrieved successfully');

    } catch (error) {
      logger.error('Error retrieving quiz analytics:', error);
      return ApiResponse.error(res, 'Internal server error', 500);
    }
  }

  // Helper methods
  getBloomsComplexity(bloomsLevel) {
    const complexityMap = {
      'remember': 1,
      'understand': 2,
      'apply': 3,
      'analyze': 4,
      'evaluate': 5,
      'create': 6
    };
    return complexityMap[bloomsLevel] || 1;
  }

  async updateStudentProfile(userId, responseData) {
    try {
      const studentProfile = await StudentProfile.findOne({ userId });
      if (studentProfile) {
        // Update ability level
        studentProfile.abilityLevel = responseData.updated_ability;
        
        // Update Bloom's progress
        if (responseData.blooms_progress) {
          Object.keys(responseData.blooms_progress).forEach(level => {
            if (studentProfile.bloomsLevels[level] !== undefined) {
              studentProfile.bloomsLevels[level] = responseData.blooms_progress[level];
            }
          });
        }

        await studentProfile.save();
      }
    } catch (error) {
      logger.error('Error updating student profile:', error);
    }
  }

  async updateQuizAnalytics(quizId, quizAttempt) {
    try {
      const quiz = await Quiz.findById(quizId);
      if (quiz) {
        quiz.analytics.totalAttempts += 1;
        
        // Update average score
        const totalScore = quiz.analytics.averageScore * (quiz.analytics.totalAttempts - 1) + quizAttempt.score;
        quiz.analytics.averageScore = totalScore / quiz.analytics.totalAttempts;
        
        // Update average time
        if (quizAttempt.totalTime) {
          const totalTime = quiz.analytics.averageTime * (quiz.analytics.totalAttempts - 1) + quizAttempt.totalTime;
          quiz.analytics.averageTime = totalTime / quiz.analytics.totalAttempts;
        }

        await quiz.save();
      }
    } catch (error) {
      logger.error('Error updating quiz analytics:', error);
    }
  }

  analyzeBloomsPerformance(attempts) {
    const bloomsLevels = ['remember', 'understand', 'apply', 'analyze', 'evaluate', 'create'];
    const analysis = {};

    bloomsLevels.forEach(level => {
      const levelData = attempts.reduce((acc, attempt) => {
        const performance = attempt.bloomsPerformance[level];
        if (performance && performance.total > 0) {
          acc.totalQuestions += performance.total;
          acc.correctAnswers += performance.correct;
        }
        return acc;
      }, { totalQuestions: 0, correctAnswers: 0 });

      analysis[level] = {
        accuracy: levelData.totalQuestions > 0 ? levelData.correctAnswers / levelData.totalQuestions : 0,
        totalQuestions: levelData.totalQuestions
      };
    });

    return analysis;
  }

  analyzeDifficultyDistribution(attempts) {
    const difficulties = { easy: 0, medium: 0, hard: 0 };
    let totalResponses = 0;

    attempts.forEach(attempt => {
      attempt.responses.forEach(response => {
        totalResponses++;
        if (response.difficulty < -0.5) {
          difficulties.easy++;
        } else if (response.difficulty > 0.5) {
          difficulties.hard++;
        } else {
          difficulties.medium++;
        }
      });
    });

    return {
      easy: totalResponses > 0 ? difficulties.easy / totalResponses : 0,
      medium: totalResponses > 0 ? difficulties.medium / totalResponses : 0,
      hard: totalResponses > 0 ? difficulties.hard / totalResponses : 0
    };
  }
}

module.exports = new AdaptiveQuizController();