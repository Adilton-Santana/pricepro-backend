"""
Router de Usuários

Endpoints relacionados a gestão de usuários:
- GET /users/me - Obter dados do usuário atual
- PUT /users/me - Atualizar dados do usuário atual
- POST /users/me/change-password - Alterar senha
- DELETE /users/me - Deletar conta
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.connection import get_db
from core.dependencies import get_current_user, check_rate_limit
from controllers.user_controller import UserController
from schemas.user import UserResponse, UserUpdate, PasswordChange
from models.user import User

router = APIRouter(
    prefix="/users",
    tags=["Usuários"],
    dependencies=[Depends(check_rate_limit)]  # Rate limiting aplicado a todas as rotas
)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Obter dados do usuário atual",
    description="Retorna as informações do usuário autenticado."
)
def get_current_user_info(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> UserResponse:
    """
    Obtém os dados do usuário atual.
    
    Requer autenticação via Bearer token.
    """
    return UserController.get_current_user(current_user.id, db)


@router.put(
    "/me",
    response_model=UserResponse,
    summary="Atualizar dados do usuário",
    description="Atualiza as informações do usuário autenticado."
)
def update_current_user(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> UserResponse:
    """
    Atualiza os dados do usuário atual.
    
    Campos atualizáveis:
    - full_name
    - email (deve ser único)
    """
    return UserController.update_user(current_user.id, user_data, db)


@router.post(
    "/me/change-password",
    summary="Alterar senha",
    description="Altera a senha do usuário autenticado."
)
def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Altera a senha do usuário.
    
    Requer:
    - Senha atual correta
    - Nova senha forte
    """
    return UserController.change_password(current_user.id, password_data, db)


@router.delete(
    "/me",
    summary="Deletar conta",
    description="Deleta a conta do usuário autenticado."
)
def delete_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Deleta a conta do usuário.
    
    AVISO: Esta ação é irreversível e deletará todos os produtos associados.
    """
    return UserController.delete_account(current_user.id, db)
