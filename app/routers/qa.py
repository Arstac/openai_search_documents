"""
Router para endpoints de Q&A (preguntas y respuestas).
"""
import logging
from typing import List
from fastapi import APIRouter, HTTPException, status

from ..models.schemas import AskRequest, AskResponse
from ..services import openai_service, file_manager
from ..core.config import settings

# Configurar logging
logger = logging.getLogger(__name__)

# Crear router
router = APIRouter(prefix="/qa", tags=["Q&A"])


@router.post(
    "/ask",
    response_model=AskResponse,
    summary="Pregunta sobre archivos específicos",
    description="Envía una pregunta sobre uno o más archivos y obtiene una respuesta del modelo de OpenAI."
)
def ask_question(request: AskRequest):
    """
    Procesar una pregunta sobre archivos.
    
    Args:
        request: Solicitud con la pregunta y IDs de archivos
        
    Returns:
        AskResponse: Respuesta del modelo con información adicional
        
    Raises:
        HTTPException: Si no hay archivos disponibles o ocurre un error
    """
    try:
        # Determinar los IDs de archivos a usar
        file_ids: List[str] = []
        
        if request.file_id:
            file_ids.append(request.file_id)
        
        if request.extra_file_ids:
            file_ids.extend(request.extra_file_ids)
        
        # Si no se especificaron archivos, usar el último subido
        if not file_ids:
            if not file_manager.has_files():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No hay file_id especificado y no hay archivos subidos en esta sesión."
                )
            
            latest_file_id = file_manager.get_latest_file_id()
            if latest_file_id:
                file_ids = [latest_file_id]
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se pudo obtener un archivo válido."
                )
        
        # Validar que tenemos archivos para procesar
        if not file_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Se requiere al menos un archivo para procesar la pregunta."
            )
        
        logger.info(f"Procesando pregunta con {len(file_ids)} archivo(s)")
        
        # Procesar la pregunta
        answer = openai_service.ask_about_files(
            question=request.question,
            file_ids=file_ids
        )
        
        return AskResponse(
            answer=answer,
            used_file_ids=file_ids,
            model=settings.openai_model
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error inesperado procesando pregunta: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor procesando la pregunta"
        )
