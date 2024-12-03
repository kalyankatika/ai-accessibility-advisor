import os
from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
import concurrent.futures
from urllib.parse import urlparse

from utils.html_parser import HTMLParser
from utils.accessibility_checker import AccessibilityChecker
from utils.color_validator import ColorValidator
from utils.custom_rules import CustomRule
from models import db, AnalysisHistory

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "a11y-checker-secret-key"

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Initialize database
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/history')
def history():
    analyses = AnalysisHistory.query.order_by(AnalysisHistory.timestamp.desc()).all()
    return render_template('history.html', history=analyses)

@app.route('/history/<int:analysis_id>')
def view_analysis(analysis_id):
    analysis = AnalysisHistory.query.get_or_404(analysis_id)
    return render_template('report.html', batch_results=[{
        'url': analysis.url,
        'success': analysis.success,
        'error': analysis.error_message if not analysis.success else None,
        'accessibility': analysis.accessibility_issues,
        'colors': analysis.color_issues
    }])

@app.route('/custom-rules-page')
def custom_rules_page():
    return render_template('custom_rules.html')

# Store a11y checker instance globally for custom rules
global_checker = AccessibilityChecker("<html></html>")

def analyze_single_url(url):
    try:
        # Parse HTML content
        parser = HTMLParser(url)
        html_content = parser.get_content()
        
        # Initialize checkers
        color_validator = ColorValidator(html_content)
        
        # Use global checker for accessibility checks
        global_checker.soup = BeautifulSoup(html_content, 'html.parser')
        a11y_issues = global_checker.analyze()
        color_issues = color_validator.validate()
        
        # Store analysis in database
        analysis = AnalysisHistory(
            url=url,
            accessibility_issues=a11y_issues,
            color_issues=color_issues,
            success=True
        )
        db.session.add(analysis)
        db.session.commit()
        
        return {
            'accessibility': a11y_issues,
            'colors': color_issues,
            'url': url,
            'success': True
        }
    except Exception as e:
        # Store failed analysis
        analysis = AnalysisHistory(
            url=url,
            success=False,
            error_message=str(e)
        )
        db.session.add(analysis)
        db.session.commit()
        
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

@app.route('/custom-rules', methods=['GET'])
def list_custom_rules():
    rules = []
    for rule in global_checker.custom_rule_manager.rules:
        rules.append({
            'name': rule.name,
            'description': rule.description,
            'selector': rule.selector,
            'condition': rule.condition,
            'message': rule.message,
            'recommendation': rule.recommendation,
            'severity': rule.severity
        })
    return jsonify(rules)

@app.route('/custom-rules', methods=['POST'])
def create_custom_rule():
    try:
        data = request.json
        required_fields = ['name', 'description', 'selector', 'condition', 'message', 'recommendation']
        
        # Validate required fields
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
                
        # Create new rule
        rule = CustomRule(
            name=data['name'],
            description=data['description'],
            selector=data['selector'],
            condition=data['condition'],
            message=data['message'],
            recommendation=data['recommendation'],
            severity=data.get('severity', 'warning')
        )
        
        # Add rule to checker
        global_checker.add_custom_rule(rule)
        
        return jsonify({'message': 'Custom rule created successfully'}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/custom-rules/<rule_name>', methods=['DELETE'])
def delete_custom_rule(rule_name):
    try:
        global_checker.remove_custom_rule(rule_name)
        return jsonify({'message': 'Custom rule deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400