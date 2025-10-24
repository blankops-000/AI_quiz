import React from 'react';

const ResultDisplay = ({ result, type }) => {
  if (!result) return null;

  const renderContent = () => {
    switch (type) {
      case 'sentiment':
        return (
          <div className="sentiment-result">
            <div className="sentiment-badge">
              <span className={`sentiment ${result.sentiment}`}>
                {result.sentiment?.toUpperCase()}
              </span>
              {result.score && (
                <span className="score">Score: {result.score.toFixed(2)}</span>
              )}
            </div>
          </div>
        );

      case 'text-analysis':
        return (
          <div className="analysis-result">
            {result.sentiment && (
              <div className="metric">
                <strong>Sentiment:</strong> {result.sentiment} 
                {result.confidence && ` (${(result.confidence * 100).toFixed(1)}%)`}
              </div>
            )}
            {result.word_count && (
              <div className="metric">
                <strong>Word Count:</strong> {result.word_count}
              </div>
            )}
            {result.keywords && (
              <div className="metric">
                <strong>Keywords:</strong> {result.keywords.join(', ')}
              </div>
            )}
          </div>
        );

      case 'quiz':
        return (
          <div className="quiz-result">
            <div className="quiz-info">
              <strong>Topic:</strong> {result.topic} | 
              <strong>Difficulty:</strong> {result.difficulty}
            </div>
            {result.questions && (
              <div className="questions-preview">
                <p>{result.questions.length} questions generated</p>
              </div>
            )}
          </div>
        );

      case 'text-generation':
        return (
          <div className="generated-text">
            <div className="text-content">
              {result.text}
            </div>
            <div className="text-meta">
              <small>Length: {result.length} words</small>
            </div>
          </div>
        );

      default:
        return <pre>{JSON.stringify(result, null, 2)}</pre>;
    }
  };

  return (
    <div className="result-display">
      <div className="result-content">
        {renderContent()}
        {result.note && (
          <div className="result-note">
            <small>{result.note}</small>
          </div>
        )}
      </div>
    </div>
  );
};

export default ResultDisplay;