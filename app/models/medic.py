from app.extensions import db
from app.models.user import User

class Medic(User):
    __tablename__ = 'medics'
    __mapper_args__ = {
        'polymorphic_identity': 'medic'
    }
    
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    
    certificate_file = db.Column(db.String(180), nullable=False)
    crm = db.Column(db.String(80), nullable=False, unique=True)
    
    requests_consult = db.relationship('RequestConsult', back_populates='medic', lazy='dynamic')
    prescriptions = db.relationship('Prescription', back_populates='medic', lazy='dynamic')
    consults = db.relationship('Consult', back_populates='medic', lazy='dynamic')
    
    def __repr__(self):
        return f'<Medic {self.fullname}>'
