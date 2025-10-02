from flask import Blueprint

blueprint = Blueprint("api", __name__, url_prefix="/api")

from . import paramedic
from . import patient
from . import v1