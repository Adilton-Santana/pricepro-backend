"""
Arquivo de Configuração Central do PricePro

Contém todas as configurações da aplicação incluindo:
- Configurações do banco de dados PostgreSQL
- Configurações do Redis para cache e rate limiting
- Configurações de segurança e JWT
- Configurações gerais da aplicação
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """
    Classe de configurações da aplicação usando Pydantic BaseSettings.
    As variáveis podem ser sobrescritas por variáveis de ambiente.
    """
    
    # Configurações Gerais
    APP_NAME: str = "PricePro API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "API para precificação inteligente de produtos"
    DEBUG: bool = True
    
    # Configurações do Banco de Dados PostgreSQL
    DATABASE_URL: str = "postgresql://pricepro_user:pricepro_pass@localhost:5432/pricepro_db"
    DATABASE_ECHO: bool = False  # Logs SQL (útil para debug)
    
    # Configurações do Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    REDIS_URL: str = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
    
    # Configurações de Segurança JWT
    SECRET_KEY: str = "your-secret-key-change-this-in-production-min-32-chars"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # Token de acesso expira em 30 minutos
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7  # Token de refresh expira em 7 dias
    
    # Configurações de IA
    ABACUSAI_API_KEY: Optional[str] = None  # API Key para Abacus.AI LLM
    
    # Configurações de Rate Limiting
    RATE_LIMIT_REQUESTS: int = 200  # 200 requisições
    RATE_LIMIT_WINDOW: int = 60  # Por minuto (60 segundos)
    
    # Configurações de Password Reset
    PASSWORD_RESET_TOKEN_EXPIRE_HOURS: int = 1  # Token de recuperação expira em 1 hora
    
    # Configurações de Paginação
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    # Configurações CORS
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Instância global de configurações
settings = Settings()
