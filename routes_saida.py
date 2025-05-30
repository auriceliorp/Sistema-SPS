# routes_saida.py
# Rotas para saída de materiais com paginação, filtro e geração de documento

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app_render import db
from models import Item, SaidaMaterial, SaidaItem, Usuario
from datetime import date
from sqlalchemy.orm import aliased

# Define o blueprint para as rotas de saída
saida_bp = Blueprint('saida_bp', __name__)

# -------------------- LISTAR SAÍDAS COM FILTRO E PAGINAÇÃO -------------------- #
@saida_bp.route('/saidas')
@login_required
def lista_saidas():
    page = request.args.get('page', 1, type=int)
    filtro = request.args.get('filtro')
    busca = request.args.get('busca', '').strip().lower()

    # Aliases para evitar conflito entre usuario_id e solicitante_id
    responsavel = aliased(Usuario)
    solicitante = aliased(Usuario)

    # Inicia query com joins explícitos e sem conflito
    query = db.session.query(SaidaMaterial).join(responsavel, SaidaMaterial.usuario).join(solicitante, SaidaMaterial.solicitante)

    if filtro and busca:
        if filtro == 'id':
            query = query.filter(SaidaMaterial.id == busca)
        elif filtro == 'data':
            try:
                dia, mes, ano = map(int, busca.split('/'))
                query = query.filter(SaidaMaterial.data_movimento == date(ano, mes, dia))
            except:
                flash('Formato de data inválido. Use DD/MM/AAAA.', 'warning')
        elif filtro == 'responsavel':
            query = query.filter(responsavel.nome.ilike(f'%{busca}%'))
        elif filtro == 'solicitante':
            query = query.filter(solicitante.nome.ilike(f'%{busca}%'))
        elif filtro == 'setor':
            query = query.join(solicitante.unidade_local).filter(solicitante.unidade_local.has(descricao_ilike=busca))

    saidas = query.order_by(SaidaMaterial.data_movimento.desc()).paginate(page=page, per_page=10)

    return render_template('saidas/list.html', saidas=saidas, filtro=filtro, busca=busca)


# -------------------- NOVA SAÍDA -------------------- #
@saida_bp.route('/nova_saida', methods=['GET', 'POST'])
@login_required
def nova_saida():
    itens = Item.query.all()
    usuarios = Usuario.query.order_by(Usuario.nome).all()

    if request.method == 'POST':
        try:
            data_movimento = date.fromisoformat(request.form.get('data_movimento'))
            numero_documento = request.form.get('numero_documento')
            observacao = request.form.get('observacao')
            solicitante_id = int(request.form.get('solicitante'))

            nova_saida = SaidaMaterial(
                data_movimento=data_movimento,
                numero_documento=numero_documento,
                observacao=observacao,
                usuario_id=current_user.id,
                solicitante_id=solicitante_id
            )
            db.session.add(nova_saida)
            db.session.flush()

            item_ids = request.form.getlist('item_id[]')
            quantidades = request.form.getlist('quantidade[]')
            valores_unitarios = request.form.getlist('valor_unitario[]')

            for i in range(len(item_ids)):
                if not item_ids[i] or not quantidades[i] or not valores_unitarios[i]:
                    continue

                item = Item.query.get(int(item_ids[i]))
                quantidade = int(quantidades[i])
                valor_unitario = float(valores_unitarios[i].replace(',', '.'))

                if item.estoque_atual < quantidade:
                    flash(f"Estoque insuficiente para '{item.nome}'", 'danger')
                    db.session.rollback()
                    return redirect(url_for('saida_bp.nova_saida'))

                item.estoque_atual -= quantidade
                item.saldo_financeiro -= quantidade * valor_unitario

                if item.grupo and item.grupo.natureza_despesa:
                    item.grupo.natureza_despesa.valor -= quantidade * valor_unitario

                saida_item = SaidaItem(
                    item_id=item.id,
                    quantidade=quantidade,
                    valor_unitario=valor_unitario,
                    saida_id=nova_saida.id
                )
                db.session.add(saida_item)

            db.session.commit()
            flash('Saída registrada com sucesso.', 'success')
            return redirect(url_for('saida_bp.lista_saidas'))

        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao registrar saída: {e}', 'danger')
            print(e)

    ano_atual = date.today().year
    ultima_saida = SaidaMaterial.query.order_by(SaidaMaterial.id.desc()).first()
    if ultima_saida and ultima_saida.numero_documento and '/' in ultima_saida.numero_documento:
        try:
            ultimo_num = int(ultima_saida.numero_documento.split('/')[0])
            numero_documento = f"{ultimo_num + 1:03}/{ano_atual}"
        except:
            numero_documento = f"001/{ano_atual}"
    else:
        numero_documento = f"001/{ano_atual}"

    return render_template('saidas/form.html', itens=itens, usuarios=usuarios, numero_documento=numero_documento)

# -------------------- ESTORNAR SAÍDA DE MATERIAL -------------------- #
@saida_bp.route('/saida/estornar/<int:saida_id>', methods=['POST'])
@login_required
def estornar_saida(saida_id):
    from utils.auditoria import registrar_auditoria

    saida = SaidaMaterial.query.get_or_404(saida_id)

    if saida.estornada:
        flash('Esta saída já foi estornada anteriormente.', 'warning')
        return redirect(url_for('saida_bp.lista_saidas'))

    itens = SaidaItem.query.filter_by(saida_id=saida_id).all()

    try:
        # Coletar dados para auditoria
        dados_antes = {
            'saida': {
                'id': saida.id,
                'numero_documento': saida.numero_documento,
                'data_movimento': saida.data_movimento.strftime('%Y-%m-%d'),
                'responsavel_id': saida.usuario_id,
                'solicitante_id': saida.solicitante_id
            },
            'itens': [
                {
                    'item_id': item.item_id,
                    'quantidade': item.quantidade,
                    'valor_unitario': float(item.valor_unitario)
                } for item in itens
            ]
        }

        for item_saida in itens:
            item = Item.query.get(item_saida.item_id)
            if item:
                # Recompõe o estoque
                item.estoque_atual += item_saida.quantidade
                item.saldo_financeiro += item_saida.quantidade * float(item_saida.valor_unitario)
                item.valor_unitario = item.saldo_financeiro / item.estoque_atual if item.estoque_atual > 0 else 0.0

                # Recompõe a natureza de despesa (se aplicável)
                if item.grupo and item.grupo.natureza_despesa:
                    item.grupo.natureza_despesa.valor += item_saida.quantidade * float(item_saida.valor_unitario)

        saida.estornada = True

        registrar_auditoria(
            acao='estorno',
            tabela='saida_material',
            registro_id=saida.id,
            dados_antes=dados_antes,
            dados_depois=None
        )

        db.session.commit()
        flash('Saída estornada com sucesso.', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao estornar saída: {e}', 'danger')
        print(e)

    return redirect(url_for('saida_bp.lista_saidas'))



# -------------------- REQUISIÇÃO (IMPRESSÃO) -------------------- #
@saida_bp.route('/requisicao/<int:saida_id>')
@login_required
def requisicao_saida(saida_id):
    saida = SaidaMaterial.query.get_or_404(saida_id)
    return render_template('saidas/detail.html', saida=saida)
