from app.extensions import db
from app.models.user import User

class Paramedic(User):
    __tablename__ = 'paramedics'
    __mapper_args__ = {
        'polymorphic_identity': 'paramedic'
    }
    
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    
    rg_image = db.Column(db.String(255))
    paramedic_photo = db.Column(db.String(255))
    
    requests_emergency = db.relationship('RequestEmergency', back_populates='paramedic', lazy='dynamic')
    emergencies = db.relationship('Emergency', back_populates='paramedic', lazy='dynamic')
    current_location = db.Column(db.JSON, nullable=True)
    
    def __repr__(self):
        return f'<Paramedic {self.fullname}>'

