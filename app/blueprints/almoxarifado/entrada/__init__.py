from flask import Blueprint

bp = Blueprint('entrada', __name__, url_prefix='/entrada')

from app.blueprints.almoxarifado.entrada import routes 