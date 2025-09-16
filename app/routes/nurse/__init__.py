
from flask import Blueprint

blueprint = Blueprint("nurse", __name__, url_prefix="/nurse")

from . import views
from . import controllers