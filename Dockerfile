# Dockerfile

# ====================================================================================
# ===== --- Estágio Base ---                                                     =====
# ====================================================================================

FROM python:3.10-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /service

# ====================================================================================
# ===== --- Estágio de Dependências ---                                          =====
# ====================================================================================

FROM base AS dependencies

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ====================================================================================
# ===== --- Estágio de Aplicação Final ---                                       =====
# ====================================================================================

FROM dependencies AS final

COPY alembic.ini /service/alembic.ini
COPY ./alembic /service/alembic

COPY ./app /service/app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--reload-dir", "/service/app", "--reload-exclude", "/service/alembic", "--reload-exclude", "*.pyc", "--reload-exclude", "*__pycache__*"]
