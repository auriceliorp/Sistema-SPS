from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.blueprints.patrimonio import bp
from app.models.patrimonio import BemPatrimonial, GrupoPatrimonio
from app.models.user import Usuario
from app.services.patrimonio import PatrimonioService
from app.utils.exceptions import BemPatrimonialNaoEncontradoError
from app.utils.decorators import admin_required

@bp.route('/', methods=['GET'])
@login_required
def index():
    numero_ul = request.args.get('numero_ul')
    numero_sap = request.args.get('numero_sap')
    grupo_bem = request.args.get('grupo_bem')
    detentor_id = request.args.get('detentor_id', type=int)
    localizacao = request.args.get('localizacao')
    status = request.args.get('status')
    
    bens = PatrimonioService.buscar_bens(
        numero_ul=numero_ul,
        numero_sap=numero_sap,
        grupo_bem=grupo_bem,
        detentor_id=detentor_id,
        localizacao=localizacao,
        status=status
    )
    return render_template('patrimonio/index.html', bens=bens)

@bp.route('/novo', methods=['GET', 'POST'])
@login_required
@admin_required
def novo():
    if request.method == 'POST':
        try:
            bem = PatrimonioService.cadastrar_bem(
                numero_ul=request.form.get('numero_ul'),
                numero_sap=request.form.get('numero_sap'),
                numero_siads=request.form.get('numero_siads'),
                nome=request.form.get('nome'),
                descricao=request.form.get('descricao'),
                grupo_bem=request.form.get('grupo_bem'),
                classificacao_contabil=request.form.get('classificacao_contabil'),
                detentor_id=request.form.get('detentor_id', type=int),
                localizacao=request.form.get('localizacao'),
                valor_aquisicao=float(request.form.get('valor_aquisicao', 0)),
                data_aquisicao=request.form.get('data_aquisicao'),
                foto=request.form.get('foto'),
                observacoes=request.form.get('observacoes')
            )
            flash('Bem patrimonial cadastrado com sucesso!', 'success')
            return redirect(url_for('patrimonio.index'))
        except Exception as e:
            flash(f'Erro ao cadastrar bem patrimonial: {str(e)}', 'danger')
    
    usuarios = Usuario.query.all()
    grupos = GrupoPatrimonio.query.all()
    return render_template('patrimonio/novo.html', usuarios=usuarios, grupos=grupos)

@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar(id):
    try:
        if request.method == 'POST':
            bem = PatrimonioService.atualizar_bem(
                bem_id=id,
                numero_ul=request.form.get('numero_ul'),
                numero_sap=request.form.get('numero_sap'),
                numero_siads=request.form.get('numero_siads'),
                nome=request.form.get('nome'),
                descricao=request.form.get('descricao'),
                grupo_bem=request.form.get('grupo_bem'),
                classificacao_contabil=request.form.get('classificacao_contabil'),
                detentor_id=request.form.get('detentor_id', type=int),
                localizacao=request.form.get('localizacao'),
                valor_aquisicao=float(request.form.get('valor_aquisicao', 0)),
                data_aquisicao=request.form.get('data_aquisicao'),
                foto=request.form.get('foto'),
                observacoes=request.form.get('observacoes'),
                status=request.form.get('status')
            )
            flash('Bem patrimonial atualizado com sucesso!', 'success')
            return redirect(url_for('patrimonio.index'))
        else:
            bem = BemPatrimonial.query.get_or_404(id)
            usuarios = Usuario.query.all()
            grupos = GrupoPatrimonio.query.all()
            return render_template('patrimonio/editar.html', bem=bem, usuarios=usuarios, grupos=grupos)
    except BemPatrimonialNaoEncontradoError:
        flash('Bem patrimonial não encontrado.', 'danger')
        return redirect(url_for('patrimonio.index'))
    except Exception as e:
        flash(f'Erro ao atualizar bem patrimonial: {str(e)}', 'danger')
        return redirect(url_for('patrimonio.editar', id=id))

@bp.route('/excluir/<int:id>', methods=['POST'])
@login_required
@admin_required
def excluir(id):
    try:
        PatrimonioService.excluir_bem(id)
        flash('Bem patrimonial excluído com sucesso!', 'success')
    except BemPatrimonialNaoEncontradoError:
        flash('Bem patrimonial não encontrado.', 'danger')
    except Exception as e:
        flash(f'Erro ao excluir bem patrimonial: {str(e)}', 'danger')
    return redirect(url_for('patrimonio.index'))

@bp.route('/transferir/<int:id>', methods=['POST'])
@login_required
@admin_required
def transferir(id):
    try:
        bem = PatrimonioService.transferir_bem(
            bem_id=id,
            novo_detentor_id=request.form.get('novo_detentor_id', type=int),
            nova_localizacao=request.form.get('nova_localizacao'),
            observacao=request.form.get('observacao')
        )
        flash('Bem patrimonial transferido com sucesso!', 'success')
    except BemPatrimonialNaoEncontradoError:
        flash('Bem patrimonial não encontrado.', 'danger')
    except Exception as e:
        flash(f'Erro ao transferir bem patrimonial: {str(e)}', 'danger')
    return redirect(url_for('patrimonio.index'))

# API Routes
@bp.route('/api/bem/<int:id>/info', methods=['GET'])
@login_required
def get_bem_info(id):
    try:
        bem = BemPatrimonial.query.get_or_404(id)
        return jsonify({
            'id': bem.id,
            'numero_ul': bem.numero_ul,
            'nome': bem.nome,
            'detentor': bem.detentor.nome if bem.detentor else None,
            'localizacao': bem.localizacao
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500 