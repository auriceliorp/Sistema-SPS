from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.blueprints.admin import bp
from app.models.user import Usuario, Perfil
from app.models.local import Local, UnidadeLocal
from app.services.auth import AuthService
from app.services.audit import AuditService
from app.models.audit import AuditLog
from app.utils.exceptions import UsuarioNaoEncontradoError
from app.utils.decorators import admin_required

@bp.route('/')
@login_required
@admin_required
def index():
    """Página inicial da administração."""
    return render_template('admin/index.html')

@bp.route('/usuarios')
@login_required
@admin_required
def listar_usuarios():
    """Lista todos os usuários."""
    usuarios = Usuario.query.all()
    return render_template('admin/usuarios.html', usuarios=usuarios)

@bp.route('/usuario/novo', methods=['GET', 'POST'])
@login_required
@admin_required
def novo_usuario():
    """Cadastra um novo usuário."""
    if request.method == 'POST':
        try:
            usuario = AuthService.register_user(
                nome=request.form.get('nome'),
                email=request.form.get('email'),
                password=request.form.get('password'),
                matricula=request.form.get('matricula'),
                ramal=request.form.get('ramal'),
                unidade_local_id=request.form.get('unidade_local_id', type=int),
                perfil_id=request.form.get('perfil_id', type=int)
            )
            flash('Usuário cadastrado com sucesso!', 'success')
            return redirect(url_for('admin.listar_usuarios'))
        except Exception as e:
            flash(f'Erro ao cadastrar usuário: {str(e)}', 'danger')
    
    perfis = Perfil.query.all()
    unidades = UnidadeLocal.query.all()
    return render_template(
        'admin/novo_usuario.html',
        perfis=perfis,
        unidades=unidades
    )

@bp.route('/usuario/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_usuario(id):
    """Edita um usuário existente."""
    try:
        if request.method == 'POST':
            usuario = AuthService.update_user(
                user_id=id,
                nome=request.form.get('nome'),
                email=request.form.get('email'),
                matricula=request.form.get('matricula'),
                ramal=request.form.get('ramal'),
                unidade_local_id=request.form.get('unidade_local_id', type=int),
                perfil_id=request.form.get('perfil_id', type=int),
                ativo=request.form.get('ativo') == 'on'
            )
            flash('Usuário atualizado com sucesso!', 'success')
            return redirect(url_for('admin.listar_usuarios'))
        else:
            usuario = Usuario.query.get_or_404(id)
            perfis = Perfil.query.all()
            unidades = UnidadeLocal.query.all()
            return render_template(
                'admin/editar_usuario.html',
                usuario=usuario,
                perfis=perfis,
                unidades=unidades
            )
    except UsuarioNaoEncontradoError:
        flash('Usuário não encontrado.', 'danger')
        return redirect(url_for('admin.listar_usuarios'))
    except Exception as e:
        flash(f'Erro ao atualizar usuário: {str(e)}', 'danger')
        return redirect(url_for('admin.editar_usuario', id=id))

@bp.route('/usuario/<int:id>/excluir', methods=['POST'])
@login_required
@admin_required
def excluir_usuario(id):
    """Exclui um usuário."""
    try:
        AuthService.delete_user(id)
        flash('Usuário excluído com sucesso!', 'success')
    except UsuarioNaoEncontradoError:
        flash('Usuário não encontrado.', 'danger')
    except Exception as e:
        flash(f'Erro ao excluir usuário: {str(e)}', 'danger')
    return redirect(url_for('admin.listar_usuarios'))

@bp.route('/perfis')
@login_required
@admin_required
def listar_perfis():
    """Lista todos os perfis."""
    perfis = Perfil.query.all()
    return render_template('admin/perfis.html', perfis=perfis)

@bp.route('/perfil/novo', methods=['GET', 'POST'])
@login_required
@admin_required
def novo_perfil():
    """Cadastra um novo perfil."""
    if request.method == 'POST':
        try:
            perfil = Perfil(nome=request.form.get('nome'))
            db.session.add(perfil)
            db.session.commit()
            flash('Perfil cadastrado com sucesso!', 'success')
            return redirect(url_for('admin.listar_perfis'))
        except Exception as e:
            flash(f'Erro ao cadastrar perfil: {str(e)}', 'danger')
            db.session.rollback()
    
    return render_template('admin/novo_perfil.html')

@bp.route('/perfil/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_perfil(id):
    """Edita um perfil existente."""
    perfil = Perfil.query.get_or_404(id)
    if request.method == 'POST':
        try:
            perfil.nome = request.form.get('nome')
            db.session.commit()
            flash('Perfil atualizado com sucesso!', 'success')
            return redirect(url_for('admin.listar_perfis'))
        except Exception as e:
            flash(f'Erro ao atualizar perfil: {str(e)}', 'danger')
            db.session.rollback()
    
    return render_template('admin/editar_perfil.html', perfil=perfil)

@bp.route('/perfil/<int:id>/excluir', methods=['POST'])
@login_required
@admin_required
def excluir_perfil(id):
    """Exclui um perfil."""
    try:
        perfil = Perfil.query.get_or_404(id)
        db.session.delete(perfil)
        db.session.commit()
        flash('Perfil excluído com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao excluir perfil: {str(e)}', 'danger')
        db.session.rollback()
    return redirect(url_for('admin.listar_perfis'))

@bp.route('/locais')
@login_required
@admin_required
def listar_locais():
    """Lista todos os locais."""
    locais = Local.query.all()
    return render_template('admin/locais.html', locais=locais)

@bp.route('/local/novo', methods=['GET', 'POST'])
@login_required
@admin_required
def novo_local():
    """Cadastra um novo local."""
    if request.method == 'POST':
        try:
            local = Local(descricao=request.form.get('descricao'))
            db.session.add(local)
            db.session.commit()
            flash('Local cadastrado com sucesso!', 'success')
            return redirect(url_for('admin.listar_locais'))
        except Exception as e:
            flash(f'Erro ao cadastrar local: {str(e)}', 'danger')
            db.session.rollback()
    
    return render_template('admin/novo_local.html')

@bp.route('/local/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_local(id):
    """Edita um local existente."""
    local = Local.query.get_or_404(id)
    if request.method == 'POST':
        try:
            local.descricao = request.form.get('descricao')
            db.session.commit()
            flash('Local atualizado com sucesso!', 'success')
            return redirect(url_for('admin.listar_locais'))
        except Exception as e:
            flash(f'Erro ao atualizar local: {str(e)}', 'danger')
            db.session.rollback()
    
    return render_template('admin/editar_local.html', local=local)

@bp.route('/local/<int:id>/excluir', methods=['POST'])
@login_required
@admin_required
def excluir_local(id):
    """Exclui um local."""
    try:
        local = Local.query.get_or_404(id)
        db.session.delete(local)
        db.session.commit()
        flash('Local excluído com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao excluir local: {str(e)}', 'danger')
        db.session.rollback()
    return redirect(url_for('admin.listar_locais'))

@bp.route('/unidades')
@login_required
@admin_required
def listar_unidades():
    """Lista todas as unidades locais."""
    unidades = UnidadeLocal.query.all()
    return render_template('admin/unidades.html', unidades=unidades)

@bp.route('/unidade/nova', methods=['GET', 'POST'])
@login_required
@admin_required
def nova_unidade():
    """Cadastra uma nova unidade local."""
    if request.method == 'POST':
        try:
            unidade = UnidadeLocal(
                codigo=request.form.get('codigo'),
                descricao=request.form.get('descricao'),
                local_id=request.form.get('local_id', type=int)
            )
            db.session.add(unidade)
            db.session.commit()
            flash('Unidade local cadastrada com sucesso!', 'success')
            return redirect(url_for('admin.listar_unidades'))
        except Exception as e:
            flash(f'Erro ao cadastrar unidade local: {str(e)}', 'danger')
            db.session.rollback()
    
    locais = Local.query.all()
    return render_template('admin/nova_unidade.html', locais=locais)

@bp.route('/unidade/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_unidade(id):
    """Edita uma unidade local existente."""
    unidade = UnidadeLocal.query.get_or_404(id)
    if request.method == 'POST':
        try:
            unidade.codigo = request.form.get('codigo')
            unidade.descricao = request.form.get('descricao')
            unidade.local_id = request.form.get('local_id', type=int)
            db.session.commit()
            flash('Unidade local atualizada com sucesso!', 'success')
            return redirect(url_for('admin.listar_unidades'))
        except Exception as e:
            flash(f'Erro ao atualizar unidade local: {str(e)}', 'danger')
            db.session.rollback()
    
    locais = Local.query.all()
    return render_template('admin/editar_unidade.html', unidade=unidade, locais=locais)

@bp.route('/unidade/<int:id>/excluir', methods=['POST'])
@login_required
@admin_required
def excluir_unidade(id):
    """Exclui uma unidade local."""
    try:
        unidade = UnidadeLocal.query.get_or_404(id)
        db.session.delete(unidade)
        db.session.commit()
        flash('Unidade local excluída com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao excluir unidade local: {str(e)}', 'danger')
        db.session.rollback()
    return redirect(url_for('admin.listar_unidades'))

@bp.route('/auditoria')
@login_required
@admin_required
def logs_auditoria():
    """Lista os logs de auditoria."""
    usuario_id = request.args.get('usuario_id', type=int)
    acao = request.args.get('acao')
    tabela = request.args.get('tabela')
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    
    logs = AuditService.buscar_logs(
        usuario_id=usuario_id,
        acao=acao,
        tabela=tabela,
        data_inicio=data_inicio,
        data_fim=data_fim
    )
    
    usuarios = Usuario.query.all()
    return render_template(
        'admin/auditoria.html',
        logs=logs,
        usuarios=usuarios
    )

@bp.route('/auditoria/limpar', methods=['POST'])
@login_required
@admin_required
def limpar_logs():
    """Remove logs antigos."""
    try:
        dias = int(request.form.get('dias', 90))
        quantidade = AuditService.limpar_logs_antigos(dias)
        flash(f'{quantidade} logs removidos com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao limpar logs: {str(e)}', 'danger')
    return redirect(url_for('admin.logs_auditoria'))

# API Routes
@bp.route('/api/usuario/<int:id>/info', methods=['GET'])
@login_required
@admin_required
def get_usuario_info(id):
    """Retorna informações de um usuário em formato JSON."""
    try:
        usuario = Usuario.query.get_or_404(id)
        return jsonify({
            'id': usuario.id,
            'nome': usuario.nome,
            'email': usuario.email,
            'matricula': usuario.matricula,
            'ramal': usuario.ramal,
            'unidade_local': usuario.unidade_local.descricao if usuario.unidade_local else None,
            'perfil': usuario.perfil.nome if usuario.perfil else None,
            'ativo': usuario.ativo
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/api/auditoria/log/<int:id>/detalhes', methods=['GET'])
@login_required
@admin_required
def get_log_detalhes(id):
    """Retorna detalhes de um log em formato JSON."""
    try:
        log = AuditLog.query.get_or_404(id)
        return jsonify({
            'id': log.id,
            'data_hora': log.data_hora.strftime('%d/%m/%Y %H:%M:%S'),
            'usuario': log.usuario.nome if log.usuario else None,
            'acao': log.acao,
            'tabela': log.tabela,
            'registro_id': log.registro_id,
            'dados_anteriores': log.dados_anteriores,
            'dados_novos': log.dados_novos,
            'ip_address': log.ip_address,
            'user_agent': log.user_agent
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500 