from typing import Optional
from datetime import datetime
from app.extensions import db
from app.models.user import Usuario
from app.utils.exceptions import UsuarioNaoEncontradoError

class AuthService:
    @staticmethod
    def authenticate_user(email: str, password: str) -> Optional[Usuario]:
        """
        Autentica um usuário com email e senha.
        
        Args:
            email: Email do usuário
            password: Senha do usuário
            
        Returns:
            Usuario: Objeto do usuário se autenticado com sucesso
            None: Se a autenticação falhar
        """
        user = Usuario.query.filter_by(email=email).first()
        if user and user.check_password(password):
            user.update_ultimo_acesso()
            return user
        return None

    @staticmethod
    def register_user(
        nome: str,
        email: str,
        password: str,
        matricula: Optional[str] = None,
        ramal: Optional[str] = None,
        unidade_local_id: Optional[int] = None,
        perfil_id: Optional[int] = None
    ) -> Usuario:
        """
        Registra um novo usuário no sistema.
        
        Args:
            nome: Nome completo do usuário
            email: Email do usuário
            password: Senha do usuário
            matricula: Matrícula do usuário (opcional)
            ramal: Ramal do usuário (opcional)
            unidade_local_id: ID da unidade local (opcional)
            perfil_id: ID do perfil (opcional)
            
        Returns:
            Usuario: Objeto do usuário criado
            
        Raises:
            SQLAlchemyError: Se houver erro no banco de dados
        """
        user = Usuario(
            nome=nome,
            email=email,
            matricula=matricula,
            ramal=ramal,
            unidade_local_id=unidade_local_id,
            perfil_id=perfil_id
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return user

    @staticmethod
    def change_password(user_id: int, old_password: str, new_password: str) -> bool:
        """
        Altera a senha de um usuário.
        
        Args:
            user_id: ID do usuário
            old_password: Senha atual
            new_password: Nova senha
            
        Returns:
            bool: True se a senha foi alterada com sucesso, False caso contrário
            
        Raises:
            UsuarioNaoEncontradoError: Se o usuário não for encontrado
        """
        user = Usuario.query.get(user_id)
        if not user:
            raise UsuarioNaoEncontradoError(f"Usuário com ID {user_id} não encontrado")
            
        if user.check_password(old_password):
            user.set_password(new_password)
            user.senha_temporaria = False
            db.session.commit()
            return True
            
        return False

    @staticmethod
    def reset_password(user_id: int, new_password: str) -> None:
        """
        Redefine a senha de um usuário (usado por administradores).
        
        Args:
            user_id: ID do usuário
            new_password: Nova senha
            
        Raises:
            UsuarioNaoEncontradoError: Se o usuário não for encontrado
        """
        user = Usuario.query.get(user_id)
        if not user:
            raise UsuarioNaoEncontradoError(f"Usuário com ID {user_id} não encontrado")
            
        user.set_password(new_password)
        user.senha_temporaria = True
        db.session.commit()

    @staticmethod
    def deactivate_user(user_id: int) -> None:
        """
        Desativa um usuário no sistema.
        
        Args:
            user_id: ID do usuário
            
        Raises:
            UsuarioNaoEncontradoError: Se o usuário não for encontrado
        """
        user = Usuario.query.get(user_id)
        if not user:
            raise UsuarioNaoEncontradoError(f"Usuário com ID {user_id} não encontrado")
            
        user.ativo = False
        db.session.commit()

    @staticmethod
    def activate_user(user_id: int) -> None:
        """
        Ativa um usuário no sistema.
        
        Args:
            user_id: ID do usuário
            
        Raises:
            UsuarioNaoEncontradoError: Se o usuário não for encontrado
        """
        user = Usuario.query.get(user_id)
        if not user:
            raise UsuarioNaoEncontradoError(f"Usuário com ID {user_id} não encontrado")
            
        user.ativo = True
        db.session.commit() 