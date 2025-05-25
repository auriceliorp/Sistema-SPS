from app.extensions import db
from datetime import datetime

class BemPatrimonial(db.Model):
    __tablename__ = 'bens_patrimoniais'

    id = db.Column(db.Integer, primary_key=True)
    numero_ul = db.Column(db.String(50), unique=True, nullable=False)       # Nº Patrimônio da Unidade Local
    numero_sap = db.Column(db.String(50), unique=True, nullable=False)      # Nº SAP
    numero_siads = db.Column(db.String(50), unique=True, nullable=True)     # Nº SIADS (pode ser preenchido depois)
    nome = db.Column(db.String(120), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    grupo_bem = db.Column(db.String(100), nullable=True)                    # Grupo ou categoria do bem
    classificacao_contabil = db.Column(db.String(100), nullable=True)       # Classificação contábil
    foto = db.Column(db.String(255), nullable=True)                         # Caminho para o arquivo da foto
    detentor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    detentor = db.relationship('Usuario', back_populates='bens')
    localizacao = db.Column(db.String(100), nullable=True)
    data_aquisicao = db.Column(db.Date, nullable=True)
    valor_aquisicao = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(50), default='Ativo')  # Ativo, Baixado, Em transferência etc.
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    observacoes = db.Column(db.Text, nullable=True)
    excluido = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<BemPatrimonial {self.numero_ul} - {self.nome}>'

    @property
    def idade(self):
        if not self.data_aquisicao:
            return None
        hoje = datetime.now().date()
        delta = hoje - self.data_aquisicao
        return delta.days // 365

class GrupoPatrimonio(db.Model):
    __tablename__ = 'grupos_patrimonio'

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), nullable=False)
    descricao = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f'<GrupoPatrimonio {self.codigo} - {self.descricao}>' 