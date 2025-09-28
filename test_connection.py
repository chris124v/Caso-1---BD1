"""
Script de prueba para verificar conexion a MySQL

"""

import logging
from app.config.database import db_config

# Configurar logging para ver los mensajes
logging.basicConfig(level=logging.INFO)

def main():

    print("Probando conexion a MySQL")
    print("=" * 50)
    
    # Test basico de conexion
    if db_config.test_connection():
        print("Conexión exitosa!")
        
        # Obtener informacion de la base de datos
        print("\nInformacion de la base de datos:")
        print("-" * 30)
        
        db_info = db_config.get_database_info()
        
        if "error" not in db_info:
            print(f"MySQL Version: {db_info['mysql_version']}")
            print(f"Base de datos actual: {db_info['current_database']}")
            print(f"Número de tablas: {db_info['tables_count']}")
            
            if db_info['tables']:
                print(f"\nTablas encontradas:")
                for table in db_info['tables'][:10]:  # Mostrar maximo 10 tablas
                    print(f"   - {table}")
                    
                if len(db_info['tables']) > 10:
                    print(f"   ... y {len(db_info['tables']) - 10} mas")

            else:
                print("No se encontraron tablas en la base de datos")
                
            print(f"\nConfiguracion de conexion:")
            config = db_info['connection_config']
            print(f"   Host: {config['host']}:{config['port']}")
            print(f"   Usuario: {config['user']}")
            print(f"   Base de datos: {config['database']}")
        else:
            print(f"Error obteniendo informacion: {db_info['error']}")
    else:
        print("Error de conexion")

if __name__ == "__main__":
    main()