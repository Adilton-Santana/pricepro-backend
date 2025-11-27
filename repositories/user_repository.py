"""
Repository de Usuário

Camada de acesso a dados para operações com usuários.
Responsável por todas as queries relacionadas à tabela users.
"""

from sqlalchemy.orm import Session
from typing import Optional, List
from models.user import User, UserRole
from schemas.user import UserCreate, UserUpdate
from core.security import hash_password


class UserRepository:
    """
    Repository para operações de banco de dados com usuários.
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, user_data: UserCreate) -> User:
        """
        Cria um novo usuário no banco de dados.
        
        Args:
            user_data: Dados do usuário a ser criado
            
        Returns:
            Usuário criado
        """
        db_user = User(
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=hash_password(user_data.password),
            role=UserRole.USER
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Busca usuário por ID.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Usuário encontrado ou None
        """
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        """
        Busca usuário por email.
        
        Args:
            email: Email do usuário
            
        Returns:
            Usuário encontrado ou None
        """
        return self.db.query(User).filter(User.email == email).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Busca todos os usuários com paginação.
        
        Args:
            skip: Número de registros a pular
            limit: Número máximo de registros a retornar
            
        Returns:
            Lista de usuários
        """
        return self.db.query(User).offset(skip).limit(limit).all()
    
    def update(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """
        Atualiza dados de um usuário.
        
        Args:
            user_id: ID do usuário
            user_data: Dados a serem atualizados
            
        Returns:
            Usuário atualizado ou None se não encontrado
        """
        db_user = self.get_by_id(user_id)
        if not db_user:
            return None
        
        # Atualiza apenas os campos fornecidos
        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def update_password(self, user_id: int, new_password: str) -> Optional[User]:
        """
        Atualiza a senha de um usuário.
        
        Args:
            user_id: ID do usuário
            new_password: Nova senha em texto plano (será hasheada)
            
        Returns:
            Usuário atualizado ou None se não encontrado
        """
        db_user = self.get_by_id(user_id)
        if not db_user:
            return None
        
        db_user.hashed_password = hash_password(new_password)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def delete(self, user_id: int) -> bool:
        """
        Deleta um usuário.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            True se deletado com sucesso, False se não encontrado
        """
        db_user = self.get_by_id(user_id)
        if not db_user:
            return False
        
        self.db.delete(db_user)
        self.db.commit()
        return True
    
    def exists_by_email(self, email: str) -> bool:
        """
        Verifica se um usuário com o email já existe.
        
        Args:
            email: Email a verificar
            
        Returns:
            True se existe, False caso contrário
        """
        return self.db.query(User).filter(User.email == email).count() > 0
    
    def count(self) -> int:
        """
        Conta o número total de usuários.
        
        Returns:
            Número de usuários
        """
        return self.db.query(User).count()
