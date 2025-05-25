import pytest
from app import create_app, db
from app.models.item import Item, Grupo, NaturezaDespesa
from app.models.fornecedor import Fornecedor
from app.models.usuario import Usuario, Perfil

@pytest.fixture(scope='session')
def app():
    """Cria uma instância do app para toda a sessão de testes."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        # Criar dados básicos para teste
        _criar_dados_teste()
        
    return app

@pytest.fixture(scope='function')
def client(app):
    """Cria um cliente de teste limpo para cada função de teste."""
    return app.test_client()

def _criar_dados_teste():
    """Cria dados básicos no banco para os testes."""
    # Criar perfis
    perfil_admin = Perfil(nome='ADMIN')
    perfil_almox = Perfil(nome='ALMOXARIFE')
    db.session.add_all([perfil_admin, perfil_almox])
    
    # Criar usuário de teste
    usuario = Usuario(
        nome='Usuário Teste',
        email='teste@teste.com',
        matricula='12345',
        perfil=perfil_admin
    )
    usuario.set_senha('teste123')
    db.session.add(usuario)
    
    # Criar grupo e natureza de despesa
    grupo = Grupo(nome='Grupo Teste')
    natureza = NaturezaDespesa(codigo='339030', nome='Material de Consumo')
    db.session.add_all([grupo, natureza])
    
    # Criar fornecedor
    fornecedor = Fornecedor(
        nome='Fornecedor Teste',
        cnpj='12345678901234'
    )
    db.session.add(fornecedor)
    
    db.session.commit() 