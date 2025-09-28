"""
Repositorio base con funcionalidades comunes de acceso a datos 
para los repositorios como sales y settlements.
"""
#Librerias estandar, tambien traemos la configuracion de la base de datos
import pymysql
import logging
from typing import List, Dict, Any, Optional, Tuple
from app.config.database import db_config
from datetime import datetime
import hashlib  #Esto seria para generar checksums

#Clase base del repositorio
class BaseRepository:
    
    #Constructor especifico de la clase que se ejecuta al crear la instancia
    def __init__(self):
        self.logger = logging.getLogger(__name__)   #Logger especifico para este modulo

        self.table_id_mapping = {
            "MKUsers": "IdUser",
            "MKRoles": "IdRole",
            "MKPermissions": "IdPermission",
            "MKUserRoles": "IdUserRole",
            "MKRolePermissions": "IdRolePermission",
            "MKCountries": "IdCountry",
            "MKStates": "IdState",
            "MKCities": "IdCity",
            "MKAddresses": "IdAddress",
            "MKContractTypes": "IdContractType",
            "MKContractStatus": "IdContractStatus",
            "MKContracts": "IdContract",
            "MKContractTerms": "IdContractTerms",
            "MKCommerceCategories": "IdCommerceCategory",
            "MKCommerceStatus": "IdCommerceStatus",
            "MKCommerces": "IdCommerce",
            "MKMercado": "IdMercado",
            "MKBuilding": "IdBuilding",
            "MKMercadoPerBuilding": "IdMercadoPerBuilding",
            "MKSpaceStatus": "IdSpaceStatus",
            "MKSpaceTypes": "IdSpaceType",
            "MKSpaces": "IdSpace",
            "MKContractsPerCommerces": "IdContractPerCommerce",
            "MKContractRenewals": "IdContractRenewal",
            "MKPaymentMethods": "IdPaymentMethod",
            "MKSales": "IdSale",
            "MKProductCategories": "IdProductCategory",
            "MKProductBrand": "IdProductBrand",
            "MKInventory": "IdInventory",
            "MKProducts": "IdProduct",
            "MKSalesDetails": "IdSaleDetails",
            "MKInvoices": "IdInvoice",
            "MKInvoiceDetails": "IdInvoiceDetail",
            "MKReceipts": "IdReceipt",
            "MKSaleDiscounts": "IdSaleDiscounts",
            "MKInitialInvestment": "IdInitialInvestment",
            "MKTransactionTypes": "IdTransactionType",
            "MKCommerceSettlement": "IdCommerceSettlement",
            "MKRelatedEntityType": "idRelatedEntityType",
            "MKTransactionSubTypes": "IdTransactionSubTypes",
            "MKFinancialTransactions": "IdFinancialTransaction",
            "MKCommissionCalculatios": "IdCommissionCalculations",
            "MKLogSeverities": "IdLogSeverity",
            "MKLogSource": "IdLogSource",
            "MKLogType": "IdLogType",
            "MKLogs": "IdLog",
            "MKSpaceAttributes": "IdSpaceAttributes",
            "MKInventoryMovements": "IdInventoryMovement",
            "MKProductsPerMercadoPerBuilding": "IdProductsInMercadoBuilding",
            "MKProductPrices": "IdProductPrices",
            "MKBarcode": "IdBarcode",
            "MKCommerceSettlementDetail": "IdCommerceSettlementDetail",
            "MKSpacesPerSpaceAttributes": "IdSpacePerSpaceAttributes",
            "MKUsersPerMercado": "IdUsersPerMercado",
            "MKUsersPerCommerce": "IdUsersPerCommerce",
            "MKCommissionCalculationsDetails": "IdCommissionCalculationsDetails"
        }
    
    #Obtenemos conexion a la base de datos
    def get_connection(self) -> pymysql.Connection:
        return db_config.get_connection()
    
    #Esta funcion seria para ejecutar consultas SELECT y retornar resultados indicados 
    def execute_query(self, query: str, params: Optional[Tuple] = None) -> List[Dict[str, Any]]:
        
        connection = None #Inicializamos la conexion en None

        #Manejo de errores
        try:

            #Conexio activa
            connection = self.get_connection()

            #Trae todo el resultado de la consulta
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                results = cursor.fetchall()
                return results
        
        #En caso de error, lo loguea y relanza la excepcion
        except Exception as e:
            self.logger.error(f"Error ejecutando query: {str(e)}")
            raise Exception(f"Error en consulta a la base de datos: {str(e)}")
        
        #Sin importar si hubo error o no, cierra la conexion con la base de datos
        finally:
            if connection:
                connection.close()
    
    #Esta funcion seria para ejecutar consultas INSERT/UPDATE/DELETE que no son SELECT basicamente
    def execute_non_query(self, query: str, params: Optional[Tuple] = None) -> int:
       
        connection = None

        #Exception handling
        try:

            #Conexion activa con la base de datos
            connection = self.get_connection()

            #Ejecuta la consulta y confirma la transaccion
            with connection.cursor() as cursor:
                affected_rows = cursor.execute(query, params)
                connection.commit()
                return affected_rows
        
        #Errores se manejan con rollback para que vuelva al estado previo
        except Exception as e:
            if connection:
                connection.rollback()
            self.logger.error(f"Error ejecutando non-query: {str(e)}")
            raise Exception(f"Error en operación de base de datos: {str(e)}")
        
        #Nuevamente se cierra la conexion
        finally:
            if connection:
                connection.close()
    
    #Esto seria para consultas que retornan un solo valor, como count(*) o demas
    def execute_scalar(self, query: str, params: Optional[Tuple] = None) -> Any:
        
        connection = None

        #exception handling
        try:

            #Realiza la conexion con la base de datos
            connection = self.get_connection()

            #Ejecuta la consulta y retorna el primer valor de la primera fila
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                result = cursor.fetchone()
                return list(result.values())[0] if result else None #Retorna el primer valor o None si no hay resultados
        
        # Manejo de errores
        except Exception as e:
            self.logger.error(f"Error ejecutando scalar query: {str(e)}")
            raise Exception(f"Error en consulta escalar: {str(e)}")
        
        #Cierra la conexion
        finally:
            if connection:
                connection.close()
    
    #Este seria propiamenente para llamar stored procedures que haremos despues 
    def call_stored_procedure(self, proc_name: str, params: Optional[Tuple] = None) -> Dict[str, Any]:
        
        connection = None

        #Ecxeption handling
        try:
            connection = self.get_connection()

            with connection.cursor() as cursor:

                # Construir la llamada al stored procedure
                if params:
                    placeholders = ', '.join(['%s'] * len(params))  # Creamos placeholders para los parámetros
                    call_query = f"CALL {proc_name}({placeholders})" # Consulta CALL con placeholders
                    cursor.execute(call_query, params)  # Ejecuta la consulta con los parametros
                
                else:
                    cursor.execute(f"CALL {proc_name}()")
                
                # Obtener resultados si los hay
                results = []

                try:
                    results = cursor.fetchall() #Trae todos los resultados

                except:
                    # No hay resultados de SELECT
                    pass
                
                # Confirmar transaccion con commit
                connection.commit()
                
                #Este seria el diccionario que retorna los resultados
                return {
                    'success': True,
                    'results': results,
                    'affected_rows': cursor.rowcount
                }
        
        #Manejo de errores con rollback
        except Exception as e:
            if connection:
                connection.rollback()

            self.logger.error(f"Error llamando stored procedure {proc_name}: {str(e)}")
            raise Exception(f"Error ejecutando procedimiento almacenado: {str(e)}")
        
        #Cierra la conexion
        finally:

            if connection:
                connection.close()
    
    #Este seria para la generacion de checksums, usamos 160 bits que seria lo recomendado y tambien lo usamos en el diseno
    def generate_checksum(self, data: str) -> bytes:
        
        return hashlib.sha256(data.encode()).digest()[:20]  # 160 bits = 20 bytes, aqui ya usamos el hashlib
    
    #Este metodo es para dar utilidad a MK Logs 
    def log_operation(self, user_id: int, operation: str, description: str, reference_id1: int = 0, reference_id2: int = 0, 
        value1: str = "", value2: str = "", computer: str = "API") -> None:
        
        try:
            checksum_data = f"{user_id}{operation}{description}{datetime.now().isoformat()}" #Creamos el string para checksum
            checksum = self.generate_checksum(checksum_data) #Genereramos el hash de integridad
            
            #Este seria el query para insertar el log
            log_query = """
                INSERT INTO MKLogs (
                    description, postTime, computer, username, trace, 
                    referenceID1, referenceID2, value1, value2, checksum, 
                    lastUpdate, IDLogSeverityFK, IDLogSourceFK, IDLogTypeFK, IDUserFK2, createdAt
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1, 1, 1, %s, %s
                )
            """
            
            #Parametros para el query, importante el datetime que es ahor o lo registra segun hora actual digamos
            params = (
                description, datetime.now(), computer, f"user_{user_id}", operation,
                reference_id1, reference_id2, value1, value2, checksum,
                datetime.now(), user_id, datetime.now()
            )
            
            self.execute_non_query(log_query, params)
            
        except Exception as e:
            # Log de error pero no fallar la operacion principal
            self.logger.warning(f"Error registrando log: {str(e)}")
    

    #Metodo para obtener el siguiente ID disponible en una tabla dada
    def get_next_id(self, table_name: str) -> int:
        if table_name not in self.table_id_mapping:
            raise ValueError(f"Tabla '{table_name}' no encontrada en el mapeo")
    
        id_column = self.table_id_mapping[table_name]
        query = f"SELECT COALESCE(MAX({id_column}), 0) + 1 FROM {table_name}"
        return self.execute_scalar(query) or 1