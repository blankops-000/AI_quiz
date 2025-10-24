from flask import Blueprint, request, jsonify
from controllers.analysis_controller import AnalysisController
from controllers.prediction_controller import PredictionController
from controllers.training_controller import TrainingController
from controllers.adaptive_quiz_controller import AdaptiveQuizController
from utils.validators import validate_request
import logging

logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__)

# Initialize controllers
analysis_controller = AnalysisController()
prediction_controller = PredictionController()
training_controller = TrainingController()
adaptive_quiz_controller = AdaptiveQuizController()

@api_bp.route('/analyze/text', methods=['POST'])
def analyze_text():
    try:
        data = request.get_json()
        
        if not validate_request(data, ['text']):
            return jsonify({
                'success': False,
                'message': 'Text is required'
            }), 400
        
        result = analysis_controller.analyze_text(data['text'])
        
        return jsonify({
            'success': True,
            'data': result,
            'message': 'Text analysis completed'
        }), 200
        
    except Exception as e:
        logger.error(f"Text analysis error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Text analysis failed'
        }), 500

@api_bp.route('/analyze/sentiment', methods=['POST'])
def analyze_sentiment():
    try:
        data = request.get_json()
        
        if not validate_request(data, ['text']):
            return jsonify({
                'success': False,
                'message': 'Text is required'
            }), 400
        
        result = analysis_controller.analyze_sentiment(data['text'])
        
        return jsonify({
            'success': True,
            'data': result,
            'message': 'Sentiment analysis completed'
        }), 200
        
    except Exception as e:
        logger.error(f"Sentiment analysis error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Sentiment analysis failed'
        }), 500

@api_bp.route('/generate/text', methods=['POST'])
def generate_text():
    try:
        data = request.get_json()
        
        if not validate_request(data, ['prompt']):
            return jsonify({
                'success': False,
                'message': 'Prompt is required'
            }), 400
        
        result = prediction_controller.generate_text(
            data['prompt'],
            data.get('max_length', 100),
            data.get('temperature', 0.7)
        )
        
        return jsonify({
            'success': True,
            'data': result,
            'message': 'Text generation completed'
        }), 200
        
    except Exception as e:
        logger.error(f"Text generation error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Text generation failed'
        }), 500

@api_bp.route('/generate/quiz', methods=['POST'])
def generate_quiz():
    try:
        data = request.get_json()
        
        if not validate_request(data, ['topic']):
            return jsonify({
                'success': False,
                'message': 'Topic is required'
            }), 400
        
        result = prediction_controller.generate_quiz(
            data['topic'],
            data.get('num_questions', 5),
            data.get('difficulty', 'medium')
        )
        
        return jsonify({
            'success': True,
            'data': result,
            'message': 'Quiz generation completed'
        }), 200
        
    except Exception as e:
        logger.error(f"Quiz generation error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Quiz generation failed'
        }), 500

@api_bp.route('/recommendations', methods=['POST'])
def get_recommendations():
    try:
        data = request.get_json()
        
        if not validate_request(data, ['user_id']):
            return jsonify({
                'success': False,
                'message': 'User ID is required'
            }), 400
        
        result = prediction_controller.get_recommendations(
            data['user_id'],
            data.get('preferences', {}),
            data.get('limit', 10)
        )
        
        return jsonify({
            'success': True,
            'data': result,
            'message': 'Recommendations generated'
        }), 200
        
    except Exception as e:
        logger.error(f"Recommendations error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Recommendations failed'
        }), 500

@api_bp.route('/train/model', methods=['POST'])
def train_model():
    try:
        data = request.get_json()
        
        if not validate_request(data, ['model_type', 'training_data']):
            return jsonify({
                'success': False,
                'message': 'Model type and training data are required'
            }), 400
        
        result = training_controller.train_model(
            data['model_type'],
            data['training_data'],
            data.get('parameters', {})
        )
        
        return jsonify({
            'success': True,
            'data': result,
            'message': 'Model training initiated'
        }), 200
        
    except Exception as e:
        logger.error(f"Model training error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Model training failed'
        }), 500

# Adaptive Quiz Endpoints
@api_bp.route('/quiz/adaptive/generate', methods=['POST'])
def generate_adaptive_quiz():
    try:
        data = request.get_json()
        
        if not validate_request(data, ['user_id', 'subject', 'topic']):
            return jsonify({
                'success': False,
                'message': 'User ID, subject, and topic are required'
            }), 400
        
        result = adaptive_quiz_controller.generate_adaptive_quiz(data)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
        
    except Exception as e:
        logger.error(f"Adaptive quiz generation error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Adaptive quiz generation failed'
        }), 500

@api_bp.route('/quiz/adaptive/response', methods=['POST'])
def process_quiz_response():
    try:
        data = request.get_json()
        
        if not validate_request(data, ['user_id', 'quiz_id', 'question_id', 'answer']):
            return jsonify({
                'success': False,
                'message': 'User ID, quiz ID, question ID, and answer are required'
            }), 400
        
        result = adaptive_quiz_controller.process_quiz_response(data)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
        
    except Exception as e:
        logger.error(f"Quiz response processing error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Quiz response processing failed'
        }), 500

@api_bp.route('/quiz/adaptive/analyze', methods=['POST'])
def analyze_quiz_performance():
    try:
        data = request.get_json()
        
        if not validate_request(data, ['user_id', 'responses']):
            return jsonify({
                'success': False,
                'message': 'User ID and responses are required'
            }), 400
        
        result = adaptive_quiz_controller.analyze_quiz_performance(data)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
        
    except Exception as e:
        logger.error(f"Quiz performance analysis error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Quiz performance analysis failed'
        }), 500

@api_bp.route('/student/profile', methods=['GET'])
def get_student_profile():
    try:
        user_id = request.args.get('user_id')
        
        if not user_id:
            return jsonify({
                'success': False,
                'message': 'User ID is required'
            }), 400
        
        # This would typically fetch from database
        # For now, return a sample profile
        profile_data = {
            'user_id': user_id,
            'ability_level': 0.0,
            'blooms_progress': {
                'remember': 0.8,
                'understand': 0.7,
                'apply': 0.6,
                'analyze': 0.4,
                'evaluate': 0.3,
                'create': 0.2
            },
            'subject_abilities': {
                'Computer Science': 0.5,
                'Mathematics': 0.3
            },
            'learning_style': 'adaptive',
            'performance_metrics': {
                'total_quizzes': 15,
                'average_score': 75.5,
                'improvement_rate': 0.15
            }
        }
        
        return jsonify({
            'success': True,
            'data': profile_data,
            'message': 'Student profile retrieved successfully'
        }), 200
        
    except Exception as e:
        logger.error(f"Student profile retrieval error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Failed to retrieve student profile'
        }), 500