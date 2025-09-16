from app.extensions import db
from datetime import datetime

class RequestSos(db.Model):
    __tablename__ = "request_sos"
    id = db.Column(db.Integer, primary_key=True)

    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    patient = db.relationship("Patient", back_populates="requests_sos", uselist=False, lazy=True)

    nurse_id = db.Column(db.Integer, db.ForeignKey("nurses.id"), nullable=True)
    nurse = db.relationship("Nurse", back_populates="requests_sos", uselist=False, lazy=True)
    
    status = db.Column(db.String(20), nullable=False, default="pending")
    
    accepted_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f"<RequestSos {self.id}>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "nurse_id": self.nurse_id,
            "status": self.status,
            "accepted_at": self.accepted_at,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "patient": self.patient.to_dict() if self.patient else None,
            "nurse": self.nurse.to_dict() if self.nurse else None
        }


