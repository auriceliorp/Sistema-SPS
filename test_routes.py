from app import create_app
from flask import url_for

app = create_app()

def test_routes():
    with app.test_request_context():
        # Rotas principais do almoxarifado
        print("\nRotas Principais do Almoxarifado:")
        print("-" * 50)
        main_routes = [
            'almoxarifado.index',
            'almoxarifado.listar_itens',
            'almoxarifado.novo_item',
            'almoxarifado.listar_entradas',
            'almoxarifado.nova_entrada',
            'almoxarifado.listar_saidas',
            'almoxarifado.nova_saida'
        ]
        
        for route in main_routes:
            try:
                url = url_for(route)
                print(f"✓ {route:40} -> {url}")
            except Exception as e:
                print(f"✗ {route:40} -> ERRO: {str(e)}")

        # Rotas de operações com parâmetros
        print("\nRotas de Operações:")
        print("-" * 50)
        param_routes = [
            ('almoxarifado.editar_item', {'id': 1}),
            ('almoxarifado.excluir_item', {'id': 1}),
            ('almoxarifado.estornar_entrada', {'id': 1}),
            ('almoxarifado.estornar_saida', {'id': 1})
        ]
        
        for route, params in param_routes:
            try:
                url = url_for(route, **params)
                print(f"✓ {route:40} -> {url}")
            except Exception as e:
                print(f"✗ {route:40} -> ERRO: {str(e)}")

        # Rotas da API
        print("\nRotas da API:")
        print("-" * 50)
        api_routes = [
            ('almoxarifado.get_item_info', {'id': 1}),
            ('almoxarifado.get_item_movimentos', {'id': 1})
        ]
        
        for route, params in api_routes:
            try:
                url = url_for(route, **params)
                print(f"✓ {route:40} -> {url}")
            except Exception as e:
                print(f"✗ {route:40} -> ERRO: {str(e)}")

if __name__ == '__main__':
    test_routes() 