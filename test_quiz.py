#!/usr/bin/env python3

import os
import sys
sys.path.append('ai-service/src')

from services.openai_service import OpenAIService
from controllers.prediction_controller import PredictionController

def test_quiz_generation():
    """Test quiz generation with ChatGPT"""
    
    # Check if API key is set
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key == 'sk-your-actual-openai-api-key-here':
        print("❌ OpenAI API key not configured!")
        print("Please set your OpenAI API key in ai-service/.env file")
        print("Replace 'sk-your-actual-openai-api-key-here' with your actual API key")
        return False
    
    try:
        # Test OpenAI service
        openai_service = OpenAIService()
        if not openai_service.is_available():
            print("❌ OpenAI service not available")
            return False
        
        print("✅ OpenAI service initialized")
        
        # Test quiz generation
        controller = PredictionController()
        result = controller.generate_quiz("Mathematics", 2, "medium")
        
        print("✅ Quiz generated successfully!")
        print(f"Generated {len(result['questions'])} questions")
        
        for i, q in enumerate(result['questions'], 1):
            print(f"\nQuestion {i}: {q['question']}")
            for j, option in enumerate(q['options']):
                print(f"  {chr(65+j)}) {option}")
            print(f"Answer: {q['answer']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv('ai-service/.env')
    
    print("Testing ChatGPT Quiz Generation...")
    test_quiz_generation()