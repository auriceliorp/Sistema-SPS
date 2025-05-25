from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user, login_required

def admin_required(f):
    """
    Decorator que requer que o usuário seja administrador.
    Deve ser usado após o decorator @login_required.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Você não tem permissão para acessar esta página.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

def solicitante_required(f):
    """
    Decorator que requer que o usuário seja solicitante.
    Deve ser usado após o decorator @login_required.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_solicitante:
            flash('Você não tem permissão para acessar esta página.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

def perfil_required(perfis_autorizados):
    """
    Decorator que requer que o usuário tenha um dos perfis autorizados.
    Deve ser usado após o decorator @login_required.
    
    Args:
        perfis_autorizados: Lista de nomes de perfis autorizados
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or not current_user.perfil or current_user.perfil.nome not in perfis_autorizados:
                flash('Você não tem permissão para acessar esta página.', 'danger')
                return redirect(url_for('main.index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def audit_log(acao, tabela):
    """
    Decorator que registra a ação no log de auditoria.
    
    Args:
        acao: Nome da ação (insert, update, delete, etc)
        tabela: Nome da tabela afetada
    """
    from app.models.audit import AuditLog
    from app.extensions import db
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Executa a função original
            result = f(*args, **kwargs)
            
            # Registra o log
            log = AuditLog(
                usuario_id=current_user.id if current_user.is_authenticated else None,
                acao=acao,
                tabela=tabela,
                registro_id=kwargs.get('id')  # Assume que o ID está nos kwargs
            )
            db.session.add(log)
            db.session.commit()
            
            return result
        return decorated_function
    return decorator 