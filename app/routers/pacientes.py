# app/routers/pacientes.py

# ====================================================================================
# ===== --- Importações ---                                                      =====
# ====================================================================================

from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..dependencies import get_db, require_admin_user, require_secretaria_user

# ====================================================================================
# ===== --- Configuração do Router ---                                           =====
# ====================================================================================

router = APIRouter(
    prefix="/pacientes",
    tags=["Pacientes"],
    responses={404: {"description": "Não encontrado"}},
)


# ====================================================================================
# ===== --- Endpoints para Pacientes ---                                         =====
# ====================================================================================


@router.post("/", response_model=schemas.Paciente, status_code=status.HTTP_201_CREATED)
async def criar_novo_paciente(
    paciente: schemas.PacienteCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[models.User, Depends(require_secretaria_user)],
):
    """
    Cria um novo paciente no sistema.

    Permite o cadastro completo de um paciente, incluindo seus dados pessoais
    e informações de endereço. A validação de CPF (se ativada no schema)
    garante a integridade do dado.
    """
    db_paciente_por_cpf = crud.get_paciente_by_cpf(db, cpf=paciente.cpf)
    if db_paciente_por_cpf:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CPF já cadastrado no sistema.",
        )
    if paciente.cns:
        db_paciente_por_cns = crud.get_paciente_by_cns(db, cns=paciente.cns)
        if db_paciente_por_cns:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CNS já cadastrado no sistema.",
            )
    return crud.create_paciente(db=db, paciente=paciente)


@router.get("/", response_model=List[schemas.Paciente])
async def listar_pacientes(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Retorna uma lista de pacientes cadastrados.

    Suporta paginação através dos parâmetros `skip` (pular N registros)
    e `limit` (máximo de M registros por página).
    """
    pacientes = crud.get_pacientes(db, skip=skip, limit=limit)
    return pacientes


@router.get("/{paciente_id}", response_model=schemas.Paciente)
async def obter_paciente_por_id(paciente_id: int, db: Session = Depends(get_db)):
    """
    Obtém os detalhes de um paciente específico pelo seu ID.
    """
    db_paciente = crud.get_paciente_by_id(db, paciente_id=paciente_id)
    if db_paciente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Paciente não encontrado"
        )
    return db_paciente


@router.get("/cpf/{cpf_paciente}", response_model=schemas.Paciente)
async def obter_paciente_por_cpf(cpf_paciente: str, db: Session = Depends(get_db)):
    """
    Obtém os detalhes de um paciente específico pelo seu CPF.
    """
    db_paciente = crud.get_paciente_by_cpf(db, cpf=cpf_paciente)
    if db_paciente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paciente com este CPF não encontrado",
        )
    return db_paciente


@router.get("/cns/{cns_paciente}", response_model=schemas.Paciente)
async def obter_paciente_por_cns(cns_paciente: str, db: Session = Depends(get_db)):
    """
    Obtém os detalhes de um paciente específico pelo seu CNS.
    """
    db_paciente = crud.get_paciente_by_cns(db, cns=cns_paciente)
    if db_paciente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paciente com este CNS não encontrado",
        )
    return db_paciente


@router.put("/{paciente_id}", response_model=schemas.Paciente)
async def atualizar_dados_paciente(
    paciente_id: int,
    paciente_update: schemas.PacienteUpdate,
    db: Session = Depends(get_db),
):
    """
    Atualiza os dados de um paciente existente.

    Permite a atualização de telefone e/ou endereço.
    Apenas os campos fornecidos na requisição serão alterados.
    """
    db_paciente = crud.get_paciente_by_id(db, paciente_id=paciente_id)
    if db_paciente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Paciente não encontrado"
        )

    updated_paciente = crud.update_paciente(
        db=db, paciente_id=paciente_id, paciente_update=paciente_update
    )
    return updated_paciente


@router.delete("/{paciente_id}", response_model=schemas.Paciente)
async def remover_paciente(
    paciente_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_admin: Annotated[models.User, Depends(require_admin_user)],
):
    """
    Remove um paciente do sistema.

    Ao remover um paciente, seu endereço associado também será removido
    devido à configuração de cascata no banco de dados.
    """
    db_paciente = crud.delete_paciente(db, paciente_id=paciente_id)
    if db_paciente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Paciente não encontrado"
        )
    return db_paciente
