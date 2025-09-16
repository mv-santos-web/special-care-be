from app.extensions import db
from app.models.user import User

class Patient(User):
    __tablename__ = 'patients'
    __mapper_args__ = {
        'polymorphic_identity': 'patient'
    }
    
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    consults = db.relationship('Consult', back_populates='patient', lazy='dynamic')
    emergencies = db.relationship('Emergency', back_populates='patient', lazy='dynamic')
    medic_records = db.relationship('MedicRecord', back_populates='patient', lazy='dynamic')
    
    # Define the relationship with back_populates instead of backref
    prescriptions = db.relationship('Prescription', back_populates='patient', lazy='dynamic')
    
    requests_care = db.relationship('RequestCare', back_populates='patient', lazy='dynamic')
    requests_consult = db.relationship('RequestConsult', back_populates='patient', lazy='dynamic')
    requests_emergency = db.relationship('RequestEmergency', back_populates='patient', lazy='dynamic')
    requests_sos = db.relationship('RequestSos', back_populates='patient', lazy='dynamic')
    
    rg_image_path = db.Column(db.String(255), nullable=True)
    patient_photo_path = db.Column(db.String(255), nullable=True)
    healt_info = db.Column(db.JSON, nullable=True, default={"weight": "0", "height": "0", "imc": "0"})
    current_location = db.Column(db.JSON, nullable=True)
    
    def __repr__(self):
        return f'<Patient id={self.id} fullname={self.fullname}>'
    
