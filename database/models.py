from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(64), nullable=False)
    role = db.Column(db.String(16), nullable=False)
    message = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(8), default="en")
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "session_id": self.session_id,
            "role": self.role,
            "message": self.message,
            "language": self.language,
            "timestamp": self.timestamp.isoformat(),
        }


class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gate = db.Column(db.String(8), nullable=False)
    alert_type = db.Column(db.String(32), nullable=False)
    severity = db.Column(db.String(16), default="info")
    message = db.Column(db.Text, nullable=False)
    ai_recommendations = db.Column(db.Text, default="")
    resolved = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "gate": self.gate,
            "alert_type": self.alert_type,
            "severity": self.severity,
            "message": self.message,
            "ai_recommendations": self.ai_recommendations,
            "resolved": self.resolved,
            "timestamp": self.timestamp.isoformat(),
        }


class SensorReading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gate = db.Column(db.String(8), nullable=False)
    density = db.Column(db.Float, default=0.0)
    queue_time = db.Column(db.Integer, default=0)
    crowd_flow = db.Column(db.String(16), default="stable")
    status = db.Column(db.String(16), default="normal")
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "gate": self.gate,
            "density": self.density,
            "queue_time": self.queue_time,
            "crowd_flow": self.crowd_flow,
            "status": self.status,
            "timestamp": self.timestamp.isoformat(),
        }
