# Q&A sobre archivos con OpenAI

Una aplicación FastAPI profesional para subir archivos y hacer preguntas sobre su contenido usando la API de OpenAI.

## 🚀 Características

- **Subida de archivos**: Sube documentos (PDF, TXT, DOCX, CSV, JSON) a OpenAI Files API
- **Q&A inteligente**: Haz preguntas sobre el contenido de los archivos usando modelos de OpenAI
- **API RESTful**: Interfaz bien documentada con FastAPI
- **Arquitectura modular**: Código organizado profesionalmente
- **Configuración flexible**: Variables de entorno para fácil configuración
- **Validaciones robustas**: Validación de tipos de archivo y tamaños
- **Logging**: Sistema de logging integrado
- **CORS**: Configuración de CORS para integraciones frontend

## 📁 Estructura del proyecto

```
openai_search_documents/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Aplicación FastAPI principal
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py           # Configuración centralizada
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py          # Modelos Pydantic
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── files.py            # Endpoints de archivos
│   │   ├── qa.py               # Endpoints de Q&A
│   │   └── health.py           # Health checks
│   └── services/
│       ├── __init__.py
│       ├── openai_service.py   # Servicio OpenAI
│       └── file_manager.py     # Gestión de archivos
├── main.py                     # Punto de entrada
├── requirements.txt            # Dependencias
├── .env.example               # Ejemplo de variables de entorno
├── .env                       # Variables de entorno (no subir a git)
└── README.md                  # Este archivo
```

## 🛠️ Instalación

### 1. Clonar el repositorio
```bash
git clone <tu-repositorio>
cd openai_search_documents
```

### 2. Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
```bash
cp .env.example .env
```

Edita el archivo `.env` y configura tu API key de OpenAI:
```env
OPENAI_API_KEY=tu_api_key_de_openai_aqui
OPENAI_MODEL=gpt-4o
```

## 🚀 Uso

### Ejecutar la aplicación
```bash
# Usando uvicorn directamente
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# O usando el script principal
python main.py
```

La aplicación estará disponible en:
- **API**: http://localhost:8000
- **Documentación interactiva**: http://localhost:8000/docs
- **Documentación ReDoc**: http://localhost:8000/redoc

### Endpoints principales

#### 1. Subir archivo
```bash
curl -X POST "http://localhost:8000/files/upload" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@tu_archivo.pdf"
```

#### 2. Hacer una pregunta
```bash
curl -X POST "http://localhost:8000/qa/ask" \
     -H "accept: application/json" \
     -H "Content-Type: application/json" \
     -d '{
       "question": "¿Cuál es el tema principal de este documento?",
       "file_id": "file-abc123"
     }'
```

#### 3. Ver archivos recientes
```bash
curl -X GET "http://localhost:8000/files/recent" \
     -H "accept: application/json"
```

## 📖 Documentación de la API

### Modelos de datos

#### AskRequest
```python
{
  "question": "string",           # Pregunta sobre el archivo
  "file_id": "string",           # ID del archivo específico (opcional)
  "extra_file_ids": ["string"]   # IDs adicionales de archivos (opcional)
}
```

#### UploadResponse
```python
{
  "filename": "string",  # Nombre del archivo subido
  "file_id": "string"    # ID del archivo en OpenAI
}
```

#### AskResponse
```python
{
  "answer": "string",         # Respuesta generada por el modelo
  "used_file_ids": ["string"], # IDs de archivos utilizados
  "model": "string"           # Modelo de OpenAI utilizado
}
```

### Configuración

La aplicación se configura a través de variables de entorno:

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `OPENAI_API_KEY` | API key de OpenAI | **Requerido** |
| `OPENAI_MODEL` | Modelo de OpenAI a usar | `gpt-4o` |
| `DEBUG` | Modo debug | `false` |
| `MAX_FILE_SIZE` | Tamaño máximo de archivo (bytes) | `10485760` (10MB) |
| `ALLOWED_FILE_TYPES` | Tipos de archivo permitidos | Ver config.py |

## 🔒 Tipos de archivo soportados

- **Texto plano**: `.txt`
- **PDF**: `.pdf`
- **Word**: `.doc`, `.docx`
- **CSV**: `.csv`
- **JSON**: `.json`

## 🧪 Testing

```bash
# Ejecutar tests (cuando estén implementados)
pytest

# Con coverage
pytest --cov=app tests/
```

## 🚀 Deployment

### Usando Docker (opcional)
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Variables de entorno para producción
```env
DEBUG=false
OPENAI_API_KEY=tu_api_key_de_produccion
ALLOWED_ORIGINS=["https://tu-dominio.com"]
```

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🔧 Desarrollo

### Estructura de código
- **Separación de responsabilidades**: Cada módulo tiene una responsabilidad específica
- **Configuración centralizada**: Todas las configuraciones en `config.py`
- **Modelos tipados**: Uso de Pydantic para validación de datos
- **Logging**: Sistema de logging estructurado
- **Error handling**: Manejo robusto de errores

### Mejoras futuras
- [ ] Autenticación y autorización
- [ ] Rate limiting
- [ ] Cache de respuestas
- [ ] Base de datos para persistencia
- [ ] Tests automatizados
- [ ] Métricas y monitoring
- [ ] Docker y kubernetes manifests

## 🆘 Soporte

Si encuentras algún problema o tienes preguntas:

1. Revisa la documentación
2. Busca en los issues existentes
3. Crea un nuevo issue con detalles del problema

## 📊 Estado del proyecto

- ✅ API funcional
- ✅ Documentación
- ✅ Estructura modular
- ✅ Configuración por variables de entorno
- ⏳ Tests automatizados
- ⏳ Docker setup
- ⏳ CI/CD pipeline
