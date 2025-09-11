"""
Servicio para gestión de archivos en memoria.
"""
import logging
from typing import Dict, List, Optional

from ..models.schemas import FileInfo

# Configurar logging
logger = logging.getLogger(__name__)


class FileManagerService:
    """Servicio para gestionar archivos en memoria (demo)."""
    
    def __init__(self):
        """Inicializar el gestor de archivos."""
        self._recent_files: Dict[str, str] = {}  # filename -> file_id
    
    def add_file(self, filename: str, file_id: str) -> None:
        """
        Agregar un archivo a la lista de archivos recientes.
        
        Args:
            filename: Nombre del archivo
            file_id: ID del archivo en OpenAI
        """
        self._recent_files[filename] = file_id
        logger.info(f"Archivo agregado a la cache: {filename} -> {file_id}")
    
    def get_recent_files(self) -> List[FileInfo]:
        """
        Obtener la lista de archivos recientes.
        
        Returns:
            List[FileInfo]: Lista de información de archivos
        """
        return [
            FileInfo(filename=filename, file_id=file_id)
            for filename, file_id in self._recent_files.items()
        ]
    
    def get_file_id(self, filename: str) -> Optional[str]:
        """
        Obtener el ID de un archivo por su nombre.
        
        Args:
            filename: Nombre del archivo
            
        Returns:
            Optional[str]: ID del archivo o None si no existe
        """
        return self._recent_files.get(filename)
    
    def get_latest_file_id(self) -> Optional[str]:
        """
        Obtener el ID del último archivo subido.
        
        Returns:
            Optional[str]: ID del último archivo o None si no hay archivos
        """
        if not self._recent_files:
            return None
        return list(self._recent_files.values())[-1]
    
    def clear_files(self) -> None:
        """Limpiar la lista de archivos recientes."""
        self._recent_files.clear()
        logger.info("Cache de archivos limpiada")
    
    def has_files(self) -> bool:
        """
        Verificar si hay archivos en la cache.
        
        Returns:
            bool: True si hay archivos, False en caso contrario
        """
        return len(self._recent_files) > 0
    
    def get_file_count(self) -> int:
        """
        Obtener el número de archivos en la cache.
        
        Returns:
            int: Número de archivos
        """
        return len(self._recent_files)


# Instancia global del gestor de archivos
file_manager = FileManagerService()
