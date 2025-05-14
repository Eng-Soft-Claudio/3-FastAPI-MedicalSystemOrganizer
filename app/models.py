# app/models.py

# ====================================================================================
# ===== --- Importações ---                                                      =====
# ====================================================================================
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship

from .database import Base
from .schemas import NomeMedico 


# ====================================================================================
# ===== --- Modelos ---                                                          =====
# ====================================================================================

# --- Modelo de endereço ---
class Endereco(Base):
    """
    Modelo da tabela 'enderecos'.
    Armazena os detalhes do endereço associado a um paciente.
    """
    __tablename__ = "enderecos"

    id = Column(Integer, primary_key=True, index=True)
    rua = Column(String, index=True)
    numero = Column(String, nullable=True)
    bairro = Column(String, index=True)
    cidade = Column(String, index=True)
    estado = Column(String(2)) 
    cep = Column(String(9), index=True)

    paciente_id = Column(Integer, ForeignKey("pacientes.id"), unique=True) 
    paciente = relationship("Paciente", back_populates="endereco")

# --- Modelo de paciente ---
class Paciente(Base):
    """
    Modelo da tabela 'pacientes'.
    Representa um paciente no sistema da clínica.
    """
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    nome_completo = Column(String, index=True)
    data_nascimento = Column(Date)
    nome_da_mae = Column(String)
    cpf = Column(String, unique=True, index=True) 
    endereco = relationship("Endereco", back_populates="paciente", uselist=False, cascade="all, delete-orphan")

# --- Modelo de agendamento ---
class Agendamento(Base):
    """
    Modelo da tabela 'agendamentos'.
    Registra os agendamentos de consultas dos pacientes com os médicos.
    """
    __tablename__ = "agendamentos"

    id = Column(Integer, primary_key=True, index=True)
    nome_medico = Column(SAEnum(NomeMedico))
    especialidade = Column(String)
    data_primeira_consulta = Column(Date)
    data_proxima_consulta = Column(Date, nullable=True)
    valor_consulta = Column(Float) 
    descricao = Column(String, nullable=True)
    receituario = Column(String, nullable=True)

    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    paciente = relationship("Paciente")

# --- Modelo de médico ---
class Medico(Base):
    """
    Modelo da tabela 'medicos'.
    Armazenaria informações detalhadas sobre os médicos.
    """
    __tablename__ = "medicos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True)
    especialidade = Column(String)