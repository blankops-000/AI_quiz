import logging
from typing import Dict, List, Any, Union
import json

logger = logging.getLogger(__name__)

class PostprocessingService:
    def __init__(self):
        self.confidence_thresholds = {
            'high': 0.8,
            'medium': 0.6,
            'low': 0.4
        }
    
    def format_sentiment_result(self, sentiment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format sentiment analysis results"""
        try:
            if not sentiment_data:
                return self._get_default_sentiment()
            
            # Extract sentiment information
            overall_sentiment = sentiment_data.get('overall_sentiment', 'neutral')
            confidence = sentiment_data.get('confidence', 0.5)
            scores = sentiment_data.get('scores', {})
            
            # Determine confidence level
            confidence_level = self._get_confidence_level(confidence)
            
            # Format the result
            formatted_result = {
                'sentiment': overall_sentiment,
                'confidence': round(confidence, 3),
                'confidence_level': confidence_level,
                'scores': {k: round(v, 3) for k, v in scores.items()},
                'interpretation': self._interpret_sentiment(overall_sentiment, confidence)
            }
            
            return formatted_result
            
        except Exception as e:
            logger.error(f"Sentiment result formatting failed: {str(e)}")
            return self._get_default_sentiment()
    
    def format_text_analysis_result(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format text analysis results"""
        try:
            formatted_result = {
                'summary': {
                    'word_count': analysis_data.get('word_count', 0),
                    'character_count': analysis_data.get('character_count', 0),
                    'readability_score': round(analysis_data.get('readability_score', 0), 2)
                },
                'sentiment': self.format_sentiment_result(analysis_data.get('sentiment', {})),
                'entities': self._format_entities(analysis_data.get('entities', {})),
                'keywords': self._format_keywords(analysis_data.get('keywords', [])),
                'metadata': {
                    'processed_at': analysis_data.get('timestamp'),
                    'processing_time': analysis_data.get('processing_time'),
                    'model_version': analysis_data.get('model_version', '1.0')
                }
            }
            
            return formatted_result
            
        except Exception as e:
            logger.error(f"Text analysis result formatting failed: {str(e)}")
            return {}
    
    def format_quiz_result(self, quiz_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format quiz generation results"""
        try:
            questions = quiz_data.get('questions', [])
            
            # Format each question
            formatted_questions = []
            for i, question in enumerate(questions):
                formatted_question = {
                    'id': question.get('id', i + 1),
                    'question': question.get('question', ''),
                    'options': question.get('options', []),
                    'correct_answer': question.get('correct_answer', 'A'),
                    'explanation': question.get('explanation', ''),
                    'difficulty': quiz_data.get('difficulty', 'medium'),
                    'points': self._calculate_question_points(quiz_data.get('difficulty', 'medium'))
                }
                formatted_questions.append(formatted_question)
            
            # Calculate total points
            total_points = sum(q['points'] for q in formatted_questions)
            
            formatted_result = {
                'quiz_info': {
                    'topic': quiz_data.get('topic', ''),
                    'difficulty': quiz_data.get('difficulty', 'medium'),
                    'total_questions': len(formatted_questions),
                    'total_points': total_points,
                    'estimated_time': len(formatted_questions) * 2  # 2 minutes per question
                },
                'questions': formatted_questions,
                'instructions': self._generate_quiz_instructions(quiz_data.get('difficulty', 'medium')),
                'metadata': {
                    'generated_at': quiz_data.get('timestamp'),
                    'version': '1.0'
                }
            }
            
            return formatted_result
            
        except Exception as e:
            logger.error(f"Quiz result formatting failed: {str(e)}")
            return {}
    
    def format_recommendations(self, recommendations_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format recommendation results"""
        try:
            recommendations = recommendations_data.get('recommendations', [])
            
            # Format each recommendation
            formatted_recommendations = []
            for i, rec in enumerate(recommendations):
                formatted_rec = {
                    'id': rec.get('id', i + 1),
                    'title': rec.get('title', f'Recommendation {i + 1}'),
                    'description': rec.get('description', ''),
                    'score': round(rec.get('score', 0.5), 3),
                    'confidence': self._get_confidence_level(rec.get('score', 0.5)),
                    'category': rec.get('category', 'general'),
                    'tags': rec.get('tags', []),
                    'reasoning': rec.get('reasoning', 'Based on your preferences')
                }
                formatted_recommendations.append(formatted_rec)
            
            # Sort by score
            formatted_recommendations.sort(key=lambda x: x['score'], reverse=True)
            
            formatted_result = {
                'user_id': recommendations_data.get('user_id'),
                'total_recommendations': len(formatted_recommendations),
                'recommendations': formatted_recommendations,
                'preferences_used': recommendations_data.get('preferences', {}),
                'metadata': {
                    'generated_at': recommendations_data.get('timestamp'),
                    'algorithm_version': '1.0'
                }
            }
            
            return formatted_result
            
        except Exception as e:
            logger.error(f"Recommendations formatting failed: {str(e)}")
            return {}
    
    def _get_confidence_level(self, confidence: float) -> str:
        """Determine confidence level based on score"""
        if confidence >= self.confidence_thresholds['high']:
            return 'high'
        elif confidence >= self.confidence_thresholds['medium']:
            return 'medium'
        else:
            return 'low'
    
    def _interpret_sentiment(self, sentiment: str, confidence: float) -> str:
        """Provide interpretation of sentiment analysis"""
        confidence_level = self._get_confidence_level(confidence)
        
        interpretations = {
            'positive': {
                'high': 'The text expresses clearly positive sentiment',
                'medium': 'The text appears to be positive',
                'low': 'The text may be slightly positive'
            },
            'negative': {
                'high': 'The text expresses clearly negative sentiment',
                'medium': 'The text appears to be negative',
                'low': 'The text may be slightly negative'
            },
            'neutral': {
                'high': 'The text is clearly neutral',
                'medium': 'The text appears to be neutral',
                'low': 'The text sentiment is unclear'
            }
        }
        
        return interpretations.get(sentiment, {}).get(confidence_level, 'Sentiment analysis inconclusive')
    
    def _format_entities(self, entities: Dict[str, List]) -> Dict[str, List]:
        """Format named entities"""
        formatted_entities = {}
        
        for entity_type, entity_list in entities.items():
            formatted_entities[entity_type] = [
                {
                    'text': entity.get('text', ''),
                    'confidence': round(entity.get('confidence', 0.0), 3)
                }
                for entity in entity_list
            ]
        
        return formatted_entities
    
    def _format_keywords(self, keywords: List[Dict]) -> List[Dict]:
        """Format keywords"""
        return [
            {
                'word': kw.get('word', ''),
                'frequency': kw.get('frequency', 0),
                'importance': round(kw.get('frequency', 0) / max(k.get('frequency', 1) for k in keywords), 3) if keywords else 0
            }
            for kw in keywords[:10]  # Top 10 keywords
        ]
    
    def _calculate_question_points(self, difficulty: str) -> int:
        """Calculate points for a question based on difficulty"""
        points_map = {
            'easy': 1,
            'medium': 2,
            'hard': 3
        }
        return points_map.get(difficulty, 2)
    
    def _generate_quiz_instructions(self, difficulty: str) -> List[str]:
        """Generate instructions for quiz"""
        base_instructions = [
            "Read each question carefully",
            "Select the best answer from the given options",
            "You can review your answers before submitting"
        ]
        
        difficulty_instructions = {
            'easy': ["Take your time to think through each question"],
            'medium': ["Some questions may require deeper thinking", "Consider all options before selecting"],
            'hard': ["These questions are challenging", "Apply your knowledge and reasoning skills", "Don't rush through the questions"]
        }
        
        return base_instructions + difficulty_instructions.get(difficulty, [])
    
    def _get_default_sentiment(self) -> Dict[str, Any]:
        """Get default sentiment result"""
        return {
            'sentiment': 'neutral',
            'confidence': 0.5,
            'confidence_level': 'medium',
            'scores': {'neutral': 0.5},
            'interpretation': 'Unable to determine sentiment'
        }