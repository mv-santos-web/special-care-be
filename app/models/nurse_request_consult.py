from app.extensions import db
from datetime import datetime

class RequestConsult(db.Model):
    __tablename__ = "request_consult"
    id = db.Column(db.Integer, primary_key=True)
    
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    nurse_id = db.Column(db.Integer, db.ForeignKey("nurses.id"), nullable=False)
    medic_id = db.Column(db.Integer, db.ForeignKey("medics.id"), nullable=True)
    
    consult_type = db.Column(db.String(80), nullable=False, default='teleconsulta')
    status = db.Column(db.String(50), nullable=False, default="pending")
    observations = db.Column(db.String(255), nullable=False)
    accepted_at = db.Column(db.DateTime, nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    
    patient = db.relationship("Patient", back_populates="requests_consult", lazy=True, uselist=False)
    nurse = db.relationship("Nurse", back_populates="requests_consult", lazy=True, uselist=False)
    medic = db.relationship("Medic", back_populates="requests_consult", lazy=True, uselist=False)
    
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())

    def to_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "nurse_id": self.nurse_id,
            "consult_type": self.consult_type,
            "date": self.date.strftime('%d/%m/%Y %H:%M:%S'),
            "medic_id": self.medic_id,
            "observations": self.observations,
            "accepted_at": self.accepted_at.strftime('%d/%m/%Y %H:%M:%S') if self.accepted_at else None,
            "status": self.status,
            "patient": self.patient.to_dict() if self.patient else None,
            "nurse": self.nurse.to_dict() if self.nurse else None,
            "medic": self.medic.to_dict() if self.medic else None,
            "created_at": self.created_at.strftime('%d/%m/%Y %H:%M:%S'),
            "updated_at": self.updated_at.strftime('%d/%m/%Y %H:%M:%S')
        }
    
    def __repr__(self):
        return f"<RequestConsult {self.id}>"