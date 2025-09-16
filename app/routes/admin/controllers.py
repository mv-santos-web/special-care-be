from flask import request, jsonify, flash, redirect, url_for, current_app
from werkzeug.utils import secure_filename
import os
from datetime import datetime

from app.routes.admin import blueprint
from app.decorators import admin_required
from flask_login import current_user, login_user, logout_user, login_required
from app.services.admin_service import AdminService

# Auth Routes

@blueprint.route('/login', methods=["POST"])
def auth_admin_post():
    try:
        admin_service = AdminService()
        email = request.json.get("email")
        password = request.json.get("password")
        remember = request.json.get("remember")
        admin = admin_service.auth_admin(email, password)
        login_user(admin, remember=remember)
        flash(f'Bem-vindo(a), {admin.fullname}!', 'success')
        return jsonify({"error": False, "message": "Logged in successfully", "data": admin.to_dict()})
    except Exception as e:
        print("Login error: ", e)
        flash(f'Erro ao fazer login, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/logout', methods=["GET"])
@login_required
def logout_admin():
    try:
        logout_user()
        flash("Logged out successfully", 'success')
        return redirect(url_for('admin.get_login'))
    except Exception as e:
        flash(f'Erro ao fazer logout, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/register', methods=["POST"])
def register_admin_post():
    try:
        admin_service = AdminService()
        admin_service.add_admin(**request.json)
        flash("Admin registered successfully", 'success')
        return jsonify({"error": False, "message": "Admin registered successfully"})
    except Exception as e:
        flash(f'Erro ao registrar admin, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/data', methods=["GET"])
def get_admins_data():
    try:
        admin_service = AdminService()
        admins = admin_service.get_admins()
        return jsonify({"error": False, "message": "Admins fetched successfully", "data": admins})
    except Exception as e:
        flash(f'Erro ao buscar admins, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/<int:admin_id>/data', methods=["GET"])
def admin_data_get(admin_id):
    try:
        admin_service = AdminService()
        admin = admin_service.get_admin(admin_id)
        return jsonify(admin.to_dict())
    except Exception as e:
        flash(f'Erro ao buscar admin, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/<int:admin_id>/edit', methods=["POST"])
def edit_admin_post(admin_id):
    try:
        admin_service = AdminService()
        admin_service.update_admin(admin_id, **request.json)
        flash("Admin updated successfully", 'success')
        return jsonify({"error": False, "message": "Admin updated successfully"})
    except Exception as e:
        print("Edit error: ", e)
        flash(f'Erro ao atualizar admin, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/<int:admin_id>/view', methods=["GET"])
def view_admin(admin_id):
    try:
        admin_service = AdminService()
        admin = admin_service.get_admin(admin_id)
        return jsonify(admin.to_dict())
    except Exception as e:
        flash(f'Erro ao buscar admin, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/<int:admin_id>/delete', methods=["GET"])
def delete_admin(admin_id):
    try:
        admin_service = AdminService()
        admin_service.delete_admin(admin_id)
        flash("Admin deleted successfully", 'success')
        return jsonify({"error": False, "message": "Admin deleted successfully"})
    except Exception as e:
        flash(f'Erro ao deletar admin, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500


# Medics Routes

@blueprint.route('/medics/data', methods=["GET"])
@admin_required
def get_medics_data():
    try:
        admin_service = AdminService()
        medics = admin_service.get_medics()
        return jsonify({"error": False, "message": "Medics fetched successfully", "data": medics})
    except Exception as e:
        print("Medics error: ", e)
        flash(f'Erro ao buscar médicos, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/medics/add', methods=["POST"])
@admin_required
def medic_admin_add():
    try:
        admin_service = AdminService()
        
        certificate_file = request.files['certificate_file']
        cert_filename = secure_filename(certificate_file.filename)
        certificate_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'],"certificates", cert_filename))
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], "certificates", cert_filename)
        
        print(file_path)
        print(request.form)
        
        medic_data = {
            "fullname": request.form.get("fullname"),
            "email": request.form.get("email"),
            "cpf": request.form.get("cpf"),
            "crm": request.form.get("crm"),
            "birthdate": datetime.strptime(request.form.get("birthdate"), "%Y-%m-%d"),
            "gender": request.form.get("gender"),
            "password": request.form.get("password"),
            "phone": request.form.get("phone"),
            "address": request.form.get("address"),
            "certificate_file": file_path
        }
        
        admin_service.add_medic(**medic_data)
        flash("Medic added successfully", 'success')
        return redirect(url_for('admin.get_medics'))
    except Exception as e:
        print("Medic error: ", e)
        flash(f'Erro ao adicionar medic, {str(e)}.', 'error')
        return redirect(url_for('admin.get_medics'))

@blueprint.route('/medics/<int:medic_id>/data', methods=["GET"])
@admin_required
def medic_admin_edit_view(medic_id):
    try:
        admin_service = AdminService()
        medic = admin_service.get_medic(medic_id)
        return jsonify(medic.to_dict())
    except Exception as e:
        print("Medic error: ", e)
        flash(f'Erro ao buscar medic, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/medics/<int:medic_id>/edit', methods=["POST"])
@admin_required
def medic_admin_edit_post(medic_id):
    try:
        admin_service = AdminService()
        json_data = request.json
        print(json_data)
        medic = admin_service.update_medic(medic_id, **json_data)
        flash("Medic updated successfully", 'success')
        return jsonify({"error": False, "message": "Medic updated successfully", "data": medic.to_dict()})
    except Exception as e:
        print("Medic error: ", e)
        flash(f'Erro ao atualizar medic, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/medics/<int:medic_id>/delete', methods=["GET"])
@admin_required
def medic_admin_delete(medic_id):
    try:
        admin_service = AdminService()
        admin_service.delete_medic(medic_id)
        flash("Medic deleted successfully", 'success')
        return jsonify({"error": False, "message": "Medic deleted successfully"})
    except Exception as e:
        print("Medic error: ", e)
        flash(f'Erro ao deletar medic, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500


# Enfermeiros Routes

@blueprint.route('/nurses/data', methods=["GET"])
@admin_required
def get_nurses_data():
    try:
        admin_service = AdminService()
        nurses = admin_service.get_nurses()
        return jsonify({"error": False, "message": "Nurses fetched successfully", "data": nurses})
    except Exception as e:
        print("Nurses error: ", e)
        flash(f'Erro ao buscar enfermeiros, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/nurses/add', methods=["POST"])
@admin_required
def nurse_admin_add():
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
@admin_required
def nurse_admin_edit(nurse_id):
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
@admin_required
def nurse_admin_delete(nurse_id):
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
@admin_required
def nurse_admin_view(nurse_id):
    try:
        admin_service = AdminService()
        nurse = admin_service.get_nurse(nurse_id)
        return jsonify({"error": False, "message": "Nurse fetched successfully", "data": nurse.to_dict()})
    except Exception as e:
        print("Nurse error: ", e)
        flash(f'Erro ao buscar enfermeiro, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500


# Paramédicos Routes

@blueprint.route('/paramedics/data', methods=["GET"])
@admin_required
def get_paramedics_data():
    try:
        admin_service = AdminService()
        paramedics = admin_service.get_paramedics()
        return jsonify({"error": False, "message": "Paramedics fetched successfully", "data": paramedics})
    except Exception as e:
        print("Paramedics error: ", e)
        flash(f'Erro ao buscar paramédicos, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500
    
@blueprint.route('/paramedics/add', methods=["POST"])
@admin_required
def paramedic_admin_add():
    try:
        
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
        
        admin_service = AdminService()
        admin_service.add_paramedic(**json_data)
        flash("Paramedic added successfully", 'success')
        return redirect(url_for('admin.get_paramedics'))
    except Exception as e:
        print("Paramedic error: ", e)
        flash(f'Erro ao adicionar paramédico, {str(e)}.', 'error')
        return redirect(url_for('admin.get_paramedics'))

@blueprint.route('/paramedics/<int:paramedic_id>/edit', methods=["POST"])
@admin_required
def paramedic_admin_edit(paramedic_id):
    try:
        admin_service = AdminService()
        admin_service.update_paramedic(paramedic_id, **request.json)
        flash("Paramedic updated successfully", 'success')
        return jsonify({"error": False, "message": "Paramedic updated successfully"})
    except Exception as e:
        print("Paramedic error: ", e)
        flash(f'Erro ao atualizar paramédico, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/paramedics/<int:paramedic_id>/delete', methods=["GET"])
@admin_required
def paramedic_admin_delete(paramedic_id):
    try:
        admin_service = AdminService()
        admin_service.delete_paramedic(paramedic_id)
        flash("Paramedic deleted successfully", 'success')
        return jsonify({"error": False, "message": "Paramedic deleted successfully"})
    except Exception as e:
        print("Paramedic error: ", e)
        flash(f'Erro ao deletar paramédico, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/paramedics/<int:paramedic_id>/view')
@admin_required
def paramedic_admin_view(paramedic_id):
    try:
        admin_service = AdminService()
        paramedic = admin_service.get_paramedic(paramedic_id)
        return jsonify(paramedic.to_dict())
    except Exception as e:
        print("Paramedic error: ", e)
        flash(f'Erro ao buscar paramédico, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500


# Pacientes Routes

@blueprint.route('/patients/data', methods=["GET"])
@admin_required
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
@admin_required
def patient_admin_add():
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
@admin_required
def patient_admin_edit(patient_id):
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
@admin_required
def patient_admin_delete(patient_id):
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
@admin_required
def patient_admin_view(patient_id):
    try:
        admin_service = AdminService()
        patient = admin_service.get_patient(patient_id)
        return jsonify(patient.to_dict())
    except Exception as e:
        print("Patient error: ", e)
        flash(f'Erro ao buscar paciente, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500


# Consults Routes

@blueprint.route('/consults/data', methods=["GET"])
@admin_required
def get_consults_data():
    try:
        admin_service = AdminService()
        consults = admin_service.get_consults()
        return jsonify({"error": False, "message": "Consults fetched successfully", "data": consults})
    except Exception as e:
        print("Consults error: ", e)
        flash(f'Erro ao buscar consultas, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/consults/add', methods=["POST"])
@admin_required
def consult_admin_add():
    try:
        admin_service = AdminService()
        admin_service.add_consult(**request.json)
        flash("Consult added successfully", 'success')
        return jsonify({"error": False, "message": "Consult added successfully"})
    except Exception as e:
        print("Consult error: ", e)
        flash(f'Erro ao adicionar consulta, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/consults/<int:consult_id>/edit', methods=["POST"])
@admin_required
def consult_admin_edit(consult_id):
    try:
        admin_service = AdminService()
        admin_service.update_consult(consult_id, **request.json)
        flash("Consult updated successfully", 'success')
        return jsonify({"error": False, "message": "Consult updated successfully"})
    except Exception as e:
        print("Consult error: ", e)
        flash(f'Erro ao atualizar consulta, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/consults/<int:consult_id>/delete', methods=["GET"])
@admin_required
def consult_admin_delete(consult_id):
    try:
        admin_service = AdminService()
        admin_service.delete_consult(consult_id)
        flash("Consult deleted successfully", 'success')
        return jsonify({"error": False, "message": "Consult deleted successfully"})
    except Exception as e:
        print("Consult error: ", e)
        flash(f'Erro ao deletar consulta, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/consults/<int:consult_id>/view', methods=["GET"])
@admin_required
def consult_admin_view(consult_id):
    try:
        admin_service = AdminService()
        consult = admin_service.get_consult(consult_id)
        return jsonify(consult.to_dict())
    except Exception as e:
        print("Consult error: ", e)
        flash(f'Erro ao buscar consulta, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500


# Emergencies Routes

@blueprint.route('/emergencies/data', methods=["GET"])
@admin_required
def get_emergencies_data():
    try:
        admin_service = AdminService()
        emergencies = admin_service.get_emergencies()
        return jsonify({"error": False, "message": "Emergencies fetched successfully", "data": emergencies})
    except Exception as e:
        print("Emergencies error: ", e)
        flash(f'Erro ao buscar emergências, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/emergencies/add', methods=["POST"])
@admin_required
def emergency_admin_add():
    try:
        admin_service = AdminService()
        admin_service.add_emergency(**request.json)
        flash("Emergency added successfully", 'success')
        return jsonify({"error": False, "message": "Emergency added successfully"})
    except Exception as e:
        print("Emergency error: ", e)
        flash(f'Erro ao adicionar emergência, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/emergencies/<int:emergency_id>/edit', methods=["POST"])
@admin_required
def emergency_admin_edit(emergency_id):
    try:
        admin_service = AdminService()
        admin_service.update_emergency(emergency_id, **request.json)
        flash("Emergency updated successfully", 'success')
        return jsonify({"error": False, "message": "Emergency updated successfully"})
    except Exception as e:
        print("Emergency error: ", e)
        flash(f'Erro ao atualizar emergência, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/emergencies/<int:emergency_id>/delete', methods=["GET"])
@admin_required
def emergency_admin_delete(emergency_id):
    try:
        admin_service = AdminService()
        admin_service.delete_emergency(emergency_id)
        flash("Emergency deleted successfully", 'success')
        return jsonify({"error": False, "message": "Emergency deleted successfully"})
    except Exception as e:
        print("Emergency error: ", e)
        flash(f'Erro ao deletar emergência, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/emergencies/<int:emergency_id>/view', methods=["GET"])
@admin_required
def emergency_admin_view(emergency_id):
    try:
        admin_service = AdminService()
        emergency = admin_service.get_emergency(emergency_id)
        return jsonify(emergency.to_dict())
    except Exception as e:
        print("Emergency error: ", e)
        flash(f'Erro ao buscar emergência, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500


# Prescriptions Routes

@blueprint.route('/prescriptions/data', methods=["GET"])
@admin_required
def get_prescriptions_data():
    try:
        admin_service = AdminService()
        prescriptions = admin_service.get_prescriptions()
        return jsonify({"error": False, "message": "Prescriptions fetched successfully", "data": prescriptions})
    except Exception as e:
        print("Prescriptions error: ", e)
        flash(f'Erro ao buscar prescrições, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/prescriptions/add', methods=["POST"])
@admin_required
def prescription_admin_add():
    try:
        admin_service = AdminService()
        admin_service.add_prescription(**request.json)
        flash("Prescription added successfully", 'success')
        return jsonify({"error": False, "message": "Prescription added successfully"})
    except Exception as e:
        print("Prescription error: ", e)
        flash(f'Erro ao adicionar prescrição, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500
    
@blueprint.route('/prescriptions/<int:prescription_id>/view', methods=["GET"])
@admin_required
def prescription_admin_view(prescription_id):
    try:
        admin_service = AdminService()
        prescription = admin_service.get_prescription(prescription_id)
        return jsonify(prescription.to_dict())
    except Exception as e:
        print("Prescription error: ", e)
        flash(f'Erro ao buscar prescrição, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/prescriptions/<int:prescription_id>/delete', methods=["GET"])
@admin_required
def prescription_admin_delete(prescription_id):
    try:
        admin_service = AdminService()
        admin_service.delete_prescription(prescription_id)
        flash("Prescription deleted successfully", 'success')
        return jsonify({"error": False, "message": "Prescription deleted successfully"})
    except Exception as e:
        print("Prescription error: ", e)
        flash(f'Erro ao deletar prescrição, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/prescriptions/<int:prescription_id>/download', methods=["GET"])
@admin_required
def prescription_admin_download(prescription_id):
    try:
        admin_service = AdminService()
        prescription = admin_service.get_prescription(prescription_id)
        return send_file(prescription.pdf_path, as_attachment=True)
    except Exception as e:
        print("Prescription error: ", e)
        flash(f'Erro ao baixar prescrição, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500


# Medical Records Routes

@blueprint.route('/medical_records/data', methods=["GET"])
@admin_required
def get_medical_records_data():
    try:
        admin_service = AdminService()
        medical_records = admin_service.get_medic_records()
        return jsonify({"error": False, "message": "Medical records fetched successfully", "data": medical_records})
    except Exception as e:
        print("Medical records error: ", e)
        flash(f'Erro ao buscar registros médicos, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/medical_records/add', methods=["POST"])
@admin_required
def medical_record_admin_add():
    try:
        admin_service = AdminService()
        admin_service.add_medic_record(**request.json)
        flash("Medical record added successfully", 'success')
        return jsonify({"error": False, "message": "Medical record added successfully"})
    except Exception as e:
        print("Medical record error: ", e)
        flash(f'Erro ao adicionar registro médico, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500
    
@blueprint.route('/medical_records/<int:medical_record_id>/edit', methods=["POST"])
@admin_required
def medical_record_admin_edit(medical_record_id):
    try:
        admin_service = AdminService()
        admin_service.update_medic_record(medical_record_id, **request.json)
        flash("Medical record updated successfully", 'success')
        return jsonify({"error": False, "message": "Medical record updated successfully"})
    except Exception as e:
        print("Medical record error: ", e)
        flash(f'Erro ao atualizar registro médico, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/medical_records/<int:medical_record_id>/delete', methods=["GET"])
@admin_required
def medical_record_admin_delete(medical_record_id):
    try:
        admin_service = AdminService()
        admin_service.delete_medic_record(medical_record_id)
        flash("Medical record deleted successfully", 'success')
        return jsonify({"error": False, "message": "Medical record deleted successfully"})
    except Exception as e:
        print("Medical record error: ", e)
        flash(f'Erro ao deletar registro médico, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500
  
@blueprint.route('/medical_records/<int:medical_record_id>/view', methods=["GET"])
@admin_required
def medical_record_admin_view(medical_record_id):
    try:
        admin_service = AdminService()
        medical_record = admin_service.get_medic_record(medical_record_id)
        return jsonify(medical_record.to_dict())
    except Exception as e:
        print("Medical record error: ", e)
        flash(f'Erro ao buscar registro médico, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500
  
    
    
    
    
    