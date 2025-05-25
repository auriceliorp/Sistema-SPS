from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.item import Item
from app.models.movimento import SaidaMaterial, SaidaItem
from app.models.local import UnidadeLocal
from app.services.almoxarifado import AlmoxarifadoService
from app.utils.exceptions import ItemNaoEncontradoError, EstoqueInsuficienteError
from app.utils.decorators import admin_required
from app.blueprints.almoxarifado.saida import bp
from datetime import datetime

@bp.route('/')
@login_required
def lista_saidas():
    """Lista todas as saídas de material."""
    page = request.args.get('page', 1, type=int)
    filtro = request.args.get('filtro', 'setor')
    busca = request.args.get('busca', '').strip().lower()
    
    saidas = AlmoxarifadoService.buscar_saidas(
        page=page,
        filtro=filtro,
        busca=busca
    )
    
    return render_template(
        'saidas/list.html',
        saidas=saidas,
        filtro=filtro,
        busca=busca
    )

@bp.route('/nova', methods=['GET', 'POST'])
@login_required
def nova_saida():
    """Cadastra uma nova saída de material."""
    if request.method == 'POST':
        try:
            saida = AlmoxarifadoService.registrar_saida(
                data_saida=datetime.strptime(request.form.get('data_saida'), '%Y-%m-%d'),
                setor_id=request.form.get('setor'),
                requisitante=request.form.get('requisitante'),
                tipo_saida=request.form.get('tipo_saida'),
                observacao=request.form.get('observacao'),
                usuario_id=current_user.id
            )
            flash('Saída registrada com sucesso!', 'success')
            return redirect(url_for('almoxarifado.saida.lista_saidas'))
        except EstoqueInsuficienteError as e:
            flash(str(e), 'danger')
        except Exception as e:
            flash(f'Erro ao registrar saída: {str(e)}', 'danger')
    
    setores = UnidadeLocal.query.all()
    itens = Item.query.filter_by(excluido=False).all()
    return render_template('saidas/form.html', setores=setores, itens=itens)

@bp.route('/<int:id>')
@login_required
def visualizar_saida(id):
    """Visualiza os detalhes de uma saída específica."""
    saida = SaidaMaterial.query.get_or_404(id)
    return render_template('saidas/detail.html', saida=saida)

@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_saida(id):
    """Edita uma saída existente."""
    saida = SaidaMaterial.query.get_or_404(id)
    
    if saida.status == 'Finalizada':
        flash('Não é possível editar uma saída finalizada.', 'warning')
        return redirect(url_for('almoxarifado.saida.lista_saidas'))
    
    if request.method == 'POST':
        try:
            AlmoxarifadoService.atualizar_saida(
                saida_id=id,
                data_saida=datetime.strptime(request.form.get('data_saida'), '%Y-%m-%d'),
                setor_id=request.form.get('setor'),
                requisitante=request.form.get('requisitante'),
                tipo_saida=request.form.get('tipo_saida'),
                observacao=request.form.get('observacao')
            )
            flash('Saída atualizada com sucesso!', 'success')
            return redirect(url_for('almoxarifado.saida.lista_saidas'))
        except Exception as e:
            flash(f'Erro ao atualizar saída: {str(e)}', 'danger')
    
    setores = UnidadeLocal.query.all()
    itens = Item.query.filter_by(excluido=False).all()
    return render_template('saidas/form.html', saida=saida, setores=setores, itens=itens)

@bp.route('/excluir/<int:id>', methods=['POST'])
@login_required
@admin_required
def excluir_saida(id):
    """Exclui uma saída existente."""
    saida = SaidaMaterial.query.get_or_404(id)
    
    if saida.status == 'Finalizada':
        flash('Não é possível excluir uma saída finalizada.', 'warning')
        return redirect(url_for('almoxarifado.saida.lista_saidas'))
    
    try:
        AlmoxarifadoService.excluir_saida(id)
        flash('Saída excluída com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao excluir saída: {str(e)}', 'danger')
    
    return redirect(url_for('almoxarifado.saida.lista_saidas'))

@bp.route('/imprimir/<int:id>')
@login_required
def imprimir_saida(id):
    """Gera uma versão para impressão da saída."""
    saida = SaidaMaterial.query.get_or_404(id)
    return render_template('saidas/print.html', saida=saida) 