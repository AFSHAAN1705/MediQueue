from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100))
    is_available = db.Column(db.Boolean, default=True)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    arrival_time = db.Column(db.Integer, nullable=False) # Minute of the day or epoch
    treatment_time = db.Column(db.Integer, nullable=False) # Burst time
    emergency_level = db.Column(db.Integer, default=1) # 1: Low, 5: Critical (Priority)
    status = db.Column(db.String(20), default="WAITING") # WAITING, TREATING, DISCHARGED
    
    # Metrics
    start_time = db.Column(db.Integer, nullable=True)
    completion_time = db.Column(db.Integer, nullable=True)
    turnaround_time = db.Column(db.Integer, nullable=True)
    waiting_time = db.Column(db.Integer, nullable=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "arrival_time": self.arrival_time,
            "treatment_time": self.treatment_time,
            "emergency_level": self.emergency_level,
            "status": self.status,
            "start_time": self.start_time,
            "completion_time": self.completion_time,
            "turnaround_time": self.turnaround_time,
            "waiting_time": self.waiting_time
        }
