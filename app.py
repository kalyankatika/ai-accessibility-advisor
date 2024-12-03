from flask import Flask, render_template, request, jsonify
from flask_migrate import Migrate
from urllib.parse import urlparse
import concurrent.futures
from datetime import datetime, date
from collections import Counter
import os
from bs4 import BeautifulSoup

from models import db, AnalysisHistory, IssueMetrics
from utils.html_parser import HTMLParser
from utils.accessibility_checker import AccessibilityChecker
from utils.color_validator import ColorValidator
from utils.custom_rules import CustomRule

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

# Create tables
with app.app_context():
    db.create_all()

# Initialize global accessibility checker
global_checker = AccessibilityChecker("")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    urls = request.form.get('urls', '').strip().split('\n')
    urls = [url.strip() for url in urls if url.strip()]
    
    if not urls:
        return jsonify({'error': 'No URLs provided'}), 400
    
    if len(urls) > 10:
        return jsonify({'error': 'Maximum 10 URLs allowed'}), 400
    
    # Validate URLs
    for url in urls:
        try:
            result = urlparse(url)
            if not all([result.scheme, result.netloc]):
                return jsonify({'error': f'Invalid URL format: {url}'}), 400
        except Exception:
            return jsonify({'error': f'Invalid URL format: {url}'}), 400
    
    # Process URLs concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(analyze_single_url, url): url for url in urls}
        results = []
        
        for future in concurrent.futures.as_completed(future_to_url):
            results.append(future.result())
    
    return render_template('report.html', batch_results=results)

@app.route('/history', methods=['GET'])
def view_history():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # Get paginated history
    history = AnalysisHistory.query.order_by(
        AnalysisHistory.created_at.desc()
    ).paginate(page=page, per_page=per_page)
    
    return render_template('history.html', history=history)

@app.route('/api/metrics/<path:url>', methods=['GET'])
def get_url_metrics(url):
    # Get metrics for specific URL
    metrics = IssueMetrics.query.filter_by(url=url).order_by(
        IssueMetrics.date.desc()
    ).limit(30).all()
    
    return jsonify([metric.to_dict() for metric in metrics])

@app.route('/metrics', methods=['GET'])
def view_metrics():
    # Get URLs with metrics
    urls = db.session.query(IssueMetrics.url).distinct().all()
    urls = [url[0] for url in urls]
    
    return render_template('metrics.html', urls=urls)

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
        
        # Store analysis results
        analysis = AnalysisHistory(
            url=url,
            accessibility_issues=a11y_issues,
            color_issues=color_issues,
            success=True
        )
        
        # Calculate metrics
        total_issues = len(a11y_issues) + len(color_issues)
        error_count = sum(1 for issue in a11y_issues + color_issues if issue['type'] == 'error')
        warning_count = sum(1 for issue in a11y_issues + color_issues if issue['type'] == 'warning')
        
        # Count issues by category
        category_counts = Counter()
        for issue in a11y_issues + color_issues:
            category_counts[issue['category']] += 1
        
        # Store metrics
        metrics = IssueMetrics(
            url=url,
            date=date.today(),
            total_issues=total_issues,
            error_count=error_count,
            warning_count=warning_count,
            category_counts=dict(category_counts)
        )
        
        db.session.add(analysis)
        db.session.add(metrics)
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
