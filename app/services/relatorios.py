from typing import List, Dict, Any, Optional
from datetime import datetime, date
import pandas as pd
from sqlalchemy import func
from app.extensions import db
from app.models.item import Item
from app.models.movimento import EntradaMaterial, SaidaMaterial, EntradaItem, SaidaItem
from app.models.patrimonio import BemPatrimonial
from app.models.fornecedor import Fornecedor

class RelatoriosService:
    @staticmethod
    def gerar_relatorio_estoque(
        grupo_id: Optional[int] = None,
        abaixo_minimo: bool = False
    ) -> pd.DataFrame:
        """
        Gera relatório de estoque atual.
        
        Args:
            grupo_id: Filtrar por grupo específico
            abaixo_minimo: Filtrar apenas itens abaixo do estoque mínimo
            
        Returns:
            DataFrame com os dados do relatório
        """
        query = db.session.query(
            Item.codigo,
            Item.nome,
            Item.unidade_medida,
            Item.saldo,
            Item.estoque_minimo,
            Item.estoque_maximo,
            Item.valor_medio
        ).filter(Item.excluido == False)
        
        if grupo_id:
            query = query.filter(Item.grupo_id == grupo_id)
        if abaixo_minimo:
            query = query.filter(Item.saldo <= Item.estoque_minimo)
            
        df = pd.read_sql(query.statement, db.session.bind)
        
        # Calcula valor total
        df['valor_total'] = df['saldo'] * df['valor_medio']
        
        return df

    @staticmethod
    def gerar_relatorio_movimentacao(
        data_inicio: date,
        data_fim: date,
        tipo_movimento: Optional[str] = None
    ) -> Dict[str, pd.DataFrame]:
        """
        Gera relatório de movimentação de estoque.
        
        Args:
            data_inicio: Data inicial
            data_fim: Data final
            tipo_movimento: 'entrada' ou 'saida' (opcional)
            
        Returns:
            Dict com DataFrames de entrada e saída
        """
        relatorio = {}
        
        # Relatório de Entradas
        if not tipo_movimento or tipo_movimento == 'entrada':
            query_entrada = db.session.query(
                EntradaMaterial.data_movimento,
                EntradaMaterial.numero_nota_fiscal,
                Fornecedor.nome.label('fornecedor'),
                Item.codigo,
                Item.nome,
                EntradaItem.quantidade,
                EntradaItem.valor_unitario,
                (EntradaItem.quantidade * EntradaItem.valor_unitario).label('valor_total')
            ).join(EntradaItem).join(Item).join(Fornecedor).filter(
                EntradaMaterial.data_movimento.between(data_inicio, data_fim),
                EntradaMaterial.estornada == False
            )
            
            relatorio['entradas'] = pd.read_sql(query_entrada.statement, db.session.bind)
        
        # Relatório de Saídas
        if not tipo_movimento or tipo_movimento == 'saida':
            query_saida = db.session.query(
                SaidaMaterial.data_movimento,
                Item.codigo,
                Item.nome,
                SaidaItem.quantidade,
                SaidaItem.valor_unitario,
                (SaidaItem.quantidade * SaidaItem.valor_unitario).label('valor_total')
            ).join(SaidaItem).join(Item).filter(
                SaidaMaterial.data_movimento.between(data_inicio, data_fim),
                SaidaMaterial.estornada == False
            )
            
            relatorio['saidas'] = pd.read_sql(query_saida.statement, db.session.bind)
        
        return relatorio

    @staticmethod
    def gerar_relatorio_patrimonio(
        grupo_bem: Optional[str] = None,
        detentor_id: Optional[int] = None,
        localizacao: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Gera relatório de bens patrimoniais.
        
        Args:
            grupo_bem: Filtrar por grupo específico
            detentor_id: Filtrar por detentor
            localizacao: Filtrar por localização
            
        Returns:
            DataFrame com os dados do relatório
        """
        query = db.session.query(
            BemPatrimonial.numero_ul,
            BemPatrimonial.numero_sap,
            BemPatrimonial.nome,
            BemPatrimonial.grupo_bem,
            BemPatrimonial.classificacao_contabil,
            BemPatrimonial.localizacao,
            BemPatrimonial.data_aquisicao,
            BemPatrimonial.valor_aquisicao,
            BemPatrimonial.status
        ).filter(BemPatrimonial.excluido == False)
        
        if grupo_bem:
            query = query.filter(BemPatrimonial.grupo_bem == grupo_bem)
        if detentor_id:
            query = query.filter(BemPatrimonial.detentor_id == detentor_id)
        if localizacao:
            query = query.filter(BemPatrimonial.localizacao == localizacao)
            
        return pd.read_sql(query.statement, db.session.bind)

    @staticmethod
    def gerar_relatorio_fornecedores() -> pd.DataFrame:
        """
        Gera relatório de fornecedores com total de compras.
        
        Returns:
            DataFrame com os dados do relatório
        """
        query = db.session.query(
            Fornecedor.nome,
            Fornecedor.cnpj,
            Fornecedor.email,
            Fornecedor.telefone,
            func.count(EntradaMaterial.id).label('total_compras'),
            func.sum(EntradaItem.quantidade * EntradaItem.valor_unitario).label('valor_total')
        ).outerjoin(EntradaMaterial).outerjoin(EntradaItem).group_by(Fornecedor.id)
        
        return pd.read_sql(query.statement, db.session.bind)

    @staticmethod
    def exportar_para_excel(df: pd.DataFrame, nome_arquivo: str) -> str:
        """
        Exporta um DataFrame para Excel.
        
        Args:
            df: DataFrame a ser exportado
            nome_arquivo: Nome do arquivo sem extensão
            
        Returns:
            str: Caminho do arquivo gerado
        """
        import os
        from app.extensions import app
        
        # Garante que o diretório de uploads existe
        diretorio = os.path.join(app.root_path, 'static', 'uploads', 'relatorios')
        os.makedirs(diretorio, exist_ok=True)
        
        # Gera nome único para o arquivo
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        arquivo = f"{nome_arquivo}_{timestamp}.xlsx"
        caminho = os.path.join(diretorio, arquivo)
        
        # Exporta para Excel
        df.to_excel(caminho, index=False, engine='openpyxl')
        
        return f"/static/uploads/relatorios/{arquivo}" 