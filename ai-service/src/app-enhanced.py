from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import random

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'AI Service',
        'version': '1.0.0'
    }), 200

@app.route('/api/analyze/text', methods=['POST'])
def analyze_text():
    data = request.get_json()
    text = data.get('text', '')
    
    # Simple sentiment analysis based on keywords
    positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'love', 'like']
    negative_words = ['bad', 'terrible', 'awful', 'hate', 'dislike', 'horrible']
    
    text_lower = text.lower()
    pos_count = sum(1 for word in positive_words if word in text_lower)
    neg_count = sum(1 for word in negative_words if word in text_lower)
    
    if pos_count > neg_count:
        sentiment = 'positive'
        confidence = min(0.9, 0.6 + (pos_count * 0.1))
    elif neg_count > pos_count:
        sentiment = 'negative'
        confidence = min(0.9, 0.6 + (neg_count * 0.1))
    else:
        sentiment = 'neutral'
        confidence = 0.5
    
    return jsonify({
        'success': True,
        'data': {
            'sentiment': sentiment,
            'confidence': confidence,
            'word_count': len(text.split()),
            'keywords': text.split()[:5]
        }
    }), 200

@app.route('/api/analyze/sentiment', methods=['POST'])
def analyze_sentiment():
    data = request.get_json()
    text = data.get('text', '')
    
    # Simple sentiment scoring
    positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'love', 'like', 'happy', 'joy']
    negative_words = ['bad', 'terrible', 'awful', 'hate', 'dislike', 'horrible', 'sad', 'angry']
    
    text_lower = text.lower()
    pos_score = sum(1 for word in positive_words if word in text_lower)
    neg_score = sum(1 for word in negative_words if word in text_lower)
    
    if pos_score > neg_score:
        sentiment = 'positive'
        score = min(1.0, 0.5 + (pos_score * 0.1))
    elif neg_score > pos_score:
        sentiment = 'negative'
        score = max(-1.0, -0.5 - (neg_score * 0.1))
    else:
        sentiment = 'neutral'
        score = 0.0
    
    return jsonify({
        'success': True,
        'data': {
            'sentiment': sentiment,
            'score': score
        }
    }), 200

@app.route('/api/generate/quiz', methods=['POST'])
def generate_quiz():
    data = request.get_json()
    topic = data.get('topic', 'General')
    num_questions = data.get('num_questions', 5)
    difficulty = data.get('difficulty', 'medium')
    
    # Sample quiz questions by topic
    quiz_data = {
        'Science': [
            {'q': 'What is the chemical symbol for water?', 'options': ['H2O', 'CO2', 'NaCl', 'O2'], 'answer': 'H2O'},
            {'q': 'What planet is closest to the Sun?', 'options': ['Venus', 'Mercury', 'Earth', 'Mars'], 'answer': 'Mercury'},
            {'q': 'What gas do plants absorb from the atmosphere?', 'options': ['Oxygen', 'Nitrogen', 'Carbon Dioxide', 'Hydrogen'], 'answer': 'Carbon Dioxide'}
        ],
        'History': [
            {'q': 'In which year did World War II end?', 'options': ['1944', '1945', '1946', '1947'], 'answer': '1945'},
            {'q': 'Who was the first President of the United States?', 'options': ['Thomas Jefferson', 'John Adams', 'George Washington', 'Benjamin Franklin'], 'answer': 'George Washington'}
        ],
        'Mathematics': [
            {'q': 'What is 15 + 27?', 'options': ['42', '41', '43', '40'], 'answer': '42'},
            {'q': 'What is the square root of 64?', 'options': ['6', '7', '8', '9'], 'answer': '8'}
        ]
    }
    
    # Get questions for topic or use general questions
    questions = quiz_data.get(topic, [
        {'q': f'Sample {topic} question 1?', 'options': ['A', 'B', 'C', 'D'], 'answer': 'A'},
        {'q': f'Sample {topic} question 2?', 'options': ['A', 'B', 'C', 'D'], 'answer': 'B'}
    ])
    
    # Select random questions up to num_questions
    selected_questions = random.sample(questions, min(num_questions, len(questions)))
    
    return jsonify({
        'success': True,
        'data': {
            'topic': topic,
            'difficulty': difficulty,
            'questions': [{'question': q['q'], 'options': q['options'], 'answer': q['answer']} for q in selected_questions]
        }
    }), 200

@app.route('/api/generate/text', methods=['POST'])
def generate_text():
    data = request.get_json()
    prompt = data.get('prompt', '')
    max_length = data.get('max_length', 100)
    temperature = data.get('temperature', 0.7)
    
    # Simple text generation based on prompt
    templates = [
        f"Based on '{prompt}', here's an interesting perspective: This topic relates to many aspects of modern life and technology.",
        f"Regarding '{prompt}': This is a fascinating subject that has evolved significantly over time.",
        f"When considering '{prompt}', it's important to understand the various factors involved."
    ]
    
    generated_text = random.choice(templates)[:max_length]
    
    return jsonify({
        'success': True,
        'data': {
            'text': generated_text,
            'prompt': prompt,
            'length': len(generated_text)
        }
    }), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    print(f"Starting Enhanced AI Service on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)