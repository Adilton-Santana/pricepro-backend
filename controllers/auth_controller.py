"""
Controller de Autenticação

Responsável por coordenar as operações de autenticação entre routers e services.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Dict

from services.auth_service import AuthService
from services.user_service import UserService
from schemas.user import UserCreate, UserLogin, PasswordResetRequest, PasswordReset
from schemas.auth import LoginResponse, Token, PasswordResetTokenResponse


class AuthController:
    """
    Controller para operações de autenticação.
    """
    
    @staticmethod
    def register(user_data: UserCreate, db: Session) -> LoginResponse:
        """
        Registra um novo usuário e faz login automático.
        
        Args:
            user_data: Dados do usuário
            db: Sessão do banco de dados
            
        Returns:
            Tokens de acesso e refresh + dados do usuário
        """
        user_service = UserService(db)
        auth_service = AuthService(db)
        
        # Cria o usuário
        user = user_service.create_user(user_data)
        
        # Faz login automático
        result = auth_service.login(user.email, user_data.password)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao fazer login automático após registro"
            )
        
        access_token, refresh_token, user = result
        
        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user={
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role.value
            }
        )
    
    @staticmethod
    def login(credentials: UserLogin, db: Session) -> LoginResponse:
        """
        Realiza login de um usuário.
        
        Args:
            credentials: Credenciais de login
            db: Sessão do banco de dados
            
        Returns:
            Tokens de acesso e refresh + dados do usuário
            
        Raises:
            HTTPException: Se credenciais inválidas
        """
        auth_service = AuthService(db)
        result = auth_service.login(credentials.email, credentials.password)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token, refresh_token, user = result
        
        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user={
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role.value
            }
        )
    
    @staticmethod
    def refresh_token(refresh_token: str, db: Session) -> Token:
        """
        Gera novos tokens usando um refresh token.
        
        Args:
            refresh_token: Token de refresh
            db: Sessão do banco de dados
            
        Returns:
            Novos tokens de acesso e refresh
            
        Raises:
            HTTPException: Se refresh token inválido
        """
        auth_service = AuthService(db)
        result = auth_service.refresh_access_token(refresh_token)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token inválido ou expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        new_access_token, new_refresh_token = result
        
        return Token(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer"
        )
    
    @staticmethod
    def logout(refresh_token: str, db: Session) -> Dict:
        """
        Realiza logout invalidando o refresh token.
        
        Args:
            refresh_token: Token de refresh
            db: Sessão do banco de dados
            
        Returns:
            Mensagem de sucesso
        """
        auth_service = AuthService(db)
        auth_service.logout(refresh_token)
        
        return {"message": "Logout realizado com sucesso"}
    
    @staticmethod
    def request_password_reset(request: PasswordResetRequest, db: Session) -> PasswordResetTokenResponse:
        """
        Solicita recuperação de senha.
        
        Args:
            request: Email do usuário
            db: Sessão do banco de dados
            
        Returns:
            Mensagem com token de reset
            
        Raises:
            HTTPException: Se usuário não encontrado
        """
        auth_service = AuthService(db)
        reset_token = auth_service.request_password_reset(request.email)
        
        if not reset_token:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        
        # TODO: Enviar token por email
        # Por enquanto, retorna na resposta para testes
        
        return PasswordResetTokenResponse(
            message="Token de recuperação gerado com sucesso. Em produção, este token seria enviado por email.",
            reset_token=reset_token
        )
    
    @staticmethod
    def reset_password(reset_data: PasswordReset, db: Session) -> Dict:
        """
        Reseta a senha usando um token de recuperação.
        
        Args:
            reset_data: Token e nova senha
            db: Sessão do banco de dados
            
        Returns:
            Mensagem de sucesso
            
        Raises:
            HTTPException: Se token inválido
        """
        auth_service = AuthService(db)
        success = auth_service.reset_password(reset_data.token, reset_data.new_password)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token de recuperação inválido ou expirado"
            )
        
        return {"message": "Senha resetada com sucesso"}
