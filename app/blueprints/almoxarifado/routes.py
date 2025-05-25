from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.blueprints.almoxarifado import bp
from app.models.item import Item, Grupo, NaturezaDespesa
from app.models.movimento import EntradaMaterial, EntradaItem, SaidaMaterial, SaidaItem
from app.models.fornecedor import Fornecedor
from app.services.almoxarifado import AlmoxarifadoService
from app.utils.exceptions import ItemNaoEncontradoError, EstoqueInsuficienteError
from app.utils.decorators import admin_required, perfil_required

@bp.route('/')
@login_required
def index():
    """Página inicial do almoxarifado."""
    itens = Item.query.filter_by(excluido=False).all()
    return render_template('almoxarifado/index.html', itens=itens)

@bp.route('/itens')
@login_required
def listar_itens():
    """Lista todos os itens do almoxarifado."""
    codigo = request.args.get('codigo')
    nome = request.args.get('nome')
    grupo_id = request.args.get('grupo_id', type=int)
    natureza_id = request.args.get('natureza_id', type=int)
    
    itens = AlmoxarifadoService.buscar_itens(
        codigo=codigo,
        nome=nome,
        grupo_id=grupo_id,
        natureza_id=natureza_id
    )
    grupos = Grupo.query.all()
    naturezas = NaturezaDespesa.query.all()
    
    return render_template(
        'itens/list.html',
        itens=itens,
        grupos=grupos,
        naturezas=naturezas
    )

@bp.route('/item/novo', methods=['GET', 'POST'])
@login_required
@admin_required
def novo_item():
    """Cadastra um novo item."""
    if request.method == 'POST':
        try:
            item = AlmoxarifadoService.cadastrar_item(
                codigo=request.form.get('codigo'),
                nome=request.form.get('nome'),
                descricao=request.form.get('descricao'),
                unidade_medida=request.form.get('unidade_medida'),
                grupo_id=request.form.get('grupo_id', type=int),
                natureza_despesa_id=request.form.get('natureza_despesa_id', type=int),
                estoque_minimo=float(request.form.get('estoque_minimo', 0)),
                estoque_maximo=float(request.form.get('estoque_maximo', 0))
            )
            flash('Item cadastrado com sucesso!', 'success')
            return redirect(url_for('almoxarifado.listar_itens'))
        except Exception as e:
            flash(f'Erro ao cadastrar item: {str(e)}', 'danger')
    
    grupos = Grupo.query.all()
    naturezas = NaturezaDespesa.query.all()
    return render_template(
        'almoxarifado/novo_item.html',
        grupos=grupos,
        naturezas=naturezas
    )

@bp.route('/item/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_item(id):
    """Edita um item existente."""
    try:
        if request.method == 'POST':
            item = AlmoxarifadoService.atualizar_item(
                item_id=id,
                codigo=request.form.get('codigo'),
                nome=request.form.get('nome'),
                descricao=request.form.get('descricao'),
                unidade_medida=request.form.get('unidade_medida'),
                grupo_id=request.form.get('grupo_id', type=int),
                natureza_despesa_id=request.form.get('natureza_despesa_id', type=int),
                estoque_minimo=float(request.form.get('estoque_minimo', 0)),
                estoque_maximo=float(request.form.get('estoque_maximo', 0))
            )
            flash('Item atualizado com sucesso!', 'success')
            return redirect(url_for('almoxarifado.listar_itens'))
        else:
            item = Item.query.get_or_404(id)
            grupos = Grupo.query.all()
            naturezas = NaturezaDespesa.query.all()
            return render_template(
                'almoxarifado/editar_item.html',
                item=item,
                grupos=grupos,
                naturezas=naturezas
            )
    except ItemNaoEncontradoError:
        flash('Item não encontrado.', 'danger')
        return redirect(url_for('almoxarifado.listar_itens'))
    except Exception as e:
        flash(f'Erro ao atualizar item: {str(e)}', 'danger')
        return redirect(url_for('almoxarifado.editar_item', id=id))

@bp.route('/item/<int:id>/excluir', methods=['POST'])
@login_required
@admin_required
def excluir_item(id):
    """Exclui um item."""
    try:
        AlmoxarifadoService.excluir_item(id)
        flash('Item excluído com sucesso!', 'success')
    except ItemNaoEncontradoError:
        flash('Item não encontrado.', 'danger')
    except Exception as e:
        flash(f'Erro ao excluir item: {str(e)}', 'danger')
    return redirect(url_for('almoxarifado.listar_itens'))

@bp.route('/entradas')
@login_required
def listar_entradas():
    """Lista todas as entradas de material."""
    entradas = EntradaMaterial.query.filter_by(estornada=False).all()
    return render_template('almoxarifado/entradas.html', entradas=entradas)

@bp.route('/entrada/nova', methods=['GET', 'POST'])
@login_required
@perfil_required(['ALMOXARIFE', 'ADMIN'])
def nova_entrada():
    """Registra uma nova entrada de material."""
    if request.method == 'POST':
        try:
            entrada = AlmoxarifadoService.registrar_entrada(
                data_movimento=request.form.get('data_movimento'),
                data_nota_fiscal=request.form.get('data_nota_fiscal'),
                numero_nota_fiscal=request.form.get('numero_nota_fiscal'),
                fornecedor_id=request.form.get('fornecedor_id', type=int),
                itens=request.form.getlist('itens'),
                quantidades=request.form.getlist('quantidades'),
                valores_unitarios=request.form.getlist('valores_unitarios')
            )
            flash('Entrada registrada com sucesso!', 'success')
            return redirect(url_for('almoxarifado.listar_entradas'))
        except Exception as e:
            flash(f'Erro ao registrar entrada: {str(e)}', 'danger')
    
    itens = Item.query.filter_by(excluido=False).all()
    fornecedores = Fornecedor.query.all()
    return render_template(
        'almoxarifado/nova_entrada.html',
        itens=itens,
        fornecedores=fornecedores
    )

@bp.route('/entrada/<int:id>/estornar', methods=['POST'])
@login_required
@admin_required
def estornar_entrada(id):
    """Estorna uma entrada de material."""
    try:
        AlmoxarifadoService.estornar_entrada(id)
        flash('Entrada estornada com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao estornar entrada: {str(e)}', 'danger')
    return redirect(url_for('almoxarifado.listar_entradas'))

@bp.route('/saidas')
@login_required
def listar_saidas():
    """Lista todas as saídas de material."""
    saidas = SaidaMaterial.query.filter_by(estornada=False).all()
    return render_template('almoxarifado/saidas.html', saidas=saidas)

@bp.route('/saida/nova', methods=['GET', 'POST'])
@login_required
@perfil_required(['ALMOXARIFE', 'ADMIN'])
def nova_saida():
    """Registra uma nova saída de material."""
    if request.method == 'POST':
        try:
            saida = AlmoxarifadoService.registrar_saida(
                data_movimento=request.form.get('data_movimento'),
                requisitante_id=request.form.get('requisitante_id', type=int),
                itens=request.form.getlist('itens'),
                quantidades=request.form.getlist('quantidades'),
                observacao=request.form.get('observacao')
            )
            flash('Saída registrada com sucesso!', 'success')
            return redirect(url_for('almoxarifado.listar_saidas'))
        except EstoqueInsuficienteError as e:
            flash(str(e), 'danger')
        except Exception as e:
            flash(f'Erro ao registrar saída: {str(e)}', 'danger')
    
    itens = Item.query.filter_by(excluido=False).all()
    return render_template('almoxarifado/nova_saida.html', itens=itens)

@bp.route('/saida/<int:id>/estornar', methods=['POST'])
@login_required
@admin_required
def estornar_saida(id):
    """Estorna uma saída de material."""
    try:
        AlmoxarifadoService.estornar_saida(id)
        flash('Saída estornada com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao estornar saída: {str(e)}', 'danger')
    return redirect(url_for('almoxarifado.listar_saidas'))

# API Routes
@bp.route('/api/item/<int:id>/info', methods=['GET'])
@login_required
def get_item_info(id):
    """Retorna informações de um item em formato JSON."""
    try:
        item = Item.query.get_or_404(id)
        return jsonify({
            'id': item.id,
            'codigo': item.codigo,
            'nome': item.nome,
            'unidade_medida': item.unidade_medida,
            'saldo': item.saldo,
            'valor_medio': item.valor_medio
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/api/item/<int:id>/movimentos', methods=['GET'])
@login_required
def get_item_movimentos(id):
    """Retorna os movimentos de um item em formato JSON."""
    try:
        movimentos = AlmoxarifadoService.buscar_movimentos_item(id)
        return jsonify([{
            'id': m.id,
            'data': m.data_movimento.strftime('%d/%m/%Y'),
            'tipo': m.tipo,
            'quantidade': m.quantidade,
            'valor_unitario': m.valor_unitario,
            'valor_total': m.valor_total
        } for m in movimentos])
    except Exception as e:
        return jsonify({'error': str(e)}), 500 