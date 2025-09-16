from app.models.patient import Patient
from app.models.medic_record import MedicRecord
from app.models.consult import Consult
from app.models.prescription import Prescription
from app.models.emergency import Emergency
from app.models.user import User

from app.models.patient_request_consult import RequestCare as PatientRequestConsult
from app.models.patient_request_emergency import RequestSos as PatientRequestEmergency    
from app.models.nurse_request_consult import RequestConsult as NurseRequestConsult
from app.models.nurse_request_emergency import RequestEmergency as NurseRequestEmergency

from app.extensions import db
from app.services.firebase_service import FirebaseService

from datetime import datetime
from sqlalchemy import or_
import uuid

firebase_service = FirebaseService()

class PatientService:

    def __init__(self):
        self.firebase_service = firebase_service
    
    def auth_patient(self, email, password):
        try:
            check_patient = Patient.query.filter_by(email=email).first()
            if check_patient and check_patient.check_password(password):
                return check_patient
            else:
                raise Exception("Invalid email or password")
        except Exception as e:
            raise e
    
    def sign_up_patient(self, **kwargs):
        try:    
            
            cpf = kwargs.get('cpf')
            check_cpf = User.query.filter_by(cpf=cpf).first()
            if check_cpf:
                raise Exception("CPF already exists")
            
            email = kwargs.get('email')
            check_email = User.query.filter_by(email=email).first()
            if check_email:
                raise Exception("Email already exists")
        
            patient = Patient(**kwargs)
            patient.set_password(kwargs.get('password'))
            db.session.add(patient)
            db.session.commit()
            return patient.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e
    
    def edit_patient(self, patient_id, **kwargs):
        try:
            patient = Patient.query.filter_by(id=patient_id).first()
            if not patient:
                raise Exception("Patient not found")
            
            if kwargs.get('fullname') and kwargs.get('fullname') != "":
                patient.fullname = kwargs.get('fullname')
            if kwargs.get('cpf') and kwargs.get('cpf') != "":
                patient.cpf = kwargs.get('cpf')
            if kwargs.get('email') and kwargs.get('email') != "":
                patient.email = kwargs.get('email')
            if kwargs.get('phone') and kwargs.get('phone') != "":
                patient.phone = kwargs.get('phone')
            if kwargs.get('address') and kwargs.get('address') != "":
                patient.address = kwargs.get('address')
            if kwargs.get('birthdate') and kwargs.get('birthdate') != "":
                patient.birthdate = kwargs.get('birthdate')
            if kwargs.get('gender') and kwargs.get('gender') != "":
                patient.gender = kwargs.get('gender')
            if kwargs.get('password') and kwargs.get('password') != "":
                patient.set_password(kwargs.get('password'))
            if kwargs.get('healt_info') and kwargs.get('healt_info') != "":
                patient.healt_info = kwargs.get('healt_info')
            
            db.session.commit()
            return patient.to_dict()
            
        except Exception as e:
            db.session.rollback()
            raise e
    
    def update_location(self, patient_id, location_data):
        try:
            patient = Patient.query.filter_by(id=patient_id).first()
            if not patient:
                raise Exception("Patient not found")
            
            loc_data = {"latitude": location_data['latitude'], "longitude": location_data['longitude']}
            
            patient.current_location = loc_data
            db.session.commit()
            return patient.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e
    
    def update_fcm_token(self, patient_id, token):
        try:
            user = User.query.filter_by(id=patient_id).first()
            if not user:
                raise Exception("User not found")
            
            user.fcm_token = token
            db.session.commit()
            return user.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e
    
    def create_request_consult(self, patient_id, observations):
        try:
            
            patient = Patient.query.filter_by(id=patient_id).first()
            if not patient:
                raise Exception("Patient not found")
            
            patient_request_consult = PatientRequestConsult(patient_id=patient_id, observations=observations)
            patient_request_consult.status = "pending"
            db.session.add(patient_request_consult)
            db.session.commit()
            
            self.firebase_service.save_request_care(
                patient_id=patient_id,
                patient_fullname=patient.fullname,
                observations=observations,
                status="pending"
            )
            return patient_request_consult.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e
    
    def create_request_emergency(self, patient_id):
        try:
            patient = Patient.query.filter_by(id=patient_id).first()
            if not patient:
                raise Exception("Patient not found")
            
            request_sos = PatientRequestEmergency(
                patient_id=patient_id,
                status="pending",
            )
            
            db.session.add(request_sos)
            db.session.commit()
            
            self.firebase_service.save_request_emergency(
                id=str(uuid.uuid4()),
                patient_fullname=patient.fullname,
                status="pending",
                created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                updated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
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
    
    def get_prescriptions(self, patient_id):
        try:
            prescriptions = Prescription.query.filter_by(patient_id=patient_id).all()
            return [prescription.to_dict() for prescription in prescriptions]
        except Exception as e:
            raise e
    
    def get_prescription(self, prescription_id):
        try:
            prescription = Prescription.query.filter_by(id=prescription_id).first()
            if not prescription:
                raise Exception("Prescription not found")
            return prescription.to_dict()
        except Exception as e:
            raise e    
    
    def get_emergencies(self, patient_id):
        try:
            emergencies = Emergency.query.filter_by(patient_id=patient_id).all()
            return [emergency.to_dict() for emergency in emergencies]
        except Exception as e:
            raise e

    def get_emergency(self, emergency_id):
        try:
            emergency = Emergency.query.filter_by(id=emergency_id).first()
            if not emergency:
                raise Exception("Emergency not found")
            return emergency.to_dict()
        except Exception as e:
            raise e    
    
    def get_active_request_consult(self, patient_id):
        try:
            requests = PatientRequestConsult.query.filter_by(patient_id=patient_id).filter(
                or_(PatientRequestConsult.status == "pending", PatientRequestConsult.status == "accepted", PatientRequestConsult.status == "canceled", PatientRequestConsult.status == "finished")
            ).all()
            return [request.to_dict() for request in requests]
        except Exception as e:
            raise e
    
    def get_active_request_emergency(self, patient_id):
        try:
            requests = PatientRequestEmergency.query.filter_by(patient_id=patient_id).filter(
                or_(PatientRequestEmergency.status == "pending", PatientRequestEmergency.status == "accepted", PatientRequestEmergency.status == "in_progress")
            ).all()
            return [request.to_dict() for request in requests]
        except Exception as e:
            raise e

    def get_active_consult(self, patient_id):
        try:
            consults = NurseRequestConsult.query.filter_by(patient_id=patient_id).filter(
                NurseRequestConsult.status.in_("pending", "accepted", "in_progress")
            ).all()
            return [consult.to_dict() for consult in consults]
        except Exception as e:
            raise e
    
    def get_active_emergency(self, patient_id):
        try:
            emergencies = NurseRequestEmergency.query.filter_by(patient_id=patient_id).filter(
                or_(NurseRequestEmergency.status == "pending", NurseRequestEmergency.status == "accepted", NurseRequestEmergency.status == "in_progress")
            ).all()
            return [emergency.to_dict() for emergency in emergencies]
        except Exception as e:
            raise e

    def delete_patient(self, patient_id):
        try:
            patient = Patient.query.filter_by(id=patient_id).first()
            if not patient:
                raise Exception("Patient not found")
            db.session.delete(patient)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e

    def get_patient(self, patient_id):
        try:
            patient = Patient.query.filter_by(id=patient_id).first()
            if not patient:
                raise Exception("Patient not found")
            return patient
        except Exception as e:
            raise e


    def get_nurse_emergency_request_by_id(self, emergency_id):
        try:
            emergency = NurseRequestEmergency.query.filter_by(id=emergency_id).first()
            if not emergency:
                raise Exception("Emergency not found")
            return emergency.to_dict()
        except Exception as e:
            raise e
    
    
    
