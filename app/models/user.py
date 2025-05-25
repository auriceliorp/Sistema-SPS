from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db, login

class Perfil(db.Model):
    __tablename__ = 'perfil'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return f'<Perfil {self.nome}>'

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    matricula = db.Column(db.String(50))
    ramal = db.Column(db.String(20))
    unidade_local_id = db.Column(db.Integer, db.ForeignKey('unidade_local.id'))
    perfil_id = db.Column(db.Integer, db.ForeignKey('perfil.id'))
    senha_temporaria = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    ultimo_acesso = db.Column(db.DateTime)

    # Relacionamentos
    unidade_local = db.relationship('UnidadeLocal', back_populates='usuarios')
    perfil = db.relationship('Perfil', backref='usuarios')
    bens = db.relationship('BemPatrimonial', back_populates='detentor')
    
    def set_password(self, password):
        """Define a senha do usuário usando hash."""
        self.senha = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica se a senha está correta."""
        return check_password_hash(self.senha, password)
    
    def update_ultimo_acesso(self):
        """Atualiza a data do último acesso."""
        self.ultimo_acesso = datetime.utcnow()
        db.session.commit()
    
    @property
    def is_admin(self):
        """Verifica se o usuário é administrador."""
        return self.perfil and self.perfil.nome == 'Administrador'
    
    def __repr__(self):
        return f'<Usuario {self.nome}>'

@login.user_loader
def load_user(id):
    return Usuario.query.get(int(id)) 