import unittest
from app import app, db
from models import Usuario, Perfil, UnidadeLocal, Item, Fornecedor, NaturezaDespesa, Grupo
from werkzeug.security import generate_password_hash
from datetime import datetime

class TestRoutes(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
            self._criar_dados_teste()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def _criar_dados_teste(self):
        # Criar perfis
        perfis = {
            'admin': Perfil(nome='Administrador'),
            'solicitante': Perfil(nome='Solicitante'),
            'consultor': Perfil(nome='Consultor')
        }
        for perfil in perfis.values():
            db.session.add(perfil)
        db.session.commit()

        # Criar unidade local
        ul = UnidadeLocal(codigo='001', descricao='Unidade Teste')
        db.session.add(ul)
        db.session.commit()

        # Criar usuário de teste
        usuario = Usuario(
            nome='Usuário Teste',
            email='teste@teste.com',
            senha=generate_password_hash('123456'),
            matricula='12345',
            perfil_id=perfis['admin'].id,
            unidade_local_id=ul.id
        )
        db.session.add(usuario)

        # Criar natureza de despesa
        nd = NaturezaDespesa(codigo='339030', nome='Material de Consumo')
        db.session.add(nd)
        db.session.commit()

        # Criar grupo
        grupo = Grupo(nome='Material de Escritório', natureza_despesa_id=nd.id)
        db.session.add(grupo)
        db.session.commit()

        # Criar item
        item = Item(
            codigo_sap='123456',
            nome='Caneta',
            descricao='Caneta esferográfica azul',
            unidade='UN',
            grupo_id=grupo.id,
            estoque_atual=100,
            valor_unitario=1.50
        )
        db.session.add(item)

        # Criar fornecedor
        fornecedor = Fornecedor(
            tipo='PJ',
            nome='Fornecedor Teste',
            cnpj_cpf='12345678901234',
            cidade='Cidade Teste',
            uf='UF'
        )
        db.session.add(fornecedor)
        db.session.commit()

    def _login(self):
        return self.app.post('/login', data={
            'email': 'teste@teste.com',
            'senha': '123456'
        }, follow_redirects=True)

    def test_rotas_publicas(self):
        """Testa rotas que não requerem autenticação"""
        rotas = ['/', '/login', '/esqueci_senha']
        for rota in rotas:
            response = self.app.get(rota)
            self.assertEqual(response.status_code, 200)

    def test_rotas_autenticadas(self):
        """Testa rotas que requerem autenticação"""
        self._login()
        rotas = [
            '/home',
            '/almoxarifado',
            '/usuario/',
            '/item/itens',
            '/fornecedor/',
            '/entrada/lista',
            '/saida/saidas',
            '/relatorio/mapa_fechamento'
        ]
        for rota in rotas:
            response = self.app.get(rota)
            self.assertIn(response.status_code, [200, 302])

    def test_crud_fornecedor(self):
        """Testa CRUD completo de fornecedor"""
        self._login()
        
        # Criar
        response = self.app.post('/fornecedor/novo', data={
            'tipo': 'PJ',
            'nome': 'Novo Fornecedor',
            'cnpj': '98765432101234',
            'cidade': 'Nova Cidade',
            'uf': 'UF'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Listar
        response = self.app.get('/fornecedor/')
        self.assertEqual(response.status_code, 200)

        # Editar
        fornecedor = Fornecedor.query.filter_by(nome='Novo Fornecedor').first()
        response = self.app.post(f'/fornecedor/editar/{fornecedor.id}', data={
            'tipo': 'PJ',
            'nome': 'Fornecedor Atualizado',
            'cnpj': '98765432101234',
            'cidade': 'Cidade Atualizada',
            'uf': 'UF'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_crud_item(self):
        """Testa CRUD completo de item"""
        self._login()
        
        # Criar
        response = self.app.post('/item/novo', data={
            'codigo_sap': '654321',
            'nome': 'Novo Item',
            'descricao': 'Descrição do novo item',
            'unidade': 'UN',
            'grupo_id': 1,
            'estoque_atual': 50,
            'valor_unitario': 2.50
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Listar
        response = self.app.get('/item/itens')
        self.assertEqual(response.status_code, 200)

        # Editar
        item = Item.query.filter_by(codigo_sap='654321').first()
        response = self.app.post(f'/item/editar/{item.id}', data={
            'codigo_sap': '654321',
            'nome': 'Item Atualizado',
            'descricao': 'Descrição atualizada',
            'unidade': 'UN',
            'grupo_id': 1,
            'estoque_atual': 60,
            'valor_unitario': 3.00
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main() 