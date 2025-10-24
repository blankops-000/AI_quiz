from flask import Flask, jsonify
from flask_cors import CORS
import os

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
    return jsonify({
        'success': True,
        'message': 'Text analysis endpoint (simplified)',
        'data': {'sentiment': 'positive', 'confidence': 0.8}
    }), 200

@app.route('/api/generate/quiz', methods=['POST'])
def generate_quiz():
    from flask import request
    data = request.get_json() or {}
    topic = data.get('topic', 'General Knowledge')
    count = data.get('count', 5)
    
    questions = generate_actual_questions(topic, count)
    
    return jsonify({
        'success': True,
        'message': f'Generated {len(questions)} questions on {topic}',
        'data': {'questions': questions}
    }), 200

def generate_actual_questions(topic, count):
    question_templates = {
        'Mathematics': [
            {'q': 'What is 15 + 27?', 'opts': ['42', '41', '43', '40'], 'ans': '42'},
            {'q': 'What is 8 × 7?', 'opts': ['56', '54', '58', '52'], 'ans': '56'},
            {'q': 'What is 144 ÷ 12?', 'opts': ['12', '11', '13', '10'], 'ans': '12'},
            {'q': 'What is the square root of 64?', 'opts': ['8', '7', '9', '6'], 'ans': '8'},
            {'q': 'What is 25% of 80?', 'opts': ['20', '18', '22', '16'], 'ans': '20'}
        ],
        'Science': [
            {'q': 'What is the chemical symbol for water?', 'opts': ['H2O', 'CO2', 'O2', 'H2'], 'ans': 'H2O'},
            {'q': 'How many planets are in our solar system?', 'opts': ['8', '7', '9', '10'], 'ans': '8'},
            {'q': 'What gas do plants absorb from the atmosphere?', 'opts': ['Carbon dioxide', 'Oxygen', 'Nitrogen', 'Hydrogen'], 'ans': 'Carbon dioxide'},
            {'q': 'What is the speed of light?', 'opts': ['299,792,458 m/s', '300,000,000 m/s', '299,000,000 m/s', '298,000,000 m/s'], 'ans': '299,792,458 m/s'},
            {'q': 'What is the hardest natural substance?', 'opts': ['Diamond', 'Gold', 'Iron', 'Quartz'], 'ans': 'Diamond'}
        ],
        'History': [
            {'q': 'In which year did World War II end?', 'opts': ['1945', '1944', '1946', '1943'], 'ans': '1945'},
            {'q': 'Who was the first President of the United States?', 'opts': ['George Washington', 'John Adams', 'Thomas Jefferson', 'Benjamin Franklin'], 'ans': 'George Washington'},
            {'q': 'Which empire was ruled by Julius Caesar?', 'opts': ['Roman Empire', 'Greek Empire', 'Egyptian Empire', 'Persian Empire'], 'ans': 'Roman Empire'},
            {'q': 'In which year did the Berlin Wall fall?', 'opts': ['1989', '1988', '1990', '1987'], 'ans': '1989'},
            {'q': 'Who discovered America in 1492?', 'opts': ['Christopher Columbus', 'Vasco da Gama', 'Ferdinand Magellan', 'Marco Polo'], 'ans': 'Christopher Columbus'}
        ]
    }
    
    # Get questions for the topic or use general knowledge
    topic_questions = question_templates.get(topic, question_templates['Mathematics'])
    
    # Return requested number of questions
    import random
    selected = random.sample(topic_questions, min(count, len(topic_questions)))
    
    return [{
        'question': q['q'],
        'options': q['opts'],
        'answer': q['ans']
    } for q in selected]

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    print(f"Starting AI Service on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)