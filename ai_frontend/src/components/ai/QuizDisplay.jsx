import React, { useState } from 'react';

const QuizDisplay = ({ quizData }) => {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [showResults, setShowResults] = useState(false);

  if (!quizData?.questions) return null;

  const questions = quizData.questions;

  const handleAnswerSelect = (questionIndex, answer) => {
    setSelectedAnswers(prev => ({
      ...prev,
      [questionIndex]: answer
    }));
  };

  const calculateScore = () => {
    let correct = 0;
    questions.forEach((q, index) => {
      if (selectedAnswers[index] === q.answer) correct++;
    });
    return correct;
  };

  const nextQuestion = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    } else {
      setShowResults(true);
    }
  };

  if (showResults) {
    const score = calculateScore();
    const percentage = Math.round((score / questions.length) * 100);
    
    return (
      <div className="quiz-results">
        <h3>Quiz Complete!</h3>
        <div className="score-display">
          <div className="score-circle">
            <span className="score">{score}/{questions.length}</span>
            <span className="percentage">{percentage}%</span>
          </div>
        </div>
        <button onClick={() => {
          setCurrentQuestion(0);
          setSelectedAnswers({});
          setShowResults(false);
        }} className="btn btn-primary">
          Retake Quiz
        </button>
      </div>
    );
  }

  const question = questions[currentQuestion];

  return (
    <div className="quiz-display">
      <div className="quiz-header">
        <h4>Question {currentQuestion + 1} of {questions.length}</h4>
        <div className="progress-bar">
          <div 
            className="progress-fill" 
            style={{ width: `${((currentQuestion + 1) / questions.length) * 100}%` }}
          ></div>
        </div>
      </div>
      
      <div className="question-content">
        <h3>{question.question}</h3>
        <div className="options">
          {question.options.map((option, index) => (
            <button
              key={index}
              className={`option-btn ${selectedAnswers[currentQuestion] === option ? 'selected' : ''}`}
              onClick={() => handleAnswerSelect(currentQuestion, option)}
            >
              {option}
            </button>
          ))}
        </div>
      </div>

      <div className="quiz-controls">
        <button 
          onClick={nextQuestion}
          disabled={!selectedAnswers[currentQuestion]}
          className="btn btn-primary"
        >
          {currentQuestion === questions.length - 1 ? 'Finish Quiz' : 'Next Question'}
        </button>
      </div>
    </div>
  );
};

export default QuizDisplay;