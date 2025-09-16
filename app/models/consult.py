from app.extensions import db
from datetime import datetime

class Consult(db.Model):
    __tablename__ = 'consults'
    id = db.Column(db.Integer, primary_key=True)
    
    medic_id = db.Column(db.Integer, db.ForeignKey('medics.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    
    consult_type = db.Column(db.String(80), nullable=False, default='teleconsulta')
    status = db.Column(db.String(80), nullable=False, default='pending')
    observations = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    create_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    update_at = db.Column(db.DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())
    
    # Relationships
    medic = db.relationship('Medic', back_populates='consults', lazy=True, uselist=False)
    patient = db.relationship('Patient', back_populates='consults', lazy=True, uselist=False)
    
    def __repr__(self):
        return f'<Consult {self.id}>'   
    
    
    def to_dict(self):
        return {
            'id': self.id,
            'medic_id': self.medic_id,
            'patient_id': self.patient_id,
            'consult_type': self.consult_type,
            'create_at': self.create_at.strftime('%d/%m/%Y %H:%M:%S'),
            'update_at': self.update_at.strftime('%d/%m/%Y %H:%M:%S'),
            'observations': self.observations,
            'date': self.date.strftime('%d/%m/%Y %H:%M:%S'),
            'status': self.status,
            'medic': self.medic.to_dict() if self.medic else None,
            'patient': self.patient.to_dict() if self.patient else None
        }
