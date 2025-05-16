# Dockerfile

# ====================================================================================
# ===== --- Estágio Base ---                                                     =====
# ====================================================================================
# Usar uma imagem base oficial do Python mais enxuta.
FROM python:3.10-slim AS base

# Definir variáveis de ambiente para Python.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Definir o diretório de trabalho raiz para nossa aplicação/serviço.
WORKDIR /service


# ====================================================================================
# ===== --- Estágio de Dependências ---                                          =====
# ====================================================================================
# Usar um estágio separado para instalar dependências pode otimizar o cache do Docker.
FROM base AS dependencies

# Copiar apenas o arquivo de dependências Python.
COPY requirements.txt requirements.txt

# Instalar as dependências Python.
# --no-cache-dir reduz o tamanho da imagem.
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


# ====================================================================================
# ===== --- Estágio de Aplicação Final ---                                       =====
# ====================================================================================
# Começar do estágio base novamente para uma imagem final mais limpa, se necessário,
# ou continuar de 'dependencies' se não houver otimizações de múltiplos estágios complexas.
# Para este projeto, continuar de 'dependencies' é suficiente.
FROM dependencies AS final

# Copiar os arquivos e diretórios do Alembic para o WORKDIR do contêiner.
# Isso permite que os comandos 'alembic' executados dentro do contêiner encontrem sua configuração.
COPY alembic.ini /service/alembic.ini
COPY ./alembic /service/alembic

# Copiar o código da aplicação (tudo dentro da pasta local 'app')
# para um subdiretório 'app' dentro do WORKDIR do contêiner.
# Estrutura resultante no contêiner: /service/app/main.py, /service/app/models.py, etc.
COPY ./app /service/app

# Expor a porta que a aplicação FastAPI (via Uvicorn) estará ouvindo.
EXPOSE 8000

# Comando para executar a aplicação Uvicorn quando o contêiner iniciar.
# - app.main:app : Especifica o módulo 'main' dentro do pacote 'app' e a instância 'app' do FastAPI.
# - --host 0.0.0.0 : Faz o servidor ouvir em todas as interfaces de rede disponíveis.
# - --port 8000 : Porta dentro do contêiner.
# - --reload : Habilita o recarregamento automático em desenvolvimento para mudanças no código.
# - --reload-dir /service/app : Especifica o diretório a ser observado para o reload.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--reload-dir", "/service/app", "--reload-exclude", "/service/alembic", "--reload-exclude", "*.pyc", "--reload-exclude", "*__pycache__*"]
