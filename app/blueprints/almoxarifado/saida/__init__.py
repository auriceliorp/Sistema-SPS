from flask import Blueprint

bp = Blueprint('saida', __name__, url_prefix='/saida')

from app.blueprints.almoxarifado.saida import routes 