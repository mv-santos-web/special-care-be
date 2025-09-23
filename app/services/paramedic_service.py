from app.models.user import User
from app.models.paramedic import Paramedic

from app.models.nurse_request_emergency import RequestEmergency as NurseRequestEmergency

from app.extensions import db
from app.services.firebase_service import FirebaseService
from app.services.fcm_service import FCMService

from sqlalchemy import or_
from datetime import datetime

firebase_service = FirebaseService()
fcm_service = FCMService()

class ParamedicService:

    def __init__(self):
        self.firebase_service = firebase_service
        self.fcm_service = fcm_service
    
    def auth_paramedic(self, email, password):
        try:
            check_paramedic = User.query.filter_by(email=email).first()
            if check_paramedic and check_paramedic.check_password(password) and check_paramedic.active and check_paramedic.type == "paramedic":
                return check_paramedic
            else:
                raise Exception("Invalid email or password")
        except Exception as e:
            raise e
    
    def update_location(self, paramedic_id, location_data):
        try:
            paramedic = Paramedic.query.filter_by(id=paramedic_id).first()
            if not paramedic:
                raise Exception("Paramedic not found")
            
            loc_data = {"latitude": location_data['latitude'], "longitude": location_data['longitude']}
            
            paramedic.current_location = loc_data
            db.session.commit()
            return paramedic.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e
    
    def update_fcm_token(self, paramedic_id, token):
        try:
            paramedic = User.query.filter_by(id=paramedic_id).first()
            if not paramedic:
                raise Exception("Paramedic not found")
            
            paramedic.fcm_token = token['token']
            db.session.commit()
            return paramedic.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e
    
    def sign_up_paramedic(self, **kwargs):
        try:    
            
            cpf = kwargs.get('cpf')
            check_cpf = User.query.filter_by(cpf=cpf).first()
            if check_cpf:
                raise Exception("CPF already exists")
            
            email = kwargs.get('email')
            check_email = User.query.filter_by(email=email).first()
            if check_email:
                raise Exception("Email already exists")
        
            medic = Paramedic(**kwargs)
            medic.set_password(kwargs.get('password'))
            db.session.add(medic)
            db.session.commit()
            return medic.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e
    
    def edit_paramedic(self, paramedic_id, **kwargs):
        try:
            paramedic = Paramedic.query.filter_by(id=paramedic_id).first()
            if not paramedic:
                raise Exception("Paramedic not found")
            
            if kwargs.get('fullname') and kwargs.get('fullname') != "":
                paramedic.fullname = kwargs.get('fullname')
            if kwargs.get('cpf') and kwargs.get('cpf') != "":
                paramedic.cpf = kwargs.get('cpf')
            if kwargs.get('email') and kwargs.get('email') != "":
                paramedic.email = kwargs.get('email')
            if kwargs.get('phone') and kwargs.get('phone') != "":
                paramedic.phone = kwargs.get('phone')
            if kwargs.get('address') and kwargs.get('address') != "":
                paramedic.address = kwargs.get('address')
            if kwargs.get('birthdate') and kwargs.get('birthdate') != "":
                paramedic.birthdate = kwargs.get('birthdate')
            if kwargs.get('gender') and kwargs.get('gender') != "":
                paramedic.gender = kwargs.get('gender')
            if kwargs.get('password') and kwargs.get('password') != "":
                paramedic.set_password(kwargs.get('password'))
            
            db.session.commit()
            return paramedic.to_dict()
            
        except Exception as e:
            db.session.rollback()
            raise e
    
    def get_active_request_emergency(self, paramedic_id):
        try:
            requests = NurseRequestEmergency.query.filter(or_(NurseRequestEmergency.paramedic_id == None, NurseRequestEmergency.paramedic_id == paramedic_id)).filter(
                or_(NurseRequestEmergency.status == "pending", NurseRequestEmergency.status == "accepted", NurseRequestEmergency.status == "arrived")
            ).all()
            return [request.to_dict() for request in requests]
        except Exception as e:
            raise e
    
    def delete_paramedic(self, paramedic_id):
        try:
            paramedic = Paramedic.query.filter_by(id=paramedic_id).first()
            if not paramedic:
                raise Exception("Paramedic not found")
            
            if paramedic.rg_image:
                os.remove(paramedic.rg_image)
            
            if paramedic.paramedic_photo:
                os.remove(paramedic.paramedic_photo)
                
            db.session.delete(paramedic)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e

    def get_emergency(self, emergency_id):
        try:
            emergency = NurseRequestEmergency.query.filter_by(id=emergency_id).first()
            return emergency
        except Exception as e:
            raise e

    def get_paramedics(self):
        try:
            paramedics = Paramedic.query.all()
            return [paramedic.to_dict() for paramedic in paramedics]
        except Exception as e:
            raise e
    
    def get_paramedic(self, paramedic_id):
        try:
            paramedic = Paramedic.query.filter_by(id=paramedic_id).first()
            return paramedic
        except Exception as e:
            raise e

    def accept_emergency(self, emergency_id, current_user_id):
        try:
            emergency = NurseRequestEmergency.query.filter_by(id=emergency_id).first()
            if not emergency:
                raise Exception("Emergency not found")
            
            emergency.paramedic_id = current_user_id
            emergency.status = "accepted"
            db.session.commit()

            paramedic = User.query.filter_by(id=current_user_id).first()
            self.fcm_service.notify_user(
                emergency.patient.fcm_token,
                "Emergencia aceita !",
                f"O {paramedic.fullname} aceitou sua emergencia!",
                {
                    "type": "update", "target": "nurse_emergency_request"
                }
            )
            return True
            
        except Exception as e:
            db.session.rollback()
            raise e

    def cancel_emergency(self, emergency_id):
        try:
            emergency = NurseRequestEmergency.query.filter_by(id=emergency_id).first()
            if not emergency:
                raise Exception("Emergency not found")
            
            emergency.status = "canceled"
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    def finish_emergency(self, emergency_id):
        try:
            emergency = NurseRequestEmergency.query.filter_by(id=emergency_id).first()
            if not emergency:
                raise Exception("Emergency not found")
            
            emergency.status = "finished"
            db.session.commit()
            
            paramedic = User.query.filter_by(id=emergency.paramedic_id).first()
            self.fcm_service.notify_user(
                emergency.patient.fcm_token,
                "Emergencia finalizada !",
                f"O {paramedic.fullname} finalizou sua emergencia!",
                {
                    "type": "update", "target": "nurse_emergency_request"
                }
            )
        except Exception as e:
            db.session.rollback()
            raise e
    
    def arrived_emergency(self, emergency_id):
        try:
            emergency = NurseRequestEmergency.query.filter_by(id=emergency_id).first()
            if not emergency:
                raise Exception("Emergency not found")
            
            emergency.status = "arrived"
            db.session.commit()
            
            paramedic = User.query.filter_by(id=emergency.paramedic_id).first()
            self.fcm_service.notify_user(
                emergency.patient.fcm_token,
                "Paramédico no local !",
                f"O {paramedic.fullname} chegou a sua localização, aguarde o atendimento!",
                {
                    "type": "update", "target": "nurse_emergency_request"
                }
            )
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    def update_location(self, paramedic_id, location):
        try:
            paramedic = Paramedic.query.filter_by(id=paramedic_id).first()
            if not paramedic:
                raise Exception("Paramedic not found")
            
            paramedic.current_location = location
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
