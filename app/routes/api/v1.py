from flask import request, jsonify, Response, send_file
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.services.patient_service import PatientService
from . import blueprint

@blueprint.route('/v1/patient/auth', methods=['POST'])
def v1_patient_auth():
    data = request.get_json()
            
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()
    
    if not data or not email or not password:
        return Response("Por favor envie os dados de autenticação corretamente", 400)
    
    try:
        patient = PatientService().auth_patient(email, password)
        if patient and patient.active:
            access_token = create_access_token(identity=str(patient.id))
            return jsonify({
                "success": True,
                "access_token": access_token,
                "user": patient.to_dict()
            }), 200
        else:
            return Response("Credenciais inválidas ou usuário inativo", 401)
    except Exception as e:
        print("Error", e)
        return Response(str(e), 500)

@blueprint.route('/v1/patient/register', methods=['POST'])
def v1_patient_register():
    try:
        data = request.get_json()
        patient_service = PatientService()
        patient_service.sign_up_patient(**data)
        return jsonify({"error": False, "message": "Patient registered successfully"})
    except Exception as e:
        print("Patient error: ", e)
        return Response(str(e), 500)

@blueprint.route('/v1/patient/data', methods=['GET'])
@jwt_required()
def v1_get_user():
    try:
        current_user_id = get_jwt_identity()
        patient_service = PatientService()
        patient = patient_service.get_patient(current_user_id)
        return jsonify(patient.to_dict())
    except Exception as e:
        print("Patient error: ", e)
        return Response(str(e), 500)

@blueprint.route('/v1/patient/update_fcm_token', methods=["POST"])
@jwt_required()
def v1_update_fcm_token():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        fcm_token = data.get('token')
        patient_service = PatientService()
        patient_service.update_fcm_token(current_user_id, fcm_token)
        return jsonify({"error": False, "message": "FCM token updated successfully"})
    except Exception as e:
        print("FCM token error: ", e)
        return Response(str(e), 500)

@blueprint.route('/v1/patient/update_location', methods=["POST"])
@jwt_required()
def v1_update_location():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        location = data.get('location')
        patient_service = PatientService()
        patient_service.update_location(current_user_id, location)
        return jsonify({"error": False, "message": "Location updated successfully"})
    except Exception as e:
        print("Location error: ", e)
        return Response(str(e), 500)
    
@blueprint.route('/v1/patient/solicit_consult', methods=["POST"])
@jwt_required()
def v1_solicit_consult():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        description = data.get('description')
        patient_service = PatientService()
        patient_service.create_request_consult(current_user_id, description)
        return jsonify({"error": False, "message": "Consulta solicitada com sucesso"})
    except Exception as e:
        print("Consult error: ", e)
        return Response(str(e), 500)

@blueprint.route('/v1/patient/solicit_emergency', methods=["POST"])
@jwt_required()
def v1_solicit_emergency():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        description = data.get('description')
        patient_service = PatientService()
        patient_service.create_request_emergency(current_user_id)
        return jsonify({"error": False, "message": "Emergência solicitada com sucesso"})
    except Exception as e:
        print("Emergency error: ", e)
        return Response(str(e), 500)

@blueprint.route('/v1/patient/consult_request_patient/data', methods=['GET'])
@jwt_required()
def v1_get_consult_request_patient():
    try:
        current_user_id = get_jwt_identity()
        patient_service = PatientService()
        consult_requests = patient_service.get_consults_request_patient(current_user_id)
        return jsonify(consult_requests)
    except Exception as e:
        print("Consult requests error: ", e)
        return Response(str(e), 500)

@blueprint.route('/v1/patient/consult_request_nurse/data', methods=['GET'])
@jwt_required()
def v1_get_consult_request_nurse():
    try:
        current_user_id = get_jwt_identity()
        patient_service = PatientService()
        consult_requests = patient_service.get_consults_request_nurse(current_user_id)
        return jsonify(consult_requests)
    except Exception as e:
        print("Consult requests error: ", e)
        return Response(str(e), 500)

@blueprint.route('/v1/patient/consults/data', methods=['GET'])
@jwt_required()
def v1_get_consults():
    try:
        current_user_id = get_jwt_identity()
        patient_service = PatientService()
        consults = patient_service.get_consults(current_user_id)
        return jsonify(consults)
    except Exception as e:
        print("Consults error: ", e)
        return Response(str(e), 500)

@blueprint.route('/v1/patient/consults/<consult_id>/data', methods=['GET'])
@jwt_required()
def v1_get_consult_data(consult_id):
    try:
        patient_service = PatientService()
        consult = patient_service.get_consult(consult_id)
        return jsonify(consult)
    except Exception as e:
        print("Consults error: ", e)
        return Response(str(e), 500)

@blueprint.route('/v1/patient/medical_record/data', methods=['GET'])
@jwt_required()
def v1_get_medical_record():
    try:
        current_user_id = get_jwt_identity()
        patient_service = PatientService()
        medical_record = patient_service.get_medical_record(current_user_id)
        return jsonify(medical_record)
    except Exception as e:
        print("Medical record error: ", e)
        return Response(str(e), 500)

@blueprint.route('/v1/patient/recipes/data', methods=['GET'])
@jwt_required()
def v1_get_recipes():
    try:
        current_user_id = get_jwt_identity()
        patient_service = PatientService()
        recipes = patient_service.get_prescriptions(current_user_id)
        return jsonify(recipes)
    except Exception as e:
        print("Recipes error: ", e)
        return Response(str(e), 500)

@blueprint.route('/v1/patient/recipes/<recipe_id>/data', methods=['GET'])
@jwt_required()
def v1_get_recipe(recipe_id):
    try:
        current_user_id = get_jwt_identity()
        patient_service = PatientService()
        recipes = patient_service.get_prescription(recipe_id)
        return jsonify(recipes)
    except Exception as e:
        print("Recipes error: ", e)
        return Response(str(e), 500)

@blueprint.route('/v1/patient/recipes/<recipe_id>/download', methods=["GET"])
def v1_download_recipe(recipe_id):
    try:
        patient_service = PatientService()
        prescription = patient_service.get_prescription(recipe_id)
        return send_file(prescription['pdf_path'], as_attachment=True)
    except Exception as e:
        print("Prescription error: ", e)
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/v1/patient/emergency_request_patient/data', methods=['GET'])
@jwt_required()
def v1_get_emergency_request_patient():
    try:
        current_user_id = get_jwt_identity()
        patient_service = PatientService()
        emergency_requests = patient_service.get_emergencys_request_patient(current_user_id)
        return jsonify(emergency_requests)
    except Exception as e:
        print("Emergency requests error: ", e)
        return Response(str(e), 500)
    
@blueprint.route('/v1/patient/emergency_request_nurse/data', methods=['GET'])
@jwt_required()
def v1_get_emergency_request_nurse():
    try:
        current_user_id = get_jwt_identity()
        patient_service = PatientService()
        emergency_requests = patient_service.get_emergencys_request_nurse(current_user_id)
        return jsonify(emergency_requests)
    except Exception as e:
        print("Emergency requests error: ", e)
        return Response(str(e), 500)
    
@blueprint.route('/v1/patient/call_emergency', methods=['GET'])
@jwt_required()
def v1_call_emergency():
    try:
        current_user_id = get_jwt_identity()
        patient_service = PatientService()
        patient_service.create_request_emergency(current_user_id)
        return jsonify({"error": False, "message": "Emergency called successfully"})
    except Exception as e:
        print("Emergency error: ", e)
        return Response(str(e), 500)

@blueprint.route('/v1/patient/emergency_request/<request_emergency_id>/data', methods=['GET'])
@jwt_required()
def v1_get_emergency_request(request_emergency_id):
    try:
        patient_service = PatientService()
        emergency_requests = patient_service.get_nurse_emergency_request_by_id(request_emergency_id)
        return jsonify(emergency_requests)
    except Exception as e:
        print("Emergency requests error: ", e)
        return Response(str(e), 500)


    