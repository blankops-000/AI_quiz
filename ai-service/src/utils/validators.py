import logging
from typing import Dict, List, Any, Union

logger = logging.getLogger(__name__)

def validate_request(data: Dict[str, Any], required_fields: List[str]) -> bool:
    """Validate that request data contains required fields"""
    try:
        if not data or not isinstance(data, dict):
            return False
        
        for field in required_fields:
            if field not in data or data[field] is None:
                logger.warning(f"Missing required field: {field}")
                return False
            
            # Check for empty strings
            if isinstance(data[field], str) and not data[field].strip():
                logger.warning(f"Empty required field: {field}")
                return False
        
        return True
        
    except Exception as e:
        logger.error(f"Request validation failed: {str(e)}")
        return False

def validate_text_input(text: str, min_length: int = 1, max_length: int = 10000) -> bool:
    """Validate text input"""
    try:
        if not text or not isinstance(text, str):
            return False
        
        text = text.strip()
        
        if len(text) < min_length:
            logger.warning(f"Text too short: {len(text)} < {min_length}")
            return False
        
        if len(text) > max_length:
            logger.warning(f"Text too long: {len(text)} > {max_length}")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"Text validation failed: {str(e)}")
        return False

def validate_quiz_parameters(data: Dict[str, Any]) -> bool:
    """Validate quiz generation parameters"""
    try:
        # Check topic
        if not validate_text_input(data.get('topic', ''), min_length=2, max_length=100):
            return False
        
        # Check number of questions
        num_questions = data.get('num_questions', 5)
        if not isinstance(num_questions, int) or num_questions < 1 or num_questions > 20:
            logger.warning(f"Invalid number of questions: {num_questions}")
            return False
        
        # Check difficulty
        difficulty = data.get('difficulty', 'medium')
        valid_difficulties = ['easy', 'medium', 'hard']
        if difficulty not in valid_difficulties:
            logger.warning(f"Invalid difficulty: {difficulty}")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"Quiz parameters validation failed: {str(e)}")
        return False

def validate_training_data(data: Dict[str, Any]) -> bool:
    """Validate training data"""
    try:
        # Check model type
        model_type = data.get('model_type')
        valid_model_types = ['text_classification', 'sentiment_analysis', 'recommendation']
        if model_type not in valid_model_types:
            logger.warning(f"Invalid model type: {model_type}")
            return False
        
        # Check training data
        training_data = data.get('training_data')
        if not training_data or not isinstance(training_data, list):
            logger.warning("Training data must be a non-empty list")
            return False
        
        if len(training_data) < 10:
            logger.warning(f"Insufficient training data: {len(training_data)} samples")
            return False
        
        # Validate training data structure based on model type
        if model_type in ['text_classification', 'sentiment_analysis']:
            return validate_text_training_data(training_data)
        elif model_type == 'recommendation':
            return validate_recommendation_training_data(training_data)
        
        return True
        
    except Exception as e:
        logger.error(f"Training data validation failed: {str(e)}")
        return False

def validate_text_training_data(training_data: List[Dict]) -> bool:
    """Validate text classification/sentiment training data"""
    try:
        for i, item in enumerate(training_data):
            if not isinstance(item, dict):
                logger.warning(f"Training item {i} is not a dictionary")
                return False
            
            if 'text' not in item or 'label' not in item:
                logger.warning(f"Training item {i} missing 'text' or 'label' field")
                return False
            
            if not validate_text_input(item['text'], min_length=1, max_length=5000):
                logger.warning(f"Invalid text in training item {i}")
                return False
            
            if not item['label'] or not isinstance(item['label'], str):
                logger.warning(f"Invalid label in training item {i}")
                return False
        
        return True
        
    except Exception as e:
        logger.error(f"Text training data validation failed: {str(e)}")
        return False

def validate_recommendation_training_data(training_data: List[Dict]) -> bool:
    """Validate recommendation training data"""
    try:
        for i, item in enumerate(training_data):
            if not isinstance(item, dict):
                logger.warning(f"Training item {i} is not a dictionary")
                return False
            
            if 'user_id' not in item or 'item_id' not in item:
                logger.warning(f"Training item {i} missing 'user_id' or 'item_id' field")
                return False
            
            if not item['user_id'] or not item['item_id']:
                logger.warning(f"Empty user_id or item_id in training item {i}")
                return False
            
            # Validate rating if present
            if 'rating' in item:
                rating = item['rating']
                if not isinstance(rating, (int, float)) or rating < 0:
                    logger.warning(f"Invalid rating in training item {i}")
                    return False
        
        return True
        
    except Exception as e:
        logger.error(f"Recommendation training data validation failed: {str(e)}")
        return False

def validate_user_preferences(preferences: Dict[str, Any]) -> bool:
    """Validate user preferences for recommendations"""
    try:
        if not isinstance(preferences, dict):
            return False
        
        # Validate categories if present
        if 'categories' in preferences:
            categories = preferences['categories']
            if not isinstance(categories, list):
                logger.warning("Categories must be a list")
                return False
            
            for category in categories:
                if not isinstance(category, str) or not category.strip():
                    logger.warning("Invalid category in preferences")
                    return False
        
        # Validate tags if present
        if 'tags' in preferences:
            tags = preferences['tags']
            if not isinstance(tags, list):
                logger.warning("Tags must be a list")
                return False
            
            for tag in tags:
                if not isinstance(tag, str) or not tag.strip():
                    logger.warning("Invalid tag in preferences")
                    return False
        
        return True
        
    except Exception as e:
        logger.error(f"User preferences validation failed: {str(e)}")
        return False

def sanitize_text(text: str) -> str:
    """Sanitize text input"""
    try:
        if not text or not isinstance(text, str):
            return ""
        
        # Remove potentially harmful characters
        sanitized = text.strip()
        
        # Remove null bytes
        sanitized = sanitized.replace('\x00', '')
        
        # Limit length
        if len(sanitized) > 10000:
            sanitized = sanitized[:10000]
        
        return sanitized
        
    except Exception as e:
        logger.error(f"Text sanitization failed: {str(e)}")
        return ""

def validate_file_upload(file_data: Dict[str, Any]) -> bool:
    """Validate file upload data"""
    try:
        if not file_data or not isinstance(file_data, dict):
            return False
        
        # Check required fields
        required_fields = ['filename', 'content', 'content_type']
        for field in required_fields:
            if field not in file_data:
                logger.warning(f"Missing file field: {field}")
                return False
        
        # Validate filename
        filename = file_data['filename']
        if not filename or not isinstance(filename, str):
            logger.warning("Invalid filename")
            return False
        
        # Check file extension
        allowed_extensions = ['.txt', '.csv', '.json', '.pdf']
        if not any(filename.lower().endswith(ext) for ext in allowed_extensions):
            logger.warning(f"Unsupported file type: {filename}")
            return False
        
        # Check content size
        content = file_data['content']
        if len(content) > 10 * 1024 * 1024:  # 10MB limit
            logger.warning("File too large")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"File upload validation failed: {str(e)}")
        return False