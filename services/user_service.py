"""
Serviço de Usuário

Responsável por toda a lógica de negócio relacionada a usuários:
- Criação e gestão de usuários
- Validações de negócio
- Troca de senha
"""

from sqlalchemy.orm import Session
from typing import Optional, List
from fastapi import HTTPException, status

from repositories.user_repository import UserRepository
from schemas.user import UserCreate, UserUpdate, PasswordChange
from core.security import verify_password, validate_password_strength
from models.user import User


class UserService:
    """
    Serviço para gerenciar operações de usuários.
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
    
    def create_user(self, user_data: UserCreate) -> User:
        """
        Cria um novo usuário.
        
        Args:
            user_data: Dados do usuário
            
        Returns:
            Usuário criado
            
        Raises:
            HTTPException: Se email já existe ou senha inválida
        """
        # Valida se email já existe
        if self.user_repo.exists_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado"
            )
        
        # Valida força da senha
        is_valid, message = validate_password_strength(user_data.password)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )
        
        # Cria o usuário
        return self.user_repo.create(user_data)
    
    def get_user(self, user_id: int) -> Optional[User]:
        """
        Busca um usuário por ID.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Usuário encontrado ou None
        """
        return self.user_repo.get_by_id(user_id)
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Busca um usuário por email.
        
        Args:
            email: Email do usuário
            
        Returns:
            Usuário encontrado ou None
        """
        return self.user_repo.get_by_email(email)
    
    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """
        Atualiza dados de um usuário.
        
        Args:
            user_id: ID do usuário
            user_data: Dados a serem atualizados
            
        Returns:
            Usuário atualizado ou None se não encontrado
            
        Raises:
            HTTPException: Se email já existe
        """
        # Se está atualizando email, verifica se já existe
        if user_data.email:
            existing_user = self.user_repo.get_by_email(user_data.email)
            if existing_user and existing_user.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email já cadastrado"
                )
        
        return self.user_repo.update(user_id, user_data)
    
    def change_password(self, user_id: int, password_data: PasswordChange) -> bool:
        """
        Altera a senha de um usuário.
        
        Args:
            user_id: ID do usuário
            password_data: Dados de troca de senha
            
        Returns:
            True se senha alterada com sucesso
            
        Raises:
            HTTPException: Se senha atual incorreta ou nova senha inválida
        """
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        
        # Verifica senha atual
        if not verify_password(password_data.old_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Senha atual incorreta"
            )
        
        # Valida nova senha
        is_valid, message = validate_password_strength(password_data.new_password)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )
        
        # Atualiza a senha
        self.user_repo.update_password(user_id, password_data.new_password)
        return True
    
    def delete_user(self, user_id: int) -> bool:
        """
        Deleta um usuário.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            True se deletado com sucesso, False se não encontrado
        """
        return self.user_repo.delete(user_id)
    
    def list_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Lista todos os usuários com paginação.
        
        Args:
            skip: Número de registros a pular
            limit: Número máximo de registros
            
        Returns:
            Lista de usuários
        """
        return self.user_repo.get_all(skip, limit)
