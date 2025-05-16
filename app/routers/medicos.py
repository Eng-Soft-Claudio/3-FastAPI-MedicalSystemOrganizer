# app/routers/medicos.py

# ====================================================================================
# ===== --- Importações ---                                                      =====
# ====================================================================================
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..dependencies import get_db

# ====================================================================================
# ===== --- Configuração do Router ---                                           =====
# ====================================================================================
router = APIRouter(
    prefix="/medicos",
    tags=["Médicos"],
    responses={404: {"description": "Médico não encontrado"}},
)


# ====================================================================================
# ===== --- Endpoints para Médicos ---                                           =====
# ====================================================================================


@router.post("/", response_model=schemas.Medico, status_code=status.HTTP_201_CREATED)
async def criar_novo_medico(
    medico: schemas.MedicoCreate, db: Session = Depends(get_db)
):
    """
    Cria um novo médico no sistema.

    Verifica se já existe um médico com o mesmo nome antes de criar,
    para evitar duplicatas simples.
    """
    db_medico_existente = crud.get_medico_by_nome(db, nome=medico.nome)
    if db_medico_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um médico cadastrado com este nome.",
        )
    return crud.create_medico(db=db, medico=medico)


@router.get("/", response_model=List[schemas.Medico])
async def listar_medicos(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Retorna uma lista de todos os médicos cadastrados no sistema.
    Suporta paginação.
    """
    medicos = crud.get_medicos(db, skip=skip, limit=limit)
    return medicos


@router.get("/{medico_id}", response_model=schemas.Medico)
async def obter_medico_por_id(medico_id: int, db: Session = Depends(get_db)):
    """
    Obtém os detalhes de um médico específico pelo seu ID.
    """
    db_medico = crud.get_medico_by_id(db, medico_id=medico_id)
    if db_medico is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Médico não encontrado"
        )
    return db_medico


@router.put("/{medico_id}", response_model=schemas.Medico)
async def atualizar_dados_medico(
    medico_id: int,
    medico_update: schemas.MedicoUpdate,
    db: Session = Depends(get_db),
) -> models.Medico:
    """
    Atualiza os dados de um médico existente.
    Permite a atualização parcial dos dados do médico (nome, especialidade, telefone).
    Apenas os campos fornecidos na requisição serão alterados.
    """
    db_medico_existente = crud.get_medico_by_id(db, medico_id=medico_id)
    if db_medico_existente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Médico não encontrado para atualização",
        )
    updated_medico = crud.update_medico(
        db=db, medico_id=medico_id, medico_update=medico_update
    )
    if updated_medico is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Erro ao atualizar médico ou médico não encontrado",
        )
    return updated_medico


@router.delete("/{medico_id}", response_model=schemas.Medico)
async def remover_medico(medico_id: int, db: Session = Depends(get_db)):
    """
    Remove um médico do sistema.

    NOTA: Esta é uma deleção física. Em um sistema real, pode ser preferível
    "inativar" um médico para preservar o histórico de agendamentos.
    Se um médico for removido, deve-se considerar o que acontece com
    seus agendamentos futuros e passados (ex: desassociar, reatribuir, arquivar).
    """
    # Validação adicional: verificar se o médico possui agendamentos ativos
    # Se sim, talvez impedir a deleção ou exigir uma ação confirmatória.
    # Por ora, faremos a deleção direta se ele for encontrado.

    db_medico_removido = crud.delete_medico(db, medico_id=medico_id)
    if db_medico_removido is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Médico não encontrado para remoção",
        )
    return db_medico_removido
