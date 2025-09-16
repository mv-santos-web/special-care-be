from app.extensions import db
from datetime import datetime

class MedicRecord(db.Model):
    __tablename__ = 'medic_records'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    
    medic_history = db.Column(db.Text, nullable=False)
    medicines = db.Column(db.Text, nullable=False)
    observations = db.Column(db.Text)
    
    patient = db.relationship('Patient', back_populates='medic_records', lazy=True)
    
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    def to_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "medic_history": self.medic_history,
            "medicines": self.medicines,
            "observations": self.observations,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "patient": self.patient.to_dict() if self.patient else None
        }
