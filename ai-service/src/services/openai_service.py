import os
import logging
import openai
from config.ai_config import AI_CONFIG

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize OpenAI client"""
        try:
            if self.api_key:
                openai.api_key = self.api_key
                self.client = openai
                logger.info("OpenAI client initialized successfully")
            else:
                logger.warning("OpenAI API key not found. OpenAI services will be unavailable.")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {str(e)}")
    
    def generate_text(self, prompt, max_length=100, temperature=0.7):
        """Generate text using OpenAI GPT"""
        try:
            if not self.client or not self.api_key:
                raise Exception("OpenAI client not available")
            
            response = self.client.Completion.create(
                engine=AI_CONFIG['openai']['text_model'],
                prompt=prompt,
                max_tokens=max_length,
                temperature=temperature,
                n=1,
                stop=None
            )
            
            return response.choices[0].text.strip()
            
        except Exception as e:
            logger.error(f"OpenAI text generation failed: {str(e)}")
            raise
    
    def generate_quiz_question(self, topic, difficulty='medium'):
        """Generate quiz question using OpenAI"""
        try:
            if not self.client or not self.api_key:
                raise Exception("OpenAI client not available")
            
            prompt = f"""Generate a {difficulty} difficulty multiple choice question about {topic}.
            
Format the response as:
Question: [Your question here]
A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]
Correct Answer: [A/B/C/D]
Explanation: [Brief explanation]

Topic: {topic}
Difficulty: {difficulty}"""
            
            response = self.client.Completion.create(
                engine=AI_CONFIG['openai']['text_model'],
                prompt=prompt,
                max_tokens=300,
                temperature=0.7,
                n=1,
                stop=None
            )
            
            return response.choices[0].text.strip()
            
        except Exception as e:
            logger.error(f"OpenAI quiz generation failed: {str(e)}")
            raise
    
    def analyze_text_with_gpt(self, text, analysis_type='general'):
        """Analyze text using OpenAI GPT"""
        try:
            if not self.client or not self.api_key:
                raise Exception("OpenAI client not available")
            
            prompts = {
                'general': f"Analyze the following text and provide insights about its content, tone, and key themes:\n\n{text}",
                'sentiment': f"Analyze the sentiment of the following text. Classify it as positive, negative, or neutral and explain why:\n\n{text}",
                'summary': f"Provide a concise summary of the following text:\n\n{text}",
                'keywords': f"Extract the main keywords and key phrases from the following text:\n\n{text}"
            }
            
            prompt = prompts.get(analysis_type, prompts['general'])
            
            response = self.client.Completion.create(
                engine=AI_CONFIG['openai']['text_model'],
                prompt=prompt,
                max_tokens=200,
                temperature=0.3,
                n=1,
                stop=None
            )
            
            return response.choices[0].text.strip()
            
        except Exception as e:
            logger.error(f"OpenAI text analysis failed: {str(e)}")
            raise
    
    def generate_recommendations(self, user_preferences, context='general'):
        """Generate recommendations using OpenAI"""
        try:
            if not self.client or not self.api_key:
                raise Exception("OpenAI client not available")
            
            prompt = f"""Based on the following user preferences, generate 5 personalized recommendations:

User Preferences: {user_preferences}
Context: {context}

Please provide recommendations in the following format:
1. [Recommendation 1] - [Brief explanation]
2. [Recommendation 2] - [Brief explanation]
3. [Recommendation 3] - [Brief explanation]
4. [Recommendation 4] - [Brief explanation]
5. [Recommendation 5] - [Brief explanation]"""
            
            response = self.client.Completion.create(
                engine=AI_CONFIG['openai']['text_model'],
                prompt=prompt,
                max_tokens=400,
                temperature=0.7,
                n=1,
                stop=None
            )
            
            return response.choices[0].text.strip()
            
        except Exception as e:
            logger.error(f"OpenAI recommendations failed: {str(e)}")
            raise
    
    def is_available(self):
        """Check if OpenAI service is available"""
        return self.client is not None and self.api_key is not None