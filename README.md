# 🏥 FastAPI Medical System Organizer
<p align:justify>
Sistema de Gerenciamento Médico desenvolvido com FastAPI, visando otimizar o controle de pacientes, médicos e consultas em ambientes clínicos e hospitalares.  
</p>

--- 

## 📌 Visão Geral

Este projeto oferece uma API RESTful robusta para gerenciamento de entidades médicas, incluindo:

    Pacientes: Cadastro, atualização, listagem e exclusão.

    Médicos: Gerenciamento completo de profissionais de saúde.

    Consultas: Agendamento, atualização e cancelamento de consultas médicas.
<p align:justify>
A arquitetura é modular, utilizando padrões como Repository Pattern e Service Layer, promovendo escalabilidade e manutenção facilitada.
</p>

---

## 🧱 Estrutura do Projeto

```bash
FastAPI-MedicalSystemOrganizer/
.
├── .env (não versionado / dados sensíveis)
│  
├── alembic
│   ├── env.py
│   ├── __pycache__
│   ├── README
│   ├── script.py.mako
│   └── versions
│       └── fe71d1277bc1_add_users_table_and_update_fks.py
├── alembic.ini
├── app
│   ├── config.py
│   ├── crud.py
│   ├── database.py
│   ├── dependencies.py
│   ├── enums.py
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── __pycache__
│   ├── routers
│   │   ├── agendamentos.py
│   │   ├── auth.py
│   │   ├── __init__.py
│   │   ├── medicos.py
│   │   ├── pacientes.py
│   │   └── __pycache__
│   ├── schemas.py
│   └── security.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── typings
    └── validate_docbr
        ├── BaseDoc.pyi
        ├── CNS.pyi
        ├── CPF.pyi
        └── __init__.pyi

```


app/models/: Definições das entidades do banco de dados utilizando SQLAlchemy.

app/schemas/: Esquemas de validação e serialização com Pydantic.

app/services/: Lógica de negócios encapsulada em serviços.

app/api/routes/: Endpoints organizados por recurso.

typings/validate_docbr/: Validação de documentos brasileiros (e.g., CPF).

---

## 🚀 Tecnologias Utilizadas

    FastAPI: Framework web moderno e de alto desempenho.

    SQLAlchemy: ORM para interação com o banco de dados.

    Alembic: Gerenciamento de migrações do banco de dados.

    Pydantic: Validação de dados baseada em modelos.

    Docker & Docker Compose: Containerização e orquestração de serviços.

    validate-docbr: Validação de documentos brasileiros como CPF.

---

## ⚙️ Configuração e Execução

Pré-requisitos  

```bash
Docker instalado.  
Docker Compose instalado.
```

Clonar o repositório:

```bash
git clone https://github.com/Eng-Soft-Claudio/FastAPI-MedicalSystemOrganizer.git
cd FastAPI-MedicalSystemOrganizer
```

Copie o arquivo .env.example para .env e ajuste conforme necessário.  
    
```bash
cp .env.example .env
```
    
Construir e iniciar os containers:  
    
```bash
docker-compose up --build
```

Acessar a aplicação:  
     
```bash
API: http://localhost:8000
Documentação Swagger: http://localhost:8000/docs  
Documentação ReDoc: http://localhost:8000/redoc
```

---

## 🧪 Testes

Será implementado a integração de testes unitários e de integração utilizando framework pytest.

---

## 📄 Licença

Copyright 2025 Cláudio de Lima Tosta
<p align="justify">
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
</p>
<p align="justify">
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
</p>
<p align="justify">
THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
</p>

---
