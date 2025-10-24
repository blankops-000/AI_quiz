from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import openai
import random

app = Flask(__name__)
CORS(app)

# Set OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY', 'your-openai-api-key-here')

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'AI Service with ChatGPT',
        'version': '2.0.0'
    }), 200

@app.route('/api/analyze/text', methods=['POST'])
def analyze_text():
    data = request.get_json()
    text = data.get('text', '')
    
    try:
        # Use ChatGPT for text analysis
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a text analysis expert. Analyze the given text and provide sentiment, key themes, and insights in JSON format."},
                {"role": "user", "content": f"Analyze this text: {text}"}
            ],
            max_tokens=200
        )
        
        analysis = response.choices[0].message.content
        
        return jsonify({
            'success': True,
            'data': {
                'analysis': analysis,
                'word_count': len(text.split()),
                'character_count': len(text)
            }
        }), 200
        
    except Exception as e:
        # Fallback to simple analysis
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
                'keywords': text.split()[:5],
                'note': 'Using fallback analysis (ChatGPT unavailable)'
            }
        }), 200

@app.route('/api/analyze/sentiment', methods=['POST'])
def analyze_sentiment():
    data = request.get_json()
    text = data.get('text', '')
    
    try:
        # Use ChatGPT for sentiment analysis
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a sentiment analysis expert. Analyze the sentiment of the given text and respond with only a JSON object containing 'sentiment' (positive/negative/neutral) and 'score' (number between -1 and 1)."},
                {"role": "user", "content": text}
            ],
            max_tokens=50
        )
        
        result = response.choices[0].message.content
        
        return jsonify({
            'success': True,
            'data': {
                'chatgpt_analysis': result,
                'text_analyzed': text
            }
        }), 200
        
    except Exception as e:
        # Fallback sentiment analysis
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
                'score': score,
                'note': 'Using fallback analysis (ChatGPT unavailable)'
            }
        }), 200

@app.route('/api/generate/quiz', methods=['POST'])
def generate_quiz():
    data = request.get_json()
    topic = data.get('topic', 'General')
    num_questions = data.get('num_questions', 5)
    difficulty = data.get('difficulty', 'medium')
    
    try:
        # Use ChatGPT for quiz generation
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a quiz generator. Create {num_questions} {difficulty} level multiple choice questions about {topic}. Return only a JSON array with objects containing 'question', 'options' (array of 4 choices), and 'answer' (correct option)."},
                {"role": "user", "content": f"Generate {num_questions} {difficulty} questions about {topic}"}
            ],
            max_tokens=800
        )
        
        quiz_content = response.choices[0].message.content
        
        return jsonify({
            'success': True,
            'data': {
                'topic': topic,
                'difficulty': difficulty,
                'questions_generated_by': 'ChatGPT',
                'quiz_data': quiz_content
            }
        }), 200
        
    except Exception as e:
        # Fallback quiz generation
        quiz_data = {
            'Science': [
                {'question': 'What is the chemical symbol for water?', 'options': ['H2O', 'CO2', 'NaCl', 'O2'], 'answer': 'H2O'},
                {'question': 'What planet is closest to the Sun?', 'options': ['Venus', 'Mercury', 'Earth', 'Mars'], 'answer': 'Mercury'}
            ],
            'History': [
                {'question': 'In which year did World War II end?', 'options': ['1944', '1945', '1946', '1947'], 'answer': '1945'},
                {'question': 'Who was the first President of the United States?', 'options': ['Thomas Jefferson', 'John Adams', 'George Washington', 'Benjamin Franklin'], 'answer': 'George Washington'}
            ]
        }
        
        questions = quiz_data.get(topic, [
            {'question': f'Sample {topic} question?', 'options': ['A', 'B', 'C', 'D'], 'answer': 'A'}
        ])
        
        selected_questions = random.sample(questions, min(num_questions, len(questions)))
        
        return jsonify({
            'success': True,
            'data': {
                'topic': topic,
                'difficulty': difficulty,
                'questions': selected_questions,
                'note': 'Using fallback quiz (ChatGPT unavailable)'
            }
        }), 200

@app.route('/api/generate/text', methods=['POST'])
def generate_text():
    data = request.get_json()
    prompt = data.get('prompt', '')
    max_length = data.get('max_length', 100)
    temperature = data.get('temperature', 0.7)
    
    try:
        # Use ChatGPT for text generation
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a creative writer. Generate text based on the given prompt. Keep it under {max_length} words."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_length * 2,
            temperature=temperature
        )
        
        generated_text = response.choices[0].message.content
        
        return jsonify({
            'success': True,
            'data': {
                'text': generated_text,
                'prompt': prompt,
                'generated_by': 'ChatGPT',
                'length': len(generated_text.split())
            }
        }), 200
        
    except Exception as e:
        # Fallback text generation
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
                'length': len(generated_text.split()),
                'note': 'Using fallback generation (ChatGPT unavailable)'
            }
        }), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    print(f"Starting AI Service with ChatGPT integration on port {port}")
    print("Note: Set OPENAI_API_KEY environment variable for full functionality")
    app.run(host='0.0.0.0', port=port, debug=True)