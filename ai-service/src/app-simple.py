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
    return jsonify({
        'success': True,
        'message': 'Quiz generation endpoint (simplified)',
        'data': {'questions': [{'question': 'Sample question?', 'options': ['A', 'B', 'C', 'D'], 'answer': 'A'}]}
    }), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    print(f"Starting AI Service on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)