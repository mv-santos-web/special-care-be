from app.models.patient import Patient
from app.models.medic_record import MedicRecord
from app.models.consult import Consult
from app.models.user import User
from app.models.nurse import Nurse
from app.models.paramedic import Paramedic

from app.models.patient_request_consult import RequestCare as PatientRequestConsult
from app.models.patient_request_emergency import RequestSos as PatientRequestEmergency    
from app.models.nurse_request_consult import RequestConsult as NurseRequestConsult
from app.models.nurse_request_emergency import RequestEmergency as NurseRequestEmergency

from app.extensions import db
from app.services.firebase_service import FirebaseService
from app.services.fcm_service import FCMService

from sqlalchemy import or_
from datetime import datetime

firebase_service = FirebaseService()
fcm_service = FCMService()

class NurseService:

    def __init__(self):
        self.firebase_service = firebase_service
        self.fcm_service = fcm_service
    
    def auth_nurse(self, email, password):
        try:
            check_nurse = User.query.filter_by(email=email).first()
            if check_nurse and check_nurse.check_password(password):
                return check_nurse
            else:
                raise Exception("Invalid email or password")
        except Exception as e:
            raise e
    
    def sign_up_nurse(self, **kwargs):
        try:    
            
            cpf = kwargs.get('cpf')
            check_cpf = Nurse.query.filter_by(cpf=cpf).first()
            if check_cpf:
                raise Exception("CPF already exists")
            
            email = kwargs.get('email')
            check_email = Nurse.query.filter_by(email=email).first()
            if check_email:
                raise Exception("Email already exists")
        
            nurse = Nurse(**kwargs)
            nurse.set_password(kwargs.get('password'))
            db.session.add(nurse)
            db.session.commit()
            return nurse.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e
    
    def edit_nurse(self, nurse_id, **kwargs):
        try:
            nurse = Nurse.query.filter_by(id=nurse_id).first()
            if not nurse:
                raise Exception("Nurse not found")
            
            if kwargs.get('fullname') and kwargs.get('fullname') != "":
                nurse.fullname = kwargs.get('fullname')
            if kwargs.get('cpf') and kwargs.get('cpf') != "":
                nurse.cpf = kwargs.get('cpf')
            if kwargs.get('email') and kwargs.get('email') != "":
                nurse.email = kwargs.get('email')
            if kwargs.get('phone') and kwargs.get('phone') != "":
                nurse.phone = kwargs.get('phone')
            if kwargs.get('address') and kwargs.get('address') != "":
                nurse.address = kwargs.get('address')
            if kwargs.get('birthdate') and kwargs.get('birthdate') != "":
                nurse.birthdate = kwargs.get('birthdate')
            if kwargs.get('gender') and kwargs.get('gender') != "":
                nurse.gender = kwargs.get('gender')
            if kwargs.get('password') and kwargs.get('password') != "":
                nurse.set_password(kwargs.get('password'))
            if kwargs.get('healt_info') and kwargs.get('healt_info') != "":
                nurse.healt_info = kwargs.get('healt_info')
            
            db.session.commit()
            return nurse.to_dict()
            
        except Exception as e:
            db.session.rollback()
            raise e
    
    def create_request_consult(self, nurse_id, patient_id, observations, consult_type, consult_date):
        try:
            nurse = Nurse.query.filter_by(id=nurse_id).first()
            patient = Patient.query.filter_by(id=patient_id).first()
            if not nurse or not patient:
                raise Exception("Nurse or Patient not found")
            consult_date = consult_date.replace("T", " ")
            consult_date = datetime.strptime(consult_date, "%Y-%m-%d %H:%M")
            
            nurse_request_consult = NurseRequestConsult(nurse_id=nurse_id, patient_id=patient_id, observations=observations, consult_type=consult_type, date=consult_date)
            nurse_request_consult.status = "pending"
            request_id = db.session.add(nurse_request_consult)
            db.session.commit()
            
            self.firebase_service.save_request_consult_medic(
                id=request_id,
                patient_fullname=patient.fullname,
                observations=observations,
                status="pending",
                created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                updated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            return nurse_request_consult.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e
    
    def create_request_emergency(self, nurse_id, patient_id, **kwargs):
        try:
            nurse = Nurse.query.filter_by(id=nurse_id).first()
            patient = Patient.query.filter_by(id=patient_id).first()
            
            if not nurse or not patient:
                raise Exception("Nurse or Patient not found")
            
            if not kwargs.get('severity') or kwargs.get('severity') == "":
                raise Exception("Severity is required")
            
            if not kwargs.get('emergency_type') or kwargs.get('emergency_type') == "":
                raise Exception("Emergency type is required")
            
            request_sos = NurseRequestEmergency(
                nurse_id=nurse_id,
                patient_id=patient_id,
                severity=kwargs.get('severity'),
                emergency_type=kwargs.get('emergency_type'),
                status="pending",
            )
            
            db.session.add(request_sos)
            db.session.commit()
            
            # self.firebase_service.save_request_emergency(
            #     id=request_sos.id,
            #     patient_fullname=patient.fullname,
            #     status="pending",
            #     created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            #     updated_at=datetime.now()   .strftime("%Y-%m-%d %H:%M:%S")
            # )
            return request_sos.to_dict()      
        except Exception as e:
            db.session.rollback()
            raise e
    
    def get_medical_record(self, patient_id):
        try:
            medical_record = MedicRecord.query.filter_by(patient_id=patient_id).first()
            return medical_record.to_dict()
        except Exception as e:
            raise e
    
    def get_consults(self, patient_id):
        try:
            consults = Consult.query.filter_by(patient_id=patient_id).all()
            return [consult.to_dict() for consult in consults]
        except Exception as e:
            raise e
    
    def get_consult(self, consult_id):
        try:
            consult = Consult.query.filter_by(id=consult_id).first()
            if not consult:
                raise Exception("Consult not found")
            return consult.to_dict()
        except Exception as e:
            raise e    
    
    def get_active_request_consult(self, nurse_id):
        try:
            requests = PatientRequestConsult.query.filter(or_(PatientRequestConsult.nurse_id == None, PatientRequestConsult.nurse_id == nurse_id)).all()
            return [request.to_dict() for request in requests]
        except Exception as e:
            raise e
    
    def get_active_request_emergency(self, nurse_id):
        try:
            requests = PatientRequestEmergency.query.filter(or_(PatientRequestEmergency.nurse_id == None, PatientRequestEmergency.nurse_id == nurse_id)).all()
            return [request.to_dict() for request in requests]
        except Exception as e:
            raise e

    def delete_nurse(self, nurse_id):
        try:
            nurse = Nurse.query.filter_by(id=nurse_id).first()
            if not nurse:
                raise Exception("Nurse not found")
            
            if nurse.rg_image:
                os.remove(nurse.rg_image)
            
            if nurse.nurse_photo:
                os.remove(nurse.nurse_photo)
                
            db.session.delete(nurse)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e

    def accept_request_consult(self, request_consult_id, nurse_id):
        try:
            request_consult = PatientRequestConsult.query.filter_by(id=request_consult_id).first()
            if not request_consult:
                raise Exception("Request consult not found")
            
            if request_consult.nurse_id:
                raise Exception("Request consult already accepted")
            
            patient = User.query.get(request_consult.patient_id)
            
            request_consult.nurse_id = nurse_id
            request_consult.status = "accepted"
            db.session.commit()
            
            self.fcm_service.notify_user(
                title="Solicitação de consulta aceita",
                message="Um de nossos enfermeiros acabou de aceitar sua solicitação de consulta, acesse o app para ser atendido.",
                user_id=patient.fcm_token,
                data={
                    'update': 'consult_cares'
                }
            )
            return request_consult.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e

    def cancel_request_consult(self, request_consult_id):
        try:
            request_consult = PatientRequestConsult.query.filter_by(id=request_consult_id).first()
            if not request_consult:
                raise Exception("Request consult not found")
            
            request_consult.status = "cancelled"
            db.session.commit()
            
            patient = User.query.get(request_consult.patient_id)
            
            self.fcm_service.notify_user(
                title="Solicitação de consulta cancelada",
                message="Um de nossos enfermeiros acabou de cancelar sua solicitação de consulta, acesse o app para mais informações.",
                user_id=patient.fcm_token,
                data={
                    'update': 'consult_cares'
                }
            )
            
            return request_consult.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e

    def attend_request_consult(self, request_consult_id):
        try:
            request_consult = PatientRequestConsult.query.filter_by(id=request_consult_id).first()
            if not request_consult:
                raise Exception("Request consult not found")
            
            request_consult.status = "in_progress"
            db.session.commit()
            
            patient = User.query.get(request_consult.patient_id)
            
            self.fcm_service.notify_user(
                title="O enfermeiro esta prestes a atendê-lo",
                message="Um de nossos enfermeiros esta prestes a atendê-lo, acesse o app para mais informações.",
                user_id=patient.fcm_token,
                data={
                    'update': 'consult_cares'
                }
            )
            
            return request_consult.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e

    def finish_request_consult(self, request_consult_id):
        try:
            request_consult = PatientRequestConsult.query.filter_by(id=request_consult_id).first()
            if not request_consult:
                raise Exception("Request consult not found")
            
            request_consult.status = "finished"
            db.session.commit()
            
            patient = User.query.get(request_consult.patient_id)
            
            self.fcm_service.notify_user(
                title="O enfermeiro finalizou a con sulta",
                message="Um de nossos enfermeiros finalizou a consulta, acesse o app para mais informações.",
                user_id=patient.fcm_token,
                data={
                    'update': 'consult_cares'
                }
            )
            
            return request_consult.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e

    def get_requests_consult_data(self, request_consult_id):
        try:
            request_consult = PatientRequestConsult.query.filter_by(id=request_consult_id).first()
            if not request_consult:
                raise Exception("Request consult not found")
            return request_consult.to_dict()
        except Exception as e:
            raise e

    def get_requests_care(self, nurse_id):
        try:
            requests = PatientRequestCare.query.filter_by(nurse_id=nurse_id).all()
            return [request.to_dict() for request in requests]
        except Exception as e:
            raise e

    def get_medic_records(self):
        try:
            medic_records = MedicRecord.query.all()
            return [medic_record.to_dict() for medic_record in medic_records]
        except Exception as e:
            raise e
    
    def get_request_emergency_data(self, request_emergency_id):
        try:
            request_emergency = PatientRequestEmergency.query.filter_by(id=request_emergency_id).first()
            if not request_emergency:
                raise Exception("Request emergency not found")
            return request_emergency
        except Exception as e:
            raise e
    
    def get_request_emergency(self, request_emergency_id):
        try:
            request_emergency = PatientRequestEmergency.query.filter_by(id=request_emergency_id).first()
            if not request_emergency:
                raise Exception("Request emergency not found")
            return request_emergency
        except Exception as e:
            raise e
    
    def accept_request_emergency(self, request_emergency_id, nurse_id):
        try:
            request_emergency = db.session.query(PatientRequestEmergency).filter_by(id=request_emergency_id).first()
            if not request_emergency:
                raise Exception("Request emergency not found")
            
            request_emergency.nurse_id = nurse_id
            request_emergency.status = "accepted"
            db.session.commit()
            
            patient = User.query.get(request_emergency.patient_id)
            
            self.fcm_service.notify_user(
                title="O enfermeiro aceitou sua solicitação de emergência",
                message="Um de nossos enfermeiros aceitou sua solicitação de emergência, acesse o app para mais informações.",
                user_id=patient.fcm_token,
                data={
                    'update': 'consult_sos'
                }
            )
            
            return request_emergency.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e
        
    def cancel_request_emergency(self, request_emergency_id):
        try:
            request_emergency = db.session.query(PatientRequestEmergency).filter_by(id=request_emergency_id).first()
            if not request_emergency:
                raise Exception("Request emergency not found")
            
            request_emergency.status = "cancelled"
            db.session.commit()
            
            patient = User.query.get(request_emergency.patient_id)
            
            self.fcm_service.notify_user(
                title="Solicitação de emergência cancelada",
                message="Um de nossos enfermeiros acabou de cancelar sua solicitação de emergência, acesse o app para mais informações.",
                user_id=patient.fcm_token,
                data={
                    'update': 'consult_sos'
                }
            )
            
            return request_emergency.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e  
    
    def attend_request_emergency(self, request_emergency_id):
        try:
            request_emergency = db.session.query(PatientRequestEmergency).filter_by(id=request_emergency_id).first()
            if not request_emergency:
                raise Exception("Request emergency not found")
            
            request_emergency.status = "in_progress"
            db.session.commit()
            
            patient = User.query.get(request_emergency.patient_id)
            
            self.fcm_service.notify_user(
                title="O enfermeiro esta prestes a atendê-lo",
                message="Um de nossos enfermeiros esta prestes a atendê-lo, acesse o app para mais informações.",
                user_id=patient.fcm_token,
                data={
                    'update': 'consult_sos'
                }
            )
            
            return request_emergency.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e
        
    def finish_request_emergency(self, request_emergency_id):
        try:
            request_emergency = db.session.query(PatientRequestEmergency).filter_by(id=request_emergency_id).first()
            if not request_emergency:
                raise Exception("Request emergency not found")
            
            request_emergency.status = "finished"
            db.session.commit()
            
            patient = User.query.get(request_emergency.patient_id)
            
            self.fcm_service.notify_user(
                title="O enfermeiro finalizou a emergência",
                message="Um de nossos enfermeiros finalizou a emergência, acesse o app para mais informações.",
                user_id=patient.fcm_token,
                data={
                    'update': 'consult_sos'
                }
            )
            
            return request_emergency.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e   
    
    def notify_paramedics(self, request_emergency_id):
        try:
            request_emergency = db.session.query(PatientRequestEmergency).filter_by(id=request_emergency_id).first()
            if not request_emergency:
                raise Exception("Request emergency not found")
            
            paramedics = User.query.filter_by(type="paramedic").all()
            
            for paramedic in paramedics:
                self.fcm_service.notify_user(
                    title="Nova emergência",
                    message="Um paciente acabou de solicitar uma emergência !",
                    user_id=paramedic.fcm_token,
                    data={
                        'update': 'consult_sos'
                    }
                )
            
            return True
        except Exception as e:
            raise e