from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB

db = SQLAlchemy()

class AnalysisHistory(db.Model):
    __tablename__ = 'analysis_history'
    
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(2048), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    accessibility_issues = db.Column(JSONB)
    color_issues = db.Column(JSONB)
    success = db.Column(db.Boolean, default=True)
    error_message = db.Column(db.String(500))
