from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB

db = SQLAlchemy()

class AnalysisHistory(db.Model):
    __tablename__ = 'analysis_history'
    
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(2048), nullable=False)
    accessibility_issues = db.Column(JSONB)
    color_issues = db.Column(JSONB)
    success = db.Column(db.Boolean, default=True)
    error_message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'url': self.url,
            'accessibility_issues': self.accessibility_issues,
            'color_issues': self.color_issues,
            'success': self.success,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat()
        }
