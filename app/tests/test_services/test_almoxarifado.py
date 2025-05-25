import pytest
from datetime import datetime
from app import db
from app.models.item import Item
from app.models.fornecedor import Fornecedor
from app.services.almoxarifado import AlmoxarifadoService
from app.utils.exceptions import EstoqueInsuficienteError, ItemNaoEncontradoError

def test_registrar_entrada(app):
    with app.app_context():
        # Preparar
        fornecedor = Fornecedor(
            tipo='Pessoa Jurídica',
            nome='Fornecedor Teste',
            cnpj_cpf='12345678901234'
        )
        db.session.add(fornecedor)
        
        item = Item(
            codigo_sap='SAP001',
            nome='Item Teste',
            descricao='Descrição do Item Teste',
            unidade='UN',
            valor_unitario=10.0,
            estoque_atual=0
        )
        db.session.add(item)
        db.session.commit()
        
        # Executar
        entrada = AlmoxarifadoService.registrar_entrada(
            item_id=item.id,
            quantidade=10,
            valor_unitario=10.0,
            fornecedor_id=fornecedor.id,
            nota_fiscal='NF001',
            data_movimento=datetime.now(),
            usuario_id=1
        )
        
        # Verificar
        assert entrada is not None
        assert item.estoque_atual == 10
        assert item.valor_unitario == 10.0
        assert item.saldo_financeiro == 100.0

def test_registrar_entrada_item_inexistente(app):
    with app.app_context():
        # Preparar
        fornecedor = Fornecedor(
            tipo='Pessoa Jurídica',
            nome='Fornecedor Teste',
            cnpj_cpf='12345678901234'
        )
        db.session.add(fornecedor)
        db.session.commit()
        
        # Executar e Verificar
        with pytest.raises(ItemNaoEncontradoError):
            AlmoxarifadoService.registrar_entrada(
                item_id=999,
                quantidade=10,
                valor_unitario=10.0,
                fornecedor_id=fornecedor.id,
                nota_fiscal='NF001',
                data_movimento=datetime.now(),
                usuario_id=1
            )

def test_registrar_saida(app):
    with app.app_context():
        # Preparar
        item = Item(
            codigo_sap='SAP001',
            nome='Item Teste',
            descricao='Descrição do Item Teste',
            unidade='UN',
            valor_unitario=10.0,
            estoque_atual=20
        )
        db.session.add(item)
        db.session.commit()
        
        # Executar
        saida = AlmoxarifadoService.registrar_saida(
            item_id=item.id,
            quantidade=5,
            solicitante_id=1,
            data_movimento=datetime.now(),
            usuario_id=1
        )
        
        # Verificar
        assert saida is not None
        assert item.estoque_atual == 15
        assert item.saldo_financeiro == 150.0

def test_registrar_saida_estoque_insuficiente(app):
    with app.app_context():
        # Preparar
        item = Item(
            codigo_sap='SAP001',
            nome='Item Teste',
            descricao='Descrição do Item Teste',
            unidade='UN',
            valor_unitario=10.0,
            estoque_atual=5
        )
        db.session.add(item)
        db.session.commit()
        
        # Executar e Verificar
        with pytest.raises(EstoqueInsuficienteError):
            AlmoxarifadoService.registrar_saida(
                item_id=item.id,
                quantidade=10,
                solicitante_id=1,
                data_movimento=datetime.now(),
                usuario_id=1
            )

def test_listar_itens_baixo_estoque(app):
    with app.app_context():
        # Preparar
        item1 = Item(
            codigo_sap='SAP001',
            nome='Item 1',
            descricao='Descrição do Item 1',
            unidade='UN',
            valor_unitario=10.0,
            estoque_atual=5,
            estoque_minimo=10
        )
        
        item2 = Item(
            codigo_sap='SAP002',
            nome='Item 2',
            descricao='Descrição do Item 2',
            unidade='UN',
            valor_unitario=20.0,
            estoque_atual=15,
            estoque_minimo=10
        )
        
        db.session.add_all([item1, item2])
        db.session.commit()
        
        # Executar
        itens_baixo_estoque = AlmoxarifadoService.listar_itens_baixo_estoque()
        
        # Verificar
        assert len(itens_baixo_estoque) == 1
        assert itens_baixo_estoque[0].codigo_sap == 'SAP001' 