import os

# AI Service Configuration
AI_CONFIG = {
    'openai': {
        'api_key': os.getenv('OPENAI_API_KEY'),
        'text_model': 'text-davinci-003',
        'chat_model': 'gpt-3.5-turbo',
        'max_tokens': 1000,
        'temperature': 0.7
    },
    'huggingface': {
        'api_key': os.getenv('HUGGINGFACE_API_KEY'),
        'sentiment_model': 'cardiffnlp/twitter-roberta-base-sentiment-latest',
        'text_generation_model': 'gpt2',
        'ner_model': 'dbmdz/bert-large-cased-finetuned-conll03-english',
        'classification_model': 'facebook/bart-large-mnli'
    },
    'models': {
        'cache_dir': './models/cache',
        'save_dir': './models/saved',
        'max_model_size': '1GB'
    },
    'processing': {
        'max_text_length': 10000,
        'batch_size': 32,
        'timeout': 30
    },
    'quiz': {
        'max_questions': 20,
        'min_questions': 1,
        'default_questions': 5,
        'difficulties': ['easy', 'medium', 'hard'],
        'default_difficulty': 'medium'
    },
    'recommendations': {
        'max_recommendations': 50,
        'default_recommendations': 10,
        'min_score_threshold': 0.1
    }
}

# Environment-specific overrides
if os.getenv('FLASK_ENV') == 'development':
    AI_CONFIG['processing']['timeout'] = 60
    AI_CONFIG['models']['cache_dir'] = './dev_models/cache'

elif os.getenv('FLASK_ENV') == 'production':
    AI_CONFIG['processing']['batch_size'] = 64
    AI_CONFIG['models']['cache_dir'] = '/app/models/cache'