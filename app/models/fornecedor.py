from app.extensions import db

class Fornecedor(db.Model):
    __tablename__ = 'fornecedores'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20), nullable=False)  # 'Pessoa Física' ou 'Pessoa Jurídica'
    nome = db.Column(db.String(120), nullable=False)
    cnpj_cpf = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=True)
    telefone = db.Column(db.String(20), nullable=True)
    celular = db.Column(db.String(20), nullable=True)
    endereco = db.Column(db.String(200), nullable=True)
    numero = db.Column(db.String(10), nullable=True)
    complemento = db.Column(db.String(100), nullable=True)
    cep = db.Column(db.String(10), nullable=True)
    cidade = db.Column(db.String(100), nullable=True)
    uf = db.Column(db.String(2), nullable=True)
    inscricao_estadual = db.Column(db.String(50), nullable=True)
    inscricao_municipal = db.Column(db.String(50), nullable=True)

    __table_args__ = (
        db.UniqueConstraint('nome', 'cnpj_cpf', name='uq_nome_cnpjcpf'),
    )

    def __repr__(self):
        return f'<Fornecedor {self.nome} - {self.cnpj_cpf}>'

    @property
    def endereco_completo(self):
        partes = [self.endereco]
        if self.numero:
            partes.append(f', {self.numero}')
        if self.complemento:
            partes.append(f' - {self.complemento}')
        if self.cidade and self.uf:
            partes.append(f', {self.cidade}/{self.uf}')
        if self.cep:
            partes.append(f' - CEP: {self.cep}')
        return ''.join(partes)

    @property
    def contatos(self):
        contatos = []
        if self.telefone:
            contatos.append(f'Tel: {self.telefone}')
        if self.celular:
            contatos.append(f'Cel: {self.celular}')
        if self.email:
            contatos.append(f'Email: {self.email}')
        return ' | '.join(contatos) 