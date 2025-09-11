"""
Aplicación FastAPI principal modularizada.
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .routers import files_router, qa_router, health_router

# Configurar logging
logging.basicConfig(
    level=logging.INFO if not settings.debug else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """
    Crear y configurar la aplicación FastAPI.
    
    Returns:
        FastAPI: Aplicación configurada
    """
    # Crear aplicación FastAPI
    app = FastAPI(
        title=settings.app_name,
        description=settings.app_description,
        version=settings.app_version,
        debug=settings.debug,
    )
    
    # Configurar CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=settings.allow_credentials,
        allow_methods=settings.allowed_methods,
        allow_headers=settings.allowed_headers,
    )
    
    # Incluir routers
    app.include_router(health_router)
    app.include_router(files_router)
    app.include_router(qa_router)
    
    logger.info(f"Aplicación {settings.app_name} v{settings.app_version} creada exitosamente")
    
    return app


# Crear instancia de la aplicación
app = create_app()
