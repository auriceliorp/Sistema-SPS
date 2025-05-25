from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.blueprints.auth import bp
from app.blueprints.auth.forms import LoginForm, RegistrationForm, ResetPasswordForm
from app.services.auth import AuthService
from app.utils.exceptions import UsuarioNaoEncontradoError

def is_safe_url(target):
    """Verifica se a URL de redirecionamento é segura."""
    return not target or '//' not in target

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = AuthService.authenticate_user(form.email.data, form.password.data)
        if not user:
            flash('Email ou senha inválidos', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not is_safe_url(next_page):
            next_page = url_for('main.index')
        return redirect(next_page)
    
    return render_template('auth/login.html', title='Login', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = AuthService.register_user(
                nome=form.nome.data,
                email=form.email.data,
                password=form.password.data,
                matricula=form.matricula.data
            )
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash(f'Erro ao realizar cadastro: {str(e)}', 'danger')
            return redirect(url_for('auth.register'))
    
    return render_template('auth/register.html', title='Registro', form=form)

@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        try:
            AuthService.reset_password(form.email.data, form.password.data)
            flash('Senha redefinida com sucesso!', 'success')
            return redirect(url_for('auth.login'))
        except UsuarioNaoEncontradoError:
            flash('Email não encontrado.', 'danger')
        except Exception as e:
            flash(f'Erro ao redefinir senha: {str(e)}', 'danger')
        return redirect(url_for('auth.reset_password_request'))
    
    return render_template('auth/reset_password_request.html', title='Redefinir Senha', form=form)

@bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        try:
            old_password = request.form.get('old_password')
            new_password = request.form.get('new_password')
            
            if AuthService.change_password(current_user.id, old_password, new_password):
                flash('Senha alterada com sucesso!', 'success')
                return redirect(url_for('main.index'))
            else:
                flash('Senha atual incorreta.', 'danger')
        except Exception as e:
            flash(f'Erro ao alterar senha: {str(e)}', 'danger')
        
        return redirect(url_for('auth.change_password'))
    
    return render_template('auth/change_password.html', title='Alterar Senha') 