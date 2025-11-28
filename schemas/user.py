"""
Schemas Pydantic para Usuário

Define os schemas de validação de dados para operações com usuários:
- Criação de usuário
- Atualização de usuário
- Resposta de usuário (sem senha)
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from models.user import UserRole


class UserBase(BaseModel):
    """
    Schema base para Usuário com campos comuns.
    """
    email: EmailStr = Field(..., description="Email do usuário")
    full_name: str = Field(..., min_length=2, max_length=255, description="Nome completo")


class UserCreate(UserBase):
    """
    Schema para criação de novo usuário.
    
    Campos adicionais:
        password: Senha do usuário (será validada e criptografada)
    """
    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="Senha do usuário (mínimo 8 caracteres)"
    )


class UserUpdate(BaseModel):
    """
    Schema para atualização de usuário.
    Todos os campos são opcionais.
    """
    full_name: Optional[str] = Field(None, min_length=2, max_length=255)
    email: Optional[EmailStr] = None


class UserResponse(UserBase):
    """
    Schema de resposta para Usuário.
    Não inclui a senha.
    """
    id: int
    role: UserRole
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    """
    Schema para login de usuário.
    """
    email: EmailStr = Field(..., description="Email do usuário")
    password: str = Field(..., description="Senha do usuário")


class PasswordChange(BaseModel):
    """
    Schema para mudança de senha.
    """
    old_password: str = Field(..., description="Senha atual")
    new_password: str = Field(
        ...,
        min_length=8,
        description="Nova senha (mínimo 8 caracteres)"
    )


class PasswordResetRequest(BaseModel):
    """
    Schema para solicitação de recuperação de senha.
    """
    email: EmailStr = Field(..., description="Email do usuário")


class PasswordReset(BaseModel):
    """
    Schema para reset de senha com token.
    """
    token: str = Field(..., description="Token de recuperação")
    new_password: str = Field(
        ...,
        min_length=8,
        description="Nova senha (mínimo 8 caracteres)"
    )
