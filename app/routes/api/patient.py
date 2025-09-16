from flask import request, jsonify, send_file
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

from app.services.firebase_service import FirebaseService
from app.services.patient_service import PatientService
from . import blueprint

firebase_service = FirebaseService()

@blueprint.route('/auth_patient', methods=['POST'])
def auth_patient():
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'message': 'Dados de autenticação não fornecidos'
        }), 400
        
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()
    
    if not email or not password:
        return jsonify({
            'success': False,
            'message': 'Email e senha são obrigatórios'
        }), 400
    
    try:
        patient = PatientService().auth_patient(email, password)
        if patient and patient.active:  
            access_token = create_access_token(identity=str(patient.id))  # Changed to use just the ID
            return jsonify({
                'success': True,
                'access_token': access_token,
                'user': {
                    'id': patient.id,
                    'fullname': patient.fullname,
                    'email': patient.email,
                    'type': 'patient'
                }
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Credenciais inválidas ou usuário inativo'
            }), 401
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': str(e)
        }), 404

@blueprint.route('/patients/update_fcm_token', methods=["POST"])
@jwt_required()
def update_fcm_token():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        fcm_token = data.get('token')
        patient_service = PatientService()
        patient_service.update_fcm_token(current_user_id, fcm_token)
        return jsonify({"error": False, "message": "FCM token updated successfully"})
    except Exception as e:
        print("FCM token error: ", e)
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route("/patients/data", methods=["GET"])
@jwt_required()
def get_patients_data():
    try:
        patient_service = PatientService()
        patients = patient_service.get_patients()
        return jsonify({"error": False, "message": "Pacientes fetched successfully", "data": patients})
    except Exception as e:
        print("Patients error: ", e)
        flash(f'Erro ao buscar pacientes, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/patients/me', methods=['GET'])
@jwt_required()
def get_patient_data():
    try:
        current_user_id = get_jwt_identity()
        patient_service = PatientService()
        patient = patient_service.get_patient(current_user_id)
        return jsonify(patient.to_dict())
    except Exception as e:
        print("Patient error: ", e)
        return jsonify({"error": True, "message": str(e)}), 500
    
@blueprint.route('/patients/nurse_emergencies_requests/data', methods=['GET'])
@jwt_required()
def get_nurse_emergencies_patient_data():
    try:
        current_user_id = get_jwt_identity()
        patient_service = PatientService()
        emergencies = patient_service.get_active_request_emergency(current_user_id)
        return jsonify(emergencies)
    except Exception as e:
        print("Emergencies error: ", e)
        return jsonify({"error": True, "message": str(e)}), 500
    
@blueprint.route('/patients/emergencies/<int:emergency_id>/accept', methods=['GET'])
@jwt_required()
def accept_emergency_patient(emergency_id):
    try:
        current_user_id = get_jwt_identity()
        patient_service = PatientService()
        patient_service.accept_emergency(emergency_id, current_user_id)
        return jsonify({"error": False, "message": "Emergency accepted successfully"})
    except Exception as e:
        print("Emergency error: ", e)
        return jsonify({"error": True, "message": str(e)}), 500
    
@blueprint.route('/patients/emergencies/<int:emergency_id>/finish', methods=['GET'])
@jwt_required()
def finish_emergency_patient(emergency_id):
    try:
        patient_service = PatientService()
        patient_service.finish_emergency(emergency_id)
        return jsonify({"error": False, "message": "Emergency finished successfully"})
    except Exception as e:
        print("Emergency error: ", e)
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/patients/emergencies/<int:emergency_id>/cancel', methods=['GET'])
@jwt_required()
def cancel_emergency_patient(emergency_id):
    try:
        patient_service = PatientService()
        patient_service.cancel_emergency(emergency_id)
        return jsonify({"error": False, "message": "Emergency canceled successfully"})
    except Exception as e:
        print("Emergency error: ", e)
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/patients/emergencies/call', methods=['GET'])
@jwt_required()
def call_emergency_patient():
    try:
        current_user_id = get_jwt_identity()
        patient_service = PatientService()
        patient_service.create_request_emergency(current_user_id)
        return jsonify({"error": False, "message": "Emergency called successfully"})
    except Exception as e:
        print("Emergency error: ", e)
        return jsonify({"error": True, "message": str(e)}), 500


@blueprint.route('/patient/update_location', methods=['POST'])
@jwt_required()
def update_location_patient():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        patient_service = PatientService()
        patient_service.update_location(current_user_id, data)
        return jsonify({"error": False, "message": "Location updated successfully"})
    except Exception as e:
        print("Location error: ", e)
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/patient/medical_records/data', methods=['GET'])
@jwt_required()
def get_medical_records_patient():
    try:
        current_user_id = get_jwt_identity()
        patient_service = PatientService()
        medical_records = patient_service.get_medical_record(current_user_id)
        return jsonify(medical_records)
    except Exception as e:
        print("Medical records error: ", e)
        return jsonify({"error": True, "message": str(e)}), 500


@blueprint.route('/patient/consults/data', methods=['GET'])
@jwt_required()
def get_consults_patient():
    try:
        current_user_id = get_jwt_identity()
        patient_service = PatientService()
        consults = patient_service.get_consults(current_user_id)
        return jsonify(consults)
    except Exception as e:
        print("Consults error: ", e)
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/patient/consults/<int:consult_id>/data', methods=['GET'])
@jwt_required()
def get_consult_patient(consult_id):
    try:
        patient_service = PatientService()
        consult = patient_service.get_consult(consult_id)
        return jsonify(consult)
    except Exception as e:
        print("Consult error: ", e)
        return jsonify({"error": True, "message": str(e)}), 500


@blueprint.route('/patient/prescriptions/data', methods=['GET'])
@jwt_required()
def get_prescriptions_patient():
    try:
        current_user_id = get_jwt_identity()
        patient_service = PatientService()
        prescriptions = patient_service.get_prescriptions(current_user_id)
        return jsonify(prescriptions)
    except Exception as e:
        print("Prescriptions error: ", e)
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/patient/prescriptions/<int:prescription_id>/data', methods=['GET'])
@jwt_required()
def get_prescription_patient(prescription_id):
    try:
        patient_service = PatientService()
        prescription = patient_service.get_prescription(prescription_id)
        return jsonify(prescription)
    except Exception as e:
        print("Prescription error: ", e)
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/patient/prescriptions/<int:prescription_id>/download', methods=['GET'])
def download_prescription_patient(prescription_id):
    try:
        patient_service = PatientService()
        prescription = patient_service.get_prescription(prescription_id)
        return send_file(prescription['pdf_path'], as_attachment=True)
    except Exception as e:
        print("Prescription error: ", e)
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/patient/medic_record', methods=['GET'])
@jwt_required()
def get_medic_record_patient():
    try:
        current_user_id = get_jwt_identity()
        patient_service = PatientService()
        medic_record = patient_service.get_medical_record(current_user_id)
        return jsonify(medic_record)
    except Exception as e:
        print("Medic record error: ", e)
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/patient/request_consult_nurse/data', methods=['GET'])
@jwt_required()
def get_active_request_consult_nurse():
    try:
        current_user_id = get_jwt_identity()
        patient_service = PatientService()
        requests = patient_service.get_active_request_consult(current_user_id)
        return jsonify(requests)
    except Exception as e:
        print("Request error: ", e)
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/patient/request_consult_nurse/add', methods=['POST'])
@jwt_required()
def request_consult_nurse():
    try:
        current_user_id = get_jwt_identity()
        patient_service = PatientService()
        
        data = request.get_json()
        observations = data.get('observations')
        
        patient_service.create_request_consult(current_user_id, observations=observations)
        
        user_data = patient_service.get_patient(current_user_id)
        
        notification_data = {
            'id': str(uuid.uuid4()),
            'patient_fullname': user_data.fullname,
            'observations': observations,
            'status': 'pending',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        firebase_service.save_request_care(**notification_data)
        
        return jsonify({"error": False, "message": "Request sent successfully"})
    except Exception as e:
        print("Request error: ", e)
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/patient/request_consult_nurse', methods=['POST'])
@jwt_required()
def make_request_consult_nurse():
    try:
        current_user_id = get_jwt_identity()
        observations = request.get_json().get('description')
        patient_service = PatientService()
        patient_service.create_request_consult(current_user_id, observations=observations)
        return jsonify({"error": False, "message": "Request accepted successfully"})
    except Exception as e:
        print("Request error: ", e)
        return jsonify({"error": True, "message": str(e)}), 500


@blueprint.route('/patient/nurse_emergencies_requests/data', methods=["GET"])
@jwt_required()
def get_emergencies_paramedic():
    try:
        current_user_id = get_jwt_identity()
        patient_service = PatientService()
        response = patient_service.get_active_emergency(current_user_id)
        return jsonify(response)
    except Exception as error:
        print("Error:", error)
        return jsonify({"error": str(error)})

@blueprint.route('/patient/request_emergency_nurse/data', methods=["GET"])
@jwt_required()
def get_emergencies_nurse():
    try:
        current_user_id = get_jwt_identity()
        patient_service = PatientService()
        response = patient_service.get_active_request_emergency(current_user_id)
        return jsonify(response)
    except Exception as error:
        print("Error:", error)
        return jsonify({"error": str(error)})
    
@blueprint.route('/patient/nurse_emegency_request/data', methods=['GET'])
@jwt_required()
def get_emergencies_nurse_data():
    try:
        current_user_id = get_jwt_identity()
        patient_service = PatientService()
        response = patient_service.get_active_emergency(current_user_id)
        return jsonify(response)
    except Exception as error:
        print("Error:", error)
        return jsonify({"error": str(error)})

@blueprint.route('/patient/nurse_emegency_request/<int:emergency_id>/data', methods=['GET'])
@jwt_required()
def get_emergencies_nurse_data_id(emergency_id):
    try:
        patient_service = PatientService()
        response = patient_service.get_nurse_emergency_request_by_id(emergency_id)
        return jsonify(response)
    except Exception as error:
        print("Error:", error)
        return jsonify({"error": str(error)})


