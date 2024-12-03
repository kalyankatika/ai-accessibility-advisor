import os
import concurrent.futures
from flask import Flask, render_template, request, jsonify
from utils.html_parser import HTMLParser
from utils.accessibility_checker import AccessibilityChecker
from utils.color_validator import ColorValidator
from urllib.parse import urlparse

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "a11y-checker-secret-key"

@app.route('/')
def index():
    return render_template('index.html')

def analyze_single_url(url):
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
        
        return {
            'accessibility': a11y_issues,
            'colors': color_issues,
            'url': url,
            'success': True
        }
    except Exception as e:
        return {
            'url': url,
            'error': str(e),
            'success': False
        }

@app.route('/analyze', methods=['POST'])
def analyze():
    urls = request.form.get('urls', '').strip().split('\n')
    urls = [url.strip() for url in urls if url.strip()]
    
    if not urls:
        return jsonify({'error': 'At least one URL is required'}), 400
        
    if len(urls) > 10:
        return jsonify({'error': 'Maximum 10 URLs allowed for batch processing'}), 400
    
    # Validate URLs
    for url in urls:
        try:
            result = urlparse(url)
            if not all([result.scheme, result.netloc]):
                return jsonify({'error': f'Invalid URL format: {url}'}), 400
        except Exception:
            return jsonify({'error': f'Invalid URL format: {url}'}), 400
    
    try:
        # Process URLs concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_url = {executor.submit(analyze_single_url, url): url for url in urls}
            results = []
            
            for future in concurrent.futures.as_completed(future_to_url):
                result = future.result()
                results.append(result)
        
        return render_template('report.html', batch_results=results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
