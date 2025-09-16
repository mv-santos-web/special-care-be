from flask import render_template

from app.routes.admin import blueprint
from app.decorators import admin_required

@blueprint.route("/login", methods=["GET"])
def get_login():
    return render_template("admin/login.html")

@blueprint.route("/", methods=["GET"])
@admin_required
def index():
    return render_template("admin/index.html")

@blueprint.route('/consults', methods=["GET"])
@admin_required
def get_consults():
    return render_template("admin/consults.html")

@blueprint.route('/medical_records', methods=["GET"])
@admin_required
def get_medical_records():
    return render_template("admin/medical_records.html")

@blueprint.route('/prescriptions', methods=["GET"])
@admin_required
def get_prescriptions():
    return render_template("admin/prescriptions.html")

@blueprint.route('/medics', methods=["GET"])
@admin_required
def get_medics():
    return render_template("admin/medics.html")

@blueprint.route('/nurses', methods=["GET"])
@admin_required
def get_nurses():
    return render_template("admin/nurses.html")

@blueprint.route('/patients', methods=["GET"])
@admin_required
def get_patients():
    return render_template("admin/patients.html")

@blueprint.route('/paramedics', methods=["GET"])
@admin_required
def get_paramedics():
    return render_template("admin/paramedics.html")

@blueprint.route('/emergencies', methods=["GET"])
@admin_required
def get_emergencies():
    return render_template("admin/emergencies.html")

@blueprint.route('/admins', methods=["GET"])
@admin_required
def get_admins():
    return render_template("admin/admins.html")





