"""
Schemas Pydantic para Autenticação

Define os schemas de validação de dados para operações de autenticação:
- Tokens de acesso e refresh
- Respostas de login
"""

from pydantic import BaseModel, Field
from typing import Optional
from models.user import UserRole


class Token(BaseModel):
    """
    Schema para resposta de token.
    """
    access_token: str = Field(..., description="Token JWT de acesso")
    refresh_token: str = Field(..., description="Token JWT de refresh")
    token_type: str = Field(default="bearer", description="Tipo do token")


class TokenData(BaseModel):
    """
    Schema para dados contidos no token JWT.
    """
    user_id: Optional[int] = None
    email: Optional[str] = None
    role: Optional[UserRole] = None


class RefreshTokenRequest(BaseModel):
    """
    Schema para solicitação de refresh do token.
    """
    refresh_token: str = Field(..., description="Token de refresh")


class LoginResponse(BaseModel):
    """
    Schema de resposta completa para login.
    Inclui tokens e informações do usuário.
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: dict  # Informações básicas do usuário


class PasswordResetTokenResponse(BaseModel):
    """
    Schema de resposta para solicitação de reset de senha.
    """
    message: str
    reset_token: str = Field(..., description="Token para reset de senha (normalmente seria enviado por email)")
