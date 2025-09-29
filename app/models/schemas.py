"""
Modelos Pydantic para las requests y responses de la API.
"""
from typing import Optional, List
from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    """Request model para preguntas sobre archivos."""
    question: str = Field(..., description="Pregunta sobre el archivo", min_length=1)
    file_id: Optional[str] = Field(None, description="ID del archivo específico")
    extra_file_ids: Optional[List[str]] = Field(None, description="IDs adicionales de archivos")
    system_prompt: Optional[str] = Field(
        None,
        description="Prompt del sistema personalizado (opcional). Si no se proporciona, se usará el prompt por defecto."
    )

    class Config:
        json_schema_extra = {
            "example": {
                "question": "¿Cuál es el tema principal de este documento?",
                "file_id": "file-abc123",
                "extra_file_ids": ["file-def456"],
                "system_prompt": "Eres un asistente útil que responde de manera concisa."
            }
        }


class UploadResponse(BaseModel):
    """Response model para subida de archivos."""
    filename: str = Field(..., description="Nombre del archivo subido")
    file_id: str = Field(..., description="ID del archivo en OpenAI")
    
    class Config:
        json_schema_extra = {
            "example": {
                "filename": "documento.pdf",
                "file_id": "file-abc123"
            }
        }


class AskResponse(BaseModel):
    """Response model para respuestas de preguntas."""
    answer: str = Field(..., description="Respuesta generada por el modelo")
    used_file_ids: List[str] = Field(..., description="IDs de archivos utilizados")
    model: str = Field(..., description="Modelo de OpenAI utilizado")
    system_prompt_used: str = Field(..., description="Prompt del sistema utilizado")
    
    class Config:
        json_schema_extra = {
            "example": {
                "answer": "El documento trata sobre...",
                "used_file_ids": ["file-abc123"],
                "model": "gpt-4o",
                "system_prompt_used": "Eres un asistente útil que responde de manera concisa."
            }
        }


class FileInfo(BaseModel):
    """Información básica de un archivo."""
    filename: str = Field(..., description="Nombre del archivo")
    file_id: str = Field(..., description="ID del archivo en OpenAI")
    
    class Config:
        json_schema_extra = {
            "example": {
                "filename": "documento.pdf",
                "file_id": "file-abc123"
            }
        }


class HealthResponse(BaseModel):
    """Response model para health check."""
    status: str = Field(..., description="Estado de la aplicación")
    docs: str = Field(..., description="URL de la documentación")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "ok",
                "docs": "/docs"
            }
        }
