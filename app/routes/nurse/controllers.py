from flask import request, jsonify, redirect, url_for
from flask_login import login_user, logout_user
from app.routes.nurse import blueprint
from app.decorators import nurse_required
from flask_login import current_user
from app.services.nurse_service import NurseService
from flask import flash


# Auth Routes

@blueprint.route('/login', methods=["POST"])
def auth_nurse_post():
    try:
        nurse_service = NurseService()
        email = request.json.get("email")
        password = request.json.get("password")
        remember = request.json.get("remember")
        nurse = nurse_service.auth_nurse(email, password)
        login_user(nurse, remember=remember)
        flash(f'Bem-vindo(a), {nurse.fullname}!', 'success')
        return jsonify({"error": False, "message": "Logged in successfully", "data": nurse.to_dict()})
    except Exception as e:
        print("Login error: ", e)
        flash(f'Erro ao fazer login, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500


@blueprint.route('/logout', methods=["GET"])
def logout_nurse():
    logout_user()
    flash("Logout realizado com sucesso!", 'success')
    return redirect(url_for('nurse.login'))


# Request Consults Routes

@blueprint.route("/requests_consults/data", methods=["GET"])
@nurse_required
def get_requests_consults_data():
    try:
        nurse_service = NurseService()
        requests_consults = nurse_service.get_active_request_consult(current_user.id)
        return jsonify(requests_consults)
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@blueprint.route("/requests_consults/<int:request_consult_id>/accept", methods=["GET"])
@nurse_required
def accept_request_consult(request_consult_id):
    try:
        nurse_service = NurseService()
        nurse_service.accept_request_consult(request_consult_id, current_user.id)
        return jsonify({"message": "Request consult accepted"})
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@blueprint.route("/requests_consults/<int:request_consult_id>/cancel", methods=["GET"])
@nurse_required
def cancel_request_consult(request_consult_id):
    try:
        nurse_service = NurseService()
        nurse_service.cancel_request_consult(request_consult_id)
        return jsonify({"message": "Request consult cancelled"})
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@blueprint.route("/requests_consults/<int:request_consult_id>/attend", methods=["GET"])
@nurse_required
def attend_request_consult(request_consult_id):
    try:
        nurse_service = NurseService()
        nurse_service.attend_request_consult(request_consult_id)
        return jsonify({"message": "Request consult attended"})
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@blueprint.route("/requests_consults/<int:request_consult_id>/finish", methods=["GET"])
@nurse_required
def finish_request_consult(request_consult_id):
    try:
        nurse_service = NurseService()
        nurse_service.finish_request_consult(request_consult_id)
        return jsonify({"message": "Request consult finished"})
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@blueprint.route("/requests_consults/<int:request_consult_id>/data", methods=["GET"])
@nurse_required
def get_request_consult_data(request_consult_id):
    try:
        nurse_service = NurseService()
        request_consult = nurse_service.get_requests_consult_data(request_consult_id)
        return jsonify(request_consult)
    except Exception as e:
        return jsonify({"message": str(e)}), 500


# Medic Record Routes

@blueprint.route("/medic_records/data", methods=["GET"])
@nurse_required
def get_medic_records_data():
    try:
        nurse_service = NurseService()
        medic_records = nurse_service.get_medic_records()
        return jsonify(medic_records)
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@blueprint.route("/medic_records/<int:patient_id>/data", methods=["GET"])
@nurse_required
def get_medic_record_data(patient_id):
    try:
        nurse_service = NurseService()
        medic_record = nurse_service.get_medical_record(patient_id)
        return jsonify(medic_record)
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@blueprint.route("/medic_records/<int:medic_record_id>/edit", methods=["POST"])
@nurse_required
def edit_medic_record(medic_record_id):
    try:
        nurse_service = NurseService()
        nurse_service.edit_medic_record(medic_record_id, request.json)
        return jsonify({"message": "Medic record edited"})
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@blueprint.route("/medic_records/<int:medic_record_id>/delete", methods=["GET"])
@nurse_required
def delete_medic_record(medic_record_id):
    try:
        nurse_service = NurseService()
        nurse_service.delete_medic_record(medic_record_id)
        return jsonify({"message": "Medic record deleted"})
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# Patient Routes

@blueprint.route("/patients/data", methods=["GET"])
@nurse_required
def get_patients_data():
    try:
        nurse_service = NurseService()
        patients = nurse_service.get_patients()
        return jsonify(patients)
    except Exception as e:
        return jsonify({"message": str(e)}), 500


# Request Patient Emergency Routes

@blueprint.route("/requests_emergencies_patient/data", methods=["GET"])
@nurse_required
def get_requests_emergencies_patient_data():
    try:
        nurse_service = NurseService()
        requests_emergencies = nurse_service.get_active_request_emergency(current_user.id)
        return jsonify(requests_emergencies)
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@blueprint.route("/requests_emergencies_patient/<int:request_emergency_id>/accept", methods=["GET"])
@nurse_required
def accept_request_patient_emergency(request_emergency_id):
    try:
        nurse_service = NurseService()
        nurse_service.accept_request_emergency(request_emergency_id, current_user.id)
        return jsonify({"message": "Request emergency accepted"})
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@blueprint.route("/requests_emergencies_patient/<int:request_emergency_id>/finish", methods=["GET"])
@nurse_required
def finish_request_patient_emergency(request_emergency_id):
    try:
        nurse_service = NurseService()
        nurse_service.finish_request_emergency(request_emergency_id)
        return jsonify({"message": "Request emergency finished"})
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@blueprint.route("/requests_emergencies_patient/<int:request_emergency_id>/data", methods=["GET"])
@nurse_required
def get_request_patient_emergency_data(request_emergency_id):
    try:
        nurse_service = NurseService()
        request_emergency = nurse_service.get_request_emergency_data(request_emergency_id)
        return jsonify(request_emergency.to_dict())
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@blueprint.route("/requests_emergencies_patient/<int:request_emergency_id>/cancel", methods=["GET"])
@nurse_required
def cancel_request_patient_emergency(request_emergency_id):
    try:
        nurse_service = NurseService()
        nurse_service.cancel_request_emergency(request_emergency_id)
        return jsonify({"message": "Request emergency cancelled"})
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@blueprint.route("/requests_emergencies_patient/<int:request_emergency_id>/attend", methods=["GET"])
@nurse_required
def attend_request_patient_emergency(request_emergency_id):
    try:
        nurse_service = NurseService()
        nurse_service.attend_request_emergency(request_emergency_id)
        return jsonify({"message": "Request emergency attended"})
    except Exception as e:
        return jsonify({"message": str(e)}), 500


# Request Patient Consult Routes

@blueprint.route("/requests_consults_patient/data", methods=["GET"])
@nurse_required
def get_requests_consults_patient_data():
    try:
        nurse_service = NurseService()
        requests_consults = nurse_service.get_active_request_consult(current_user.id)
        return jsonify(requests_consults)
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@blueprint.route("/requests_consults_patient/<int:request_consult_id>/accept", methods=["GET"])
@nurse_required 
def accept_request_consult_patient(request_consult_id):
    try:
        nurse_service = NurseService()
        nurse_service.accept_request_consult(request_consult_id, current_user.id)
        return jsonify({"message": "Request consult accepted"})
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@blueprint.route("/requests_consults_patient/<int:request_consult_id>/finish", methods=["GET"])
@nurse_required
def finish_request_consult_patient(request_consult_id):
    try:
        nurse_service = NurseService()
        nurse_service.finish_request_consult(request_consult_id)
        return jsonify({"message": "Request consult finished"})
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
@blueprint.route("/requests_consults_patient/<int:request_consult_id>/cancel", methods=["GET"])
@nurse_required
def cancel_request_consult_patient(request_consult_id):
    try:
        nurse_service = NurseService()
        nurse_service.cancel_request_consult(request_consult_id)
        return jsonify({"message": "Request consult cancelled"})
    except Exception as e:
        prin
        return jsonify({"message": str(e)}), 500

@blueprint.route("/requests_consults_patient/<int:request_consult_id>/attend", methods=["GET"])
@nurse_required
def attend_request_consult_patient(request_consult_id):
    try:
        nurse_service = NurseService()
        nurse_service.attend_request_consult(request_consult_id)
        return jsonify({"message": "Request consult attended"})
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@blueprint.route("/requests_consults_patient/<int:request_consult_id>/data", methods=["GET"])
@nurse_required
def get_request_consult_patient_data(request_consult_id):
    try:
        nurse_service = NurseService()
        request_consult = nurse_service.get_requests_consult_data(request_consult_id)
        return jsonify(request_consult)
    except Exception as e:
        return jsonify({"message": str(e)}), 500


# Request Emergency Patient Route

@blueprint.route("/requests_emergencies_patient/add", methods=["POST"])
@nurse_required
def add_active_request_emergency():
    try:
        data = request.json
        nurse_service = NurseService()
        requests_emergencies = nurse_service.create_request_emergency(**data)
        nurse_service.notify_paramedics(requests_emergencies['id'])
        return jsonify(requests_emergencies)
    except Exception as e:
        print("Error adding request emergency patient: ", e)
        return jsonify({"message": str(e)}), 500


# Request Nurse Consult Route

@blueprint.route("/requests_consults_nurse/add", methods=["POST"])
@nurse_required
def add_request_consult_nurse():
    try:
        data = request.json
        nurse_id = current_user.id
        patient_id = data['patient_id']
        consult_type = data['consult_type']
        observations = data['observations']
        consult_date = data['date']
        nurse_service = NurseService()
        nurse_service.create_request_consult(nurse_id, patient_id, observations, consult_type, consult_date)
        return jsonify({"message": "Request consult added"})
    except Exception as e:
        
        print("Error adding request consult nurse: ", str(e))
        return jsonify({"message": str(e)}), 500




