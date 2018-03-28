from flask import Blueprint

main = Blueprint('main_blueprint', __name__)

from . import views, errors, models
