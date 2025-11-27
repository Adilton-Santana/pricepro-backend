"""
Model de Usuário

Representa a tabela 'users' no banco de dados PostgreSQL.
Contém informações de autenticação e perfil do usuário.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.connection import Base
import enum


class UserRole(str, enum.Enum):
    """
    Enum para os roles (perfis) de usuário.
    
    - USER: Usuário comum (pode gerenciar seus próprios produtos)
    - ADMIN: Administrador (acesso total ao sistema)
    """
    USER = "user"
    ADMIN = "admin"


class User(Base):
    """
    Model de Usuário.
    
    Atributos:
        id: Identificador único
        email: Email único do usuário
        full_name: Nome completo
        hashed_password: Senha criptografada com bcrypt
        role: Perfil do usuário (user ou admin)
        is_active: Indica se a conta está ativa
        is_verified: Indica se o email foi verificado
        created_at: Data/hora de criação
        updated_at: Data/hora da última atualização
    
    Relacionamentos:
        products: Lista de produtos pertencentes ao usuário
    """
    
    __tablename__ = "users"
    
    # Campos principais
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    # Role e status
    role = Column(
        SQLEnum(UserRole),
        default=UserRole.USER,
        nullable=False
    )
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relacionamentos
    products = relationship("Product", back_populates="owner", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"
