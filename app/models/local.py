from app.extensions import db

class Local(db.Model):
    __tablename__ = 'local'
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(120), nullable=False)
    uls = db.relationship('UnidadeLocal', back_populates='local', lazy=True)

    def __repr__(self):
        return f'<Local {self.descricao}>'

class UnidadeLocal(db.Model):
    __tablename__ = 'unidade_local'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), nullable=False)
    descricao = db.Column(db.String(120), nullable=False)
    local_id = db.Column(db.Integer, db.ForeignKey('local.id'), nullable=False)
    local = db.relationship('Local', back_populates='uls')
    usuarios = db.relationship('Usuario', back_populates='unidade_local')

    def __repr__(self):
        return f'<UnidadeLocal {self.codigo} - {self.descricao}>'

    @property
    def nome_completo(self):
        return f'{self.local.descricao} - {self.descricao}' 