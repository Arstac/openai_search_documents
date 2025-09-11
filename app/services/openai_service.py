"""
Servicio para interactuar con OpenAI API.
"""
import logging
from typing import List, Dict
from openai import OpenAI
from fastapi import HTTPException

from ..core.config import settings

# Configurar logging
logger = logging.getLogger(__name__)


class OpenAIService:
    """Servicio para interacciones con OpenAI API."""
    
    def __init__(self):
        """Inicializar el cliente de OpenAI."""
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
    
    async def upload_file(self, file_content: bytes, filename: str, content_type: str) -> str:
        """
        Subir archivo a OpenAI Files API.
        
        Args:
            file_content: Contenido del archivo en bytes
            filename: Nombre del archivo
            content_type: Tipo de contenido MIME
            
        Returns:
            str: ID del archivo subido
            
        Raises:
            HTTPException: Si ocurre un error al subir el archivo
        """
        try:
            logger.info(f"Subiendo archivo: {filename}")
            
            uploaded = self.client.files.create(
                file=(filename, file_content, content_type or "application/octet-stream"),
                purpose="assistants"
            )
            
            logger.info(f"Archivo subido exitosamente. ID: {uploaded.id}")
            return uploaded.id
            
        except Exception as e:
            logger.error(f"Error subiendo archivo {filename}: {str(e)}")
            raise HTTPException(
                status_code=500, 
                detail=f"Error subiendo archivo: {str(e)}"
            )
    
    def ask_about_files(self, question: str, file_ids: List[str]) -> str:
        """
        Hacer una pregunta sobre archivos usando Responses API.
        
        Args:
            question: Pregunta del usuario
            file_ids: Lista de IDs de archivos
            
        Returns:
            str: Respuesta del modelo
            
        Raises:
            HTTPException: Si ocurre un error al procesar la pregunta
        """
        try:
            logger.info(f"Procesando pregunta con {len(file_ids)} archivo(s)")
            
            # Construir el contenido del usuario
            user_content = [{"type": "input_text", "text": question}]
            for file_id in file_ids:
                user_content.append({"type": "input_file", "file_id": file_id})
            
            # Llamada a Responses API
            response = self.client.responses.create(
                model=self.model,
                input=[
                    {
                        "role": "user",
                        "content": user_content
                    }
                ]
            )
            
            # Extraer el texto de respuesta
            out_text_parts = []
            if response.output and hasattr(response.output, "content"):
                for content in response.output.content:
                    if content.get("type") == "output_text":
                        out_text_parts.append(content.get("text", ""))
            
            answer = "\n".join(out_text_parts).strip()
            if not answer:
                answer = str(response)
            
            logger.info("Pregunta procesada exitosamente")
            return answer
            
        except Exception as e:
            logger.error(f"Error procesando pregunta: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error en procesamiento: {str(e)}"
            )


# Instancia global del servicio
openai_service = OpenAIService()
