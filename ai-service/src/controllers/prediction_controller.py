import logging
import random
from services.huggingface_service import HuggingFaceService
from services.openai_service import OpenAIService
from models.recommendation_model import RecommendationModel

logger = logging.getLogger(__name__)

class PredictionController:
    def __init__(self):
        self.hf_service = HuggingFaceService()
        self.openai_service = OpenAIService()
        self.recommendation_model = RecommendationModel()
    
    def generate_text(self, prompt, max_length=100, temperature=0.7):
        """Generate text based on prompt"""
        try:
            # Try OpenAI first, fallback to HuggingFace
            try:
                result = self.openai_service.generate_text(prompt, max_length, temperature)
            except:
                result = self.hf_service.generate_text(prompt, max_length, temperature)
            
            return {
                'generated_text': result,
                'prompt': prompt,
                'parameters': {
                    'max_length': max_length,
                    'temperature': temperature
                }
            }
            
        except Exception as e:
            logger.error(f"Text generation failed: {str(e)}")
            raise
    
    def generate_quiz(self, topic, num_questions=5, difficulty='medium'):
        """Generate quiz questions based on topic"""
        try:
            questions = []
            
            for i in range(num_questions):
                try:
                    question_text = self.openai_service.generate_quiz_question(topic, difficulty)
                    parsed_question = self._parse_question(question_text, i + 1)
                except Exception as e:
                    logger.warning(f"AI generation failed for question {i+1}: {str(e)}")
                    parsed_question = {
                        'question': f"Sample {topic} question?",
                        'options': ["A", "B", "C", "D"],
                        'answer': 'A'
                    }
                
                questions.append(parsed_question)
            
            return {
                'questions': questions
            }
            
        except Exception as e:
            logger.error(f"Quiz generation failed: {str(e)}")
            raise
    
    def get_recommendations(self, user_id, preferences=None, limit=10):
        """Get personalized recommendations for user"""
        try:
            if preferences is None:
                preferences = {}
            
            # Use recommendation model to generate suggestions
            recommendations = self.recommendation_model.get_recommendations(
                user_id, preferences, limit
            )
            
            return {
                'user_id': user_id,
                'preferences': preferences,
                'recommendations': recommendations,
                'total_count': len(recommendations)
            }
            
        except Exception as e:
            logger.error(f"Recommendations failed: {str(e)}")
            raise
    
    def _generate_fallback_question(self, topic, difficulty, question_num):
        """Generate fallback question when AI services are unavailable"""
        templates = {
            'easy': [
                f"What is a basic concept related to {topic}?",
                f"Which of the following is associated with {topic}?",
                f"What is the main purpose of {topic}?"
            ],
            'medium': [
                f"How does {topic} relate to modern applications?",
                f"What are the key principles of {topic}?",
                f"Which approach is most effective for {topic}?"
            ],
            'hard': [
                f"What are the advanced implications of {topic}?",
                f"How would you optimize {topic} for complex scenarios?",
                f"What are the theoretical foundations of {topic}?"
            ]
        }
        
        question_templates = templates.get(difficulty, templates['medium'])
        question = random.choice(question_templates)
        
        # Generate sample options
        options = [
            f"Option A related to {topic}",
            f"Option B about {topic}",
            f"Option C concerning {topic}",
            f"Option D regarding {topic}"
        ]
        
        return f"{question}\nA) {options[0]}\nB) {options[1]}\nC) {options[2]}\nD) {options[3]}\nCorrect Answer: A"
    
    def _parse_question(self, question_text, question_num):
        """Parse generated question text into structured format"""
        try:
            lines = [line.strip() for line in question_text.strip().split('\n') if line.strip()]
            
            question = ""
            options = []
            correct_answer = 'A'
            explanation = ""
            
            for line in lines:
                if line.startswith('Question:'):
                    question = line.replace('Question:', '').strip()
                elif line.startswith(('A)', 'B)', 'C)', 'D)')):
                    option_id = line[0]
                    option_text = line[2:].strip() if line[1] == ')' else line[3:].strip()
                    options.append(option_text)
                elif line.lower().startswith('correct answer:'):
                    answer_part = line.split(':', 1)[1].strip().upper()
                    correct_answer = answer_part[0] if answer_part else 'A'
                elif line.lower().startswith('explanation:'):
                    explanation = line.split(':', 1)[1].strip()
            
            # Fallback if parsing fails
            if not question:
                question = f"What is an important concept in the given topic?"
            if len(options) < 4:
                options = ["Option A", "Option B", "Option C", "Option D"]
            if not explanation:
                explanation = "This tests knowledge of the topic."
            
            return {
                'question': question,
                'options': options[:4],
                'answer': correct_answer
            }
            
        except Exception as e:
            logger.error(f"Question parsing failed: {str(e)}")
            return {
                'question': f"Sample Mathematics question?",
                'options': ["A", "B", "C", "D"],
                'answer': 'A'
            }