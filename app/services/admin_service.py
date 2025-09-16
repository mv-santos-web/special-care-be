from datetime import datetime 

from app.models.patient import Patient
from app.models.medic_record import MedicRecord
from app.models.consult import Consult
from app.models.admin import Admin
from app.models.emergency import Emergency
from app.models.prescription import Prescription
from app.models.medic import Medic
from app.models.nurse import Nurse
from app.models.paramedic import Paramedic

from app.extensions import db
from app.services.firebase_service import FirebaseService
from app.services.fcm_service import FCMService

firebase_service = FirebaseService()
fcm_service = FCMService()


class AdminService:
     
    def __init__(self):
        self.firebase_service = firebase_service
        self.fcm_service = fcm_service
         
    def auth_admin(self, email, password):
        try:
            user = db.session.query(Admin).filter_by(email=email).first()
            if not user or not user.check_password(password):
                raise Exception("Invalid email or password")
            return user
        except Exception as e:
            print("Service error: ", e)
            raise e
        
    def add_admin(self, **kwargs):
        try:
            check_email = db.session.query(Admin).filter_by(email=kwargs.get('email')).first()
            if check_email:
                raise Exception("Email already exists")
            
            check_cpf = db.session.query(Admin).filter_by(cpf=kwargs.get('cpf')).first()
            if check_cpf:
                raise Exception("CPF already exists")
            
            birthdate = datetime.strptime(kwargs.get('birthdate'), '%Y-%m-%d')
            kwargs['birthdate'] = birthdate
            
            user = Admin(**kwargs)
            user.set_password(kwargs.get('password'))
            db.session.add(user)
            db.session.commit()
            return user.to_dict()
        except Exception as e:
            print("Service error: ", e)
            db.session.rollback()
            raise e
    
    def update_admin(self, admin_id, **kwargs):
        try:
            admin = db.session.query(Admin).filter_by(id=admin_id).first()
            if not admin:
                raise Exception("Admin not found")
            
            if kwargs.get('fullname') and kwargs.get('fullname') != "":
                admin.fullname = kwargs.get('fullname')
            if kwargs.get('cpf') and kwargs.get('cpf') != "":
                admin.cpf = kwargs.get('cpf')
            if kwargs.get('birthdate') and kwargs.get('birthdate') != "":
                birthdate = datetime.strptime(kwargs.get('birthdate'), '%Y-%m-%d')
                admin.birthdate = birthdate
            if kwargs.get('gender') and kwargs.get('gender') != "":
                admin.gender = kwargs.get('gender')
            if kwargs.get('password') and kwargs.get('password') != "":
                admin.set_password(kwargs.get('password'))
            if kwargs.get('phone') and kwargs.get('phone') != "":
                admin.phone = kwargs.get('phone')
            if kwargs.get('address') and kwargs.get('address') != "":
                admin.address = kwargs.get('address')
            if kwargs.get('email') and kwargs.get('email') != "":
                admin.email = kwargs.get('email')
            
            db.session.commit()
            return admin.to_dict()
        except Exception as e:
            print("Service error: ", e)
            db.session.rollback()
            raise e
       
    
    def get_medics(self):
        try:
            medics = db.session.query(Medic).all()
            return [medic.to_dict() for medic in medics]
        except Exception as e:
            raise e
    
    def get_medic(self, medic_id):
        try:
            medic = db.session.query(Medic).filter_by(id=medic_id).first()
            return medic
        except Exception as e:
            raise e
    
    def update_medic(self, medic_id, **kwargs):
        try:
            print(kwargs)
            medic = db.session.query(Medic).filter_by(id=medic_id).first()
            if not medic:
                raise Exception("Medic not found")
            
            if kwargs.get('fullname') and kwargs.get('fullname') != "":
                medic.fullname = kwargs.get('fullname')
            if kwargs.get('cpf') and kwargs.get('cpf') != "":
                medic.cpf = kwargs.get('cpf')
            if kwargs.get('crm') and kwargs.get('crm') != "":
                medic.crm = kwargs.get('crm')
            if kwargs.get('birthdate') and kwargs.get('birthdate') != "":
                birthdate = datetime.strptime(kwargs.get('birthdate'), '%Y-%m-%d')
                medic.birthdate = birthdate
            if kwargs.get('gender') and kwargs.get('gender') != "":
                medic.gender = kwargs.get('gender')
            if kwargs.get('password') and kwargs.get('password') != "":
                medic.set_password(kwargs.get('password'))
            if kwargs.get('phone') and kwargs.get('phone') != "":
                medic.phone = kwargs.get('phone')
            if kwargs.get('address') and kwargs.get('address') != "":
                medic.address = kwargs.get('address')
            if kwargs.get('email') and kwargs.get('email') != "":
                medic.email = kwargs.get('email')
            
            db.session.commit()
            return medic
        except Exception as e:
            print("Service error: ", e)
            db.session.rollback()
            raise e
    
    def delete_medic(self, medic_id):
        try:
            medic = db.session.query(Medic).filter_by(id=medic_id).first()
            if not medic:
                raise Exception("Medic not found")
            db.session.delete(medic)
            db.session.commit()
            return True
        except Exception as e:
            print("Service error: ", e)
            db.session.rollback()
            raise e    
    
    def add_medic(self, **kwargs):
        try:
            medic = Medic(**kwargs)
            medic.set_password(kwargs.get('password'))
            db.session.add(medic)
            db.session.commit()
            return medic
        except Exception as e:
            db.session.rollback()
            raise e


    def get_nurses(self):
        try:
            nurses = db.session.query(Nurse).all()
            return [nurse.to_dict() for nurse in nurses]
        except Exception as e:
            raise e
    
    def get_nurse(self, nurse_id):
        try:
            nurse = db.session.query(Nurse).filter_by(id=nurse_id).first()
            return nurse
        except Exception as e:
            raise e

    def add_nurse(self, **kwargs):
        try:
            nurse = Nurse(**kwargs)
            nurse.set_password(kwargs.get('password'))
            db.session.add(nurse)
            db.session.commit()
            return nurse
        except Exception as e:
            db.session.rollback()
            raise e

    def update_nurse(self, nurse_id, **kwargs):
        try:
            print(kwargs)
            nurse = db.session.query(Nurse).filter_by(id=nurse_id).first()
            if not nurse:
                raise Exception("Nurse not found")
            
            if kwargs.get('fullname') and kwargs.get('fullname') != "":
                nurse.fullname = kwargs.get('fullname')
            if kwargs.get('cpf') and kwargs.get('cpf') != "":
                nurse.cpf = kwargs.get('cpf')
            if kwargs.get('coren') and kwargs.get('coren') != "":
                nurse.coren = kwargs.get('coren')
            if kwargs.get('birthdate') and kwargs.get('birthdate') != "":
                birthdate = datetime.strptime(kwargs.get('birthdate'), '%Y-%m-%d')
                nurse.birthdate = birthdate
            if kwargs.get('gender') and kwargs.get('gender') != "":
                nurse.gender = kwargs.get('gender')
            if kwargs.get('password') and kwargs.get('password') != "":
                nurse.set_password(kwargs.get('password'))
            if kwargs.get('phone') and kwargs.get('phone') != "":
                nurse.phone = kwargs.get('phone')
            if kwargs.get('address') and kwargs.get('address') != "":
                nurse.address = kwargs.get('address')
            if kwargs.get('email') and kwargs.get('email') != "":
                nurse.email = kwargs.get('email')
            
            db.session.commit()
            return nurse
        except Exception as e:
            print("Service error: ", e)
            db.session.rollback()
            raise e
    
    def delete_nurse(self, nurse_id):
        try:
            nurse = db.session.query(Nurse).filter_by(id=nurse_id).first()
            if not nurse:
                raise Exception("Nurse not found")
            db.session.delete(nurse)
            db.session.commit()
            return True
        except Exception as e:
            print("Service error: ", e)
            db.session.rollback()
            raise e
    
    
    def get_paramedics(self):
        try:
            paramedics = db.session.query(Paramedic).all()
            return [paramedic.to_dict() for paramedic in paramedics]
        except Exception as e:
            raise e
    
    def get_paramedic(self, paramedic_id):
        try:
            paramedic = db.session.query(Paramedic).filter_by(id=paramedic_id).first()
            return paramedic
        except Exception as e:
            raise e
    
    def add_paramedic(self, **kwargs):
        try:
            paramedic = Paramedic(**kwargs)
            paramedic.set_password(kwargs.get('password'))
            db.session.add(paramedic)
            db.session.commit()
            return paramedic
        except Exception as e:
            db.session.rollback()
            raise e
    
    def update_paramedic(self, paramedic_id, **kwargs):
        try:
            print(kwargs)
            paramedic = db.session.query(Paramedic).filter_by(id=paramedic_id).first()
            if not paramedic:
                raise Exception("Paramedic not found")
            
            if kwargs.get('fullname') and kwargs.get('fullname') != "":
                paramedic.fullname = kwargs.get('fullname')
            if kwargs.get('cpf') and kwargs.get('cpf') != "":
                paramedic.cpf = kwargs.get('cpf')
            if kwargs.get('birthdate') and kwargs.get('birthdate') != "":
                birthdate = datetime.strptime(kwargs.get('birthdate'), '%Y-%m-%d')
                paramedic.birthdate = birthdate
            if kwargs.get('gender') and kwargs.get('gender') != "":
                paramedic.gender = kwargs.get('gender')
            if kwargs.get('password') and kwargs.get('password') != "":
                paramedic.set_password(kwargs.get('password'))
            if kwargs.get('phone') and kwargs.get('phone') != "":
                paramedic.phone = kwargs.get('phone')
            if kwargs.get('address') and kwargs.get('address') != "":
                paramedic.address = kwargs.get('address')
            if kwargs.get('email') and kwargs.get('email') != "":
                paramedic.email = kwargs.get('email')
            
            db.session.commit()
            return paramedic
        except Exception as e:
            print("Service error: ", e)
            db.session.rollback()
            raise e
            
    def delete_paramedic(self, paramedic_id):
        try:
            paramedic = db.session.query(Paramedic).filter_by(id=paramedic_id).first()
            if not paramedic:
                raise Exception("Paramedic not found")
            db.session.delete(paramedic)
            db.session.commit()
            return True
        except Exception as e:
            print("Service error: ", e)
            db.session.rollback()
            raise e
    

    def get_patients(self):
        try:
            patients = db.session.query(Patient).all()
            return [patient.to_dict() for patient in patients]
        except Exception as e:
            raise e
    
    def get_patient(self, patient_id):
        try:
            patient = db.session.query(Patient).filter_by(id=patient_id).first()
            return patient
        except Exception as e:
            raise e
        
    def add_patient(self, **kwargs):
        try:
            patient = Patient(**kwargs)
            patient.set_password(kwargs.get('password'))
            db.session.add(patient)
            db.session.commit()
            return patient
        except Exception as e:
            db.session.rollback()
            raise e
    
    def update_patient(self, patient_id, **kwargs):
        try:
            patient = db.session.query(Patient).filter_by(id=patient_id).first()
            if not patient:
                raise Exception("Patient not found")
            
            if kwargs.get('fullname') and kwargs.get('fullname') != "":
                patient.fullname = kwargs.get('fullname')
            if kwargs.get('cpf') and kwargs.get('cpf') != "":
                patient.cpf = kwargs.get('cpf')
            if kwargs.get('birthdate') and kwargs.get('birthdate') != "":
                birthdate = datetime.strptime(kwargs.get('birthdate'), '%Y-%m-%d')
                patient.birthdate = birthdate
            if kwargs.get('gender') and kwargs.get('gender') != "":
                patient.gender = kwargs.get('gender')
            if kwargs.get('password') and kwargs.get('password') != "":
                patient.set_password(kwargs.get('password'))
            if kwargs.get('phone') and kwargs.get('phone') != "":
                patient.phone = kwargs.get('phone')
            if kwargs.get('address') and kwargs.get('address') != "":
                patient.address = kwargs.get('address')
            if kwargs.get('email') and kwargs.get('email') != "":
                patient.email = kwargs.get('email')
            
            db.session.commit()
            return patient
        except Exception as e:
            print("Service error: ", e)
            db.session.rollback()
            raise e
    
    def delete_patient(self, patient_id):
        try:
            patient = db.session.query(Patient).filter_by(id=patient_id).first()
            if not patient:
                raise Exception("Patient not found")
            db.session.delete(patient)
            db.session.commit()
            return True
        except Exception as e:
            raise e
    
       
    def get_consults(self):
        try:
            consults = db.session.query(Consult).all()
            return [consult.to_dict() for consult in consults]
        except Exception as e:
            raise e

    def get_consult(self, consult_id):
        try:
            consult = db.session.query(Consult).filter_by(id=consult_id).first()
            return consult
        except Exception as e:
            raise e
    
    def add_consult(self, **kwargs):
        try:
            consult = Consult(**kwargs)
            db.session.add(consult)
            db.session.commit()
            return consult
        except Exception as e:
            db.session.rollback()
            raise e
    
    def update_consult(self, consult_id, **kwargs):
        try:
            consult = db.session.query(Consult).filter_by(id=consult_id).first()
            if not consult:
                raise Exception("Consult not found")
            
            if kwargs.get('patient_id') and kwargs.get('patient_id') != "":
                consult.patient_id = kwargs.get('patient_id')
            if kwargs.get('medic_id') and kwargs.get('medic_id') != "":
                consult.medic_id = kwargs.get('medic_id')
            if kwargs.get('date') and kwargs.get('date') != "":
                consult.date = kwargs.get('date')
            if kwargs.get('status') and kwargs.get('status') != "":
                consult.status = kwargs.get('status')
            
            db.session.commit()
            return consult
        except Exception as e:
            db.session.rollback()
            raise e
    
    def delete_consult(self, consult_id):
        try:
            consult = db.session.query(Consult).filter_by(id=consult_id).first()
            if not consult:
                raise Exception("Consult not found")
            db.session.delete(consult)
            db.session.commit()
            return True 
        except Exception as e:
            db.session.rollback()
            raise e
    
    
    def get_emergencies(self):
        try:
            emergencies = db.session.query(Emergency).all()
            return [emergency.to_dict() for emergency in emergencies]
        except Exception as e:
            raise e
    
    def get_emergency(self, emergency_id):
        try:
            emergency = db.session.query(Emergency).filter_by(id=emergency_id).first()
            return emergency
        except Exception as e:
            raise e
    
    def add_emergency(self, **kwargs):
        try:
            emergency = Emergency(**kwargs)
            db.session.add(emergency)
            db.session.commit()
            return emergency
        except Exception as e:
            db.session.rollback()
            raise e
    
    def update_emergency(self, emergency_id, **kwargs):
        try:
            emergency = db.session.query(Emergency).filter_by(id=emergency_id).first()
            if not emergency:
                raise Exception("Emergency not found")
            
            if kwargs.get('patient_id') and kwargs.get('patient_id') != "":
                emergency.patient_id = kwargs.get('patient_id')
            if kwargs.get('medic_id') and kwargs.get('medic_id') != "":
                emergency.medic_id = kwargs.get('medic_id')
            if kwargs.get('date') and kwargs.get('date') != "":
                emergency.date = kwargs.get('date')
            if kwargs.get('status') and kwargs.get('status') != "":
                emergency.status = kwargs.get('status')
            
            db.session.commit()
            return emergency
        except Exception as e:
            db.session.rollback()
            raise e
    
    def delete_emergency(self, emergency_id):
        try:
            emergency = db.session.query(Emergency).filter_by(id=emergency_id).first()
            if not emergency:
                raise Exception("Emergency not found")
            db.session.delete(emergency)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    
    def get_admins(self):
        try:
            admins = db.session.query(Admin).all()
            return [admin.to_dict() for admin in admins]
        except Exception as e:
            raise e
    
    def get_admin(self, admin_id):
        try:
            admin = db.session.query(Admin).filter_by(id=admin_id).first()
            return admin
        except Exception as e:
            raise e

    def add_admin(self, **kwargs):
        try:
            admin = Admin(**kwargs)
            db.session.add(admin)
            db.session.commit()
            return admin
        except Exception as e:
            db.session.rollback()
            raise e
    
    def delete_admin(self, admin_id):
        try:
            admin = db.session.query(Admin).filter_by(id=admin_id).first()
            if not admin:
                raise Exception("Admin not found")
            db.session.delete(admin)
            db.session.commit()
            return True
        except Exception as e:
            raise e
    
    
    def get_prescriptions(self):
        try:
            prescriptions = db.session.query(Prescription).all()
            return [prescription.to_dict() for prescription in prescriptions]
        except Exception as e:
            raise e
    
    def get_prescription(self, prescription_id):
        try:
            prescription = db.session.query(Prescription).filter_by(id=prescription_id).first()
            return prescription
        except Exception as e:
            raise e
    
    def get_prescription_by_validation(self, validation_code):
        try:
            prescription = db.session.query(Prescription).filter_by(validation_code=validation_code).first()
            return prescription
        except Exception as e:
            raise e
    
    def add_prescription(self, **kwargs):
        try:
            prescription = Prescription(**kwargs)
            db.session.add(prescription)
            db.session.commit()
            return prescription
        except Exception as e:
            db.session.rollback()
            raise e
    
    def delete_prescription(self, prescription_id):
        try:
            prescription = db.session.query(Prescription).filter_by(id=prescription_id).first()
            if not prescription:
                raise Exception("Prescription not found")
            db.session.delete(prescription)
            db.session.commit()
            return True
        except Exception as e:
            raise e
    
    
    def get_medic_records(self):
        try:
            medic_records = db.session.query(MedicRecord).all()
            return [medic_record.to_dict() for medic_record in medic_records]
        except Exception as e:
            raise e
        
    def get_medic_record(self, medic_record_id):
        try:
            medic_record = db.session.query(MedicRecord).filter_by(id=medic_record_id).first()
            return medic_record
        except Exception as e:
            raise e
    
    def add_medic_record(self, **kwargs):
        try:
            medic_record = MedicRecord(**kwargs)
            db.session.add(medic_record)
            db.session.commit()
            return medic_record
        except Exception as e:
            db.session.rollback()
            raise e

    def delete_medic_record(self, medic_record_id):
        try:
            medic_record = db.session.query(MedicRecord).filter_by(id=medic_record_id).first()
            if not medic_record:
                raise Exception("Medic record not found")
            db.session.delete(medic_record)
            db.session.commit()
            return True
        except Exception as e:
            raise e

    def update_medic_record(self, medic_record_id, **kwargs):
        try:
            medic_record = db.session.query(MedicRecord).filter_by(id=medic_record_id).first()
            if not medic_record:
                raise Exception("Medic record not found")
            
            if kwargs.get('patient_id') and kwargs.get('patient_id') != "":
                medic_record.patient_id = kwargs.get('patient_id')
            if kwargs.get('medic_id') and kwargs.get('medic_id') != "":
                medic_record.medic_id = kwargs.get('medic_id')
            if kwargs.get('date') and kwargs.get('date') != "":
                medic_record.date = kwargs.get('date')
            if kwargs.get('status') and kwargs.get('status') != "":
                medic_record.status = kwargs.get('status')
            
            db.session.commit()
            return medic_record
        except Exception as e:
            raise e



