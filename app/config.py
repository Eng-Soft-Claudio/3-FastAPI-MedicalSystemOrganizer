# app/config.py

# ====================================================================================
# ===== --- Importações ---                                                      =====
# ====================================================================================
from pydantic_settings import BaseSettings, SettingsConfigDict


# ====================================================================================
# ===== --- Configurações da Aplicação ---                                       =====
# ====================================================================================
class Settings(BaseSettings):
    """
    Configurações globais da aplicação.
    Os valores podem ser sobrescritos por variáveis de ambiente ou por um arquivo .env.
    A prioridade é: Variáveis de Ambiente > Arquivo .env > Valores padrão na classe.
    """

    # Configurações de Segurança JWT
    SECRET_KEY: str = "valor_padrao_inseguro_mude_isso_no_env_ou_no_ambiente"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Nome da Aplicação (Opcional, mas pode ser útil)
    APP_NAME: str = "API de Agendamentos Médicos"
    APP_VERSION: str = "0.1.0"

    # Configuração para Pydantic-Settings
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


# Instância global das configurações
settings = Settings()

# Depuração inicial
print(f"Configurações Carregadas: {settings.model_dump_json(indent=2)}")
