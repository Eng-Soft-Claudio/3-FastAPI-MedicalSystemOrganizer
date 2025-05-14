# Usar uma imagem base oficial do Python
FROM python:3.10-slim

# Definir um diretório de trabalho raiz para nosso serviço/aplicação
WORKDIR /service

# Copiar o arquivo de dependências Python primeiro para aproveitar o cache do Docker
COPY requirements.txt requirements.txt

# Instalar as dependências Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar o conteúdo do diretório 'app' local para um subdiretório 'app' dentro do WORKDIR
# Agora teremos: /service/app/__init__.py, /service/app/main.py, etc.
COPY ./app /service/app

# Expor a porta que a aplicação FastAPI (via Uvicorn) estará ouvindo
EXPOSE 8000

# Comando para executar a aplicação quando o contêiner iniciar
# Chamamos 'app.main:app' para que Python reconheça 'app' como um pacote
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--reload-dir", "/service/app"]