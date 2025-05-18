#!/bin/sh

set -e

    if [ "$1" = 'uvicorn' ]; then

        echo "INFO: Aguardando PostgreSQL..."

        echo "INFO: PostgreSQL iniciado"

        echo "INFO: Aplicando migrações Alembic..."

        alembic upgrade head

        echo "INFO: Iniciando Uvicorn..."

        exec "$@"

    fi

    echo "INFO: Executando comando CLI: python -m app.cli $@"

    exec python -m app.cli "$@"
