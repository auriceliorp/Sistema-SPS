import pytest
from app import create_app
from flask import url_for

@pytest.fixture
def app():
    """Cria uma instância do app para testes."""
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    """Cria um cliente de teste."""
    return app.test_client()

def test_rotas_principais(app, client):
    """Testa se as rotas principais estão acessíveis."""
    rotas = [
        '/almoxarifado/',
        '/almoxarifado/itens',
        '/almoxarifado/entradas',
        '/almoxarifado/saidas'
    ]
    
    for rota in rotas:
        response = client.get(rota)
        # Verifica se a resposta não é 404
        assert response.status_code != 404, f"Rota {rota} não encontrada"

def test_rotas_protegidas(app, client):
    """Testa se as rotas protegidas requerem autenticação."""
    rotas = [
        '/almoxarifado/item/novo',
        '/almoxarifado/entrada/nova',
        '/almoxarifado/saida/nova'
    ]
    
    for rota in rotas:
        response = client.get(rota)
        # Deve redirecionar para login (302) ou retornar 401/403
        assert response.status_code in [302, 401, 403], f"Rota {rota} não está protegida"

def test_rotas_api(app, client):
    """Testa se as rotas da API estão funcionando."""
    rotas_api = [
        '/almoxarifado/api/item/1/info',
        '/almoxarifado/api/item/1/movimentos'
    ]
    
    for rota in rotas_api:
        response = client.get(rota)
        # API deve retornar JSON
        assert response.content_type == 'application/json'

def test_operacoes_item(app, client):
    """Testa operações CRUD de itens."""
    # Teste de criação de item (POST)
    novo_item = {
        'codigo': 'TST001',
        'nome': 'Item Teste',
        'descricao': 'Item para teste',
        'unidade_medida': 'UN',
        'grupo_id': 1,
        'natureza_despesa_id': 1
    }
    response = client.post('/almoxarifado/item/novo', data=novo_item)
    assert response.status_code in [200, 302], "Falha ao criar novo item"

    # Teste de edição de item (POST)
    response = client.post('/almoxarifado/item/1/editar', data=novo_item)
    assert response.status_code in [200, 302], "Falha ao editar item"

def test_operacoes_entrada(app, client):
    """Testa operações de entrada de material."""
    nova_entrada = {
        'data_movimento': '2024-03-20',
        'data_nota_fiscal': '2024-03-20',
        'numero_nota_fiscal': 'NF001',
        'fornecedor_id': 1,
        'itens': [1],
        'quantidades': [10],
        'valores_unitarios': [100.00]
    }
    response = client.post('/almoxarifado/entrada/nova', data=nova_entrada)
    assert response.status_code in [200, 302], "Falha ao registrar entrada"

def test_operacoes_saida(app, client):
    """Testa operações de saída de material."""
    nova_saida = {
        'data_movimento': '2024-03-20',
        'requisitante_id': 1,
        'itens': [1],
        'quantidades': [5],
        'observacao': 'Teste de saída'
    }
    response = client.post('/almoxarifado/saida/nova', data=nova_saida)
    assert response.status_code in [200, 302], "Falha ao registrar saída" 