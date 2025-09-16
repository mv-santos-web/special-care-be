from app.extensions import db
from datetime import datetime

class RequestEmergency(db.Model):
    __tablename__ = "request_emergency"
    id = db.Column(db.Integer, primary_key=True)
    
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    nurse_id = db.Column(db.Integer, db.ForeignKey("nurses.id"), nullable=False)
    paramedic_id = db.Column(db.Integer, db.ForeignKey("paramedics.id"), nullable=True)
    
    status = db.Column(db.String(20), nullable=False, default="pending")
    severity = db.Column(db.String(20), nullable=True, default="low")
    emergency_type = db.Column(db.String(20), nullable=True, default="normal")
    observations = db.Column(db.String(255), nullable=True)
    
    patient = db.relationship("Patient", back_populates="requests_emergency", lazy=True, uselist=False)
    nurse = db.relationship("Nurse", back_populates="requests_emergency", lazy=True, uselist=False)
    paramedic = db.relationship("Paramedic", back_populates="requests_emergency", lazy=True, uselist=False)
    
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())

    def to_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "nurse_id": self.nurse_id,
            "paramedic_id": self.paramedic_id,
            "severity": self.severity,
            "emergency_type": self.emergency_type,
            "observations": self.observations,
            "status": self.status,
            "patient": self.patient.to_dict() if self.patient else None,
            "nurse": self.nurse.to_dict() if self.nurse else None,
            "paramedic": self.paramedic.to_dict() if self.paramedic else None,
            "created_at": self.created_at.strftime('%d/%m/%Y %H:%M:%S'),
            "updated_at": self.updated_at.strftime('%d/%m/%Y %H:%M:%S')
        }
    
    def __repr__(self):
        return f"<RequestEmergency {self.id}>"