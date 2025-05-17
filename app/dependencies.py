# app/dependencies.py

# ====================================================================================
# ===== --- Importações ---                                                      =====
# ====================================================================================

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from . import crud, models, security
from .database import SessionLocal
from .enums import UserRole


# ====================================================================================
# ===== --- Dependências de Banco de Dados ---                                   =====
# ====================================================================================
def get_db():
    """
    Dependência FastAPI para obter uma sessão do banco de dados.
    Garante que a sessão seja fechada após a requisição.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ====================================================================================
# ===== --- Dependências de Autenticação (Espaço Reservado para o Futuro) ---    =====
# ====================================================================================

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> models.User:
    """
    Decodifica o token JWT, recupera o ID do usuário e busca o usuário no banco.
    Levanta HTTPException se o token for inválido ou o usuário não for encontrado.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        user_id_from_token = security.decode_token_sub(token)
        if user_id_from_token is None:
            raise credentials_exception
        try:
            user_id = int(user_id_from_token)
        except ValueError:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = crud.get_user_by_id(db, user_id=user_id)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[models.User, Depends(get_current_user)]
) -> models.User:
    """
    Obtém o usuário autenticado e verifica se ele está ativo.
    Levanta HTTPException se o usuário estiver inativo.
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Usuário inativo"
        )
    return current_user


async def require_admin_user(
    current_user: Annotated[models.User, Depends(get_current_active_user)]
) -> models.User:
    """
    Verifica se o usuário autenticado e ativo possui o papel de ADMIN.
    Levanta HTTPException (403 Forbidden) caso contrário.
    """
    if not (current_user.role == UserRole.ADMIN and current_user.is_superuser):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: Requer privilégios de administrador.",
        )
    return current_user


async def require_secretaria_user(
    current_user: Annotated[models.User, Depends(get_current_active_user)]
) -> models.User:
    """
    Verifica se o usuário autenticado e ativo possui o papel de SECRETARIA (ou ADMIN).
    Um admin geralmente pode fazer tudo que uma secretária faz.
    """
    if not (current_user.role == UserRole.SECRETARIA or current_user.is_superuser):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: Requer privilégios de Secretária ou Administrador.",
        )
    return current_user


async def require_medico_user(
    current_user: Annotated[models.User, Depends(get_current_active_user)]
) -> models.User:
    """
    Verifica se o usuário autenticado e ativo possui o papel de MEDICO (ou ADMIN).
    Um admin pode fazer tudo que um médico faz em termos de visualização/gerenciamento.
    Além disso, verifica se o usuário médico está vinculado a um medico_id.
    """
    is_admin = current_user.is_superuser and current_user.role == UserRole.ADMIN
    is_medico = current_user.role == UserRole.MEDICO

    if not (is_medico or is_admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: Requer privilégios de Médico ou Administrador.",
        )

    if is_medico and current_user.medico_id is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Configuração inválida: Usuário sem perfil de médico associado.",
        )
    return current_user


async def require_login_ativo(
    current_user: Annotated[models.User, Depends(get_current_active_user)]
) -> models.User:
    """Garante que o usuário está logado e ativo."""
    return current_user
