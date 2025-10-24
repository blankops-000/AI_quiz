import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv('ai-service/.env')

# Add the ai-service/src to path
sys.path.append('ai-service/src')

try:
    from services.openai_service import OpenAIService
    
    print("Testing OpenAI connection...")
    
    api_key = os.getenv('OPENAI_API_KEY')
    print(f"API Key configured: {'Yes' if api_key and not api_key.startswith('sk-proj-placeholder') else 'No'}")
    
    if api_key and not api_key.startswith('sk-proj-placeholder'):
        service = OpenAIService()
        if service.is_available():
            print("✅ OpenAI service is available")
            
            # Test quiz generation
            result = service.generate_quiz_question("Mathematics", "medium")
            print("✅ Quiz generation test:")
            print(result[:200] + "..." if len(result) > 200 else result)
        else:
            print("❌ OpenAI service not available")
    else:
        print("❌ OpenAI API key not properly configured")
        
except Exception as e:
    print(f"❌ Error: {str(e)}")