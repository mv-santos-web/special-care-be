
from flask import Blueprint

blueprint = Blueprint("public", __name__, url_prefix="/")

from . import views