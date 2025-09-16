import firebase_admin
from firebase_admin import credentials, db
import os

ROOT_PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class FirebaseService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        # Initialize Firebase Admin SDK if not already initialized
        if not firebase_admin._apps:
            cred_path = os.path.join(ROOT_PROJECT, '../specialcare-credentials.json')
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://specialcare-43bf5-default-rtdb.firebaseio.com'
            })
            
        self._initialized = True
        self.db = db.reference()
        
    def get_reference(self, path=None):
        """Get a reference to a location in the Realtime Database"""
        return self.db if path is None else self.db.child(path)
        
    def get_data(self, path=None):
        """Get data from a specific path in the Realtime Database"""
        try:
            ref = self.get_reference(path)
            return ref.get()
        except Exception as e:
            raise Exception(f"Failed to get data from {path or 'root'}: {str(e)}")
            
    def set_data(self, path, data):
        """Set data at a specific path in the Realtime Database"""
        try:
            ref = self.get_reference(path)
            ref.set(data)
            return True
        except Exception as e:
            raise Exception(f"Failed to set data at {path}: {str(e)}")
            
    def update_data(self, path, updates):
        """Update data at a specific path in the Realtime Database"""
        try:
            ref = self.get_reference(path)
            ref.update(updates)
            return True
        except Exception as e:
            raise Exception(f"Failed to update data at {path}: {str(e)}")
            
    def delete_data(self, path):
        """Delete data at a specific path in the Realtime Database"""
        try:
            ref = self.get_reference(path)
            ref.delete()
            return True
        except Exception as e:
            raise Exception(f"Failed to delete data at {path}: {str(e)}")
            
    def save_request_care(self, **kwargs):
        """Save a care request to the Realtime Database"""
        try:
            request_data = {
                'patient_fullname': kwargs.get('patient_fullname'),
                'observations': kwargs.get('observations'),
                'status': kwargs.get('status'),
                'created_at': kwargs.get('created_at'),
                'updated_at': kwargs.get('updated_at')
            }
            ref = self.get_reference('requests_care')
            ref.set(request_data)
            return True
        except Exception as e:
            raise Exception(f"Failed to save request care: {str(e)}")
        
    def save_request_consult_medic(self, **kwargs):
        """Save a care request to the Realtime Database"""
        try:
            request_data = {
                'patient_fullname': kwargs.get('patient_fullname'),
                'observations': kwargs.get('observations'),
                'status': kwargs.get('status'),
                'created_at': kwargs.get('created_at'),
                'updated_at': kwargs.get('updated_at')
            }
            ref = self.get_reference('requests_consults')
            ref.set(request_data)
            return True
        except Exception as e:
            raise Exception(f"Failed to save request care: {str(e)}")
        
        
    def save_request_emergency(self, **kwargs):
        """Save a care request to the Realtime Database"""
        try:
            request_data = {
                'patient_fullname': kwargs.get('patient_fullname'),
                'observations': kwargs.get('observations'),
                'status': kwargs.get('status'),
                'created_at': kwargs.get('created_at'),
                'updated_at': kwargs.get('updated_at')
            }
            ref = self.get_reference('requests_emergencies')
            ref.set(request_data)
            return True
        except Exception as e:
            raise Exception(f"Failed to save request emergency: {str(e)}")