
from flask import Blueprint

blueprint = Blueprint("medic", __name__, url_prefix="/medic")

from . import views
from . import controllers