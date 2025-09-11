#!/usr/bin/env python3
"""
Script de desarrollo para ejecutar la aplicación localmente.
"""
import os
import sys
import subprocess
from pathlib import Path

def check_env_file():
    """Verificar que existe el archivo .env"""
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ No se encontró el archivo .env")
        print("💡 Copia .env.example a .env y configura tu OPENAI_API_KEY")
        return False
    return True

def check_dependencies():
    """Verificar que las dependencias están instaladas"""
    try:
        import fastapi
        import openai
        import uvicorn
        print("✅ Dependencias verificadas")
        return True
    except ImportError as e:
        print(f"❌ Dependencias faltantes: {e}")
        print("💡 Ejecuta: pip install -r requirements.txt")
        return False

def run_app():
    """Ejecutar la aplicación"""
    print("🚀 Iniciando aplicación...")
    print("📖 Documentación disponible en: http://localhost:8000/docs")
    print("🔄 Presiona Ctrl+C para detener")
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\n👋 Aplicación detenida")

def main():
    """Función principal"""
    print("🔧 Verificando entorno de desarrollo...")
    
    if not check_env_file():
        return 1
    
    if not check_dependencies():
        return 1
    
    run_app()
    return 0

if __name__ == "__main__":
    sys.exit(main())
