"""
Serviço de Autenticação

Responsável por toda a lógica de negócio relacionada à autenticação:
- Login e logout
- Geração e validação de tokens
- Refresh de tokens
- Recuperação de senha
"""

from sqlalchemy.orm import Session
from typing import Optional, Tuple
from datetime import timedelta

from repositories.user_repository import UserRepository
from core.security import verify_password
from core.jwt import (
    create_access_token,
    create_refresh_token,
    create_password_reset_token,
    decode_token,
    verify_token_type
)
from database.redis_client import redis_client
from core.config import settings
from models.user import User


class AuthService:
    """
    Serviço para gerenciar autenticação de usuários.
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Autentica um usuário verificando email e senha.
        
        Args:
            email: Email do usuário
            password: Senha em texto plano
            
        Returns:
            Usuário autenticado ou None se credenciais inválidas
        """
        user = self.user_repo.get_by_email(email)
        if not user:
            return None
        
        if not verify_password(password, user.hashed_password):
            return None
        
        if not user.is_active:
            return None
        
        return user
    
    def login(self, email: str, password: str) -> Optional[Tuple[str, str, User]]:
        """
        Realiza o login de um usuário.
        
        Args:
            email: Email do usuário
            password: Senha em texto plano
            
        Returns:
            Tupla (access_token, refresh_token, user) ou None se falhar
        """
        user = self.authenticate_user(email, password)
        if not user:
            return None
        
        # Cria tokens
        access_token = create_access_token(
            data={
                "user_id": user.id,
                "email": user.email,
                "role": user.role.value
            }
        )
        
        refresh_token = create_refresh_token(
            data={"user_id": user.id}
        )
        
        # Salva o refresh token no Redis
        payload = decode_token(refresh_token)
        if payload and "jti" in payload:
            expires_in = settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60  # em segundos
            redis_client.save_refresh_token(user.id, payload["jti"], expires_in)
        
        return access_token, refresh_token, user
    
    def refresh_access_token(self, refresh_token: str) -> Optional[Tuple[str, str]]:
        """
        Gera um novo access token usando um refresh token válido.
        
        Args:
            refresh_token: Token de refresh
            
        Returns:
            Tupla (novo_access_token, novo_refresh_token) ou None se inválido
        """
        # Decodifica o refresh token
        payload = decode_token(refresh_token)
        if not payload:
            return None
        
        # Verifica se é um refresh token
        if not verify_token_type(payload, "refresh"):
            return None
        
        user_id = payload.get("user_id")
        token_jti = payload.get("jti")
        
        if not user_id or not token_jti:
            return None
        
        # Verifica se o token está válido no Redis
        if not redis_client.is_refresh_token_valid(user_id, token_jti):
            return None
        
        # Busca o usuário
        user = self.user_repo.get_by_id(user_id)
        if not user or not user.is_active:
            return None
        
        # Invalida o refresh token antigo
        redis_client.invalidate_refresh_token(user_id, token_jti)
        
        # Cria novos tokens
        new_access_token = create_access_token(
            data={
                "user_id": user.id,
                "email": user.email,
                "role": user.role.value
            }
        )
        
        new_refresh_token = create_refresh_token(
            data={"user_id": user.id}
        )
        
        # Salva o novo refresh token no Redis
        new_payload = decode_token(new_refresh_token)
        if new_payload and "jti" in new_payload:
            expires_in = settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
            redis_client.save_refresh_token(user.id, new_payload["jti"], expires_in)
        
        return new_access_token, new_refresh_token
    
    def logout(self, refresh_token: str) -> bool:
        """
        Realiza o logout invalidando o refresh token.
        
        Args:
            refresh_token: Token de refresh a ser invalidado
            
        Returns:
            True se logout bem-sucedido, False caso contrário
        """
        payload = decode_token(refresh_token)
        if not payload:
            return False
        
        user_id = payload.get("user_id")
        token_jti = payload.get("jti")
        
        if not user_id or not token_jti:
            return False
        
        redis_client.invalidate_refresh_token(user_id, token_jti)
        return True
    
    def request_password_reset(self, email: str) -> Optional[str]:
        """
        Gera um token para recuperação de senha.
        
        Args:
            email: Email do usuário
            
        Returns:
            Token de recuperação ou None se usuário não encontrado
        """
        user = self.user_repo.get_by_email(email)
        if not user:
            return None
        
        # Gera token de reset
        reset_token = create_password_reset_token(email)
        
        # TODO: Aqui seria enviado por email
        # Por enquanto, retorna o token na resposta
        
        return reset_token
    
    def reset_password(self, token: str, new_password: str) -> bool:
        """
        Reseta a senha usando um token de recuperação.
        
        Args:
            token: Token de recuperação
            new_password: Nova senha em texto plano
            
        Returns:
            True se senha resetada com sucesso, False caso contrário
        """
        payload = decode_token(token)
        if not payload:
            return False
        
        if not verify_token_type(payload, "password_reset"):
            return False
        
        email = payload.get("email")
        if not email:
            return False
        
        user = self.user_repo.get_by_email(email)
        if not user:
            return False
        
        # Atualiza a senha
        self.user_repo.update_password(user.id, new_password)
        
        return True
    
    def verify_access_token(self, token: str) -> Optional[dict]:
        """
        Verifica e decodifica um access token.
        
        Args:
            token: Access token
            
        Returns:
            Payload do token ou None se inválido
        """
        payload = decode_token(token)
        if not payload:
            return None
        
        if not verify_token_type(payload, "access"):
            return None
        
        return payload
