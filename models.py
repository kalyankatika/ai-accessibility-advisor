from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB

db = SQLAlchemy()

class AnalysisHistory(db.Model):
    __tablename__ = 'analysis_history'
    
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(2048), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    accessibility_issues = db.Column(JSONB)
    color_issues = db.Column(JSONB)
    success = db.Column(db.Boolean, default=True)
    error_message = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'url': self.url,
            'created_at': self.created_at.isoformat(),
            'accessibility_issues': self.accessibility_issues,
            'color_issues': self.color_issues,
            'success': self.success,
            'error_message': self.error_message
        }

class IssueMetrics(db.Model):
    __tablename__ = 'issue_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(2048), nullable=False)
    date = db.Column(db.Date, nullable=False)
    total_issues = db.Column(db.Integer, default=0)
    error_count = db.Column(db.Integer, default=0)
    warning_count = db.Column(db.Integer, default=0)
    category_counts = db.Column(JSONB)

    def to_dict(self):
        return {
            'id': self.id,
            'url': self.url,
            'date': self.date.isoformat(),
            'total_issues': self.total_issues,
            'error_count': self.error_count,
            'warning_count': self.warning_count,
            'category_counts': self.category_counts
        }
