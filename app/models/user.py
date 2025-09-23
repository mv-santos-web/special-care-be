from app.extensions import db, login_manager

from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import json

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(80), nullable=False)
    cpf = db.Column(db.String(80), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(180), nullable=False)
    create_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    update_at = db.Column(db.DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())
    active = db.Column(db.Boolean, nullable=False, default=True)
    type = db.Column(db.String(80), nullable=False)
    fcm_token = db.Column(db.String(255), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': 'type'  # 'type' deve ser uma coluna na tabela users
    }
    
    def __repr__(self):
        return f'<User {self.fullname}>'
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def to_dict(self):
        response = {}
        response.update({
            'id': self.id,
            'fullname': self.fullname,
            'email': self.email,
            'phone': self.phone,
            'cpf': self.cpf,
            'birthdate': self.birthdate.strftime('%d/%m/%Y'),
            'age': (datetime.now().year - self.birthdate.year),
            'gender': self.gender,
            # 'password': self.password,
            'address': self.address,
            'create_at': self.create_at.strftime('%d/%m/%Y %H:%M:%S'),
            'update_at': self.update_at.strftime('%d/%m/%Y %H:%M:%S'),
            'active': self.active,
            'fcm_token': self.fcm_token,
            'type': self.type
        })
        
        if self.type == 'medic':
            response.update({
                'crm': self.crm,
                'certificate_file': self.certificate_file
            })
        
        if self.type == 'nurse':
            response.update({
                'coren': self.coren,
                'rg_image': self.rg_image,
                'nurse_photo': self.nurse_photo
            })
        
        if self.type == 'patient':
            response.update({
                'rg_image': self.rg_image_path,
                'patient_photo': self.patient_photo_path,
                'health_info': self.healt_info,
                'current_location': self.current_location
            })
            
        if self.type == 'paramedic':
            response.update({
                'rg_image': self.rg_image,
                'paramedic_photo': self.paramedic_photo,
                'current_location': self.current_location
            })
        
        return response
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
    

    
    