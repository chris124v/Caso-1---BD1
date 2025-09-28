"""
Configuración de conexion a MySQL y variables de entorno

Aqui gestionamos las credenciales del environment y la conexion a la base de datos

"""
import os #Acceso a variables de entorno
import pymysql #Libreria para conectar a MySQL
from typing import Optional #Para tipado
from dotenv import load_dotenv #Cargar variables de entorno desde .env
import logging #Para logging

# Cargar variables de entorno desde .env
load_dotenv()

"""Configuracion de la base de datos MySQL"""

class DatabaseConfig:
    
    #Constructor de la clase que se ejecuta al crear la instancia
    def __init__(self):
        self.host = os.getenv("DB_HOST", "localhost")
        self.port = int(os.getenv("DB_PORT", 3306))
        self.user = os.getenv("DB_USER", "root")
        self.password = os.getenv("DB_PASSWORD", "")
        self.database = os.getenv("DB_NAME", "Caso1")
        
        # Logger especifico para este modulo
        self.logger = logging.getLogger(__name__)
    
    #Metodo que retorna una conexion activa a MySQL
    def get_connection(self) -> pymysql.Connection:
        
        #Bloque de manjo de errores
        try:
            connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor, #Resultados como diccionarios
                autocommit=False, #Transacciones manuales
                connect_timeout=10
            )
            
            self.logger.info(f"Conexion exitosa a MySQL: {self.host}:{self.port}/{self.database}")
            return connection
            
        #Captura cualquier error de conexion que haya 
        except Exception as e:
            error_msg = f"Error conectando a la base de datos: {str(e)}"
            self.logger.error(error_msg)
            raise Exception(error_msg) #Re-lanzar la excepcion para que el llamador la maneje
    
    #Metodo de prueba de conexion
    def test_connection(self) -> bool:
        
        try:
            conn = self.get_connection() #Conexion usando el metodo anterior
            
            # Probar con una consulta simple ,,,
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1 as test")
                result = cursor.fetchone()
                
            conn.close()
            
            if result and result['test'] == 1:
                self.logger.info("Test de conexion exitoso")
                return True
            
            else:
                self.logger.error("Test de conexión fallo")
                return False
        
        #Manejo de la excepcion
        except Exception as e:
            self.logger.error(f"Test de conexión fallo: {str(e)}")
            return False
    
    #Este solo seria un metodo extra para obtener informacion de la base de datos
    def get_database_info(self) -> dict:
        
        try:
            conn = self.get_connection()
            
            with conn.cursor() as cursor:
                # Informacion del servidor
                cursor.execute("SELECT VERSION() as version")
                version_result = cursor.fetchone()
                
                # Información de la base de datos actual
                cursor.execute("SELECT DATABASE() as current_db")
                db_result = cursor.fetchone()
                
                # Listar las tablas existentes
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                
            conn.close()
            
            #Retornar un diccionario con la informacion obtenida
            return {
                "mysql_version": version_result['version'],
                "current_database": db_result['current_db'],
                "tables_count": len(tables),
                "tables": [list(table.values())[0] for table in tables],
                "connection_config": {
                    "host": self.host,
                    "port": self.port,
                    "user": self.user,
                    "database": self.database
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error obteniendo informacion de BD: {str(e)}")
            return {"error": str(e)}

# Instancia global de configuracion
db_config = DatabaseConfig()

# Funcion helper para obtener conexion rapidamente
def get_db_connection():
    return db_config.get_connection()