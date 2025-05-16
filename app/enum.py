## app/enum.py

# ====================================================================================
# ===== --- Importações ---                                                      =====
# ====================================================================================

import enum

# ====================================================================================
# ===== --- Enums para Modelos ---                                               =====
# ====================================================================================


class UserRole(str, enum.Enum):
    """Define os papéis de usuário no sistema."""

    ADMIN = "admin"
    SECRETARIA = "secretaria"
    MEDICO = "medico"


# class StatusAgendamento(str, enum.Enum):
#     AGENDADO = "agendado"
#     CONFIRMADO = "confirmado"
#     CANCELADO = "cancelado"
#     REALIZADO = "realizado"
