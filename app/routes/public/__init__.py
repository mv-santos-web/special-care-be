
from flask import Blueprint, render_template
from app.services.admin_service import AdminService

blueprint = Blueprint("public", __name__, url_prefix="/")

@blueprint.route("validate_recipe/<token>", methods=["GET"])
def validate(token):
    admin_service = AdminService()
    recipe = admin_service.get_prescription_by_validation(token)
    print(recipe.to_dict())
    return render_template("public/validate.html", **recipe.to_dict())

