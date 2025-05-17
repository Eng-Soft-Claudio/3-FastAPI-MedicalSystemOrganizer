# app/routers/auth.py

# ====================================================================================
# ===== --- Importações ---                                                      =====
# ====================================================================================
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import crud, models, schemas, security
from ..config import settings
from ..dependencies import get_db, require_admin_user
from ..enums import UserRole

# ====================================================================================
# ===== --- Configuração do Router ---                                           =====
# ====================================================================================
router = APIRouter(
    tags=["Autenticação e Usuários"],  # Tag geral para estes endpoints
)


# ====================================================================================
# ===== --- Endpoint de Login (Obter Token) ---                                  =====
# ====================================================================================
@router.post("/auth/token", response_model=schemas.Token)
async def login_para_obter_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    """
    Fornece um token de acesso JWT após autenticar o usuário com email e senha.
    O corpo da requisição deve ser form-data com 'username' e 'password'.
    """
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Usuário inativo"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# ====================================================================================
# ===== --- Endpoint de Criação de Usuário ---                                   =====
# ====================================================================================


@router.post(
    "/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED
)
async def criar_novo_usuario_sistema(
    user_in: schemas.UserCreate,
    db: Annotated[Session, Depends(get_db)],
    _current_admin: models.User = Depends(require_admin_user),
) -> models.User:
    """
    Cria um novo usuário no sistema (Admin, Secretária, Médico).
    **ACESSO RESTRITO A ADMINISTRADORES.**
    """
    db_user_by_email = crud.get_user_by_email(db, email=user_in.email)
    if db_user_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Um usuário com este email já existe.",
        )

    if user_in.role == UserRole.MEDICO:
        if user_in.medico_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Para usuários com papel 'medico', 'medico_id' é obrigatório.",
            )
        db_medico = crud.get_medico_by_id(db, medico_id=user_in.medico_id)
        if not db_medico:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Médico com id {user_in.medico_id} não encontrado.",
            )
    elif user_in.medico_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O 'medico_id' só é aplicável para usuários com papel 'medico'.",
        )

    user_create_data = user_in.model_copy(deep=True)

    if user_in.role == UserRole.ADMIN:
        user_create_data.is_superuser = True
    else:
        user_create_data.is_superuser = False

    new_user = crud.create_user(db=db, user=user_create_data)

    return new_user
