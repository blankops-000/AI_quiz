// ============================================
// FILE: src/pages/AIAssistant.jsx
// ============================================
import React, { useState, useEffect } from 'react';
import aiService from '../services/aiService';
import authService from '../services/authService';
import LoginPrompt from '../components/common/LoginPrompt';
import LoadingSpinner from '../components/common/LoadingSpinner';
import QuizDisplay from '../components/ai/QuizDisplay';
import ResultDisplay from '../components/ai/ResultDisplay';
import '../components/ai/AIAssistant.css';

const AIAssistant = () => {
  const [activeTab, setActiveTab] = useState('text-analysis');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  
  // Text Analysis State
  const [textInput, setTextInput] = useState('');

  // Quiz Generation State
  const [quizTopic, setQuizTopic] = useState('');
  const [numQuestions, setNumQuestions] = useState(5);
  const [difficulty, setDifficulty] = useState('medium');

  // Text Generation State
  const [prompt, setPrompt] = useState('');
  const [maxLength, setMaxLength] = useState(100);
  const [temperature, setTemperature] = useState(0.7);

  useEffect(() => {
    setIsAuthenticated(authService.isAuthenticated());
  }, []);

  if (!isAuthenticated) {
    return <LoginPrompt message="Please login to access AI features" />;
  }

  const handleTextAnalysis = async () => {
    if (!textInput.trim()) {
      setError('Please enter some text to analyze');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await aiService.analyzeText(textInput);
      setResult(response.data);
    } catch (err) {
      setError(err.message || 'Text analysis failed');
    } finally {
      setLoading(false);
    }
  };

  const handleSentimentAnalysis = async () => {
    if (!textInput.trim()) {
      setError('Please enter some text to analyze');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await aiService.analyzeSentiment(textInput);
      setResult(response.data);
    } catch (err) {
      setError(err.message || 'Sentiment analysis failed');
    } finally {
      setLoading(false);
    }
  };

  const handleQuizGeneration = async () => {
    if (!quizTopic.trim()) {
      setError('Please enter a topic for the quiz');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await aiService.generateQuiz(quizTopic, {
        numQuestions,
        difficulty
      });
      setResult(response.data);
    } catch (err) {
      setError(err.message || 'Quiz generation failed');
    } finally {
      setLoading(false);
    }
  };

  const handleTextGeneration = async () => {
    if (!prompt.trim()) {
      setError('Please enter a prompt for text generation');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await aiService.generateText(prompt, {
        maxLength,
        temperature
      });
      setResult(response.data);
    } catch (err) {
      setError(err.message || 'Text generation failed');
    } finally {
      setLoading(false);
    }
  };

  const renderTabContent = () => {
    switch (activeTab) {
      case 'text-analysis':
        return (
          <div className="tab-content">
            <h3>Text Analysis</h3>
            <div className="input-group">
              <label>Enter text to analyze:</label>
              <textarea
                value={textInput}
                onChange={(e) => setTextInput(e.target.value)}
                placeholder="Enter your text here..."
                rows={6}
                className="text-input"
              />
            </div>
            <div className="button-group">
              <button 
                onClick={handleTextAnalysis}
                disabled={loading}
                className="btn btn-primary"
              >
                {loading ? 'Analyzing...' : 'Analyze Text'}
              </button>
              <button 
                onClick={handleSentimentAnalysis}
                disabled={loading}
                className="btn btn-secondary"
              >
                {loading ? 'Analyzing...' : 'Analyze Sentiment'}
              </button>
            </div>
          </div>
        );

      case 'quiz-generation':
        return (
          <div className="tab-content">
            <h3>Quiz Generation</h3>
            <div className="input-group">
              <label>Topic:</label>
              <select
                value={quizTopic}
                onChange={(e) => setQuizTopic(e.target.value)}
                className="select-input"
              >
                <option value="">Select a topic...</option>
                <option value="Science">Science</option>
                <option value="History">History</option>
                <option value="Mathematics">Mathematics</option>
                <option value="Geography">Geography</option>
                <option value="Literature">Literature</option>
                <option value="Technology">Technology</option>
                <option value="Sports">Sports</option>
                <option value="Art">Art</option>
                <option value="Music">Music</option>
                <option value="General Knowledge">General Knowledge</option>
              </select>
            </div>
            <div className="input-row">
              <div className="input-group">
                <label>Number of Questions:</label>
                <select
                  value={numQuestions}
                  onChange={(e) => setNumQuestions(parseInt(e.target.value))}
                  className="select-input"
                >
                  {[1, 2, 3, 4, 5, 10, 15, 20].map(num => (
                    <option key={num} value={num}>{num}</option>
                  ))}
                </select>
              </div>
              <div className="input-group">
                <label>Difficulty:</label>
                <select
                  value={difficulty}
                  onChange={(e) => setDifficulty(e.target.value)}
                  className="select-input"
                >
                  <option value="easy">Easy</option>
                  <option value="medium">Medium</option>
                  <option value="hard">Hard</option>
                </select>
              </div>
            </div>
            <button 
              onClick={handleQuizGeneration}
              disabled={loading}
              className="btn btn-primary"
            >
              {loading ? 'Generating...' : 'Generate Quiz'}
            </button>
          </div>
        );

      case 'text-generation':
        return (
          <div className="tab-content">
            <h3>Text Generation</h3>
            <div className="input-group">
              <label>Prompt:</label>
              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Enter your prompt here..."
                rows={4}
                className="text-input"
              />
            </div>
            <div className="input-row">
              <div className="input-group">
                <label>Max Length:</label>
                <input
                  type="number"
                  value={maxLength}
                  onChange={(e) => setMaxLength(parseInt(e.target.value))}
                  min="10"
                  max="500"
                  className="number-input"
                />
              </div>
              <div className="input-group">
                <label>Temperature:</label>
                <input
                  type="number"
                  value={temperature}
                  onChange={(e) => setTemperature(parseFloat(e.target.value))}
                  min="0.1"
                  max="1.0"
                  step="0.1"
                  className="number-input"
                />
              </div>
            </div>
            <button 
              onClick={handleTextGeneration}
              disabled={loading}
              className="btn btn-primary"
            >
              {loading ? 'Generating...' : 'Generate Text'}
            </button>
          </div>
        );

      default:
        return null;
    }
  };

  const renderResult = () => {
    if (!result) return null;

    // Special handling for quiz results
    if (activeTab === 'quiz-generation' && result.questions) {
      return (
        <div className="result-section">
          <h4>Generated Quiz:</h4>
          <QuizDisplay quizData={result} />
        </div>
      );
    }

    return (
      <div className="result-section">
        <h4>Result:</h4>
        <ResultDisplay result={result} type={activeTab} />
      </div>
    );
  };

  return (
    <div className="ai-assistant-page">
      <div className="container">
        <h1>AI Assistant</h1>
        
        <div className="tabs">
          <button
            className={`tab ${activeTab === 'text-analysis' ? 'active' : ''}`}
            onClick={() => setActiveTab('text-analysis')}
          >
            Text Analysis
          </button>
          <button
            className={`tab ${activeTab === 'quiz-generation' ? 'active' : ''}`}
            onClick={() => setActiveTab('quiz-generation')}
          >
            Quiz Generation
          </button>
          <button
            className={`tab ${activeTab === 'text-generation' ? 'active' : ''}`}
            onClick={() => setActiveTab('text-generation')}
          >
            Text Generation
          </button>
        </div>

        <div className="content">
          {renderTabContent()}
          
          {error && (
            <div className="error-message">
              <p>{error}</p>
            </div>
          )}
          
          {renderResult()}
        </div>
      </div>
    </div>
  );
};

export default AIAssistant;