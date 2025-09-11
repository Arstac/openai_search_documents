"""
Router para endpoints relacionados con archivos.
"""
import logging
from typing import List
from fastapi import APIRouter, File, UploadFile, HTTPException, status

from ..models.schemas import UploadResponse, FileInfo
from ..services import openai_service, file_manager
from ..core.config import settings

# Configurar logging
logger = logging.getLogger(__name__)

# Crear router
router = APIRouter(prefix="/files", tags=["Archivos"])


@router.post(
    "/upload",
    response_model=UploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Sube un archivo y lo envía a OpenAI Files",
    description="Sube un archivo al sistema y lo almacena en OpenAI Files API para su posterior uso en consultas."
)
async def upload_file(file: UploadFile = File(...)):
    """
    Subir un archivo a OpenAI Files API.
    
    Args:
        file: Archivo a subir
        
    Returns:
        UploadResponse: Información del archivo subido
        
    Raises:
        HTTPException: Si el archivo no es válido o ocurre un error
    """
    # Validar tipo de archivo
    if file.content_type not in settings.allowed_file_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tipo de archivo no permitido. Tipos válidos: {', '.join(settings.allowed_file_types)}"
        )
    
    # Validar tamaño del archivo
    file_content = await file.read()
    if len(file_content) > settings.max_file_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Archivo demasiado grande. Tamaño máximo: {settings.max_file_size / (1024*1024):.1f}MB"
        )
    
    # Validar nombre del archivo
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo debe tener un nombre válido"
        )
    
    try:
        # Subir archivo a OpenAI
        file_id = await openai_service.upload_file(
            file_content=file_content,
            filename=file.filename,
            content_type=file.content_type
        )
        
        # Agregar a la gestión local
        file_manager.add_file(file.filename, file_id)
        
        logger.info(f"Archivo subido exitosamente: {file.filename} -> {file_id}")
        
        return UploadResponse(filename=file.filename, file_id=file_id)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error inesperado subiendo archivo: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.get(
    "/recent",
    response_model=List[FileInfo],
    summary="Lista archivos subidos recientemente",
    description="Obtiene la lista de archivos subidos en esta sesión (almacenados en memoria para demo)."
)
def get_recent_files():
    """
    Obtener la lista de archivos recientes.
    
    Returns:
        List[FileInfo]: Lista de archivos subidos recientemente
    """
    return file_manager.get_recent_files()


@router.delete(
    "/cache",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Limpiar cache de archivos",
    description="Limpia la cache local de archivos (no elimina los archivos de OpenAI)."
)
def clear_file_cache():
    """
    Limpiar la cache de archivos locales.
    
    Note:
        Esto solo limpia la cache local, no elimina los archivos de OpenAI Files API.
    """
    file_manager.clear_files()
    logger.info("Cache de archivos limpiada por solicitud del usuario")
