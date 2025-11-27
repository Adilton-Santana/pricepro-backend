"""
Dependencies do FastAPI

Funções de dependência para uso nos endpoints:
- Autenticação de usuário
- Verificação de roles
- Rate limiting
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional

from database.connection import get_db
from database.redis_client import redis_client
from core.jwt import decode_token, verify_token_type
from repositories.user_repository import UserRepository
from models.user import User, UserRole

# Security scheme para tokens JWT
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Obtém o usuário atual a partir do token JWT.
    
    Uso:
        @app.get("/protected")
        def protected_route(current_user: User = Depends(get_current_user)):
            return {"user_id": current_user.id}
    
    Args:
        credentials: Token JWT do header Authorization
        db: Sessão do banco de dados
        
    Returns:
        Usuário autenticado
        
    Raises:
        HTTPException: Se token inválido ou usuário não encontrado
    """
    token = credentials.credentials
    
    # Decodifica o token
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verifica se é um access token
    if not verify_token_type(payload, "access"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tipo de token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Extrai o user_id do payload
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Busca o usuário no banco
    user_repo = UserRepository(db)
    user = user_repo.get_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo"
        )
    
    return user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    Verifica se o usuário é admin.
    
    Uso:
        @app.get("/admin-only")
        def admin_route(admin: User = Depends(require_admin)):
            return {"message": "Admin area"}
    
    Args:
        current_user: Usuário autenticado
        
    Returns:
        Usuário se for admin
        
    Raises:
        HTTPException: Se usuário não é admin
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: apenas administradores"
        )
    return current_user


def check_rate_limit(current_user: User = Depends(get_current_user)) -> User:
    """
    Verifica o rate limit do usuário.
    
    Implementa rate limiting de 200 requisições por minuto usando Redis.
    
    Uso:
        @app.get("/limited")
        def limited_route(user: User = Depends(check_rate_limit)):
            return {"message": "Rate limited endpoint"}
    
    Args:
        current_user: Usuário autenticado
        
    Returns:
        Usuário se dentro do limite
        
    Raises:
        HTTPException: Se excedeu o limite de requisições
    """
    # Verifica rate limit
    if not redis_client.check_rate_limit(current_user.id):
        remaining = redis_client.get_rate_limit_remaining(current_user.id)
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit excedido. Requisições restantes: {remaining}",
            headers={
                "X-RateLimit-Remaining": str(remaining),
                "Retry-After": "60"  # Tentar novamente em 60 segundos
            }
        )
    
    return current_user
