from app.extensions import db

class NaturezaDespesa(db.Model):
    __tablename__ = 'natureza_despesa'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(10), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Float, default=0.0)
    grupos = db.relationship('Grupo', back_populates='natureza_despesa')
    itens = db.relationship('Item', back_populates='natureza_despesa')

    def __repr__(self):
        return f'<NaturezaDespesa {self.codigo} - {self.nome}>'

class Grupo(db.Model):
    __tablename__ = 'grupos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    natureza_despesa_id = db.Column(db.Integer, db.ForeignKey('natureza_despesa.id'), nullable=False)
    natureza_despesa = db.relationship('NaturezaDespesa', back_populates='grupos')
    itens = db.relationship('Item', back_populates='grupo')

    def __repr__(self):
        return f'<Grupo {self.nome}>'

class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    codigo_sap = db.Column(db.String(50), nullable=False)
    codigo_siads = db.Column(db.String(50))
    nome = db.Column(db.String(120), nullable=False)
    descricao = db.Column(db.Text, nullable=False, default='')
    unidade = db.Column(db.String(50), nullable=False)
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupos.id'))
    grupo = db.relationship('Grupo', back_populates='itens')
    natureza_despesa_id = db.Column(db.Integer, db.ForeignKey('natureza_despesa.id'), nullable=False)
    natureza_despesa = db.relationship('NaturezaDespesa', back_populates='itens')
    valor_unitario = db.Column(db.Float, default=0.0)
    saldo_financeiro = db.Column(db.Float, default=0.0)
    estoque_atual = db.Column(db.Float, default=0.0)
    estoque_minimo = db.Column(db.Float, default=0.0)
    localizacao = db.Column(db.String(120), default='')
    data_validade = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return f'<Item {self.codigo_sap} - {self.nome}>'

    @property
    def em_estoque_minimo(self):
        return self.estoque_atual <= self.estoque_minimo

    @property
    def valor_total(self):
        return self.estoque_atual * self.valor_unitario 