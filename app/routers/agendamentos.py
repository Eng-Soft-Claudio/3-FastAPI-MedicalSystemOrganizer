# app/routers/agendamentos.py

# ====================================================================================
# ===== --- Importações ---                                                      =====
# ====================================================================================
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..dependencies import get_db

# ====================================================================================
# ===== --- Configuração do Router ---                                           =====
# ====================================================================================
router = APIRouter(
    prefix="/agendamentos",
    tags=["Agendamentos"],
    responses={404: {"description": "Agendamento não encontrado"}},
)


# ====================================================================================
# ===== --- Endpoints para Agendamentos ---                                      =====
# ====================================================================================


@router.post(
    "/", response_model=schemas.Agendamento, status_code=status.HTTP_201_CREATED
)
async def criar_novo_agendamento(
    agendamento: schemas.AgendamentoCreate, db: Session = Depends(get_db)
):
    """
    Cria um novo agendamento para um paciente.

    Verifica se o paciente associado ao `paciente_id` existe antes de criar
    o agendamento.
    """
    db_paciente = crud.get_paciente_by_id(db, paciente_id=agendamento.paciente_id)
    if not db_paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Paciente com id {agendamento.paciente_id} não encontrado.",
        )
    # Adicionar outras validações se necessário (ex: disponibilidade do médico)
    return crud.create_agendamento(db=db, agendamento=agendamento)


@router.get("/", response_model=List[schemas.Agendamento])
async def listar_todos_agendamentos(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Retorna uma lista de todos os agendamentos no sistema.
    Suporta paginação.
    """
    agendamentos = crud.get_agendamentos_all(db, skip=skip, limit=limit)
    return agendamentos


@router.get("/paciente/{paciente_id}", response_model=List[schemas.Agendamento])
async def listar_agendamentos_do_paciente(
    paciente_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Retorna uma lista de todos os agendamentos para um paciente específico.
    Suporta paginação.
    """
    db_paciente = crud.get_paciente_by_id(db, paciente_id=paciente_id)
    if not db_paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Paciente com id {paciente_id} não encontrado.",
        )
    agendamentos = crud.get_agendamentos_by_paciente(
        db, paciente_id=paciente_id, skip=skip, limit=limit
    )
    return agendamentos


@router.get("/{agendamento_id}", response_model=schemas.Agendamento)
async def obter_agendamento_por_id(agendamento_id: int, db: Session = Depends(get_db)):
    """
    Obtém os detalhes de um agendamento específico pelo seu ID.
    """
    db_agendamento = crud.get_agendamento_by_id(db, agendamento_id=agendamento_id)
    if db_agendamento is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Agendamento não encontrado"
        )
    return db_agendamento


@router.put("/{agendamento_id}", response_model=schemas.Agendamento)
async def atualizar_dados_agendamento(
    agendamento_id: int,
    agendamento_update: schemas.AgendamentoUpdate,
    db: Session = Depends(get_db),
):
    """
    Atualiza os dados de um agendamento existente.

    Permite a atualização parcial dos dados do agendamento.
    Apenas os campos fornecidos na requisição serão alterados.
    Não permite alterar o paciente_id de um agendamento.
    """
    db_agendamento_existente = crud.get_agendamento_by_id(
        db, agendamento_id=agendamento_id
    )
    if db_agendamento_existente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agendamento não encontrado para atualização",
        )

    updated_agendamento = crud.update_agendamento(
        db=db, agendamento_id=agendamento_id, agendamento_update=agendamento_update
    )
    return updated_agendamento


@router.delete("/{agendamento_id}", response_model=schemas.Agendamento)
async def remover_agendamento(agendamento_id: int, db: Session = Depends(get_db)):
    """
    Remove um agendamento do sistema.
    """
    db_agendamento_removido = crud.delete_agendamento(db, agendamento_id=agendamento_id)
    if db_agendamento_removido is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agendamento não encontrado para remoção",
        )
    return db_agendamento_removido
