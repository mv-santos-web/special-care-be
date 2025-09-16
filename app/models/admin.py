from app.extensions import db
from app.models.user import User

class Admin(User):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    is_active = db.Column(db.Boolean, nullable=True, default=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }
    