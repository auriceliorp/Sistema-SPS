from typing import Optional, Dict, Any
from flask import request
from app.extensions import db
from app.models.audit import AuditLog

class AuditService:
    @staticmethod
    def registrar_log(
        acao: str,
        tabela: str,
        usuario_id: Optional[int] = None,
        registro_id: Optional[int] = None,
        dados_anteriores: Optional[Dict[str, Any]] = None,
        dados_novos: Optional[Dict[str, Any]] = None
    ) -> AuditLog:
        """
        Registra uma ação no log de auditoria.
        
        Args:
            acao: Tipo de ação realizada (insert, update, delete, etc)
            tabela: Nome da tabela afetada
            usuario_id: ID do usuário que realizou a ação (opcional)
            registro_id: ID do registro afetado (opcional)
            dados_anteriores: Dados antes da alteração (opcional)
            dados_novos: Dados após a alteração (opcional)
            
        Returns:
            AuditLog: Registro de log criado
        """
        log = AuditLog(
            usuario_id=usuario_id,
            acao=acao,
            tabela=tabela,
            registro_id=registro_id,
            dados_anteriores=dados_anteriores,
            dados_novos=dados_novos,
            ip_address=request.remote_addr if request else None,
            user_agent=request.user_agent.string if request and request.user_agent else None
        )
        
        db.session.add(log)
        db.session.commit()
        
        return log

    @staticmethod
    def buscar_logs(
        usuario_id: Optional[int] = None,
        acao: Optional[str] = None,
        tabela: Optional[str] = None,
        data_inicio: Optional[str] = None,
        data_fim: Optional[str] = None,
        limite: int = 100
    ) -> list[AuditLog]:
        """
        Busca registros de log com base nos filtros fornecidos.
        
        Args:
            usuario_id: Filtrar por usuário específico
            acao: Filtrar por tipo de ação
            tabela: Filtrar por tabela
            data_inicio: Data inicial (formato: YYYY-MM-DD)
            data_fim: Data final (formato: YYYY-MM-DD)
            limite: Limite de registros retornados
            
        Returns:
            List[AuditLog]: Lista de registros encontrados
        """
        query = AuditLog.query
        
        if usuario_id:
            query = query.filter_by(usuario_id=usuario_id)
        if acao:
            query = query.filter_by(acao=acao)
        if tabela:
            query = query.filter_by(tabela=tabela)
        if data_inicio:
            query = query.filter(AuditLog.data_hora >= data_inicio)
        if data_fim:
            query = query.filter(AuditLog.data_hora <= data_fim)
            
        return query.order_by(AuditLog.data_hora.desc()).limit(limite).all()

    @staticmethod
    def limpar_logs_antigos(dias: int = 90) -> int:
        """
        Remove logs mais antigos que o número de dias especificado.
        
        Args:
            dias: Número de dias para manter os logs
            
        Returns:
            int: Número de registros removidos
        """
        from datetime import datetime, timedelta
        data_limite = datetime.utcnow() - timedelta(days=dias)
        
        deletados = AuditLog.query.filter(AuditLog.data_hora < data_limite).delete()
        db.session.commit()
        
        return deletados 