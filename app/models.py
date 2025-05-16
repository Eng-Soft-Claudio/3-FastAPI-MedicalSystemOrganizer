# app/models.py

# ====================================================================================
# ===== --- Importações ---                                                      =====
# ====================================================================================
from decimal import Decimal
from typing import Optional

from sqlalchemy import Boolean
from sqlalchemy import Enum as SAEnum
from sqlalchemy import ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Date as SQLDateType

from .database import Base
from .enum import UserRole
from .schemas import MedicoBase

# ====================================================================================
# ===== --- Modelos ---                                                          =====
# ====================================================================================


class Endereco(Base):
    """
    Modelo da tabela 'enderecos'.
    Armazena os detalhes do endereço associado a um paciente.
    """

    __tablename__ = "enderecos"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    rua: Mapped[str] = mapped_column(String, index=True)
    numero: Mapped[str | None] = mapped_column(String, nullable=True)
    bairro: Mapped[str] = mapped_column(String, index=True)
    cidade: Mapped[str] = mapped_column(String, index=True)
    estado: Mapped[str] = mapped_column(String(2))
    cep: Mapped[str] = mapped_column(String(9), index=True)
    paciente_id: Mapped[int] = mapped_column(ForeignKey("pacientes.id"), unique=True)
    paciente: Mapped["Paciente"] = relationship(back_populates="endereco")


class Paciente(Base):
    """
    Modelo da tabela 'pacientes'.
    Representa um paciente no sistema da clínica.
    """

    __tablename__ = "pacientes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome_completo: Mapped[str] = mapped_column(String, index=True)
    data_nascimento: Mapped[SQLDateType] = mapped_column(SQLDateType)
    nome_da_mae: Mapped[str] = mapped_column(String)
    cpf: Mapped[str] = mapped_column(String, unique=True, index=True)
    cns: Mapped[str | None] = mapped_column(
        String, unique=True, nullable=True, index=True
    )
    telefone: Mapped[str] = mapped_column(String)
    endereco: Mapped[Endereco | None] = relationship(
        back_populates="paciente", uselist=False, cascade="all, delete-orphan"
    )


class Agendamento(Base):
    """
    Modelo da tabela 'agendamentos'.
    Registra os agendamentos de consultas dos pacientes com os médicos.
    """

    __tablename__ = "agendamentos"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    especialidade: Mapped[str] = mapped_column(String)
    data_primeira_consulta: Mapped[SQLDateType] = mapped_column(SQLDateType)
    data_proxima_consulta: Mapped[SQLDateType | None] = mapped_column(
        SQLDateType, nullable=True
    )
    valor_consulta: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2))
    descricao: Mapped[str | None] = mapped_column(String, nullable=True)
    receituario: Mapped[str | None] = mapped_column(String, nullable=True)
    paciente_id: Mapped[int] = mapped_column(ForeignKey("pacientes.id"))
    paciente: Mapped[Paciente] = relationship()
    medico_id: Mapped[int] = mapped_column(ForeignKey("medicos.id"))
    medico: Mapped[MedicoBase] = relationship()


class Medico(Base):
    """
    Modelo da tabela 'medicos'.
    Armazenaria informações detalhadas sobre os médicos.
    """

    __tablename__ = "medicos"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String, unique=True, index=True)
    especialidade: Mapped[str] = mapped_column(String)
    telefone: Mapped[str] = mapped_column(String)


class User(Base):
    """Modelo da tabela 'users'."""

    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    nome_completo: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[UserRole] = mapped_column(
        SAEnum(UserRole, name="user_role_enum", create_type=False), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    medico_id: Mapped[int | None] = mapped_column(
        ForeignKey("medicos.id"), nullable=True, unique=True
    )
    medico_profile: Mapped[Optional[Medico]] = relationship(
        back_populates="user_account"
    )
