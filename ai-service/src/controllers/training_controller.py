import logging
import json
from datetime import datetime
from models.text_model import TextModel
from models.recommendation_model import RecommendationModel

logger = logging.getLogger(__name__)

class TrainingController:
    def __init__(self):
        self.text_model = TextModel()
        self.recommendation_model = RecommendationModel()
    
    def train_model(self, model_type, training_data, parameters=None):
        """Train a model with provided data"""
        try:
            if parameters is None:
                parameters = {}
            
            training_id = f"training_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            if model_type == 'text_classification':
                result = self._train_text_classification(training_data, parameters, training_id)
            elif model_type == 'recommendation':
                result = self._train_recommendation_model(training_data, parameters, training_id)
            elif model_type == 'sentiment_analysis':
                result = self._train_sentiment_model(training_data, parameters, training_id)
            else:
                raise ValueError(f"Unsupported model type: {model_type}")
            
            return {
                'training_id': training_id,
                'model_type': model_type,
                'status': 'initiated',
                'parameters': parameters,
                'result': result,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Model training failed: {str(e)}")
            raise
    
    def get_training_status(self, training_id):
        """Get status of training job"""
        try:
            # In a real implementation, this would check a database or job queue
            return {
                'training_id': training_id,
                'status': 'completed',
                'progress': 100,
                'metrics': {
                    'accuracy': 0.85,
                    'loss': 0.15,
                    'training_time': '5 minutes'
                },
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to get training status: {str(e)}")
            raise
    
    def _train_text_classification(self, training_data, parameters, training_id):
        """Train text classification model"""
        try:
            # Validate training data
            if not isinstance(training_data, list) or len(training_data) == 0:
                raise ValueError("Training data must be a non-empty list")
            
            # Extract features and labels
            texts = []
            labels = []
            
            for item in training_data:
                if 'text' not in item or 'label' not in item:
                    raise ValueError("Each training item must have 'text' and 'label' fields")
                texts.append(item['text'])
                labels.append(item['label'])
            
            # Train the model (simplified simulation)
            model_result = self.text_model.train_classifier(texts, labels, parameters)
            
            return {
                'model_path': f"models/text_classifier_{training_id}.pkl",
                'training_samples': len(training_data),
                'unique_labels': len(set(labels)),
                'model_metrics': model_result
            }
            
        except Exception as e:
            logger.error(f"Text classification training failed: {str(e)}")
            raise
    
    def _train_recommendation_model(self, training_data, parameters, training_id):
        """Train recommendation model"""
        try:
            # Validate training data
            if not isinstance(training_data, list) or len(training_data) == 0:
                raise ValueError("Training data must be a non-empty list")
            
            # Extract user-item interactions
            interactions = []
            
            for item in training_data:
                if 'user_id' not in item or 'item_id' not in item:
                    raise ValueError("Each training item must have 'user_id' and 'item_id' fields")
                interactions.append({
                    'user_id': item['user_id'],
                    'item_id': item['item_id'],
                    'rating': item.get('rating', 1.0),
                    'timestamp': item.get('timestamp', datetime.now().isoformat())
                })
            
            # Train the model
            model_result = self.recommendation_model.train(interactions, parameters)
            
            return {
                'model_path': f"models/recommendation_{training_id}.pkl",
                'training_interactions': len(interactions),
                'unique_users': len(set(item['user_id'] for item in interactions)),
                'unique_items': len(set(item['item_id'] for item in interactions)),
                'model_metrics': model_result
            }
            
        except Exception as e:
            logger.error(f"Recommendation model training failed: {str(e)}")
            raise
    
    def _train_sentiment_model(self, training_data, parameters, training_id):
        """Train sentiment analysis model"""
        try:
            # Validate training data
            if not isinstance(training_data, list) or len(training_data) == 0:
                raise ValueError("Training data must be a non-empty list")
            
            # Extract texts and sentiments
            texts = []
            sentiments = []
            
            for item in training_data:
                if 'text' not in item or 'sentiment' not in item:
                    raise ValueError("Each training item must have 'text' and 'sentiment' fields")
                texts.append(item['text'])
                sentiments.append(item['sentiment'])
            
            # Train the model
            model_result = self.text_model.train_sentiment_analyzer(texts, sentiments, parameters)
            
            return {
                'model_path': f"models/sentiment_{training_id}.pkl",
                'training_samples': len(training_data),
                'sentiment_classes': len(set(sentiments)),
                'model_metrics': model_result
            }
            
        except Exception as e:
            logger.error(f"Sentiment model training failed: {str(e)}")
            raise