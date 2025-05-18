# app/main.py

# ====================================================================================
# ===== --- Importações ---                                                      =====
# ====================================================================================

import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from psycopg2 import OperationalError as Psycopg2OperationalError
from sqlalchemy import text
from sqlalchemy.exc import OperationalError as SQLAlchemyOperationalError

from .database import SessionLocal
from .routers import agendamentos, auth, medicos, pacientes

# ====================================================================================
# ===== --- Rotas ---                                                          =====
# ====================================================================================


# --- Lifepan ---
@asynccontextmanager
async def lifespan(app: FastAPI):

    db_ready = False
    max_retries = 15
    retry_interval = 5

    for i in range(max_retries):
        try:
            db_test = SessionLocal()
            db_test.execute(text("SELECT 1"))
            db_test.close()
            db_ready = True
            break
        except (SQLAlchemyOperationalError, Psycopg2OperationalError) as e:
            if i < max_retries - 1:
                time.sleep(retry_interval)
            else:
                raise RuntimeError(
                    "Não foi possível conectar ao banco de dados após as tentativas."
                ) from e
                break

    if db_ready:
        # create_db_and_tables()
        print("Tabelas verificadas/criadas (via create_db_and_tables).")
    else:
        print("AVISO: Não foi possível conectar ao banco de dados.")

    yield
    print("Aplicação encerrando.")


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
@app.get("/", tags=["Default"])
async def ler_raiz():
    """
    Endpoint raiz da API.
    """
    return {
        "mensagem": "Bem-vindo à API de Agendamentos Médicos com PostgreSQL e Docker!"
    }
