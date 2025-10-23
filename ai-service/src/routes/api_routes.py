from flask import Blueprint, request, jsonify
from controllers.analysis_controller import AnalysisController
from controllers.prediction_controller import PredictionController
from controllers.training_controller import TrainingController
from utils.validators import validate_request
import logging

logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__)

# Initialize controllers
analysis_controller = AnalysisController()
prediction_controller = PredictionController()
training_controller = TrainingController()

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