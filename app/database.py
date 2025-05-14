# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
# Isso é útil especialmente se rodarmos scripts fora do contexto do Docker Compose
# que não injeta automaticamente o .env (ex: scripts de migração locais)
load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if SQLALCHEMY_DATABASE_URL is None:
    print("AVISO: Variável de ambiente DATABASE_URL não definida!")
    # Poderíamos definir uma URL padrão para SQLite em memória para testes locais
    # SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
    # Ou levantar um erro:
    raise EnvironmentError("DATABASE_URL não está configurada no ambiente ou .env")

# Cria a engine do SQLAlchemy
# O argumento connect_args é específico para SQLite, podemos remover se só usarmos PostgreSQL.
# Para PostgreSQL, não são necessários connect_args por padrão.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
    # Para SQLite apenas: connect_args={"check_same_thread": False}
)

# Cada instância de SessionLocal será uma sessão do banco de dados.
# autocommit=False e autoflush=False são padrões, mas é bom saber.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base será usada para criar cada um dos modelos do banco de dados (tabelas)
Base = declarative_base()

# Função para criar todas as tabelas no banco de dados
def create_db_and_tables():
    Base.metadata.create_all(bind=engine)

# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()