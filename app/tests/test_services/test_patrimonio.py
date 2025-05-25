import pytest
from datetime import datetime, date
from app import db
from app.models.patrimonio import BemPatrimonial
from app.models.user import Usuario
from app.services.patrimonio import PatrimonioService
from app.utils.exceptions import BemPatrimonialNaoEncontradoError

def test_cadastrar_bem(app):
    with app.app_context():
        # Preparar
        detentor = Usuario(
            nome='Detentor Teste',
            email='detentor@teste.com',
            matricula='12345'
        )
        db.session.add(detentor)
        db.session.commit()
        
        # Executar
        bem = PatrimonioService.cadastrar_bem(
            numero_ul='0401234',
            numero_sap='100987',
            nome='Computador Desktop',
            descricao='Computador Desktop Dell Optiplex',
            grupo_bem='EQUIPAMENTOS DE TI',
            detentor_id=detentor.id,
            localizacao='Sala 101',
            valor_aquisicao=5000.00,
            data_aquisicao=date(2023, 1, 1)
        )
        
        # Verificar
        assert bem is not None
        assert bem.numero_ul == '0401234'
        assert bem.numero_sap == '100987'
        assert bem.nome == 'Computador Desktop'
        assert bem.detentor_id == detentor.id
        assert bem.valor_aquisicao == 5000.00

def test_atualizar_bem(app):
    with app.app_context():
        # Preparar
        bem = BemPatrimonial(
            numero_ul='0401234',
            numero_sap='100987',
            nome='Computador Desktop',
            descricao='Computador Desktop Dell Optiplex'
        )
        db.session.add(bem)
        db.session.commit()
        
        # Executar
        bem_atualizado = PatrimonioService.atualizar_bem(
            bem_id=bem.id,
            nome='Computador Desktop Atualizado',
            descricao='Computador Desktop Dell Optiplex Atualizado',
            localizacao='Sala 102'
        )
        
        # Verificar
        assert bem_atualizado.nome == 'Computador Desktop Atualizado'
        assert bem_atualizado.descricao == 'Computador Desktop Dell Optiplex Atualizado'
        assert bem_atualizado.localizacao == 'Sala 102'

def test_atualizar_bem_inexistente(app):
    with app.app_context():
        # Executar e Verificar
        with pytest.raises(BemPatrimonialNaoEncontradoError):
            PatrimonioService.atualizar_bem(
                bem_id=999,
                nome='Teste'
            )

def test_excluir_bem(app):
    with app.app_context():
        # Preparar
        bem = BemPatrimonial(
            numero_ul='0401234',
            numero_sap='100987',
            nome='Computador Desktop',
            descricao='Computador Desktop Dell Optiplex'
        )
        db.session.add(bem)
        db.session.commit()
        
        # Executar
        PatrimonioService.excluir_bem(bem.id)
        
        # Verificar
        bem_excluido = BemPatrimonial.query.get(bem.id)
        assert bem_excluido.excluido is True

def test_excluir_bem_inexistente(app):
    with app.app_context():
        # Executar e Verificar
        with pytest.raises(BemPatrimonialNaoEncontradoError):
            PatrimonioService.excluir_bem(999)

def test_buscar_bens(app):
    with app.app_context():
        # Preparar
        bem1 = BemPatrimonial(
            numero_ul='0401234',
            numero_sap='100987',
            nome='Computador Desktop 1',
            descricao='Computador Desktop Dell Optiplex',
            grupo_bem='EQUIPAMENTOS DE TI',
            localizacao='Sala 101'
        )
        
        bem2 = BemPatrimonial(
            numero_ul='0401235',
            numero_sap='100988',
            nome='Computador Desktop 2',
            descricao='Computador Desktop HP',
            grupo_bem='EQUIPAMENTOS DE TI',
            localizacao='Sala 102'
        )
        
        bem3 = BemPatrimonial(
            numero_ul='0401236',
            numero_sap='100989',
            nome='Mesa de Escritório',
            descricao='Mesa de Escritório em L',
            grupo_bem='MOBILIÁRIO',
            localizacao='Sala 101'
        )
        
        db.session.add_all([bem1, bem2, bem3])
        db.session.commit()
        
        # Executar e Verificar
        # Busca por grupo
        bens_ti = PatrimonioService.buscar_bens(grupo_bem='EQUIPAMENTOS DE TI')
        assert len(bens_ti) == 2
        
        # Busca por localização
        bens_sala_101 = PatrimonioService.buscar_bens(localizacao='Sala 101')
        assert len(bens_sala_101) == 2
        
        # Busca por número UL parcial
        bens_ul = PatrimonioService.buscar_bens(numero_ul='040123')
        assert len(bens_ul) == 3

def test_transferir_bem(app):
    with app.app_context():
        # Preparar
        detentor1 = Usuario(
            nome='Detentor 1',
            email='detentor1@teste.com',
            matricula='12345'
        )
        
        detentor2 = Usuario(
            nome='Detentor 2',
            email='detentor2@teste.com',
            matricula='12346'
        )
        
        bem = BemPatrimonial(
            numero_ul='0401234',
            numero_sap='100987',
            nome='Computador Desktop',
            descricao='Computador Desktop Dell Optiplex',
            detentor_id=detentor1.id,
            localizacao='Sala 101'
        )
        
        db.session.add_all([detentor1, detentor2, bem])
        db.session.commit()
        
        # Executar
        bem_transferido = PatrimonioService.transferir_bem(
            bem_id=bem.id,
            novo_detentor_id=detentor2.id,
            nova_localizacao='Sala 102',
            observacao='Transferência para novo setor'
        )
        
        # Verificar
        assert bem_transferido.detentor_id == detentor2.id
        assert bem_transferido.localizacao == 'Sala 102'
        assert 'Transferência para novo setor' in bem_transferido.observacoes 