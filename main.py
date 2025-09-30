"""
Merkadit API - Caso 1
API REST para gestion de mercados gastronómicos y de comercios

Punto de entrada principal de la aplicacion FastAPI
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Creamos la aplicación FastAPI
app = FastAPI(
    title="Merkadit API - Caso 1",
    description="""
    API REST para gestión de mercados gastronómicos y comercios.
    
    ## Funcionalidades Principales
    
    * **Ventas**: Registro de ventas, reportes y consultas
    * **Liquidaciones**: Liquidación mensual de comercios y consultas históricas
    * **Stored Procedures**: Integración con registerSale y settleCommerce
    
    ## Arquitectura
    
    La API está estructurada en 4 capas:
    - **Handler Layer**: Endpoints FastAPI (este nivel)
    - **Controller Layer**: Orquestación de lógica de negocio
    - **Service Layer**: Lógica de negocio compleja
    - **Repository Layer**: Acceso a datos y stored procedures
    
    ---
    **Universidad**: TEC  
    **Curso**: Bases de Datos I  
    **Proyecto**: Caso 1 - Merkadit
    **Autor 1**: Christopher Daniel Vargas Villalta, 2024108443
    **Autor 2**: Dylan Chacon Berrocal, 2024107691
    """,
    version="1.0.0",
    contact={
        "name": "Equipo Merkadit",
        "email": "soporte@merkadit.com"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    }
)

# Configurar CORS esto permite peticiones desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware para logging de requests
@app.middleware("http")

#Middleware para registrar todas las peticiones HTTP
async def log_requests(request: Request, call_next):
    
    start_time = datetime.now()
    
    # Log de la peticion entrante
    logger.info(f" {request.method} {request.url.path}")
    
    # Procesar la peticion
    response = await call_next(request)
    
    # Calcular tiempo de procesamiento
    process_time = (datetime.now() - start_time).total_seconds()
    
    # Log de la respuesta
    logger.info(f" {request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.3f}s")
    
    # Agregar header con tiempo de procesamiento
    response.headers["X-Process-Time"] = str(process_time)
    
    return response

# Exception handler global
@app.exception_handler(Exception)

#Maneja excepciones no capturadas 
async def global_exception_handler(request: Request, exc: Exception):
    
    logger.error(f"Error no manejado: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Error interno del servidor",
            "error": str(exc),
            "timestamp": datetime.now().isoformat()
        }
    )

# ============================================================================
# IMPORTAR Y REGISTRAR ROUTERS (Handlers)
# ============================================================================

from app.handlers import sale_handler

# Registrar router de ventas
app.include_router(sale_handler.router)

# TODO: Descomentar cuando crees settlement_handler
# from app.handlers import settlement_handler
# app.include_router(settlement_handler.router)

# ============================================================================
# ENDPOINTS BÁSICOS
# ============================================================================

@app.get(
    "/",
    tags=["Info"],
    summary="Endpoint raiz",
    description="Retorna información básica de la API y enlaces a documentacion"
)
async def read_root():
    """
    Endpoint raiz de la API.
    Retorna información general y enlaces útiles.
    """
    return {
        "message": " Merkadit API funcionando correctamente",
        "version": "1.0.0",
        "proyecto": "Caso 1 - Bases de Datos I",
        "universidad": "TEC",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "sales": "/api/sales",
            "settlements": "/api/settlements",
            "health": "/health",
            "docs": "/docs",
            "redoc": "/redoc"
        },
        "stored_procedures": [
            "registerSale - Registrar venta completa",
            "settleCommerce - Liquidar comercio mensualmente"
        ]
    }

@app.get(
    "/health",
    tags=["Health"],
    summary="Health check",
    description="Verifica el estado de la API y la conexión a la base de datos"
)
async def health_check():
    """
    Endpoint de health check.
    Verifica:
    - Estado de la API
    - Conexión a la base de datos MySQL
    - Stored procedures disponibles
    """
    from app.config.database import db_config
    
    # Test de conexión a BD
    db_status = "connected" if db_config.test_connection() else "disconnected"
    
    # Obtener informacion de la BD si esta conectada
    db_info = {}
    if db_status == "connected":
        try:
            info = db_config.get_database_info()
            db_info = {
                "database": info.get('current_database'),
                "tables_count": info.get('tables_count'),
                "mysql_version": info.get('mysql_version')
            }
        except Exception as e:
            logger.error(f"Error obteniendo info de BD: {str(e)}")
            db_info = {"error": "No se pudo obtener información de la BD"}
    
    return {
        "status": "healthy" if db_status == "connected" else "unhealthy",
        "api_version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "database": {
            "status": db_status,
            **db_info
        },
        "stored_procedures": {
            "registerSale": {
                "status": "available",
                "description": "Registra una venta completa con validaciones"
            },
            "settleCommerce": {
                "status": "available",
                "description": "Liquida un comercio para el mes actual"
            }
        },
        "layers": {
            "handlers": "FastAPI endpoints (API routes)",
            "controllers": "Business logic orchestration",
            "services": "Complex business logic",
            "repositories": "Data access and stored procedures"
        }
    }

@app.get(
    "/api/info",
    tags=["Info"],
    summary="Información detallada de la API",
    description="Retorna información técnica sobre la arquitectura y configuración"
)
async def api_info():
    """
    Información técnica de la API.
    Útil para desarrolladores que integren con el sistema.
    """
    return {
        "api": {
            "name": "Merkadit API",
            "version": "1.0.0",
            "framework": "FastAPI",
            "python_version": "3.9+",
            "database": "MySQL 8.0",
            "arquitectura": "4 capas (Handler → Controller → Service → Repository)"
        },
        "endpoints_disponibles": {
            "ventas": {
                "POST /api/sales/register": "Registrar nueva venta",
                "GET /api/sales/{sale_id}": "Obtener detalles de venta",
                "GET /api/sales/report/{store_name}": "Reporte de ventas por comercio"
            },
            "liquidaciones": {
                "POST /api/settlements/settle": "Liquidar comercio",
                "GET /api/settlements/{settlement_id}": "Obtener liquidación",
                "GET /api/settlements/history/{commerce_name}": "Historial de liquidaciones"
            }
        },
        "autenticacion": "No implementada (proyecto educativo)",
        "rate_limiting": "No implementado",
        "documentacion": {
            "swagger": "/docs",
            "redoc": "/redoc",
            "openapi_json": "/openapi.json"
        }
    }


#Eventos de inicio y cierre de la aplicación

@app.on_event("startup")
async def startup_event():
    """
    Evento que se ejecuta al iniciar la aplicacion.
    Verifica la conexión a la base de datos.
    """
    logger.info("=" * 70)
    logger.info(" INICIANDO MERKADIT API")
    logger.info("=" * 70)
    
    # Verificar conexión a BD
    from app.config.database import db_config
    
    logger.info("Verificando conexión a MySQL...")
    
    if db_config.test_connection():
        logger.info("Conexión a MySQL exitosa")
        
        # Obtener info de la BD
        try:
            db_info = db_config.get_database_info()
            logger.info(f" Base de datos: {db_info.get('current_database')}")
            logger.info(f" Tablas disponibles: {db_info.get('tables_count')}")
            logger.info(f"MySQL version: {db_info.get('mysql_version')}")
        except Exception as e:
            logger.warning(f" No se pudo obtener info de BD: {str(e)}")
    else:
        logger.error(" ERROR: No se pudo conectar a MySQL")
        logger.error(" La API iniciará pero no funcionará correctamente")
    
    logger.info("=" * 70)
    logger.info(" API lista en: http://localhost:8000")
    logger.info(" Documentación en: http://localhost:8000/docs")
    logger.info("=" * 70)

@app.on_event("shutdown")
async def shutdown_event():
    """
    Evento que se ejecuta al cerrar la aplicación.
    """
    logger.info("=" * 70)
    logger.info(" CERRANDO MERKADIT API")
    logger.info("=" * 70)


# MAIN - Para ejecutar con uvicorn

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload en desarrollo
        log_level="info"
    )