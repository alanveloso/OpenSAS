from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    """Configurações da aplicação SAS Service"""
    
    # Servidor
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    workers: int = 4
    max_connections: int = 1000
    
    # Banco de dados
    database_url: str = "sqlite:///./sas_service.db"
    
    # Cache
    redis_url: Optional[str] = "redis://localhost:6379"
    cache_ttl: int = 300
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "logs/sas_service.log"
    
    # Performance
    enable_cache: bool = True
    enable_metrics: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Instância global das configurações
settings = Settings() 