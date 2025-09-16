from flask import render_template
from app.routes.nurse import blueprint
from app.decorators import nurse_required
from app.models.medic import Medic

@blueprint.route("/login", methods=["GET"])
def login():
    return render_template("nurse/login.html")

@blueprint.route("/", methods=["GET"])
@nurse_required
def index():
    return render_template("nurse/index.html")

@blueprint.route("/requests_consults", methods=["GET"])
@nurse_required
def get_requests_consults():
    return render_template("nurse/requests_care.html", medics=Medic.query.all())

@blueprint.route("/medical_records", methods=["GET"])
@nurse_required
def get_medical_records():
    return render_template("nurse/medical_records.html")

@blueprint.route("/prescriptions", methods=["GET"])
@nurse_required
def get_prescriptions():
    return render_template("nurse/prescriptions.html")

@blueprint.route("/patients", methods=["GET"])
@nurse_required
def get_patients():
    return render_template("nurse/patients.html")

@blueprint.route("/requests_emergencies", methods=["GET"])
@nurse_required
def get_req_emergencies():
    
    return render_template("nurse/requests_emergency.html")



