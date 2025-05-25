import pytest
from app import create_app, db
from app.models.user import Usuario, Perfil
from app.models.local import Local, UnidadeLocal
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False

@pytest.fixture
def app():
    app = create_app(TestConfig)
    
    with app.app_context():
        db.create_all()
        # Criar dados básicos para teste
        perfil_admin = Perfil(nome='Administrador')
        perfil_user = Perfil(nome='Usuário')
        db.session.add_all([perfil_admin, perfil_user])
        
        local = Local(descricao='Local Teste')
        db.session.add(local)
        
        unidade = UnidadeLocal(
            codigo='UL001',
            descricao='Unidade Local Teste',
            local_id=1
        )
        db.session.add(unidade)
        
        usuario = Usuario(
            nome='Admin Teste',
            email='admin@teste.com',
            matricula='12345',
            unidade_local_id=1,
            perfil_id=1
        )
        usuario.set_password('senha123')
        db.session.add(usuario)
        
        db.session.commit()
        
    yield app
    
    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def auth_headers():
    """Headers para autenticação básica."""
    return {
        'Authorization': 'Basic YWRtaW5AdGVzdGUuY29tOnNlbmhhMTIz'
    }

class AuthActions:
    def __init__(self, client):
        self._client = client
        
    def login(self, email='admin@teste.com', password='senha123'):
        return self._client.post(
            '/auth/login',
            data={'email': email, 'password': password}
        )
        
    def logout(self):
        return self._client.get('/auth/logout')

@pytest.fixture
def auth(client):
    return AuthActions(client) 