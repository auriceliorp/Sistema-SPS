from datetime import datetime
from app.extensions import db

class AuditLog(db.Model):
    """Modelo para registro de auditoria do sistema."""
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)
    data_hora = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    acao = db.Column(db.String(50), nullable=False)
    tabela = db.Column(db.String(50), nullable=False)
    registro_id = db.Column(db.Integer, nullable=True)
    dados_anteriores = db.Column(db.JSON, nullable=True)
    dados_novos = db.Column(db.JSON, nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(200), nullable=True)

    # Relacionamentos
    usuario = db.relationship('Usuario', backref=db.backref('logs_auditoria', lazy=True))

    def __init__(self, usuario_id=None, acao=None, tabela=None, registro_id=None,
                 dados_anteriores=None, dados_novos=None, ip_address=None, user_agent=None):
        self.usuario_id = usuario_id
        self.acao = acao
        self.tabela = tabela
        self.registro_id = registro_id
        self.dados_anteriores = dados_anteriores
        self.dados_novos = dados_novos
        self.ip_address = ip_address
        self.user_agent = user_agent

    def __repr__(self):
        return f'<AuditLog {self.id}: {self.acao} em {self.tabela} por {self.usuario_id}>'

    @property
    def descricao_acao(self):
        acoes = {
            'insert': 'Inserção',
            'update': 'Atualização',
            'delete': 'Exclusão',
            'estorno': 'Estorno',
            'login': 'Login',
            'logout': 'Logout'
        }
        return acoes.get(self.acao.lower(), self.acao) 