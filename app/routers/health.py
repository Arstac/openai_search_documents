"""
Router para endpoints de health check y información general.
"""
from fastapi import APIRouter

from ..models.schemas import HealthResponse
from ..core.config import settings

# Crear router
router = APIRouter(tags=["Health"])


@router.get(
    "/",
    response_model=HealthResponse,
    include_in_schema=False,
    summary="Health check",
    description="Endpoint básico para verificar que la aplicación esté funcionando."
)
def root():
    """
    Health check de la aplicación.
    
    Returns:
        HealthResponse: Estado de la aplicación y enlace a documentación
    """
    return HealthResponse(status="ok", docs="/docs")


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check detallado",
    description="Endpoint para verificar el estado de la aplicación."
)
def health_check():
    """
    Health check detallado de la aplicación.
    
    Returns:
        HealthResponse: Estado de la aplicación y enlace a documentación
    """
    return HealthResponse(status="healthy", docs="/docs")


@router.get(
    "/info",
    summary="Información de la aplicación",
    description="Obtiene información básica sobre la aplicación."
)
def app_info():
    """
    Información básica de la aplicación.
    
    Returns:
        dict: Información sobre la aplicación
    """
    return {
        "name": settings.app_name,
        "description": settings.app_description,
        "version": settings.app_version,
        "openai_model": settings.openai_model,
        "docs": "/docs",
        "redoc": "/redoc"
    }
