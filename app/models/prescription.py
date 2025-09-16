from app.extensions import db

from datetime import datetime
import hashlib

class Prescription(db.Model):
    __tablename__ = 'prescriptions'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    medic_id = db.Column(db.Integer, db.ForeignKey('medics.id'))
    
    data = db.Column(db.JSON, nullable=False, default={})
    validation_code = db.Column(db.String(100), unique=True, nullable=False)
    
    # Update to use back_populates to match the Patient model
    patient = db.relationship('Patient', back_populates='prescriptions', lazy=True, uselist=False)
    medic = db.relationship('Medic', back_populates='prescriptions', lazy=True, uselist=False)
    status = db.Column(db.String(20), nullable=False, default="signed")
    
    pdf_path = db.Column(db.String(255), nullable=False)
    
    created_date = db.Column(db.DateTime, default=datetime.now())
    updated_date = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    
    
    
    def __repr__(self):
        return f'<Prescription {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'medic_id': self.medic_id,
            'recipe_metadata': self.data,
            'validation_code': self.validation_code,
            'patient': self.patient.to_dict(),
            'medic': self.medic.to_dict(),
            'status': self.status,
            'pdf_path': self.pdf_path,
            'created_date': self.created_date.strftime('%d-%m-%Y %H:%M:%S'),
            'updated_date': self.updated_date.strftime('%d-%m-%Y %H:%M:%S')
        }