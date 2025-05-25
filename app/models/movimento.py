from app.extensions import db
from datetime import datetime

class EntradaMaterial(db.Model):
    __tablename__ = 'entrada_material'
    id = db.Column(db.Integer, primary_key=True)
    data_movimento = db.Column(db.Date, nullable=False)
    data_nota_fiscal = db.Column(db.Date, nullable=False)
    numero_nota_fiscal = db.Column(db.String(50), nullable=False)
    estornada = db.Column(db.Boolean, default=False)

    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedores.id'), nullable=False)
    fornecedor = db.relationship('Fornecedor', backref='entradas')

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    usuario = db.relationship('Usuario', backref='entradas')

    itens = db.relationship(
        'EntradaItem',
        backref='entrada_material',
        cascade="all, delete-orphan",
        overlaps="entrada,itens_relacionados"
    )

    def __repr__(self):
        return f'<EntradaMaterial {self.numero_nota_fiscal} - {self.data_movimento}>'

    @property
    def valor_total(self):
        return sum(item.valor_total for item in self.itens)

class EntradaItem(db.Model):
    __tablename__ = 'entrada_item'
    id = db.Column(db.Integer, primary_key=True)
    entrada_id = db.Column(db.Integer, db.ForeignKey('entrada_material.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    valor_unitario = db.Column(db.Numeric(10, 2), nullable=False)

    item = db.relationship('Item', backref='entradas')
    entrada = db.relationship(
        'EntradaMaterial',
        backref='itens_relacionados',
        overlaps="entrada_material,itens"
    )

    @property
    def valor_total(self):
        return self.quantidade * self.valor_unitario

    def __repr__(self):
        return f'<EntradaItem {self.item.nome} - Qtd: {self.quantidade}>'

class SaidaMaterial(db.Model):
    __tablename__ = 'saida_material'
    id = db.Column(db.Integer, primary_key=True)
    data_movimento = db.Column(db.Date, nullable=False)
    numero_documento = db.Column(db.String(50), nullable=True)
    observacao = db.Column(db.Text, nullable=True)
    estornada = db.Column(db.Boolean, default=False)

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    usuario = db.relationship('Usuario', foreign_keys=[usuario_id], backref='saidas')

    solicitante_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    solicitante = db.relationship('Usuario', foreign_keys=[solicitante_id], backref='solicitacoes_saida')

    itens = db.relationship(
        'SaidaItem',
        backref='saida_material',
        cascade='all, delete-orphan',
        overlaps="saida,itens_relacionados"
    )

    def __repr__(self):
        return f'<SaidaMaterial {self.id} - {self.data_movimento}>'

    @property
    def valor_total(self):
        return sum(item.valor_total for item in self.itens)

class SaidaItem(db.Model):
    __tablename__ = 'saida_item'
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    valor_unitario = db.Column(db.Float, nullable=False)
    saida_id = db.Column(db.Integer, db.ForeignKey('saida_material.id'), nullable=False)

    item = db.relationship('Item', backref='saidas')
    saida = db.relationship(
        'SaidaMaterial',
        backref='itens_relacionados',
        overlaps="saida_material,itens"
    )

    @property
    def valor_total(self):
        return self.quantidade * self.valor_unitario

    def __repr__(self):
        return f'<SaidaItem {self.item.nome} - Qtd: {self.quantidade}>' 