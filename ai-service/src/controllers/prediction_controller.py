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
                # Generate question using AI
                prompt = f"Generate a {difficulty} difficulty multiple choice question about {topic}. Include 4 options (A, B, C, D) and indicate the correct answer."
                
                try:
                    question_text = self.openai_service.generate_quiz_question(topic, difficulty)
                except:
                    # Fallback to template-based generation
                    question_text = self._generate_fallback_question(topic, difficulty, i + 1)
                
                # Parse the generated question
                parsed_question = self._parse_question(question_text, i + 1)
                questions.append(parsed_question)
            
            return {
                'topic': topic,
                'difficulty': difficulty,
                'total_questions': num_questions,
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
            lines = question_text.strip().split('\n')
            
            # Extract question
            question = lines[0] if lines else f"Question {question_num} about the topic"
            
            # Extract options
            options = []
            correct_answer = 'A'
            
            for line in lines[1:]:
                line = line.strip()
                if line.startswith(('A)', 'B)', 'C)', 'D)')):
                    options.append({
                        'id': line[0],
                        'text': line[3:].strip()
                    })
                elif line.lower().startswith('correct answer:'):
                    correct_answer = line.split(':')[1].strip().upper()
            
            # Ensure we have 4 options
            while len(options) < 4:
                option_id = chr(65 + len(options))  # A, B, C, D
                options.append({
                    'id': option_id,
                    'text': f"Option {option_id}"
                })
            
            return {
                'id': question_num,
                'question': question,
                'options': options[:4],
                'correct_answer': correct_answer,
                'explanation': f"This question tests knowledge about the given topic."
            }
            
        except Exception as e:
            logger.error(f"Question parsing failed: {str(e)}")
            return {
                'id': question_num,
                'question': f"Sample question {question_num}",
                'options': [
                    {'id': 'A', 'text': 'Option A'},
                    {'id': 'B', 'text': 'Option B'},
                    {'id': 'C', 'text': 'Option C'},
                    {'id': 'D', 'text': 'Option D'}
                ],
                'correct_answer': 'A',
                'explanation': 'Sample explanation'
            }