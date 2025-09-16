from flask import render_template

from app.routes.medic import blueprint
from app.decorators import medic_required
from app.models.patient import Patient

@blueprint.route("/login", methods=["GET"])
def get_login():
    return render_template("medic/login.html")

@blueprint.route("/", methods=["GET"])
@medic_required
def index():
    return render_template("medic/index.html")

@blueprint.route('/consults', methods=["GET"])
@medic_required
def get_consults():
    return render_template("medic/consults.html")

@blueprint.route('/medical_records', methods=["GET"])
@medic_required
def get_medical_records():
    return render_template("medic/medical_records.html", patients=Patient.query.all())

@blueprint.route('/prescriptions', methods=["GET"])
@medic_required
def get_prescriptions():
    return render_template("medic/prescriptions.html", patients=Patient.query.all())

@blueprint.route('/medics', methods=["GET"])
@medic_required
def get_medics():
    return render_template("medic/medics.html")

@blueprint.route('/nurses', methods=["GET"])
@medic_required
def get_nurses():
    return render_template("medic/nurses.html")

@blueprint.route('/patients', methods=["GET"])
@medic_required
def get_patients():
    return render_template("medic/patients.html")

@blueprint.route('/paramedics', methods=["GET"])
@medic_required
def get_paramedics():
    return render_template("medic/paramedics.html")

@blueprint.route('/emergencies', methods=["GET"])
@medic_required
def get_emergencies():
    return render_template("medic/emergencies.html")

@blueprint.route('/admins', methods=["GET"])
@medic_required
def get_admins():
    return render_template("medic/admins.html")

@blueprint.route('/requests_care', methods=["GET"])
@medic_required
def get_requests_care():
    return render_template("medic/requests_care.html")




