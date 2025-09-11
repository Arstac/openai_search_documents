"""
Punto de entrada principal para la aplicación Q&A OpenAI.

Este archivo mantiene la compatibilidad con el código original
pero ahora delega toda la funcionalidad a la aplicación modularizada.
"""
from app.main import app

# Para compatibilidad con uvicorn main:app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
