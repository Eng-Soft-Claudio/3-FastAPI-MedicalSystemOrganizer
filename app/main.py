# app/main.py
from fastapi import FastAPI
from .database import engine, create_db_and_tables # Importe a função e engine
from . import models # Importe os modelos para que o create_all os conheça
#models.Base.metadata.create_all(bind=engine) # Movido para uma função de evento startup

# Importe seus routers aqui quando os tiver
# from .routers import pacientes, agendamentos

# Função que será executada na inicialização da aplicação
async def lifespan(app: FastAPI):
    print("Aplicação iniciando... Criando tabelas do banco de dados se não existirem.")
    # Ao importar 'models' acima, o Python executa models.py,
    # e as classes modelo (Paciente, Endereco, etc.) são definidas
    # e se registram com a 'Base' de database.py.
    # Assim, quando create_db_and_tables() é chamada, Base.metadata
    # contém as informações das tabelas.
    create_db_and_tables()
    print("Tabelas verificadas/criadas.")
    yield
    print("Aplicação encerrando.")

app = FastAPI(
    title="API de Agendamentos Médicos", # Vem do .env ou direto aqui
    version="0.1.0", # Vem do .env ou direto aqui
    description="API para gerenciar agendamentos médicos, pacientes e médicos.",
    lifespan=lifespan # Adiciona o gerenciador de ciclo de vida
)

# Inclua os routers aqui
# app.include_router(pacientes.router)
# app.include_router(agendamentos.router)


@app.get("/")
async def ler_raiz():
    return {"mensagem": "Bem-vindo à API de Agendamentos Médicos com PostgreSQL e Docker!"}

# O endpoint /items/{item_id} era um exemplo, podemos removê-lo ou mantê-lo por enquanto.
# @app.get("/items/{item_id}")
# async def ler_item(item_id: int, q: str | None = None):
#     response_data = {"item_id": item_id}
#     if q:
#         response_data["q"] = q
#     return response_data