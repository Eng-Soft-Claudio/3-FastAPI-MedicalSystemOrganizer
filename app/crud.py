# app/crud.py

# ====================================================================================
# ===== --- Importações ---                                                      =====
# ====================================================================================

from typing import List, Optional

from sqlalchemy.orm import Session

from . import models, schemas

# ====================================================================================
# ===== --- CRUD de Pacientes (Já implementado anteriormente) ---                =====
# ====================================================================================


def get_paciente_by_id(db: Session, paciente_id: int) -> Optional[models.Paciente]:
    """
    Busca um paciente pelo seu ID no banco de dados.

    Args:
        db: A sessão ativa do banco de dados.
        paciente_id: O ID do paciente a ser recuperado.

    Returns:
        O objeto models.Paciente correspondente ao ID, ou None se não encontrado.
    """
    return db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()


def get_paciente_by_cpf(db: Session, cpf: str) -> Optional[models.Paciente]:
    """
    Busca um paciente pelo seu CPF no banco de dados.

    Args:
        db: A sessão ativa do banco de dados.
        cpf: O CPF do paciente a ser recuperado.

    Returns:
        O objeto models.Paciente correspondente ao CPF, ou None se não encontrado.
    """
    cleaned_cpf = "".join(filter(str.isdigit, cpf))
    if not cleaned_cpf:
        return None
    return db.query(models.Paciente).filter(models.Paciente.cpf == cleaned_cpf).first()


def get_paciente_by_cns(db: Session, cns: str) -> Optional[models.Paciente]:
    """
    Busca um paciente pelo seu CNS no banco de dados.

    Args:
        db: A sessão ativa do banco de dados.
        cns: O CNS do paciente a ser recuperado.

    Returns:
        O objeto models.Paciente correspondente ao CNS, ou None se não encontrado.
    """
    cleaned_cns = "".join(filter(str.isdigit, cns))
    if not cleaned_cns:
        return None
    return db.query(models.Paciente).filter(models.Paciente.cns == cleaned_cns).first()


def get_pacientes(
    db: Session, skip: int = 0, limit: int = 100
) -> List[models.Paciente]:
    """
    Retorna uma lista de pacientes do banco de dados, com opções de paginação.

    Args:
        db: A sessão ativa do banco de dados.
        skip: O número de registros a pular (para paginação).
        limit: O número máximo de registros a retornar.

    Returns:
        Uma lista de objetos models.Paciente.
    """
    return db.query(models.Paciente).offset(skip).limit(limit).all()


def create_paciente(db: Session, paciente: schemas.PacienteCreate) -> models.Paciente:
    """
    Cria um novo paciente e seu respectivo endereço no banco de dados.

    Args:
        db: A sessão ativa do banco de dados.
        paciente: Objeto schemas.PacienteCreate contendo os dados do novo paciente
                  e seu endereço.

    Returns:
        O objeto models.Paciente recém-criado, com seus dados e ID populados.
    """
    existing_paciente_cpf = get_paciente_by_cpf(db, cpf=paciente.cpf)
    if existing_paciente_cpf:
        raise ValueError(f"Paciente com CPF {paciente.cpf} já existe.")

    if paciente.cns:  # Assumindo que cns está em schemas.PacienteCreate
        # Precisaria de get_paciente_by_cns
        # existing_paciente_cns = get_paciente_by_cns(db, cns=paciente.cns)
        # if existing_paciente_cns:
        #     raise ValueError(f"Paciente com CNS {paciente.cns} já existe.")
        pass
    endereco_data = paciente.endereco.model_dump()
    db_endereco = models.Endereco(**endereco_data)
    paciente_data = paciente.model_dump(exclude={"endereco"})
    db_paciente = models.Paciente(**paciente_data)
    db_paciente.endereco = db_endereco
    db.add(db_paciente)
    db.commit()
    db.refresh(db_paciente)
    return db_paciente


def update_paciente(
    db: Session, paciente_id: int, paciente_update: schemas.PacienteUpdate
) -> Optional[models.Paciente]:
    """
    Atualiza os dados de um paciente existente e/ou seu endereço.

    Args:
        db: A sessão ativa do banco de dados.
        paciente_id: O ID do paciente a ser atualizado.
        paciente_update: Objeto com os campos a serem atualizados.
        schemas.PacienteUpdate com os campos a serem atualizados.

    Returns:
        O objeto models.Paciente atualizado, ou None se o paciente não for encontrado.
    """
    db_paciente = get_paciente_by_id(db, paciente_id)
    if not db_paciente:
        return None

    update_data = paciente_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        if key == "endereco" and value is not None:
            if db_paciente.endereco:
                endereco_update_data = value
                for end_key, end_value in endereco_update_data.items():
                    if end_value is not None:
                        setattr(db_paciente.endereco, end_key, end_value)
            else:
                db_paciente.endereco = models.Endereco(**value)
        # Ex: elif key == "telefone" and value is not None:
        #         setattr(db_paciente, key, value)

    db.commit()
    db.refresh(db_paciente)
    return db_paciente


def delete_paciente(db: Session, paciente_id: int) -> Optional[models.Paciente]:
    """
    Remove um paciente (e seu endereço associado devido à cascata) do banco de dados.

    Args:
        db: A sessão ativa do banco de dados.
        paciente_id: O ID do paciente a ser removido.

    Returns:
        O objeto models.Paciente que foi removido, ou None se não encontrado.
    """
    db_paciente = get_paciente_by_id(db, paciente_id)
    if not db_paciente:
        return None
    db.delete(db_paciente)
    db.commit()
    return db_paciente


# ====================================================================================
# ===== --- CRUD de Agendamentos ---                                             =====
# ====================================================================================


def get_agendamento_by_id(
    db: Session, agendamento_id: int
) -> Optional[models.Agendamento]:
    """
    Busca um agendamento pelo seu ID.

    Args:
        db: A sessão ativa do banco de dados.
        agendamento_id: O ID do agendamento.

    Returns:
        O objeto models.Agendamento ou None se não encontrado.
    """
    return (
        db.query(models.Agendamento)
        .filter(models.Agendamento.id == agendamento_id)
        .first()
    )


def get_agendamentos_by_paciente(
    db: Session, paciente_id: int, skip: int = 0, limit: int = 100
) -> List[models.Agendamento]:
    """
    Busca todos os agendamentos de um paciente específico.

    Args:
        db: A sessão ativa do banco de dados.
        paciente_id: O ID do paciente cujos agendamentos são desejados.
        skip: O número de registros a pular.
        limit: O número máximo de registros a retornar.

    Returns:
        Uma lista de objetos models.Agendamento.
    """
    return (
        db.query(models.Agendamento)
        .filter(models.Agendamento.paciente_id == paciente_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_agendamentos_all(
    db: Session, skip: int = 0, limit: int = 100
) -> List[models.Agendamento]:
    """
    Busca todos os agendamentos no sistema, com paginação.

    Args:
        db: A sessão ativa do banco de dados.
        skip: O número de registros a pular.
        limit: O número máximo de registros a retornar.

    Returns:
        Uma lista de objetos models.Agendamento.
    """
    return db.query(models.Agendamento).offset(skip).limit(limit).all()


def create_agendamento(
    db: Session, agendamento: schemas.AgendamentoCreate
) -> models.Agendamento:
    """
    Cria um novo agendamento.

    Args:
        db: A sessão ativa do banco de dados.
        agendamento: Objeto schemas.AgendamentoCreate com os dados do agendamento.

    Returns:
        O objeto models.Agendamento recém-criado.
    """
    db_agendamento = models.Agendamento(**agendamento.model_dump())
    db.add(db_agendamento)
    db.commit()
    db.refresh(db_agendamento)
    return db_agendamento


def update_agendamento(
    db: Session, agendamento_id: int, agendamento_update: schemas.AgendamentoUpdate
) -> Optional[models.Agendamento]:
    """
    Atualiza um agendamento existente.

    Args:
        db: A sessão ativa do banco de dados.
        agendamento_id: O ID do agendamento a ser atualizado.
        agendamento_update: Objeto com os campos a serem atualizados.
        schemas.AgendamentoUpdate com os campos a serem atualizados.

    Returns:
        O objeto models.Agendamento atualizado, ou None se não encontrado.
    """
    db_agendamento = get_agendamento_by_id(db, agendamento_id)
    if not db_agendamento:
        return None

    update_data = agendamento_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if value is not None:
            setattr(db_agendamento, key, value)

    db.commit()
    db.refresh(db_agendamento)
    return db_agendamento


def delete_agendamento(
    db: Session, agendamento_id: int
) -> Optional[models.Agendamento]:
    """
    Remove um agendamento.

    Args:
        db: A sessão ativa do banco de dados.
        agendamento_id: O ID do agendamento a ser removido.

    Returns:
        O objeto models.Agendamento removido, ou None se não encontrado.
    """
    db_agendamento = get_agendamento_by_id(db, agendamento_id)
    if not db_agendamento:
        return None

    db.delete(db_agendamento)
    db.commit()
    return db_agendamento


# ====================================================================================
# ===== --- CRUD de Médicos (Simples) ---                                        =====
# ====================================================================================


def get_medico_by_id(db: Session, medico_id: int) -> Optional[models.Medico]:
    """Busca um médico pelo ID."""
    return db.query(models.Medico).filter(models.Medico.id == medico_id).first()


def get_medico_by_nome(db: Session, nome: str) -> Optional[models.Medico]:
    """Busca um médico pelo nome."""
    return db.query(models.Medico).filter(models.Medico.nome == nome).first()


def get_medicos(db: Session, skip: int = 0, limit: int = 100) -> List[models.Medico]:
    """Retorna uma lista de médicos."""
    return db.query(models.Medico).offset(skip).limit(limit).all()


def create_medico(db: Session, medico: schemas.MedicoCreate) -> models.Medico:
    """Cria um novo médico."""
    db_medico = models.Medico(**medico.model_dump())
    db.add(db_medico)
    db.commit()
    db.refresh(db_medico)
    return db_medico


def update_medico(
    db: Session, medico_id: int, medico_update: schemas.MedicoUpdate
) -> Optional[models.Medico]:
    """Atualiza um médico existente."""
    db_medico = get_medico_by_id(db, medico_id)
    if not db_medico:
        return None
    update_data = medico_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if value is not None:
            setattr(db_medico, key, value)
    db.commit()
    db.refresh(db_medico)
    return db_medico


def delete_medico(db: Session, medico_id: int) -> Optional[models.Medico]:
    """Remove um médico."""
    db_medico = get_medico_by_id(db, medico_id)
    if not db_medico:
        return None
    db.delete(db_medico)
    db.commit()
    return db_medico
