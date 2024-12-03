import os
from flask import Flask, render_template, request, jsonify
from utils.html_parser import HTMLParser
from utils.accessibility_checker import AccessibilityChecker
from utils.color_validator import ColorValidator

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "a11y-checker-secret-key"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        # Parse HTML content
        parser = HTMLParser(url)
        html_content = parser.get_content()
        
        # Initialize checkers
        a11y_checker = AccessibilityChecker(html_content)
        color_validator = ColorValidator(html_content)
        
        # Perform analysis
        a11y_issues = a11y_checker.analyze()
        color_issues = color_validator.validate()
        
        # Combine results
        results = {
            'accessibility': a11y_issues,
            'colors': color_issues,
            'url': url
        }
        
        return render_template('report.html', results=results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
