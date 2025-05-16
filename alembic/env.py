# alembic/env.py

# ====================================================================================
# ===== --- Importações ---                                                      =====
# ====================================================================================

import os
from logging.config import fileConfig

from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool

from alembic import context

load_dotenv()

import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from app.database import Base

# ====================================================================================
# ===== --- Configuração Alembic ---                                             =====
# ====================================================================================

config = context.config  # Objeto de configuração do Alembic

db_url_from_env = os.getenv("DATABASE_URL")
if not db_url_from_env:
    raise ConnectionError(
        "DATABASE_URL não encontrada no ambiente ou no arquivo .env. "
        "Arquivo .env deve estar presente e correto."
        "Verifica se load_dotenv() foi chamado."
    )
config.set_main_option("sqlalchemy.url", db_url_from_env)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# ====================================================================================
# ===== --- Configuração de Migração Offline ---                                 =====
# ====================================================================================


def run_migrations_offline() -> None:
    """Executa migrações em modo 'offline'."""

    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# ====================================================================================
# ===== --- Configuração de Migração Online ---                                  =====
# ====================================================================================


def run_migrations_online() -> None:
    """Executa migrações em modo 'online'."""

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


# ====================================================================================
# ===== --- Execução Principal ---                                               =====
# ====================================================================================

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
