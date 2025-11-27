"""
Router de Autenticação

Endpoints relacionados a autenticação:
- POST /auth/register - Registro de novo usuário
- POST /auth/login - Login
- POST /auth/refresh - Refresh de tokens
- POST /auth/logout - Logout
- POST /auth/password-reset/request - Solicitar recuperação de senha
- POST /auth/password-reset/confirm - Confirmar recuperação de senha
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database.connection import get_db
from controllers.auth_controller import AuthController
from schemas.user import UserCreate, UserLogin, PasswordResetRequest, PasswordReset
from schemas.auth import LoginResponse, Token, RefreshTokenRequest, PasswordResetTokenResponse

router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"],
)


@router.post(
    "/register",
    response_model=LoginResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar novo usuário",
    description="Cria uma nova conta de usuário e faz login automático."
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
) -> LoginResponse:
    """
    Registra um novo usuário e faz login automático.
    
    Validações:
    - Email único
    - Senha forte (mínimo 8 caracteres)
    
    Retorna:
    - access_token: Token JWT para autenticação
    - refresh_token: Token JWT para renovar o access token
    - user: Informações básicas do usuário
    """
    return AuthController.register(user_data, db)


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Login",
    description="Autentica um usuário e retorna tokens de acesso."
)
def login(
    credentials: UserLogin,
    db: Session = Depends(get_db)
) -> LoginResponse:
    """
    Realiza login de um usuário.
    
    Retorna:
    - access_token: Token JWT para autenticação (expira em 30 minutos)
    - refresh_token: Token JWT para renovar o access token (expira em 7 dias)
    - user: Informações básicas do usuário
    """
    return AuthController.login(credentials, db)


@router.post(
    "/refresh",
    response_model=Token,
    summary="Refresh token",
    description="Gera novos tokens usando um refresh token válido."
)
def refresh_token(
    refresh_data: RefreshTokenRequest,
    db: Session = Depends(get_db)
) -> Token:
    """
    Gera novos tokens usando um refresh token.
    
    O refresh token antigo é invalidado e um novo é gerado.
    """
    return AuthController.refresh_token(refresh_data.refresh_token, db)


@router.post(
    "/logout",
    summary="Logout",
    description="Invalida o refresh token do usuário."
)
def logout(
    refresh_data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Realiza logout invalidando o refresh token.
    
    Após o logout, o refresh token não pode mais ser usado.
    O access token continuará válido até expirar (30 minutos).
    """
    return AuthController.logout(refresh_data.refresh_token, db)


@router.post(
    "/password-reset/request",
    response_model=PasswordResetTokenResponse,
    summary="Solicitar recuperação de senha",
    description="Gera um token para recuperação de senha."
)
def request_password_reset(
    request: PasswordResetRequest,
    db: Session = Depends(get_db)
) -> PasswordResetTokenResponse:
    """
    Solicita recuperação de senha.
    
    Em produção, o token seria enviado por email.
    Por enquanto, retorna o token na resposta para testes.
    """
    return AuthController.request_password_reset(request, db)


@router.post(
    "/password-reset/confirm",
    summary="Confirmar recuperação de senha",
    description="Reseta a senha usando o token de recuperação."
)
def reset_password(
    reset_data: PasswordReset,
    db: Session = Depends(get_db)
):
    """
    Reseta a senha usando um token de recuperação.
    
    O token expira em 1 hora.
    """
    return AuthController.reset_password(reset_data, db)
