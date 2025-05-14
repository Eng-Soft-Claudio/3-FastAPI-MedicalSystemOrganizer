from pydantic import BaseModel, Field, EmailStr, validator
from datetime import date
from enum import Enum
from typing import Optional # Para campos opcionais antes do Python 3.10

# --- Modelo para Endereço ---
class EnderecoBase(BaseModel):
    rua: str
    numero: str | None = None # Pode não ter número ou ser "S/N"
    bairro: str
    cidade: str
    estado: str = Field(..., min_length=2, max_length=2) # Ex: "SP", "RJ"
    cep: str = Field(..., pattern=r"^\d{5}-\d{3}$") # Ex: "12345-678"

class EnderecoCreate(EnderecoBase):
    pass

class Endereco(EnderecoBase):
    id: int # Supondo que teremos um ID quando for armazenado

    class Config:
        orm_mode = True # Para compatibilidade com ORMs

# --- Modelo para Paciente ---
class PacienteBase(BaseModel):
    nome_completo: str
    data_nascimento: date
    nome_da_mae: str
    cpf: str # A validação específica será adicionada posteriormente
    # imagem_documento_identificacao: str # Por ora, vamos pensar como armazenaremos o path/ID
    endereco: EnderecoCreate # Aninhando o modelo de criação de endereço

class PacienteCreate(PacienteBase):
    # Validação do CPF usando uma biblioteca será adicionada aqui
    # Exemplo (requer 'validate_docbr'):
    # from validate_docbr import CPF
    # @validator('cpf')
    # def validar_cpf(cls, v):
    #     cpf_validator = CPF()
    #     if not cpf_validator.validate(v):
    #         raise ValueError('CPF inválido')
    #     return cpf_validator.mask(v) # Retorna o CPF formatado/validado
    pass

class Paciente(PacienteBase):
    id: int
    # Para imagem_documento_identificacao, podemos ter a URL ou um identificador
    # imagem_documento_url: str | None = None 
    endereco: Endereco # Exibindo o endereço completo com ID

    class Config:
        orm_mode = True

# --- Médicos ---
# Inicialmente, podemos tê-los como um Enum para seleção
class NomeMedico(str, Enum):
    GABRIEL_TOSTA = "Dr. Gabriel Felipe Tosta"
    ISABELLA_URGANDARIN = "Dra. Isabella Urgandarin"

# Futuramente, poderemos ter um modelo de Médico mais completo se precisarmos de CRUD para eles
# class Medico(BaseModel):
#     id: int
#     nome: str
#     especialidade: str
#     # ... outros campos

# --- Modelo para Agendamento ---
class AgendamentoBase(BaseModel):
    # id_paciente: int # Deverá referenciar um paciente existente
    nome_medico: NomeMedico # Ou str, se não usarmos Enum
    especialidade: str # Pode ser inferida do médico ou digitada
    data_primeira_consulta: date
    data_proxima_consulta: Optional[date] = None # Opcional
    valor_consulta: float = Field(..., gt=0) # Maior que zero
    descricao: Optional[str] = None
    receituario: Optional[str] = None

class AgendamentoCreate(AgendamentoBase):
    id_paciente: int # Obrigatório ao criar um agendamento

class Agendamento(AgendamentoBase):
    id: int
    id_paciente: int # Para saber a qual paciente pertence
    # Poderíamos também carregar informações do paciente aqui, se necessário para a resposta

    class Config:
        orm_mode = True