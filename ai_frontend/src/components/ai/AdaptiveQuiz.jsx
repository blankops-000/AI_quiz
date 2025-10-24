// ============================================
// FILE: src/components/ai/AdaptiveQuiz.jsx
// ============================================
import React, { useState, useEffect } from 'react';
import { useAuth } from '../../hooks/useAuth';
import { useAI } from '../../hooks/useAI';
import LoadingSpinner from '../common/LoadingSpinner';
import Toast from '../common/Toast';
import './AdaptiveQuiz.css';

const AdaptiveQuiz = () => {
  const { user } = useAuth();
  const { processAIRequest, loading, error } = useAI();
  
  const [quizState, setQuizState] = useState('setup'); // setup, active, completed
  const [quizConfig, setQuizConfig] = useState({
    subject: 'Computer Science',
    topic: 'Algorithms and Data Structures',
    difficulty: 'medium',
    numQuestions: 10,
    targetBloomsLevels: ['apply', 'analyze']
  });
  
  const [currentQuiz, setCurrentQuiz] = useState(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [responses, setResponses] = useState([]);
  const [selectedAnswer, setSelectedAnswer] = useState('');
  const [feedback, setFeedback] = useState(null);
  const [showFeedback, setShowFeedback] = useState(false);
  const [studentProfile, setStudentProfile] = useState(null);
  const [quizResults, setQuizResults] = useState(null);
  const [toast, setToast] = useState(null);

  useEffect(() => {
    loadStudentProfile();
  }, []);

  const loadStudentProfile = async () => {
    try {
      const response = await fetch('/api/adaptive-quiz/profile', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setStudentProfile(data.data);
      }
    } catch (error) {
      console.error('Error loading student profile:', error);
    }
  };

  const generateQuiz = async () => {
    try {
      const response = await processAIRequest('adaptive-quiz/generate', {
        ...quizConfig,
        user_id: user.id
      });

      if (response.success) {
        setCurrentQuiz(response.data);
        setQuizState('active');
        setCurrentQuestionIndex(0);
        setResponses([]);
        setToast({ type: 'success', message: 'Adaptive quiz generated successfully!' });
      } else {
        setToast({ type: 'error', message: response.message || 'Failed to generate quiz' });
      }
    } catch (error) {
      setToast({ type: 'error', message: 'Error generating quiz' });
    }
  };

  const submitAnswer = async () => {
    if (!selectedAnswer) {
      setToast({ type: 'warning', message: 'Please select an answer' });
      return;
    }

    const startTime = Date.now();
    const currentQuestion = currentQuiz.questions[currentQuestionIndex];
    
    try {
      const response = await processAIRequest('adaptive-quiz/response', {
        user_id: user.id,
        quiz_id: currentQuiz.quiz_id,
        question_id: currentQuestion.id,
        answer: selectedAnswer,
        response_time: Math.floor((Date.now() - startTime) / 1000),
        is_adaptive: true,
        remaining_questions: currentQuiz.questions.slice(currentQuestionIndex + 1)
      });

      if (response.success) {
        const responseData = response.data;
        
        // Store response
        const newResponse = {
          questionId: currentQuestion.id,
          question: currentQuestion,
          userAnswer: selectedAnswer,
          isCorrect: responseData.is_correct,
          correctAnswer: responseData.correct_answer,
          responseTime: responseData.response_time || 0,
          feedback: responseData.feedback
        };
        
        setResponses(prev => [...prev, newResponse]);
        setFeedback(responseData);
        setShowFeedback(true);
        
        // Update student profile if provided
        if (responseData.blooms_progress) {
          setStudentProfile(prev => ({
            ...prev,
            abilityLevel: responseData.updated_ability,
            bloomsLevels: responseData.blooms_progress
          }));
        }
        
        // Check if there's a next question or if quiz should adapt
        if (responseData.next_question) {
          // Replace next question with adapted one
          const updatedQuestions = [...currentQuiz.questions];
          if (currentQuestionIndex + 1 < updatedQuestions.length) {
            updatedQuestions[currentQuestionIndex + 1] = responseData.next_question;
            setCurrentQuiz(prev => ({ ...prev, questions: updatedQuestions }));
          }
        }
        
      } else {
        setToast({ type: 'error', message: response.message || 'Failed to process answer' });
      }
    } catch (error) {
      setToast({ type: 'error', message: 'Error processing answer' });
    }
  };

  const nextQuestion = () => {
    setShowFeedback(false);
    setSelectedAnswer('');
    setFeedback(null);
    
    if (currentQuestionIndex + 1 < currentQuiz.questions.length) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    } else {
      completeQuiz();
    }
  };

  const completeQuiz = async () => {
    try {
      const response = await processAIRequest('adaptive-quiz/complete', {
        quiz_id: currentQuiz.quiz_id,
        responses: responses
      });

      if (response.success) {
        setQuizResults(response.data);
        setQuizState('completed');
        setToast({ type: 'success', message: 'Quiz completed! Check your results.' });
      } else {
        setToast({ type: 'error', message: response.message || 'Failed to complete quiz' });
      }
    } catch (error) {
      setToast({ type: 'error', message: 'Error completing quiz' });
    }
  };

  const resetQuiz = () => {
    setQuizState('setup');
    setCurrentQuiz(null);
    setCurrentQuestionIndex(0);
    setResponses([]);
    setSelectedAnswer('');
    setFeedback(null);
    setShowFeedback(false);
    setQuizResults(null);
  };

  const renderQuizSetup = () => (
    <div className="quiz-setup">
      <h2>Generate Adaptive Quiz</h2>
      <div className="setup-form">
        <div className="form-group">
          <label>Subject:</label>
          <select 
            value={quizConfig.subject}
            onChange={(e) => setQuizConfig(prev => ({ ...prev, subject: e.target.value }))}
          >
            <option value="Computer Science">Computer Science</option>
            <option value="Mathematics">Mathematics</option>
            <option value="Physics">Physics</option>
            <option value="Chemistry">Chemistry</option>
          </select>
        </div>
        
        <div className="form-group">
          <label>Topic:</label>
          <input
            type="text"
            value={quizConfig.topic}
            onChange={(e) => setQuizConfig(prev => ({ ...prev, topic: e.target.value }))}
            placeholder="e.g., Algorithms and Data Structures"
          />
        </div>
        
        <div className="form-group">
          <label>Initial Difficulty:</label>
          <select 
            value={quizConfig.difficulty}
            onChange={(e) => setQuizConfig(prev => ({ ...prev, difficulty: e.target.value }))}
          >
            <option value="easy">Easy</option>
            <option value="medium">Medium</option>
            <option value="hard">Hard</option>
            <option value="adaptive">Adaptive</option>
          </select>
        </div>
        
        <div className="form-group">
          <label>Number of Questions:</label>
          <input
            type="number"
            min="5"
            max="20"
            value={quizConfig.numQuestions}
            onChange={(e) => setQuizConfig(prev => ({ ...prev, numQuestions: parseInt(e.target.value) }))}
          />
        </div>
        
        <div className="form-group">
          <label>Target Bloom's Levels:</label>
          <div className="blooms-checkboxes">
            {['remember', 'understand', 'apply', 'analyze', 'evaluate', 'create'].map(level => (
              <label key={level} className="checkbox-label">
                <input
                  type="checkbox"
                  checked={quizConfig.targetBloomsLevels.includes(level)}
                  onChange={(e) => {
                    if (e.target.checked) {
                      setQuizConfig(prev => ({
                        ...prev,
                        targetBloomsLevels: [...prev.targetBloomsLevels, level]
                      }));
                    } else {
                      setQuizConfig(prev => ({
                        ...prev,
                        targetBloomsLevels: prev.targetBloomsLevels.filter(l => l !== level)
                      }));
                    }
                  }}
                />
                {level.charAt(0).toUpperCase() + level.slice(1)}
              </label>
            ))}
          </div>
        </div>
        
        <button 
          className="generate-btn"
          onClick={generateQuiz}
          disabled={loading}
        >
          {loading ? 'Generating...' : 'Generate Adaptive Quiz'}
        </button>
      </div>
      
      {studentProfile && (
        <div className="student-profile-summary">
          <h3>Your Learning Profile</h3>
          <div className="profile-stats">
            <div className="stat">
              <label>Current Ability Level:</label>
              <span className={`ability-level ${getAbilityClass(studentProfile.abilityLevel)}`}>
                {getAbilityLabel(studentProfile.abilityLevel)}
              </span>
            </div>
            <div className="blooms-progress">
              <label>Bloom's Taxonomy Progress:</label>
              <div className="progress-bars">
                {Object.entries(studentProfile.bloomsLevels || {}).map(([level, progress]) => (
                  <div key={level} className="progress-item">
                    <span className="level-name">{level}</span>
                    <div className="progress-bar">
                      <div 
                        className="progress-fill"
                        style={{ width: `${progress * 100}%` }}
                      ></div>
                    </div>
                    <span className="progress-value">{Math.round(progress * 100)}%</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );

  const renderActiveQuiz = () => {
    const currentQuestion = currentQuiz.questions[currentQuestionIndex];
    
    return (
      <div className="active-quiz">
        <div className="quiz-header">
          <h2>{currentQuiz.title}</h2>
          <div className="quiz-progress">
            <span>Question {currentQuestionIndex + 1} of {currentQuiz.total_questions}</span>
            <div className="progress-bar">
              <div 
                className="progress-fill"
                style={{ width: `${((currentQuestionIndex + 1) / currentQuiz.total_questions) * 100}%` }}
              ></div>
            </div>
          </div>
        </div>
        
        <div className="question-container">
          <div className="question-meta">
            <span className="blooms-level">Bloom's Level: {currentQuestion.blooms_level}</span>
            <span className="difficulty">Difficulty: {getDifficultyLabel(currentQuestion.difficulty)}</span>
          </div>
          
          <div className="question-text">
            <h3>{currentQuestion.text}</h3>
          </div>
          
          <div className="answer-options">
            {currentQuestion.options.map((option, index) => (
              <label key={index} className="option-label">
                <input
                  type="radio"
                  name="answer"
                  value={String.fromCharCode(65 + index)} // A, B, C, D
                  checked={selectedAnswer === String.fromCharCode(65 + index)}
                  onChange={(e) => setSelectedAnswer(e.target.value)}
                  disabled={showFeedback}
                />
                <span className="option-text">{String.fromCharCode(65 + index)}. {option}</span>
              </label>
            ))}
          </div>
          
          {showFeedback && feedback && (
            <div className={`feedback ${feedback.is_correct ? 'correct' : 'incorrect'}`}>
              <div className="feedback-header">
                <span className="feedback-icon">
                  {feedback.is_correct ? '✓' : '✗'}
                </span>
                <span className="feedback-message">
                  {feedback.is_correct ? 'Correct!' : 'Incorrect'}
                </span>
              </div>
              
              {feedback.explanation && (
                <div className="feedback-explanation">
                  <p>{feedback.explanation}</p>
                </div>
              )}
              
              {feedback.performance_insight && (
                <div className="performance-insight">
                  <p><strong>Insight:</strong> {feedback.performance_insight}</p>
                </div>
              )}
              
              <button className="next-btn" onClick={nextQuestion}>
                {currentQuestionIndex + 1 < currentQuiz.questions.length ? 'Next Question' : 'Complete Quiz'}
              </button>
            </div>
          )}
          
          {!showFeedback && (
            <div className="question-actions">
              <button 
                className="submit-btn"
                onClick={submitAnswer}
                disabled={!selectedAnswer || loading}
              >
                {loading ? 'Processing...' : 'Submit Answer'}
              </button>
            </div>
          )}
        </div>
      </div>
    );
  };

  const renderQuizResults = () => (
    <div className="quiz-results">
      <h2>Quiz Results</h2>
      
      <div className="results-summary">
        <div className="score-display">
          <div className="score-circle">
            <span className="score-value">{Math.round(quizResults.summary.score)}%</span>
          </div>
          <div className="score-details">
            <p>{quizResults.summary.correctAnswers} out of {quizResults.summary.totalQuestions} correct</p>
            <p className={quizResults.summary.isPassed ? 'passed' : 'failed'}>
              {quizResults.summary.isPassed ? 'Passed' : 'Failed'}
            </p>
          </div>
        </div>
        
        <div className="performance-metrics">
          <div className="metric">
            <label>Time Taken:</label>
            <span>{Math.floor(quizResults.summary.totalTime / 60)}m {quizResults.summary.totalTime % 60}s</span>
          </div>
          <div className="metric">
            <label>Ability Change:</label>
            <span className={quizResults.summary.abilityChange >= 0 ? 'positive' : 'negative'}>
              {quizResults.summary.abilityChange >= 0 ? '+' : ''}{quizResults.summary.abilityChange.toFixed(2)}
            </span>
          </div>
        </div>
      </div>
      
      {quizResults.analysis && (
        <div className="detailed-analysis">
          <h3>Performance Analysis</h3>
          
          {quizResults.analysis.blooms_analysis && (
            <div className="blooms-analysis">
              <h4>Bloom's Taxonomy Performance</h4>
              <div className="blooms-breakdown">
                {Object.entries(quizResults.analysis.blooms_analysis).map(([level, score]) => (
                  <div key={level} className="blooms-item">
                    <span className="level-name">{level}</span>
                    <div className="score-bar">
                      <div 
                        className="score-fill"
                        style={{ width: `${score * 100}%` }}
                      ></div>
                    </div>
                    <span className="score-text">{Math.round(score * 100)}%</span>
                  </div>
                ))}
              </div>
            </div>
          )}
          
          {quizResults.analysis.recommendations && (
            <div className="recommendations">
              <h4>Recommendations</h4>
              <ul>
                {quizResults.analysis.recommendations.map((rec, index) => (
                  <li key={index}>{rec}</li>
                ))}
              </ul>
            </div>
          )}
          
          {quizResults.analysis.next_steps && (
            <div className="next-steps">
              <h4>Next Steps</h4>
              <ul>
                {quizResults.analysis.next_steps.map((step, index) => (
                  <li key={index}>{step}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
      
      <div className="results-actions">
        <button className="retry-btn" onClick={resetQuiz}>
          Take Another Quiz
        </button>
      </div>
    </div>
  );

  const getAbilityClass = (ability) => {
    if (ability >= 2) return 'advanced';
    if (ability >= 1) return 'proficient';
    if (ability >= 0) return 'developing';
    if (ability >= -1) return 'beginning';
    return 'needs-support';
  };

  const getAbilityLabel = (ability) => {
    if (ability >= 2) return 'Advanced';
    if (ability >= 1) return 'Proficient';
    if (ability >= 0) return 'Developing';
    if (ability >= -1) return 'Beginning';
    return 'Needs Support';
  };

  const getDifficultyLabel = (difficulty) => {
    if (difficulty < -1) return 'Easy';
    if (difficulty > 1) return 'Hard';
    return 'Medium';
  };

  if (loading && !currentQuiz) {
    return <LoadingSpinner message="Generating adaptive quiz..." />;
  }

  return (
    <div className="adaptive-quiz-container">
      {quizState === 'setup' && renderQuizSetup()}
      {quizState === 'active' && renderActiveQuiz()}
      {quizState === 'completed' && renderQuizResults()}
      
      {toast && (
        <Toast
          type={toast.type}
          message={toast.message}
          onClose={() => setToast(null)}
        />
      )}
    </div>
  );
};

export default AdaptiveQuiz;