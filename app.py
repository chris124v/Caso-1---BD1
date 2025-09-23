from fastapi import FastAPI

# Crear la aplicación FastAPI
app = FastAPI(
    title="Merkadit API - Caso 1",
    description="API para gestión de mercados gastronómicos - TEC",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {
        "message": "¡Merkadit API funcionando correctamente!", 
        "proyecto": "Caso 1 - Bases de Datos I",
        "universidad": "TEC",
        "status": "OK"
    }

@app.get("/test")
def test_endpoint():
    return {
        "test": "exitoso", 
        "descripcion": "API para mercados gastronómicos",
        "funcionalidades": ["ventas", "liquidaciones", "stored procedures"]
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "database": "MySQL - pendiente conexión",
        "stored_procedures": ["registerSale", "settleCommerce"]
    }
