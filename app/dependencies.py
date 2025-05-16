# app/dependencies.py

# ====================================================================================
# ===== --- Importações ---                                                      =====
# ====================================================================================
from .database import SessionLocal


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
# Exemplo:
# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from jose import JWTError, jwt
# from . import schemas, models, crud
# from .config import settings # Supondo um arquivo de configuração com SECRET_KEY etc.

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") # ou "/auth/token"

# async def get_current_user(...):
#     pass

# async def get_current_active_user(...):
#     pass
