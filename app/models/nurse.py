from app.extensions import db
from app.models.user import User

class Nurse(User):
    __tablename__ = 'nurses'
    __mapper_args__ = {
        'polymorphic_identity': 'nurse'
    }
    
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    coren = db.Column(db.String(80), nullable=False, unique=True)
    
    rg_image = db.Column(db.String(255))
    nurse_photo = db.Column(db.String(255))
    
    requests_care = db.relationship('RequestCare', back_populates='nurse', lazy='dynamic')
    requests_consult = db.relationship('RequestConsult', back_populates='nurse', lazy='dynamic')
    requests_emergency = db.relationship('RequestEmergency', back_populates='nurse', lazy='dynamic')
    requests_sos = db.relationship('RequestSos', back_populates='nurse', lazy='dynamic')
    
    def __repr__(self):
        return f'<Nurse {self.fullname}>'
