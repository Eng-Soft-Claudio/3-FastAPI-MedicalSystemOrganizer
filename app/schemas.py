# app/schemas.py

# ====================================================================================
# ===== --- Importações ---                                                      =====
# ====================================================================================
from pydantic import BaseModel # etc.
from enum import Enum

# ====================================================================================
# ===== --- Schemas ---                                                          =====
# ====================================================================================

# --- Schemas de medico ---
class NomeMedico(str, Enum):
    GABRIEL_TOSTA = "Dr. Gabriel Felipe Tosta"
    ISABELLA_URGANDARIN = "Dra. Isabella Urgandarin"

# ... outros schemas ...