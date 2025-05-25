from datetime import datetime
from app.extensions import db

class Estoque(db.Model):
    __tablename__ = 'estoque'
    
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    valor_unitario = db.Column(db.Float, nullable=False)
    valor_total = db.Column(db.Float, nullable=False)
    data_registro = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamentos
    item = db.relationship('Item', backref='movimentos_estoque')

    def __repr__(self):
        return f'<Estoque {self.id} - Item {self.item_id}>' 