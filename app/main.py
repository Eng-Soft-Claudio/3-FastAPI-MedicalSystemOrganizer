# app/main.py

# ====================================================================================
# ===== --- Importações ---                                                      =====
# ====================================================================================

from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import create_db_and_tables
from .routers import agendamentos, auth, medicos, pacientes

# ====================================================================================
# ===== --- Rotas ---                                                          =====
# ====================================================================================


# --- Lifepan ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


# --- App ---
app = FastAPI(
    title="API de Agendamentos Médicos",
    version="0.1.0",
    description="API para gerenciar agendamentos médicos, pacientes e médicos.",
    lifespan=lifespan,
)

# --- Includes ---
app.include_router(pacientes.router)
app.include_router(agendamentos.router)
app.include_router(medicos.router)
app.include_router(auth.router)


# --- App Get ---
@app.get("/")
async def ler_raiz():
    """
    Endpoint raiz da API.
    """
    return {"mensagem": "Bem-vindo à API de Agendamentos Médicos!"}
