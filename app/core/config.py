"""
Configuración central de la aplicación.
"""
import os
from typing import List
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()


class Settings(BaseSettings):
    """Configuración de la aplicación."""
    
    # API Configuration
    app_name: str = "Q&A sobre archivos con OpenAI"
    app_description: str = "Sube un archivo y pregúntale al modelo sobre su contenido"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # OpenAI Configuration
    openai_api_key: str
    openai_model: str = "gpt-4o"
    
    # CORS Configuration
    allowed_origins: List[str] = ["*"]
    allowed_methods: List[str] = ["*"]
    allowed_headers: List[str] = ["*"]
    allow_credentials: bool = True
    
    # File Upload Configuration
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_file_types: List[str] = [
        "text/plain",
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/csv",
        "application/json"
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Instancia global de configuración
settings = Settings()
