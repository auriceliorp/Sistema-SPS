from flask import Blueprint

bp = Blueprint('almoxarifado', __name__)

from app.blueprints.almoxarifado import routes
from app.blueprints.almoxarifado.entrada import bp as entrada_bp
from app.blueprints.almoxarifado.saida import bp as saida_bp

bp.register_blueprint(entrada_bp)
bp.register_blueprint(saida_bp) 