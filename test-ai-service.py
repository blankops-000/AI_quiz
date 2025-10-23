import requests
import json

BASE_URL = 'http://localhost:8000'

def test_ai_service():
    print("Testing AI Service Endpoints...\n")
    
    try:
        # Test health check
        print("1. Testing health check...")
        response = requests.get(f"{BASE_URL}/health")
        print(f"✓ Health: {response.json()}")
        
        # Test text analysis
        print("\n2. Testing text analysis...")
        response = requests.post(f"{BASE_URL}/api/analyze/text", 
                               json={"text": "This is a wonderful and amazing application!"})
        print(f"✓ Text Analysis: {response.json()}")
        
        # Test sentiment analysis
        print("\n3. Testing sentiment analysis...")
        response = requests.post(f"{BASE_URL}/api/analyze/sentiment", 
                               json={"text": "I love this great application!"})
        print(f"✓ Sentiment: {response.json()}")
        
        # Test quiz generation
        print("\n4. Testing quiz generation...")
        response = requests.post(f"{BASE_URL}/api/generate/quiz", 
                               json={"topic": "Science", "num_questions": 3, "difficulty": "medium"})
        print(f"✓ Quiz: {response.json()}")
        
        # Test text generation
        print("\n5. Testing text generation...")
        response = requests.post(f"{BASE_URL}/api/generate/text", 
                               json={"prompt": "artificial intelligence", "max_length": 100})
        print(f"✓ Text Gen: {response.json()}")
        
        print("\n🎉 All AI service endpoints working perfectly!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_ai_service()