"""
Adaptive Quiz Controller - Handles adaptive quiz generation and management
Integrates with Pedagogical Engine for IRT-based question selection
"""

from flask import request, jsonify
import logging
from typing import Dict, List, Optional
from services.pedagogical_engine import PedagogicalEngine, Question, StudentProfile, BloomsLevel
from services.openai_service import OpenAIService
import json
import random

logger = logging.getLogger(__name__)

class AdaptiveQuizController:
    def __init__(self):
        self.pedagogical_engine = PedagogicalEngine()
        self.openai_service = OpenAIService()
        
    def generate_adaptive_quiz(self, data: Dict) -> Dict:
        """
        Generate an adaptive quiz based on student profile and requirements
        """
        try:
            # Extract parameters
            user_id = data.get('user_id')
            subject = data.get('subject', 'Computer Science')
            topic = data.get('topic', 'Algorithms and Data Structures')
            difficulty_level = data.get('difficulty', 'medium')
            num_questions = data.get('num_questions', 10)
            target_blooms_levels = data.get('target_blooms_levels', [])
            
            # Get or create student profile
            student_profile = self._get_student_profile(user_id, data.get('student_profile', {}))
            
            # Generate question pool using AI
            question_pool = self._generate_question_pool(subject, topic, difficulty_level, num_questions * 2)
            
            # Convert target Bloom's levels
            blooms_distribution = self._parse_blooms_distribution(target_blooms_levels)
            
            # Generate adaptive quiz
            selected_questions = self.pedagogical_engine.generate_adaptive_quiz(
                student_profile=student_profile,
                question_pool=question_pool,
                target_questions=num_questions,
                target_blooms_distribution=blooms_distribution
            )
            
            # Format response
            quiz_data = {
                'quiz_id': f"adaptive_{user_id}_{random.randint(1000, 9999)}",
                'title': f"Adaptive Quiz: {topic}",
                'subject': subject,
                'topic': topic,
                'is_adaptive': True,
                'total_questions': len(selected_questions),
                'estimated_time': len(selected_questions) * 2,  # 2 minutes per question
                'questions': [self._format_question(q, i) for i, q in enumerate(selected_questions)],
                'student_profile': {
                    'current_ability': student_profile.ability_level,
                    'blooms_progress': {level.name.lower(): progress 
                                     for level, progress in student_profile.blooms_progress.items()},
                    'learning_style': student_profile.learning_style
                },
                'adaptive_settings': {
                    'initial_difficulty': difficulty_level,
                    'adaptation_enabled': True,
                    'blooms_progression': True
                }
            }
            
            return {
                'success': True,
                'data': quiz_data,
                'message': 'Adaptive quiz generated successfully'
            }
            
        except Exception as e:
            logger.error(f"Error generating adaptive quiz: {str(e)}")
            return {
                'success': False,
                'message': f'Failed to generate adaptive quiz: {str(e)}'
            }
    
    def process_quiz_response(self, data: Dict) -> Dict:
        """
        Process a student's response and adapt the quiz accordingly
        """
        try:
            user_id = data.get('user_id')
            quiz_id = data.get('quiz_id')
            question_id = data.get('question_id')
            user_answer = data.get('answer')
            response_time = data.get('response_time', 0)
            
            # Get current question and student profile
            question = self._get_question_by_id(question_id)
            student_profile = self._get_student_profile(user_id)
            
            if not question or not student_profile:
                return {
                    'success': False,
                    'message': 'Question or student profile not found'
                }
            
            # Evaluate response
            is_correct = self._evaluate_response(question, user_answer)
            
            # Update student profile
            self.pedagogical_engine.update_student_profile(
                student_profile, question, is_correct, response_time
            )
            
            # Calculate feedback
            feedback = self._generate_response_feedback(question, is_correct, user_answer)
            
            # Determine next question (if adaptive)
            next_question = None
            if data.get('is_adaptive', True):
                remaining_questions = data.get('remaining_questions', [])
                if remaining_questions:
                    question_pool = [self._parse_question(q) for q in remaining_questions]
                    next_question = self.pedagogical_engine.select_next_question(
                        student_profile, question_pool
                    )
            
            response_data = {
                'question_id': question_id,
                'is_correct': is_correct,
                'correct_answer': question.correct_answer,
                'explanation': feedback.get('explanation', ''),
                'feedback': feedback,
                'updated_ability': student_profile.ability_level,
                'blooms_progress': {level.name.lower(): progress 
                                 for level, progress in student_profile.blooms_progress.items()},
                'next_question': self._format_question(next_question, 0) if next_question else None,
                'performance_insight': self._generate_performance_insight(student_profile, is_correct)
            }
            
            return {
                'success': True,
                'data': response_data,
                'message': 'Response processed successfully'
            }
            
        except Exception as e:
            logger.error(f"Error processing quiz response: {str(e)}")
            return {
                'success': False,
                'message': f'Failed to process response: {str(e)}'
            }
    
    def analyze_quiz_performance(self, data: Dict) -> Dict:
        """
        Analyze overall quiz performance and provide detailed insights
        """
        try:
            user_id = data.get('user_id')
            quiz_responses = data.get('responses', [])
            
            if not quiz_responses:
                return {
                    'success': False,
                    'message': 'No responses provided for analysis'
                }
            
            # Convert responses to analysis format
            analysis_responses = []
            for response in quiz_responses:
                question = self._parse_question(response.get('question', {}))
                is_correct = response.get('is_correct', False)
                response_time = response.get('response_time', 0)
                analysis_responses.append((question, is_correct, response_time))
            
            # Perform analysis
            performance_analysis = self.pedagogical_engine.analyze_performance(analysis_responses)
            
            # Generate recommendations
            recommendations = self._generate_learning_recommendations(performance_analysis)
            
            # Create detailed report
            analysis_report = {
                'user_id': user_id,
                'quiz_summary': {
                    'total_questions': performance_analysis.get('total_questions', 0),
                    'correct_answers': performance_analysis.get('correct_answers', 0),
                    'accuracy': performance_analysis.get('accuracy', 0),
                    'performance_level': performance_analysis.get('performance_level', 'unknown')
                },
                'irt_analysis': {
                    'estimated_ability': performance_analysis.get('estimated_ability', 0),
                    'standard_error': performance_analysis.get('ability_standard_error', 1),
                    'ability_level': self._classify_ability_level(performance_analysis.get('estimated_ability', 0))
                },
                'blooms_analysis': performance_analysis.get('blooms_performance', {}),
                'difficulty_analysis': {
                    'average_difficulty': performance_analysis.get('average_difficulty', 0),
                    'difficulty_range': self._analyze_difficulty_range(quiz_responses)
                },
                'time_analysis': {
                    'average_response_time': performance_analysis.get('average_response_time', 0),
                    'time_efficiency': self._analyze_time_efficiency(quiz_responses)
                },
                'recommendations': recommendations,
                'next_steps': self._generate_next_steps(performance_analysis)
            }
            
            return {
                'success': True,
                'data': analysis_report,
                'message': 'Performance analysis completed'
            }
            
        except Exception as e:
            logger.error(f"Error analyzing quiz performance: {str(e)}")
            return {
                'success': False,
                'message': f'Failed to analyze performance: {str(e)}'
            }
    
    def _get_student_profile(self, user_id: str, profile_data: Dict = None) -> StudentProfile:
        """Get or create student profile"""
        if profile_data:
            return StudentProfile(
                user_id=user_id,
                ability_level=profile_data.get('ability_level', 0.0),
                blooms_progress={BloomsLevel(i+1): profile_data.get('blooms_progress', {}).get(level.name.lower(), 0.0) 
                               for i, level in enumerate(BloomsLevel)},
                subject_abilities=profile_data.get('subject_abilities', {}),
                learning_style=profile_data.get('learning_style', 'adaptive')
            )
        else:
            # Default profile for new students
            return StudentProfile(user_id=user_id)
    
    def _generate_question_pool(self, subject: str, topic: str, difficulty: str, pool_size: int) -> List[Question]:
        """Generate a pool of questions using AI"""
        try:
            # Create prompt for question generation
            prompt = f"""
            Generate {pool_size} multiple-choice questions for {subject} on the topic of {topic}.
            
            Requirements:
            - Mix of difficulty levels (easy, medium, hard)
            - Cover all Bloom's Taxonomy levels (Remember, Understand, Apply, Analyze, Evaluate, Create)
            - Include IRT difficulty parameters (-2 to 2 scale)
            - Provide 4 options per question with one correct answer
            - Include explanations for correct answers
            
            Format as JSON array with this structure:
            {{
                "id": "unique_id",
                "text": "question text",
                "options": ["A", "B", "C", "D"],
                "correct_answer": "A",
                "explanation": "why this is correct",
                "difficulty": -1.5,
                "blooms_level": "apply",
                "subject": "{subject}",
                "topic": "{topic}"
            }}
            """
            
            # Generate questions using AI
            ai_response = self.openai_service.generate_text(prompt, max_tokens=2000)
            
            if ai_response.get('success'):
                try:
                    questions_data = json.loads(ai_response['data']['generated_text'])
                    questions = []
                    
                    for i, q_data in enumerate(questions_data):
                        blooms_level = self._parse_blooms_level(q_data.get('blooms_level', 'remember'))
                        question = Question(
                            id=q_data.get('id', f"q_{i}"),
                            text=q_data.get('text', ''),
                            difficulty=q_data.get('difficulty', 0.0),
                            discrimination=1.0,
                            guessing=0.25,  # 25% for 4-option MC
                            blooms_level=blooms_level,
                            subject=subject,
                            topic=topic,
                            correct_answer=q_data.get('correct_answer', 'A'),
                            options=q_data.get('options', [])
                        )
                        questions.append(question)
                    
                    return questions
                    
                except json.JSONDecodeError:
                    logger.warning("Failed to parse AI-generated questions, using fallback")
                    return self._generate_fallback_questions(subject, topic, pool_size)
            else:
                return self._generate_fallback_questions(subject, topic, pool_size)
                
        except Exception as e:
            logger.error(f"Error generating question pool: {str(e)}")
            return self._generate_fallback_questions(subject, topic, pool_size)
    
    def _generate_fallback_questions(self, subject: str, topic: str, pool_size: int) -> List[Question]:
        """Generate fallback questions when AI generation fails"""
        questions = []
        blooms_levels = list(BloomsLevel)
        difficulties = [-1.5, -0.5, 0.0, 0.5, 1.5]
        
        for i in range(pool_size):
            question = Question(
                id=f"fallback_{i}",
                text=f"Sample question {i+1} about {topic}",
                difficulty=random.choice(difficulties),
                discrimination=1.0,
                guessing=0.25,
                blooms_level=random.choice(blooms_levels),
                subject=subject,
                topic=topic,
                correct_answer="A",
                options=["Option A", "Option B", "Option C", "Option D"]
            )
            questions.append(question)
        
        return questions
    
    def _parse_blooms_distribution(self, target_levels: List[str]) -> Dict[BloomsLevel, float]:
        """Parse target Bloom's levels into distribution"""
        if not target_levels:
            # Default distribution emphasizing higher-order thinking
            return {
                BloomsLevel.REMEMBER: 0.1,
                BloomsLevel.UNDERSTAND: 0.2,
                BloomsLevel.APPLY: 0.3,
                BloomsLevel.ANALYZE: 0.2,
                BloomsLevel.EVALUATE: 0.1,
                BloomsLevel.CREATE: 0.1
            }
        
        # Equal distribution among specified levels
        weight = 1.0 / len(target_levels)
        distribution = {}
        
        for level_str in target_levels:
            blooms_level = self._parse_blooms_level(level_str)
            distribution[blooms_level] = weight
        
        return distribution
    
    def _parse_blooms_level(self, level_str: str) -> BloomsLevel:
        """Parse string to BloomsLevel enum"""
        level_map = {
            'remember': BloomsLevel.REMEMBER,
            'understand': BloomsLevel.UNDERSTAND,
            'apply': BloomsLevel.APPLY,
            'analyze': BloomsLevel.ANALYZE,
            'evaluate': BloomsLevel.EVALUATE,
            'create': BloomsLevel.CREATE
        }
        return level_map.get(level_str.lower(), BloomsLevel.REMEMBER)
    
    def _format_question(self, question: Question, index: int) -> Dict:
        """Format question for API response"""
        if not question:
            return None
            
        return {
            'id': question.id,
            'index': index,
            'text': question.text,
            'type': 'multiple-choice',
            'options': question.options or [],
            'blooms_level': question.blooms_level.name.lower(),
            'difficulty': question.difficulty,
            'subject': question.subject,
            'topic': question.topic,
            'estimated_time': 120  # 2 minutes
        }
    
    def _evaluate_response(self, question: Question, user_answer: str) -> bool:
        """Evaluate if the user's answer is correct"""
        return user_answer.strip().upper() == question.correct_answer.strip().upper()
    
    def _generate_response_feedback(self, question: Question, is_correct: bool, user_answer: str) -> Dict:
        """Generate feedback for a response"""
        if is_correct:
            return {
                'type': 'correct',
                'message': 'Correct! Well done.',
                'explanation': f"The correct answer is {question.correct_answer}.",
                'encouragement': 'Keep up the good work!'
            }
        else:
            return {
                'type': 'incorrect',
                'message': f'Incorrect. The correct answer is {question.correct_answer}.',
                'explanation': f"You selected {user_answer}, but the correct answer is {question.correct_answer}.",
                'hint': 'Review the concept and try similar questions.'
            }
    
    def _generate_performance_insight(self, student_profile: StudentProfile, is_correct: bool) -> str:
        """Generate performance insight based on current state"""
        if is_correct:
            if student_profile.ability_level > 1.0:
                return "Excellent! You're demonstrating strong mastery of this topic."
            else:
                return "Good job! You're making steady progress."
        else:
            if student_profile.ability_level < -1.0:
                return "Don't worry, this is challenging material. Keep practicing!"
            else:
                return "Close! Review the concept and you'll get it next time."
    
    def _classify_ability_level(self, ability: float) -> str:
        """Classify ability level into descriptive categories"""
        if ability >= 2.0:
            return "Advanced"
        elif ability >= 1.0:
            return "Proficient"
        elif ability >= 0.0:
            return "Developing"
        elif ability >= -1.0:
            return "Beginning"
        else:
            return "Needs Support"
    
    def _generate_learning_recommendations(self, performance_analysis: Dict) -> List[str]:
        """Generate personalized learning recommendations"""
        recommendations = []
        
        accuracy = performance_analysis.get('accuracy', 0)
        blooms_performance = performance_analysis.get('blooms_performance', {})
        
        if accuracy < 0.6:
            recommendations.append("Focus on foundational concepts before moving to advanced topics")
        
        for level, score in blooms_performance.items():
            if score < 0.5:
                recommendations.append(f"Practice more {level}-level questions to strengthen this cognitive skill")
        
        if performance_analysis.get('average_response_time', 0) > 180:  # 3 minutes
            recommendations.append("Work on time management and quick recall of key concepts")
        
        return recommendations
    
    def _generate_next_steps(self, performance_analysis: Dict) -> List[str]:
        """Generate next steps for learning progression"""
        next_steps = []
        
        performance_level = performance_analysis.get('performance_level', 'unknown')
        
        if performance_level in ['excellent', 'good']:
            next_steps.append("Ready for more challenging material")
            next_steps.append("Consider exploring advanced topics in this subject")
        elif performance_level == 'satisfactory':
            next_steps.append("Continue practicing current level material")
            next_steps.append("Gradually introduce more complex problems")
        else:
            next_steps.append("Review fundamental concepts")
            next_steps.append("Practice with easier questions first")
        
        return next_steps
    
    def _analyze_difficulty_range(self, responses: List[Dict]) -> Dict:
        """Analyze the range of difficulties attempted"""
        difficulties = [r.get('question', {}).get('difficulty', 0) for r in responses]
        if difficulties:
            return {
                'min': min(difficulties),
                'max': max(difficulties),
                'range': max(difficulties) - min(difficulties)
            }
        return {'min': 0, 'max': 0, 'range': 0}
    
    def _analyze_time_efficiency(self, responses: List[Dict]) -> str:
        """Analyze time efficiency"""
        times = [r.get('response_time', 0) for r in responses if r.get('response_time', 0) > 0]
        if times:
            avg_time = sum(times) / len(times)
            if avg_time < 60:
                return "Very efficient"
            elif avg_time < 120:
                return "Efficient"
            elif avg_time < 180:
                return "Moderate"
            else:
                return "Needs improvement"
        return "Unknown"
    
    def _get_question_by_id(self, question_id: str) -> Optional[Question]:
        """Get question by ID (placeholder - would integrate with database)"""
        # This would typically query a database
        # For now, return a sample question
        return Question(
            id=question_id,
            text="Sample question",
            difficulty=0.0,
            blooms_level=BloomsLevel.APPLY,
            correct_answer="A",
            options=["A", "B", "C", "D"]
        )
    
    def _parse_question(self, question_data: Dict) -> Question:
        """Parse question data into Question object"""
        return Question(
            id=question_data.get('id', ''),
            text=question_data.get('text', ''),
            difficulty=question_data.get('difficulty', 0.0),
            discrimination=question_data.get('discrimination', 1.0),
            guessing=question_data.get('guessing', 0.25),
            blooms_level=self._parse_blooms_level(question_data.get('blooms_level', 'remember')),
            subject=question_data.get('subject', ''),
            topic=question_data.get('topic', ''),
            correct_answer=question_data.get('correct_answer', 'A'),
            options=question_data.get('options', [])
        )