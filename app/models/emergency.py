from app.extensions import db
from datetime import datetime

class Emergency(db.Model):
    __tablename__ = 'emergencies'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), nullable=False)
    
    sollicitation_date = db.Column(db.DateTime, nullable=False)
    severity = db.Column(db.String(20), nullable=True, default="low")
    emergency_type = db.Column(db.String(20), nullable=True, default="normal")
    observations = db.Column(db.String(255), nullable=True)
    
    accepted_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, nullable=True, default=datetime.now(), onupdate=datetime.now())
    
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    patient = db.relationship('Patient', back_populates='emergencies', lazy=True, uselist=False)
    
    paramedic_id = db.Column(db.Integer, db.ForeignKey('paramedics.id'), nullable=True)
    paramedic = db.relationship('Paramedic', back_populates='emergencies', lazy=True, uselist=False)
    
    def __repr__(self):
        return f'<Emergency {self.id}>'
    
    def to_dict(self):
        
        result = {
            'id': self.id,
            'status': self.status,
            'sollicitation_date': self.sollicitation_date,
            'severity': self.severity,
            'emergency_type': self.emergency_type,
            'observations': self.observations,
            'accepted_at': self.accepted_at,
            'patient': self.patient.to_dict() if self.patient else None,
            'paramedic': self.paramedic.to_dict() if self.paramedic else None,
            'created_at': datetime.strftime(self.created_at, '%d/%m/%Y %H:%M:%S'),
            'updated_at': datetime.strftime(self.updated_at, '%d/%m/%Y %H:%M:%S')
        }
        
        return result
