from datetime import datetime
from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError
from app import db
from app.models.item import Item
from app.models.movimento import EntradaMaterial, SaidaMaterial
from app.models.estoque import Estoque
from app.utils.exceptions import EstoqueInsuficienteError, ItemNaoEncontradoError

class AlmoxarifadoService:
    @staticmethod
    def registrar_entrada(
        item_id: int,
        quantidade: int,
        valor_unitario: float,
        fornecedor_id: int,
        nota_fiscal: str,
        data_movimento: datetime,
        usuario_id: int
    ) -> EntradaMaterial:
        """
        Registra uma entrada de material no almoxarifado.
        
        Args:
            item_id: ID do item
            quantidade: Quantidade a ser entrada
            valor_unitario: Valor unitário do item
            fornecedor_id: ID do fornecedor
            nota_fiscal: Número da nota fiscal
            data_movimento: Data do movimento
            usuario_id: ID do usuário que está registrando
            
        Returns:
            EntradaMaterial: Objeto da entrada registrada
            
        Raises:
            ItemNaoEncontradoError: Se o item não for encontrado
            SQLAlchemyError: Se houver erro no banco de dados
        """
        try:
            item = Item.query.get(item_id)
            if not item:
                raise ItemNaoEncontradoError(f"Item com ID {item_id} não encontrado")

            entrada = EntradaMaterial(
                data_movimento=data_movimento,
                numero_nota_fiscal=nota_fiscal,
                fornecedor_id=fornecedor_id,
                usuario_id=usuario_id
            )
            
            # Atualiza o estoque do item
            item.estoque_atual += quantidade
            item.valor_unitario = valor_unitario
            item.saldo_financeiro += (quantidade * valor_unitario)
            
            # Registra no estoque
            estoque = Estoque(
                item_id=item_id,
                quantidade=quantidade,
                valor_unitario=valor_unitario,
                valor_total=quantidade * valor_unitario
            )
            
            db.session.add(entrada)
            db.session.add(estoque)
            db.session.commit()
            
            return entrada
            
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def registrar_saida(
        item_id: int,
        quantidade: int,
        solicitante_id: int,
        data_movimento: datetime,
        usuario_id: int,
        observacao: Optional[str] = None
    ) -> SaidaMaterial:
        """
        Registra uma saída de material do almoxarifado.
        
        Args:
            item_id: ID do item
            quantidade: Quantidade a ser saída
            solicitante_id: ID do solicitante
            data_movimento: Data do movimento
            usuario_id: ID do usuário que está registrando
            observacao: Observação opcional
            
        Returns:
            SaidaMaterial: Objeto da saída registrada
            
        Raises:
            ItemNaoEncontradoError: Se o item não for encontrado
            EstoqueInsuficienteError: Se não houver estoque suficiente
            SQLAlchemyError: Se houver erro no banco de dados
        """
        try:
            item = Item.query.get(item_id)
            if not item:
                raise ItemNaoEncontradoError(f"Item com ID {item_id} não encontrado")
                
            if item.estoque_atual < quantidade:
                raise EstoqueInsuficienteError(
                    f"Estoque insuficiente. Disponível: {item.estoque_atual}, Solicitado: {quantidade}"
                )
            
            saida = SaidaMaterial(
                data_movimento=data_movimento,
                solicitante_id=solicitante_id,
                usuario_id=usuario_id,
                observacao=observacao
            )
            
            # Atualiza o estoque do item
            item.estoque_atual -= quantidade
            item.saldo_financeiro -= (quantidade * item.valor_unitario)
            
            db.session.add(saida)
            db.session.commit()
            
            return saida
            
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def listar_itens_baixo_estoque() -> List[Item]:
        """
        Lista todos os itens com estoque abaixo do mínimo.
        
        Returns:
            List[Item]: Lista de itens com estoque baixo
        """
        return Item.query.filter(
            Item.estoque_atual <= Item.estoque_minimo
        ).all()

    @staticmethod
    def atualizar_valor_item(item_id: int, novo_valor: float) -> Item:
        """
        Atualiza o valor unitário de um item.
        
        Args:
            item_id: ID do item
            novo_valor: Novo valor unitário
            
        Returns:
            Item: Item atualizado
            
        Raises:
            ItemNaoEncontradoError: Se o item não for encontrado
            SQLAlchemyError: Se houver erro no banco de dados
        """
        try:
            item = Item.query.get(item_id)
            if not item:
                raise ItemNaoEncontradoError(f"Item com ID {item_id} não encontrado")
            
            item.valor_unitario = novo_valor
            item.saldo_financeiro = item.estoque_atual * novo_valor
            
            db.session.commit()
            return item
            
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e 