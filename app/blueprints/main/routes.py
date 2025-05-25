from flask import render_template
from flask_login import login_required, current_user
from app.blueprints.main import bp
from app.models.item import Item
from app.models.movimento import EntradaMaterial, SaidaMaterial
from app.models.patrimonio import BemPatrimonial
from app.services.almoxarifado import AlmoxarifadoService

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return render_template('painel/home.html')

@bp.route('/perfil')
@login_required
def perfil():
    return render_template('painel/perfil.html', title='Meu Perfil')

@bp.route('/sobre')
def sobre():
    return render_template('painel/sobre.html', title='Sobre o Sistema') 