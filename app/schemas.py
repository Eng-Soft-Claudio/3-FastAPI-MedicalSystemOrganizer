# app/schemas.py

# ====================================================================================
# ===== --- Importações ---                                                      =====
# ====================================================================================

import re
from datetime import date
from typing import Annotated, Optional, Type

from pydantic import BaseModel, Field, field_validator
from validate_docbr import CNS, CPF

from .enum import UserRole

# ====================================================================================
# ===== --- Funções Validadoras Auxiliares ---                                   =====
# ====================================================================================


def _validate_and_clean_br_phone(v: Optional[str]) -> Optional[str]:
    """Valida e normaliza número de telefone brasileiro (com DDD), se fornecido."""
    if v is None:
        return None

    cleaned_v = re.sub(r"\D", "", v)
    if len(cleaned_v) == 10:
        if not re.fullmatch(r"\d{2}[2-5]\d{7}", cleaned_v):
            raise ValueError("Telefone fixo inválido. Verifique DDD e número.")
    elif len(cleaned_v) == 11:
        if not re.fullmatch(r"\d{2}9\d{8}", cleaned_v):
            raise ValueError(
                "Telefone celular inválido. Deve começar com 9 após o DDD."
            )
    else:
        raise ValueError(
            "Telefone inválido. Deve conter 10 ou 11 dígitos (DDD + Número)."
        )
    return cleaned_v


# ====================================================================================
# ===== --- Schemas de Endereço ---                                              =====
# ====================================================================================


class EnderecoBase(BaseModel):
    """Schema base para dados de endereço."""

    rua: Annotated[str, Field(json_schema_extra={"example": "Rua das Palmeiras"})]
    numero: Annotated[
        str | None, Field(default=None, json_schema_extra={"example": "123A"})
    ]
    bairro: Annotated[str, Field(json_schema_extra={"example": "Centro"})]
    cidade: Annotated[
        str,
        Field(
            min_length=3, max_length=72, json_schema_extra={"example": "Cidade Exemplo"}
        ),
    ]
    estado: Annotated[
        str, Field(min_length=2, max_length=2, json_schema_extra={"example": "SP"})
    ]
    cep: Annotated[
        str, Field(pattern=r"^\d{5}-\d{3}$", json_schema_extra={"example": "12345-678"})
    ]


class EnderecoCreate(EnderecoBase):
    """Schema para criação de um novo endereço."""

    pass


class Endereco(EnderecoBase):
    """Schema para leitura/retorno de um endereço."""

    id: int

    class Config:
        from_attributes = True


# ====================================================================================
# ===== --- Schemas de Paciente ---                                              =====
# ====================================================================================


class PacienteBase(BaseModel):
    """Schema base para dados de paciente."""

    nome_completo: Annotated[
        str, Field(json_schema_extra={"example": "João Maria da Silva"})
    ]
    data_nascimento: Annotated[date, Field(json_schema_extra={"example": "1990-01-15"})]
    nome_da_mae: Annotated[str, Field(json_schema_extra={"example": "Maria da Silva"})]
    cpf: Annotated[str, Field(json_schema_extra={"example": "12345678900"})]
    cns: Annotated[
        str | None,
        Field(default=None, json_schema_extra={"example": "700000000000000"}),
    ]
    telefone: Annotated[str, Field(json_schema_extra={"example": "11987654321"})]


class PacienteCreate(PacienteBase):
    """Schema para criação de um novo paciente."""

    endereco: EnderecoCreate

    @field_validator("cpf")
    def validar_e_formatar_cpf(cls, v: str) -> str:
        """Valida o CPF."""
        cpf_validator = CPF()
        if not cpf_validator.validate(v):
            raise ValueError("CPF inválido")
        return "".join(filter(str.isdigit, v))

    @field_validator("cns", check_fields=False)
    def validar_cns(cls, v: Optional[str]) -> Optional[str]:
        """Valida o CNS, se fornecido."""
        if v is None:
            return None
        cns_validator = CNS()
        if not cns_validator.validate(v):
            raise ValueError("CNS inválido")
        return "".join(filter(str.isdigit, v))

    @field_validator("telefone")
    @classmethod
    def validar_e_limpar_telefone(cls: Type["PacienteCreate"], v: str) -> str:
        """Valida e normaliza número de telefone (com DDD)."""
        validated_phone = _validate_and_clean_br_phone(v)
        if validated_phone is None:
            raise ValueError(
                "Validador de telefone retornou None para um valor não-None."
            )
        return validated_phone


class PacienteUpdate(BaseModel):
    """Schema para atualização de um paciente."""

    telefone: Annotated[
        str | None, Field(default=None, json_schema_extra={"example": "11912345678"})
    ]

    @field_validator("telefone", check_fields=False)
    @classmethod
    def validar_e_limpar_telefone_update(
        cls: Type["PacienteUpdate"], v: Optional[str]
    ) -> Optional[str]:
        """Valida e normaliza número de telefone (com DDD), se fornecido."""
        return _validate_and_clean_br_phone(v)

    endereco: Annotated[Optional[EnderecoCreate], Field(default=None)]


class Paciente(PacienteBase):
    """Schema para leitura/retorno de um paciente."""

    id: int
    endereco: Endereco
    imagem_documento_url: Annotated[str | None, Field(default=None)]

    class Config:
        from_attributes = True


# ====================================================================================
# ===== --- Schemas de Médico ---                                                =====
# ====================================================================================


class MedicoBase(BaseModel):
    """Schema base para dados de médico."""

    nome: Annotated[str, Field(json_schema_extra={"example": "Dr. Gregory House"})]
    especialidade: Annotated[str, Field(json_schema_extra={"example": "Diagnóstico"})]
    telefone: Annotated[str, Field(json_schema_extra={"example": "11987654321"})]


class MedicoCreate(MedicoBase):
    """Schema para criação de um novo médico."""

    @field_validator("telefone")
    @classmethod
    def validar_e_limpar_telefone(cls: Type["MedicoCreate"], v: str) -> str:
        """Valida e normaliza número de telefone (com DDD)."""
        validated_phone = _validate_and_clean_br_phone(v)
        if validated_phone is None:
            raise ValueError(
                "Validador de telefone retornou None para um valor não-None."
            )
        return validated_phone


class MedicoUpdate(BaseModel):
    """Schema para atualização de um médico."""

    especialidade: Annotated[
        str | None, Field(default=None, json_schema_extra={"example": "Nefrologia"})
    ]
    telefone: Annotated[
        str | None, Field(default=None, json_schema_extra={"example": "21912345678"})
    ]

    @field_validator("telefone", check_fields=False)
    @classmethod
    def validar_telefone_para_atualizacao_medico(
        cls: Type["MedicoUpdate"], v: Optional[str]
    ) -> Optional[str]:
        """Valida e normaliza o telefone na atualização do médico, se fornecido."""
        return _validate_and_clean_br_phone(v)


class Medico(MedicoBase):
    """Schema para leitura/retorno de um médico."""

    id: int

    class Config:
        from_attributes = True


# ====================================================================================
# ===== --- Schemas de Agendamento ---                                           =====
# ====================================================================================


class MedicoParaAgendamento(BaseModel):
    """Schema reduzido do Médico para ser incluído em respostas de Agendamento."""

    id: int
    nome: str
    especialidade: str

    class Config:
        from_attributes = True


class AgendamentoBase(BaseModel):
    """Schema base para dados de agendamento."""

    medico_id: int
    especialidade: Annotated[str, Field(json_schema_extra={"example": "Cardiologia"})]
    data_primeira_consulta: Annotated[
        date, Field(json_schema_extra={"example": "2024-12-31"})
    ]
    data_proxima_consulta: Annotated[
        date | None, Field(default=None, json_schema_extra={"example": "2025-01-31"})
    ]
    valor_consulta: Annotated[float, Field(gt=0, json_schema_extra={"example": 150.75})]
    descricao: Annotated[
        str | None,
        Field(default=None, json_schema_extra={"example": "Consulta de rotina"}),
    ]
    receituario: Annotated[
        str | None,
        Field(default=None, json_schema_extra={"example": "Medicação X, 2x ao dia."}),
    ]


class AgendamentoCreate(AgendamentoBase):
    """Schema para criação de um novo agendamento."""

    paciente_id: int


class AgendamentoUpdate(BaseModel):
    """Schema para atualização de um agendamento."""

    medico_id: Annotated[Optional[int], Field(default=None)]
    especialidade: Annotated[
        str | None, Field(default=None, json_schema_extra={"example": "Clínica Geral"})
    ]
    data_primeira_consulta: Annotated[
        date | None, Field(default=None, json_schema_extra={"example": "2024-11-30"})
    ]
    data_proxima_consulta: Annotated[
        date | None, Field(default=None, json_schema_extra={"example": "2025-02-28"})
    ]
    valor_consulta: Annotated[
        float | None, Field(default=None, gt=0, json_schema_extra={"example": 200.00})
    ]
    descricao: Annotated[
        str | None, Field(default=None, json_schema_extra={"example": "Retorno"})
    ]
    receituario: Annotated[
        str | None,
        Field(default=None, json_schema_extra={"example": "Nova medicação Y."}),
    ]


class Agendamento(AgendamentoBase):
    """Schema para leitura/retorno de um agendamento."""

    id: int
    paciente_id: int
    medico: MedicoParaAgendamento

    class Config:
        from_attributes = True


# ====================================================================================
# ===== --- Schemas de Usuário ---                                               =====
# ====================================================================================
class UserBase(BaseModel):
    """Schema base para dados de usuário."""

    email: Annotated[str, Field(json_schema_extra={"example": "usuario@example.com"})]
    nome_completo: Annotated[
        str, Field(json_schema_extra={"example": "Nome Sobrenome do Usuário"})
    ]
    role: UserRole


class UserCreate(UserBase):
    """Schema para criação de um novo usuário. Recebe a senha em texto plano."""

    password: Annotated[
        str, Field(min_length=8, json_schema_extra={"example": "senhaForte123"})
    ]
    role: UserRole
    medico_id: Annotated[
        int | None,
        Field(default=None, description="ID do Médico se o papel for 'medico'"),
    ] = None


class UserUpdate(BaseModel):
    """Schema para atualização de dados básicos do usuário."""

    email: Annotated[str | None, Field(default=None)]
    nome_completo: Annotated[str | None, Field(default=None)]
    is_active: Annotated[bool | None, Field(default=None)]


class User(UserBase):
    """Schema para leitura/retorno de um usuário (sem a senha)."""

    id: int
    is_active: bool
    is_superuser: bool
    role: UserRole
    medico_id: Optional[int] = None

    class Config:
        from_attributes = True


# ====================================================================================
# ===== --- Schemas de Token ---                                                 =====
# ====================================================================================
class Token(BaseModel):
    """Schema para o token de acesso retornado no login."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema para os dados contidos dentro de um token JWT."""

    user_id: Optional[int] = None
