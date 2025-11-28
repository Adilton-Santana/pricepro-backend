"""
Controller de Usuário

Responsável por coordenar as operações de usuários entre routers e services.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Dict

from services.user_service import UserService
from schemas.user import UserResponse, UserUpdate, PasswordChange


class UserController:
    """
    Controller para operações de usuários.
    """
    
    @staticmethod
    def get_current_user(user_id: int, db: Session) -> UserResponse:
        """
        Obtém dados do usuário atual.
        
        Args:
            user_id: ID do usuário autenticado
            db: Sessão do banco de dados
            
        Returns:
            Dados do usuário
            
        Raises:
            HTTPException: Se usuário não encontrado
        """
        user_service = UserService(db)
        user = user_service.get_user(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        
        return UserResponse.from_orm(user)
    
    @staticmethod
    def update_user(user_id: int, user_data: UserUpdate, db: Session) -> UserResponse:
        """
        Atualiza dados do usuário.
        
        Args:
            user_id: ID do usuário autenticado
            user_data: Dados a serem atualizados
            db: Sessão do banco de dados
            
        Returns:
            Dados atualizados do usuário
            
        Raises:
            HTTPException: Se usuário não encontrado
        """
        user_service = UserService(db)
        user = user_service.update_user(user_id, user_data)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        
        return UserResponse.from_orm(user)
    
    @staticmethod
    def change_password(user_id: int, password_data: PasswordChange, db: Session) -> Dict:
        """
        Altera a senha do usuário.
        
        Args:
            user_id: ID do usuário autenticado
            password_data: Senha antiga e nova
            db: Sessão do banco de dados
            
        Returns:
            Mensagem de sucesso
        """
        user_service = UserService(db)
        user_service.change_password(user_id, password_data)
        
        return {"message": "Senha alterada com sucesso"}
    
    @staticmethod
    def delete_account(user_id: int, db: Session) -> Dict:
        """
        Deleta a conta do usuário.
        
        Args:
            user_id: ID do usuário autenticado
            db: Sessão do banco de dados
            
        Returns:
            Mensagem de sucesso
        """
        user_service = UserService(db)
        success = user_service.delete_user(user_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        
        return {"message": "Conta deletada com sucesso"}
