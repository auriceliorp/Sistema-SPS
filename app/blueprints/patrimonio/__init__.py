from flask import Blueprint

bp = Blueprint('patrimonio', __name__)

from app.blueprints.patrimonio import routes 