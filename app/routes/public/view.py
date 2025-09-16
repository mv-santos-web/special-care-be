from . import blueprint
from flask import render_template
from app.services.admin_service import AdminService

@blueprint.route("/validate_recipe/<token>", methods=["GET"])
def validate(token):
    admin_service = AdminService()
    recipe = admin_service.get_prescription_by_validation(token)
    return render_template("public/validate.html", **recipe.to_dict())

