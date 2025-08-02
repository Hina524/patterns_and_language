from flask import Flask, render_template, send_from_directory, request, jsonify
import os
from pattern_finder import PatternFinder
from english_grammar_analyzer import EnglishGrammarAnalyzer

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/script.js')
def script():
    return send_from_directory('.', 'script.js', mimetype='application/javascript')

@app.route('/style.css')
def style():
    return send_from_directory('.', 'style.css', mimetype='text/css')

@app.route('/api/find-patterns', methods=['POST'])
def find_patterns():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        texts = data.get('texts', [])
        level = data.get('level', 1)
        
        if not texts or not isinstance(texts, list):
            return jsonify({"error": "texts must be a non-empty list"}), 400
        
        if level not in [1, 2, 3, 4]:
            return jsonify({"error": "level must be 1, 2, 3, or 4"}), 400
        
        # Initialize pattern finder
        try:
            finder = PatternFinder(level=level)
        except Exception as e:
            return jsonify({
                "error": f"Failed to initialize spaCy model: {str(e)}. Please run: python -m spacy download en_core_web_sm"
            }), 500
        
        # Analyze texts
        result = finder.analyze_texts(texts)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/api/analyze-grammar', methods=['POST'])
def analyze_grammar():
    """
    English Grammar Analyzer API endpoint
    Analyzes text for past tense conversion, sentence type, and prepositional phrases
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({"error": "text parameter is required and must not be empty"}), 400
        
        # Initialize grammar analyzer
        try:
            analyzer = EnglishGrammarAnalyzer()
        except Exception as e:
            return jsonify({
                "error": f"Failed to initialize spaCy model: {str(e)}. Please run: python -m spacy download en_core_web_sm"
            }), 500
        
        # Analyze text
        result = analyzer.analyze_text(text)
        
        if result.get('error'):
            return jsonify({"error": result['error']}), 500
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000) 