from flask import request, jsonify, flash, redirect, url_for, current_app, send_file, render_template
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime

from app.routes.medic import blueprint
from app.decorators import medic_required
from flask_login import current_user, login_user, logout_user, login_required
from app.services.medic_service import MedicService
from app.services.pdf_service import PdfService

# Auth Routes

@blueprint.route('/login', methods=["POST"])
def auth_medic_post():
    try:
        medic_service = MedicService()
        email = request.json.get("email")
        password = request.json.get("password")
        remember = request.json.get("remember")
        medic = medic_service.auth_medic(email, password)
        login_user(medic, remember=remember)
        flash(f'Bem-vindo(a), {medic.fullname}!', 'success')
        return jsonify({"error": False, "message": "Logged in successfully", "data": medic.to_dict()})
    except Exception as e:
        print("Login error: ", e)
        flash(f'Erro ao fazer login, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/logout', methods=["GET"])
@login_required
def logout_medic():
    try:
        logout_user()
        flash("Logged out successfully", 'success')
        return redirect(url_for('medic.get_login'))
    except Exception as e:
        flash(f'Erro ao fazer logout, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/data', methods=["GET"])
@medic_required
def get_medics_data():
    try:
        medic_service = MedicService()
        medics = medic_service.get_medics()
        return jsonify({"error": False, "message": "Medics fetched successfully", "data": medics})
    except Exception as e:
        flash(f'Erro ao buscar medics, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/<int:medic_id>/data', methods=["GET"])
@medic_required
def medic_data_get(medic_id):
    try:
        medic_service = MedicService()
        medic = medic_service.get_medic(medic_id)
        return jsonify(medic.to_dict())
    except Exception as e:
        flash(f'Erro ao buscar medic, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/<int:medic_id>/edit', methods=["POST"])
@medic_required
def edit_medic_post(medic_id):
    try:
        medic_service = MedicService()
        medic_service.update_medic(medic_id, **request.json)
        flash("Medic updated successfully", 'success')
        return jsonify({"error": False, "message": "Medic updated successfully"})
    except Exception as e:
        print("Edit error: ", e)
        flash(f'Erro ao atualizar medic, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/<int:medic_id>/view', methods=["GET"])
@medic_required
def view_medic(medic_id):
    try:
        medic_service = MedicService()
        medic = medic_service.get_medic(medic_id)
        return jsonify(medic.to_dict())
    except Exception as e:
        flash(f'Erro ao buscar medic, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/<int:medic_id>/delete', methods=["GET"])
@medic_required
def delete_medic(medic_id):
    try:
        medic_service = MedicService()
        medic_service.delete_medic(medic_id)
        flash("Medic deleted successfully", 'success')
        return jsonify({"error": False, "message": "Medic deleted successfully"})
    except Exception as e:
        flash(f'Erro ao deletar medic, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500


# Enfermeiros Routes

@blueprint.route('/nurses/data', methods=["GET"])
@medic_required
def get_nurses_data():
    try:
        nurse_service = NurseService()
        nurses = nurse_service.get_nurses()
        return jsonify({"error": False, "message": "Nurses fetched successfully", "data": nurses})
    except Exception as e:
        print("Nurses error: ", e)
        flash(f'Erro ao buscar enfermeiros, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/nurses/add', methods=["POST"])
@medic_required
def nurse_medic_add():
    try: 
        form_data = request.form
        
        json_data = {
            "fullname": form_data.get("fullname"),
            "email": form_data.get("email"),
            "cpf": form_data.get("cpf"),
            "coren": form_data.get("coren"),
            "birthdate": datetime.strptime(form_data.get("birthdate"), "%Y-%m-%d"),
            "gender": form_data.get("gender"),
            "password": form_data.get("password"),
            "phone": form_data.get("phone"),
            "address": form_data.get("address"),
            "active": form_data.get("active")
        }
    
        admin_service = AdminService()
        admin_service.add_nurse(**json_data)
        flash("Nurse added successfully", 'success')
        return redirect(url_for('admin.get_nurses'))
    except Exception as e:
        print("Nurse error: ", e)
        flash(f'Erro ao adicionar enfermeiro, {str(e)}.', 'error')
        return redirect(url_for('admin.get_nurses'))

@blueprint.route('/nurses/<int:nurse_id>/edit', methods=["POST"])
@medic_required
def nurse_medic_edit(nurse_id):
    try:
        admin_service = AdminService()
        admin_service.update_nurse(nurse_id, **request.json)
        flash("Nurse updated successfully", 'success')
        return jsonify({"error": False, "message": "Nurse updated successfully"})
    except Exception as e:
        print("Edit error: ", e)
        flash(f'Erro ao atualizar enfermeiro, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/nurses/<int:nurse_id>/delete', methods=["GET"])
@medic_required
def nurse_medic_delete(nurse_id):
    try:
        admin_service = AdminService()
        admin_service.delete_nurse(nurse_id)
        flash("Nurse deleted successfully", 'success')
        return jsonify({"error": False, "message": "Nurse deleted successfully"})
    except Exception as e:
        print("Delete error: ", e)
        flash(f'Erro ao deletar enfermeiro, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/nurses/<int:nurse_id>/view')
@medic_required
def nurse_medic_view(nurse_id):
    try:
        admin_service = AdminService()
        nurse = admin_service.get_nurse(nurse_id)
        return jsonify({"error": False, "message": "Nurse fetched successfully", "data": nurse.to_dict()})
    except Exception as e:
        print("Nurse error: ", e)
        flash(f'Erro ao buscar enfermeiro, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500


# Pacientes Routes

@blueprint.route('/patients/data', methods=["GET"])
@medic_required
def get_patients_data():
    try:
        admin_service = AdminService()
        patients = admin_service.get_patients()
        return jsonify({"error": False, "message": "Patients fetched successfully", "data": patients})
    except Exception as e:
        print("Patients error: ", e)
        flash(f'Erro ao buscar pacientes, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500
    
@blueprint.route('/patients/add', methods=["POST"])
@medic_required
def patient_medic_add():
    try:
        admin_service = AdminService()
        form_data = request.form
        json_data = {
            "fullname": form_data.get("fullname"),
            "email": form_data.get("email"),
            "cpf": form_data.get("cpf"),
            "birthdate": datetime.strptime(form_data.get("birthdate"), "%Y-%m-%d"),
            "gender": form_data.get("gender"),
            "password": form_data.get("password"),
            "phone": form_data.get("phone"),
            "address": form_data.get("address"),
            "active": form_data.get("active")
        }
        admin_service.add_patient(**json_data)
        flash("Patient added successfully", 'success')
        return redirect(url_for('admin.get_patients'))
    except Exception as e:
        print("Patient error: ", e)
        flash(f'Erro ao adicionar paciente, {str(e)}.', 'error')
        return redirect(url_for('admin.get_patients'))

@blueprint.route('/patients/<int:patient_id>/edit', methods=["POST"])
@medic_required
def patient_medic_edit(patient_id):
    try:
        admin_service = AdminService()
        admin_service.update_patient(patient_id, **request.json)
        flash("Patient updated successfully", 'success')
        return jsonify({"error": False, "message": "Patient updated successfully"})
    except Exception as e:
        print("Patient error: ", e)
        flash(f'Erro ao atualizar paciente, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/patients/<int:patient_id>/delete', methods=["GET"])
@medic_required
def patient_medic_delete(patient_id):
    try:
        admin_service = AdminService()
        admin_service.delete_patient(patient_id)
        flash("Patient deleted successfully", 'success')
        return jsonify({"error": False, "message": "Patient deleted successfully"})
    except Exception as e:
        print("Patient error: ", e)
        flash(f'Erro ao deletar paciente, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/patients/<int:patient_id>/view', methods=["GET"])
@medic_required
def patient_medic_view(patient_id):
    try:
        medic_service = MedicService()
        patient = medic_service.get_patient(patient_id)
        return jsonify(patient.to_dict())
    except Exception as e:
        print("Patient error: ", e)
        flash(f'Erro ao buscar paciente, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500


# Consults Routes

@blueprint.route('/consults/data', methods=["GET"])
@medic_required
def get_consults_data():
    try:
        medic_service = MedicService()
        consults = medic_service.get_consults(current_user.id)
        return jsonify({"error": False, "message": "Consults fetched successfully", "data": consults})
    except Exception as e:
        print("Consults error: ", e)
        flash(f'Erro ao buscar consultas, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/consults/add', methods=["POST"])
@medic_required
def consult_medic_add():
    try:
        medic_service = MedicService()
        medic_service.add_consult(**request.json)
        flash("Consult added successfully", 'success')
        return jsonify({"error": False, "message": "Consult added successfully"})
    except Exception as e:
        print("Consult error: ", e)
        flash(f'Erro ao adicionar consulta, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/consults/<int:consult_id>/edit', methods=["POST"])
@medic_required
def consult_medic_edit(consult_id):
    try:
        medic_service = MedicService()
        medic_service.update_consult(consult_id, **request.json)
        flash("Consult updated successfully", 'success')
        return jsonify({"error": False, "message": "Consult updated successfully"})
    except Exception as e:
        print("Consult error: ", e)
        flash(f'Erro ao atualizar consulta, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/consults/<int:consult_id>/delete', methods=["GET"])
@medic_required
def consult_medic_delete(consult_id):
    try:
        medic_service = MedicService()
        medic_service.delete_consult(consult_id)
        flash("Consult deleted successfully", 'success')
        return jsonify({"error": False, "message": "Consult deleted successfully"})
    except Exception as e:
        print("Consult error: ", e)
        flash(f'Erro ao deletar consulta, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/consults/<int:consult_id>/view', methods=["GET"])
@medic_required
def consult_medic_view(consult_id):
    try:
        medic_service = MedicService()
        consult = medic_service.get_consult(consult_id)
        return jsonify(consult.to_dict())
    except Exception as e:
        print("Consult error: ", e)
        flash(f'Erro ao buscar consulta, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500


# Prescriptions Routes

@blueprint.route('/prescriptions/data', methods=["GET"])
@medic_required
def get_prescriptions_data():
    try:
        medic_service = MedicService()
        prescriptions = medic_service.get_prescriptions(current_user.id)
        return jsonify({"error": False, "message": "Prescriptions fetched successfully", "data": prescriptions})
    except Exception as e:
        print("Prescriptions error: ", e)
        flash(f'Erro ao buscar prescrições, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/prescriptions/add', methods=["POST"])
@medic_required
def prescription_medic_add():
    try:
        medic_service = MedicService()
        pdf_service = PdfService(current_app)
        medic_id = current_user.id
        jsonData = request.get_json()
        print(jsonData)
        
        patient_id = jsonData.get('patient_id')
        prescription_type = jsonData.get('prescription_type')
        observations = jsonData.get('observations', '')
        medicines = jsonData.get('medicines', [])
        
        if not all([patient_id, prescription_type]):
            return jsonify({'message': 'Campos obrigatórios não preenchidos'}), 400
            
        if len(medicines) == 0:
            return jsonify({'message': 'Pelo menos um medicamento deve ser selecionado'}), 400
        
        patient = medic_service.get_patient(patient_id)
        medic = medic_service.get_medic(medic_id)
        
        if not patient or not medic:
            flash(f"Paciente ou médico não encontrado", 'error')
            return jsonify({"error": True, "message": "Paciente ou médico não encontrado"}), 404

        pdf_data = {
            'patient': patient,
            'medic': medic,
            'prescription_type': 'Normal' if prescription_type == 'normal' else 'Controlada',
            'medicines': medicines,
            'observations': observations,
            'issue_date': datetime.now().isoformat()
        }   
        
        cert_pass = jsonData.get('cert_pass', '')
        
        pdf_path, validation_code = pdf_service.generate_pdf(pdf_data)
        signed_path = pdf_service.sign_pdf(pdf_path, medic['certificate_file'], password=cert_pass)
        prescription_data = {
            'patient_id': patient_id,
            'medic_id': medic_id,
            'data': pdf_data,
            'pdf_path': signed_path,
            'validation_code': validation_code
        }
        
        medic_service.create_prescription(**prescription_data)
        flash("Prescription added successfully", 'success')
        return jsonify({"error": False, "message": "Prescription added successfully"})
    except Exception as e:
        print("Prescription error: ", e)
        flash(f'Erro ao adicionar prescrição, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500
    
@blueprint.route('/prescriptions/<int:prescription_id>/view', methods=["GET"])
@medic_required
def prescription_medic_view(prescription_id):
    try:
        medic_service = MedicService()
        prescription = medic_service.get_prescription(prescription_id)
    
        # if not request.headers['json_mode']:
        #     return jsonify(prescription)
        
        prescription_data = prescription['recipe_metadata']
        return render_template('prescription_template.html', **prescription_data)    
        
    
    except Exception as e:
        print("Prescription error: ", e)
        flash(f'Erro ao buscar prescrição, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/prescriptions/<int:prescription_id>/delete', methods=["GET"])
@medic_required
def prescription_medic_delete(prescription_id):
    try:
        medic_service = MedicService()
        medic_service.delete_prescription(prescription_id)
        flash("Prescription deleted successfully", 'success')
        return jsonify({"error": False, "message": "Prescription deleted successfully"})
    except Exception as e:
        print("Prescription error: ", e)
        flash(f'Erro ao deletar prescrição, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/prescriptions/<int:prescription_id>/download', methods=["GET"])
@medic_required
def prescription_medic_download(prescription_id):
    try:
        medic_service = MedicService()
        prescription = medic_service.get_prescription(prescription_id)
        return send_file(prescription['pdf_path'], as_attachment=True)
    except Exception as e:
        print("Prescription error: ", e)
        flash(f'Erro ao baixar prescrição, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500


# Medical Records Routes

@blueprint.route('/medical_records/data', methods=["GET"])
@medic_required
def get_medical_records_data():
    try:
        medic_service = MedicService()
        medical_records = medic_service.get_medic_records()
        return jsonify({"error": False, "message": "Medical records fetched successfully", "data": medical_records})
    except Exception as e:
        print("Medical records error: ", e)
        flash(f'Erro ao buscar registros médicos, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/medical_records/add', methods=["POST"])
@medic_required
def medical_record_medic_add():
    try:
        form_data = request.form
        
        json_data = {
            'patient_id': form_data.get('patient_id'),
            'medic_history': form_data.get('medic_history'),
            'medicines': form_data.get('medicines'),
            'observations': form_data.get('observations')
        }
        print(json_data)
        medic_service = MedicService()
        medic_service.create_medic_record(**json_data)
        flash("Medical record added successfully", 'success')
        return redirect(url_for('medic.get_medical_records'))
    except Exception as e:
        print("Medical record error: ", e)
        flash(f'Erro ao adicionar registro médico, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500
    
@blueprint.route('/medical_records/<int:patient_id>/edit', methods=["POST"])
@medic_required
def medical_record_medic_edit(patient_id):
    try:
        medic_service = MedicService()
        medic_service.edit_medic_record(patient_id, **request.json)
        flash("Medical record updated successfully", 'success')
        return jsonify({"error": False, "message": "Medical record updated successfully"})
    except Exception as e:
        print("Medical record error: ", e)
        flash(f'Erro ao atualizar registro médico, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/medical_records/<int:medical_record_id>/delete', methods=["GET"])
@medic_required
def medical_record_medic_delete(medical_record_id):
    try:
        medic_service = MedicService()
        medic_service.delete_medic_record(medical_record_id)
        flash("Medical record deleted successfully", 'success')
        return jsonify({"error": False, "message": "Medical record deleted successfully"})
    except Exception as e:
        print("Medical record error: ", e)
        flash(f'Erro ao deletar registro médico, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500
  
@blueprint.route('/medical_records/<int:medical_record_id>/data', methods=["GET"])
@medic_required
def medical_record_medic_data(medical_record_id):
    try:
        medic_service = MedicService()
        medical_record = medic_service.get_medic_record(medical_record_id)
        return jsonify(medical_record)
    except Exception as e:
        print("Medical record error: ", e)
        flash(f'Erro ao buscar registro médico, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500
  
    
    
# Solicitações de Atendimento

@blueprint.route('/requests_care/data', methods=["GET"])
@medic_required
def requests_care_medic_data():
    try:
        medic_service = MedicService()
        requests_care = medic_service.get_requests_consults(current_user.id)
        return jsonify({"error": False, "message": "Requests care fetched successfully", "data": requests_care})
    except Exception as e:
        print("Requests care error: ", e)
        flash(f'Erro ao buscar solicitações de atendimento, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/requests_care/<int:request_id>/attend', methods=["GET"])
@medic_required
def requests_care_medic_attend(request_id):
    try:
        medic_service = MedicService()
        request_care = medic_service.attend_request_consult(request_id)
        return jsonify(request_care)
    except Exception as e:
        print("Requests care error: ", e)
        flash(f'Erro ao buscar solicitações de atendimento, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/requests_care/<int:request_id>/data', methods=["GET"])
@medic_required
def request_care_medic_data(request_id):
    try:
        medic_service = MedicService()
        request_care = medic_service.get_requests_consult_data(request_id)
        return jsonify(request_care)
    except Exception as e:
        print("Requests care error: ", e)
        flash(f'Erro ao buscar solicitações de atendimento, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/requests_care/<int:request_id>/accept', methods=["GET"])
@medic_required
def request_care_medic_accept(request_id):
    try:
        medic_service = MedicService()
        medic_service.accept_request_consult(request_id, current_user.id)
        return jsonify({"error": False, "message": "Request care accepted successfully"})
    except Exception as e:
        print("Requests care error: ", e)
        flash(f'Erro ao buscar solicitações de atendimento, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500    


    
    