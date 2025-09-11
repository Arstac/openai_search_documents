"""
Inicialización del módulo routers.
"""
from .files import router as files_router
from .qa import router as qa_router
from .health import router as health_router

__all__ = [
    "files_router",
    "qa_router", 
    "health_router"
]
