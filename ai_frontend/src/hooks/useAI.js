// ============================================
// FILE: src/hooks/useAI.js
// ============================================
import { useState } from 'react';
import aiService from '../services/aiService';

const useAI = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  const processRequest = async (requestData) => {
    try {
      setLoading(true);
      setError(null);
      const response = await aiService.processRequest(requestData);
      setResult(response.data);
      return response;
    } catch (err) {
      setError(err.message || 'AI request failed');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const textGeneration = async (prompt, options) => {
    return await processRequest({
      requestType: 'text-generation',
      input: { prompt, ...options }
    });
  };

  const imageAnalysis = async (imageUrl, analysisType) => {
    return await processRequest({
      requestType: 'image-analysis',
      input: { imageUrl, analysisType }
    });
  };

  const reset = () => {
    setResult(null);
    setError(null);
    setLoading(false);
  };

  return {
    loading,
    error,
    result,
    processRequest,
    textGeneration,
    imageAnalysis,
    reset
  };
};

export default useAI;