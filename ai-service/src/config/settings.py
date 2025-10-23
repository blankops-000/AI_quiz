import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_ENV') == 'development'
    
    # Server settings
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 8000))
    
    # CORS settings
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5000').split(',')
    
    # API settings
    API_VERSION = 'v1'
    API_PREFIX = f'/api/{API_VERSION}'
    
    # Rate limiting
    RATE_LIMIT_ENABLED = os.getenv('RATE_LIMIT_ENABLED', 'true').lower() == 'true'
    RATE_LIMIT_DEFAULT = os.getenv('RATE_LIMIT_DEFAULT', '100 per hour')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/ai_service.log')
    
    # AI Service settings
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')
    
    # Model settings
    MODEL_CACHE_DIR = os.getenv('MODEL_CACHE_DIR', './models/cache')
    MODEL_SAVE_DIR = os.getenv('MODEL_SAVE_DIR', './models/saved')
    
    # Processing limits
    MAX_TEXT_LENGTH = int(os.getenv('MAX_TEXT_LENGTH', 10000))
    MAX_BATCH_SIZE = int(os.getenv('MAX_BATCH_SIZE', 32))
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', 30))
    
    # Database settings (if needed for future extensions)
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    # Redis settings (if needed for caching)
    REDIS_URL = os.getenv('REDIS_URL')
    CACHE_ENABLED = os.getenv('CACHE_ENABLED', 'false').lower() == 'true'
    CACHE_TIMEOUT = int(os.getenv('CACHE_TIMEOUT', 300))  # 5 minutes

class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    RATE_LIMIT_ENABLED = False

class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = 'INFO'
    RATE_LIMIT_ENABLED = True

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    RATE_LIMIT_ENABLED = False

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get configuration based on environment"""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])