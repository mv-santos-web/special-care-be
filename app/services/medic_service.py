from app.models.medic import Medic
from app.models.patient import Patient
from app.models.medic_record import MedicRecord
from app.models.consult import Consult
from app.models.prescription import Prescription
from app.models.user import User

from app.models.nurse_request_consult import RequestConsult as NurseRequestConsult

from app.extensions import db
from app.services.firebase_service import FirebaseService
from app.services.fcm_service import FCMService
from app.services.pdf_service import PdfService

import os
from sqlalchemy import or_
from datetime import datetime

firebase_service = FirebaseService()
fcm_service = FCMService()
pdf_service = PdfService()

class MedicService:
    
    def __init__(self):
        self.firebase_service = firebase_service
        self.fcm_service = fcm_service
        self.pdf_service = pdf_service
        
    def auth_medic(self, email, password):
        try:
            check_medic = User.query.filter_by(email=email).first()
            if check_medic and check_medic.check_password(password):
                return check_medic
            else:
                raise Exception("Invalid email or password")
        except Exception as e:
            raise e
        
    def sign_up_medic(self, **kwargs):
        try:
            
            cpf = kwargs.get('cpf')
            check_cpf = User.query.filter_by(cpf=cpf).first()
            if check_cpf:
                raise Exception("CPF already exists")
            
            email = kwargs.get('email')
            check_email = User.query.filter_by(email=email).first()
            if check_email:
                raise Exception("Email already exists")
            
            crm = kwargs.get('crm')
            check_crm = Medic.query.filter_by(crm=crm).first()
            if check_crm:
                raise Exception("CRM already exists")
            
            medic = Medic(**kwargs)
            medic.set_password(kwargs.get('password'))
            db.session.add(medic)
            db.session.commit()
            return medic.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e

    def edit_medic(self, medic_id, **kwargs):
        try:
            medic = Medic.query.get(medic_id)
            if not medic:
                raise Exception("Medic not found")
            
            if kwargs.get('fullname') and kwargs.get('fullname') != "":
                medic.fullname = kwargs.get('fullname')
            if kwargs.get('cpf') and kwargs.get('cpf') != "":
                medic.cpf = kwargs.get('cpf')
            if kwargs.get('email') and kwargs.get('email') != "":
                medic.email = kwargs.get('email')
            if kwargs.get('phone') and kwargs.get('phone') != "":
                medic.phone = kwargs.get('phone')
            if kwargs.get('address') and kwargs.get('address') != "":
                medic.address = kwargs.get('address')
            if kwargs.get('birthdate') and kwargs.get('birthdate') != "":
                medic.birthdate = kwargs.get('birthdate')
            if kwargs.get('gender') and kwargs.get('gender') != "":
                medic.gender = kwargs.get('gender')
            if kwargs.get('password') and kwargs.get('password') != "":
                medic.set_password(kwargs.get('password'))
            if kwargs.get('crm') and kwargs.get('crm') != "":
                medic.crm = kwargs.get('crm')
            
            db.session.commit()
            return medic.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e

    def get_medic_records(self):
        try:
            medic_records = MedicRecord.query.all()
            return [record.to_dict() for record in medic_records]
        except Exception as e:
            raise e
    
    def get_prescriptions(self, medic_id):
        try:
            prescriptions = Prescription.query.filter_by(medic_id=medic_id).all()
            return [prescription.to_dict() for prescription in prescriptions]
        except Exception as e:
            raise e
    
    def get_requests_consults(self, medic_id):
        try:
            requests_consults = NurseRequestConsult.query.filter(or_(NurseRequestConsult.medic_id == None, NurseRequestConsult.medic_id == medic_id)).all()
            return [request.to_dict() for request in requests_consults]
        except Exception as e:
            raise e

    def get_requests_consult_data(self, request_consult_id):
        try:
            request_consult = NurseRequestConsult.query.get(request_consult_id)
            return request_consult.to_dict()
        except Exception as e:
            raise e

    def accept_request_consult(self, request_consult_id, medic_id):
        try:
            request_consult = NurseRequestConsult.query.get(request_consult_id)
            if not request_consult:
                raise Exception("Request consult not found")
            
            patient = User.query.get(request_consult.patient_id)
            consult = Consult(
                observations=request_consult.observations,
                consult_type=request_consult.consult_type,
                date=request_consult.date,
                patient_id=request_consult.patient_id,
                medic_id=medic_id,
                status="accepted"
            )
            
            request_consult.medic_id = medic_id
            request_consult.status = "accepted"
            request_consult.accepted_at = datetime.now()
            db.session.add(consult)
            db.session.commit()
            
            self.fcm_service.notify_user(
                title="Consulta Aceita !",
                message="Um de nossos médicos acabou de aceitar sua consultas, acesse o app para ser atendido.",
                user_id=patient.fcm_token,
                data={
                    'update': 'consults'
                }
            )
            
            return request_consult.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e

    def cancel_request_consult(self, request_consult_id):
        try:
            request_consult = NurseRequestConsult.query.get(request_consult_id)
            if not request_consult:
                raise Exception("Request consult not found")
            
            request_consult.status = "cancelled"
            db.session.commit()
            
            patient = User.query.get(request_consult.patient_id)
            
            self.fcm_service.notify_user(
                title="Consulta Cancelada !",
                body="Um de nossos médicos acabou de cancelar sua consulta, entre em contato com o suporte para mais informações.",
                token=patient.fcm_token
            )
            
            return request_consult.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e

    def attend_request_consult(self, request_consult_id):
        try:
            request_consult = NurseRequestConsult.query.get(request_consult_id)
            if not request_consult:
                raise Exception("Request consult not found")
            
            patient = User.query.get(request_consult.patient_id)
            
            request_consult.status = "in_progress"
            db.session.commit()
            
            self.fcm_service.notify_user(
                title="O médico está prestes a atendê-lo!",
                message="Um de nossos médicos está prestes a atendê-lo, abra o app e siga as instruções.",
                user_id=patient.fcm_token,
                data={
                    'update': 'consults'
                }
            )
            
            return request_consult.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e

    def finish_request_consult(self, request_consult_id):
        try:
            request_consult = NurseRequestConsult.query.get(request_consult_id)
            if not request_consult:
                raise Exception("Request consult not found")
            
            patient = User.query.get(request_consult.patient_id)
            
            request_consult.status = "finished"
            db.session.commit()
            
            self.fcm_service.notify_user(
                title="Consulta Finalizada !",
                message="Um de nossos médicos acabou de finalizar sua consulta, caso tenha alguma dúvida entre em contato com o suporte.",
                user_id=patient.fcm_token,
                data={
                    'update': 'consults'
                }
            )
            
            return request_consult.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e

    def create_medic_record(self, patient_id, medic_history, medicines, observations):
        try:
            medic_record = MedicRecord(patient_id=patient_id, medic_history=medic_history, medicines=medicines, observations=observations)
            db.session.add(medic_record)
            db.session.commit()
            
            return medic_record.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e

    def get_medic_record(self, patient_id):
        try:
            medic_record = MedicRecord.query.filter_by(patient_id=patient_id).first()
            return medic_record.to_dict()
        except Exception as e:
            raise e

    def create_prescription(self, patient_id, medic_id, data, validation_code, pdf_path):
        try:        
            prescription = Prescription(patient_id=patient_id, medic_id=medic_id, data=data, validation_code=validation_code, pdf_path=pdf_path)    
            db.session.add(prescription)
            db.session.commit()
            return prescription.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e

    def get_prescription(self, prescription_id):
        try:
            prescription = Prescription.query.get(prescription_id)
            return prescription.to_dict()
        except Exception as e:
            raise e



    def edit_medic_record(self, patient_id, **kwargs):
        try:
            medic_record = MedicRecord.query.filter_by(patient_id=patient_id).first()
            if not medic_record:
                raise Exception("Medic record not found")
            
            if kwargs.get('medic_history') and kwargs.get('medic_history') != "":
                medic_record.medic_history = kwargs.get('medic_history')
            if kwargs.get('medicines') and kwargs.get('medicines') != "":
                medic_record.medicines = kwargs.get('medicines')
            if kwargs.get('observations') and kwargs.get('observations') != "":
                medic_record.observations = kwargs.get('observations')
            db.session.commit()
            
            return medic_record.to_dict()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete_medic_record(self, medic_record_id):
        try:
            medic_record = MedicRecord.query.filter_by(patient_id=medic_record_id).first()
            if not medic_record:
                raise Exception("Medic record not found")
            
            db.session.delete(medic_record)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e

    def delete_prescription(self, prescription_id):
        try:
            prescription = Prescription.query.get(prescription_id)
            if not prescription:
                raise Exception("Prescription not found")
            
            os.remove(prescription.pdf_path)
            
            db.session.delete(prescription)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e

    def delete_medic(self, medic_id):
        try:
            medic = Medic.query.get(medic_id)
            if not medic:
                raise Exception("Medic not found")
            
            if medic.certificate_file:
                os.remove(medic.certificate_file)
                
            db.session.delete(medic)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e

    def get_consults(self, medic_id):
        try:
            consults = Consult.query.filter_by(medic_id=medic_id).all()
            return [consult.to_dict() for consult in consults]
        except Exception as e:
            raise e

    def get_patients(self):
        try:
            patients = Patient.query.all()
            return [patient.to_dict() for patient in patients]
        except Exception as e:
            raise e

    def get_patient(self, patient_id):
        try:
            patient = Patient.query.get(patient_id)
            return patient.to_dict()
        except Exception as e:
            raise e

    def get_medic(self, medic_id):
        try:
            medic = Medic.query.get(medic_id)
            return medic.to_dict()
        except Exception as e:
            raise e