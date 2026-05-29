from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Configurações da aplicação CAD."""
    
    # Informações da Aplicação
    app_name: str = "CAD - Corretor Acadêmico Digital"
    app_version: str = "0.1.0"
    debug: bool = True
    
    # Banco de Dados
    database_url: str = "sqlite:///./cad.db"
    
    # Segurança - JWT
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS
    allowed_origins: List[str] = ["http://localhost:3000", "http://localhost:8501"]
    

    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
