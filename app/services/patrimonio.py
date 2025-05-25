from typing import List, Optional
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.models.patrimonio import BemPatrimonial, GrupoPatrimonio
from app.utils.exceptions import BemPatrimonialNaoEncontradoError

class PatrimonioService:
    @staticmethod
    def cadastrar_bem(
        numero_ul: str,
        numero_sap: str,
        nome: str,
        descricao: str,
        grupo_bem: Optional[str] = None,
        classificacao_contabil: Optional[str] = None,
        detentor_id: Optional[int] = None,
        localizacao: Optional[str] = None,
        data_aquisicao: Optional[datetime] = None,
        valor_aquisicao: Optional[float] = None,
        foto: Optional[str] = None,
        observacoes: Optional[str] = None,
        numero_siads: Optional[str] = None
    ) -> BemPatrimonial:
        """
        Cadastra um novo bem patrimonial.
        
        Args:
            numero_ul: Número do patrimônio na Unidade Local
            numero_sap: Número do SAP
            nome: Nome do bem
            descricao: Descrição do bem
            grupo_bem: Grupo do bem (opcional)
            classificacao_contabil: Classificação contábil (opcional)
            detentor_id: ID do detentor (opcional)
            localizacao: Localização do bem (opcional)
            data_aquisicao: Data de aquisição (opcional)
            valor_aquisicao: Valor de aquisição (opcional)
            foto: Caminho da foto (opcional)
            observacoes: Observações (opcional)
            numero_siads: Número do SIADS (opcional)
            
        Returns:
            BemPatrimonial: Objeto do bem cadastrado
            
        Raises:
            SQLAlchemyError: Se houver erro no banco de dados
        """
        bem = BemPatrimonial(
            numero_ul=numero_ul,
            numero_sap=numero_sap,
            numero_siads=numero_siads,
            nome=nome,
            descricao=descricao,
            grupo_bem=grupo_bem,
            classificacao_contabil=classificacao_contabil,
            detentor_id=detentor_id,
            localizacao=localizacao,
            data_aquisicao=data_aquisicao,
            valor_aquisicao=valor_aquisicao,
            foto=foto,
            observacoes=observacoes
        )
        
        db.session.add(bem)
        db.session.commit()
        
        return bem

    @staticmethod
    def atualizar_bem(
        bem_id: int,
        numero_ul: Optional[str] = None,
        numero_sap: Optional[str] = None,
        numero_siads: Optional[str] = None,
        nome: Optional[str] = None,
        descricao: Optional[str] = None,
        grupo_bem: Optional[str] = None,
        classificacao_contabil: Optional[str] = None,
        detentor_id: Optional[int] = None,
        localizacao: Optional[str] = None,
        data_aquisicao: Optional[datetime] = None,
        valor_aquisicao: Optional[float] = None,
        foto: Optional[str] = None,
        observacoes: Optional[str] = None,
        status: Optional[str] = None
    ) -> BemPatrimonial:
        """
        Atualiza um bem patrimonial existente.
        
        Args:
            bem_id: ID do bem patrimonial
            [Demais parâmetros são opcionais e seguem a mesma estrutura do cadastro]
            
        Returns:
            BemPatrimonial: Objeto do bem atualizado
            
        Raises:
            BemPatrimonialNaoEncontradoError: Se o bem não for encontrado
            SQLAlchemyError: Se houver erro no banco de dados
        """
        bem = BemPatrimonial.query.get(bem_id)
        if not bem:
            raise BemPatrimonialNaoEncontradoError(f"Bem patrimonial com ID {bem_id} não encontrado")
            
        if numero_ul is not None:
            bem.numero_ul = numero_ul
        if numero_sap is not None:
            bem.numero_sap = numero_sap
        if numero_siads is not None:
            bem.numero_siads = numero_siads
        if nome is not None:
            bem.nome = nome
        if descricao is not None:
            bem.descricao = descricao
        if grupo_bem is not None:
            bem.grupo_bem = grupo_bem
        if classificacao_contabil is not None:
            bem.classificacao_contabil = classificacao_contabil
        if detentor_id is not None:
            bem.detentor_id = detentor_id
        if localizacao is not None:
            bem.localizacao = localizacao
        if data_aquisicao is not None:
            bem.data_aquisicao = data_aquisicao
        if valor_aquisicao is not None:
            bem.valor_aquisicao = valor_aquisicao
        if foto is not None:
            bem.foto = foto
        if observacoes is not None:
            bem.observacoes = observacoes
        if status is not None:
            bem.status = status
            
        db.session.commit()
        return bem

    @staticmethod
    def excluir_bem(bem_id: int) -> None:
        """
        Marca um bem patrimonial como excluído (exclusão lógica).
        
        Args:
            bem_id: ID do bem patrimonial
            
        Raises:
            BemPatrimonialNaoEncontradoError: Se o bem não for encontrado
            SQLAlchemyError: Se houver erro no banco de dados
        """
        bem = BemPatrimonial.query.get(bem_id)
        if not bem:
            raise BemPatrimonialNaoEncontradoError(f"Bem patrimonial com ID {bem_id} não encontrado")
            
        bem.excluido = True
        db.session.commit()

    @staticmethod
    def buscar_bens(
        numero_ul: Optional[str] = None,
        numero_sap: Optional[str] = None,
        grupo_bem: Optional[str] = None,
        detentor_id: Optional[int] = None,
        localizacao: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[BemPatrimonial]:
        """
        Busca bens patrimoniais com base em filtros.
        
        Args:
            numero_ul: Número do patrimônio na Unidade Local (opcional)
            numero_sap: Número do SAP (opcional)
            grupo_bem: Grupo do bem (opcional)
            detentor_id: ID do detentor (opcional)
            localizacao: Localização do bem (opcional)
            status: Status do bem (opcional)
            
        Returns:
            List[BemPatrimonial]: Lista de bens patrimoniais encontrados
        """
        query = BemPatrimonial.query.filter_by(excluido=False)
        
        if numero_ul:
            query = query.filter(BemPatrimonial.numero_ul.ilike(f"%{numero_ul}%"))
        if numero_sap:
            query = query.filter(BemPatrimonial.numero_sap.ilike(f"%{numero_sap}%"))
        if grupo_bem:
            query = query.filter_by(grupo_bem=grupo_bem)
        if detentor_id:
            query = query.filter_by(detentor_id=detentor_id)
        if localizacao:
            query = query.filter_by(localizacao=localizacao)
        if status:
            query = query.filter_by(status=status)
            
        return query.order_by(BemPatrimonial.nome).all()

    @staticmethod
    def transferir_bem(
        bem_id: int,
        novo_detentor_id: int,
        nova_localizacao: Optional[str] = None,
        observacao: Optional[str] = None
    ) -> BemPatrimonial:
        """
        Transfere um bem patrimonial para outro detentor.
        
        Args:
            bem_id: ID do bem patrimonial
            novo_detentor_id: ID do novo detentor
            nova_localizacao: Nova localização do bem (opcional)
            observacao: Observação sobre a transferência (opcional)
            
        Returns:
            BemPatrimonial: Objeto do bem atualizado
            
        Raises:
            BemPatrimonialNaoEncontradoError: Se o bem não for encontrado
            SQLAlchemyError: Se houver erro no banco de dados
        """
        bem = BemPatrimonial.query.get(bem_id)
        if not bem:
            raise BemPatrimonialNaoEncontradoError(f"Bem patrimonial com ID {bem_id} não encontrado")
            
        bem.detentor_id = novo_detentor_id
        if nova_localizacao:
            bem.localizacao = nova_localizacao
        if observacao:
            bem.observacoes = (bem.observacoes or "") + f"\nTransferência: {observacao}"
            
        db.session.commit()
        return bem 