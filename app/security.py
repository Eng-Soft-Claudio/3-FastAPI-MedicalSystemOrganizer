# app/security.py

# ====================================================================================
# ===== --- Importações ---                                                      =====
# ====================================================================================

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from .config import settings

# ====================================================================================
# ===== --- Configuração de Hashing de Senha ---                                 =====
# ====================================================================================

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ====================================================================================
# ===== --- Funções de Senha ---                                                 =====
# ====================================================================================


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha em texto plano corresponde à senha com hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Gera o hash de uma senha em texto plano."""
    return pwd_context.hash(password)


# ====================================================================================
# ===== --- Funções de Token JWT ---                                             =====
# ====================================================================================


def create_access_token(
    data: Dict[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """
    Cria um novo token de acesso JWT.

    Args:
        data: Dicionário com os dados a serem incluídos no payload do token (ex: 'sub').
        expires_delta: Tempo opcional para a expiração do token. Se None, usa o padrão.

    Returns:
        O token JWT codificado como string.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def decode_token_sub(
    token: str,
) -> Optional[Any]:  # Retorna Any, pois 'sub' pode ser int (id) ou str (email)
    """
    Decodifica um token JWT e retorna o 'subject' (sub) ou None se inválido/expirado.
    Usado para obter o identificador do usuário do token.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        # 'sub' é o campo padrão para o identificador do sujeito (ex: user_id ou email)
        subject: Any = payload.get("sub")
        if subject is None:
            return None  # ou levantar uma exceção de token inválido
        return subject
    except JWTError:
        return None  # ou levantar uma exceção de token inválido
