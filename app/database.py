# app/database.py

# ====================================================================================
# ===== --- Importações ---                                                      =====
# ====================================================================================
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# ====================================================================================
# ===== --- Configuração Inicial ---                                            =====
# ====================================================================================

# Carrega variáveis de Ambiente
load_dotenv()

# Carrega a URL de SQLAlchemy
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if SQLALCHEMY_DATABASE_URL is None:
    raise EnvironmentError("DATABASE_URL não está configurada no ambiente ou .env")

# Cria a engine do SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Cria a instância de SessionLocal, que será uma sessão do banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ====================================================================================
# ===== --- Base Declarativa ---                                                 =====
# ====================================================================================


# Base será usada para criar cada um dos modelos do banco de dados (tabelas)
class Base(DeclarativeBase):
    """Classe base para todos os modelos ORM SQLAlchemy."""

    pass


# ====================================================================================
# ===== --- Funções Utilitárias de Banco de Dados ---                            =====
# ====================================================================================


# Função para criar todas as tabelas no banco de dados
def create_db_and_tables():
    """
    Cria todas as tabelas no banco de dados definidas pelos modelos que herdam de Base.
    Esta função deve ser chamada na inicialização da aplicação.
    """
    Base.metadata.create_all(bind=engine)
