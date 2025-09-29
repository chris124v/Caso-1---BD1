"""
Script de prueba para verificar Repository Base
"""
import logging
from app.repositories.base_repository import BaseRepository

# Configurar logging
logging.basicConfig(level=logging.INFO)

def main():
    print("Probando Repository Base")
    print("=" * 50)
    
    try:
        repo = BaseRepository()
        
        # Test 1: Consulta simple
        print("Test 1: Consulta simple")
        result = repo.execute_query("SELECT COUNT(*) as total_tables FROM information_schema.tables WHERE table_schema = %s", ("Caso1",))
        print(f"Total de tablas en Caso1: {result[0]['total_tables']}")
        
        # Test 2: Listar algunas tablas
        print("\nTest 2: Listar tablas")
        tables = repo.execute_query("SHOW TABLES")
        print(f"Primeras 5 tablas:")
        for i, table in enumerate(tables[:5]):
            table_name = list(table.values())[0]
            print(f"   {i+1}. {table_name}")
        
        # Test 3: Obtener informacion específica
        print("\nTest 3: Verificar tabla MKUsers")
        user_count = repo.execute_scalar("SELECT COUNT(*) FROM MKUsers")
        print(f"Número de usuarios en MKUsers: {user_count}")

        # Test 4: Obtener siguiente ID

        print("\nTest 4: Verificar get_next_id()")
        try:
            next_user_id = repo.get_next_id("MKUsers")
            print(f"Siguiente ID para MKUsers: {next_user_id}")
    
            next_sale_id = repo.get_next_id("MKSales") 
            print(f"Siguiente ID para MKSales: {next_sale_id}")
    
            # Probar tabla que no existe
            try:
                repo.get_next_id("TablaInexistente")

            except ValueError as e:
                print(f"Error esperado: {e}")
        
        except Exception as e:
            print(f"Error en get_next_id: {e}")
        
        print("\nTodos los tests del Repository Base pasaron correctamente!")
        
    except Exception as e:
        print(f"Error en tests: {str(e)}")

if __name__ == "__main__":
    main()