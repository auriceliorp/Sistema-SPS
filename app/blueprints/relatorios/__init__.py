from flask import Blueprint

bp = Blueprint('relatorios', __name__)

from app.blueprints.relatorios import routes 