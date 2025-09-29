"""
Repositorio para operaciones de liquidaciones mensuales osea los settlements

"""

# Import de las librerias necesarias 
from typing import Dict, Any, Optional
from datetime import datetime, date
from decimal import Decimal
from app.repositories.base_repository import BaseRepository

#Repositorio para manejar las liquidaciones
class SettlementRepository(BaseRepository): #Hereda de BaseRepository para usar sus metodos
    
    #Constructor que se crea al crear la instancia
    def __init__(self):
        super().__init__()
        self.default_commission_percentage = Decimal('10.00')  # 10% por defecto
        self.default_base_rent = Decimal('50000.00')  # ₡50,000 base de renta por defecto
    
    #Metodo para crear una liquidacion
    def create_settlement(self, commerce_id: int, period_start: date, period_end: date, created_by_user_id: int) -> Dict[str, Any]:
        """
        Tendria lo siguiente:
            commerce_id: ID del comercio
            period_start: Fecha inicio del período
            period_end: Fecha fin del período
            created_by_user_id: ID del usuario que crea la liquidación
        """
        connection = None #Inicializa la conexion en None

        #Manejo de excepciones
        try:
            connection = self.get_connection()
            connection.begin()
            
            # 1. Validar que no exista liquidacion para este período
            existing = self._check_existing_settlement(commerce_id, period_start, period_end)
            if existing:
                raise ValueError(f"Ya existe liquidación para este periodo")
            
            # 2. Obtener terminos del contrato 
            contract_terms = self._get_contract_terms(commerce_id)
            
            # 3. Calcular totales de ventas
            sales_totals = self._get_period_sales(commerce_id, period_start, period_end)
            
            # 4. Calcular liquidacion
            base_rent = contract_terms.get('base_rent', self.default_base_rent)
            commission_percentage = contract_terms.get('commission_percentage', self.default_commission_percentage)
            
            total_sales = sales_totals['total_sales']
            commission_amount = total_sales * (commission_percentage / 100)
            settlement_amount = commission_amount - base_rent
            
            # 5. Crear liquidacion
            settlement_id = self.get_next_id("MKCommerceSettlement")
            
            #Realiza el insert en la tabla de liquidaciones
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO MKCommerceSettlement (
                        IdCommerceSettlement, IDCommerceFK6, totalSalesAmount,
                        settlementPeriodStart, settlementPeriodEnd, totalRent,
                        totalCommission, totalSettlementAmount, settlementDate,
                        createdAt, UpdatedAt, MKContractsPerCommerces_IdContractPerCommerce,
                        MKMercadoPerBuilding_IdMercadoPerBuilding
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1, 1
                    )
                """, (
                    settlement_id, commerce_id, total_sales, period_start, period_end,
                    base_rent, commission_amount, settlement_amount, datetime.now().date(),
                    datetime.now(), datetime.now()
                ))
            
            connection.commit()
            
            # 6. Log de operacion para dejar registro de la creacion de la liquidacion
            self.log_operation(
                user_id=created_by_user_id,
                operation="CREATE_SETTLEMENT",
                description=f"Liquidación creada: Comercio={commerce_id}, Total=${settlement_amount}",
                reference_id1=settlement_id,
                reference_id2=commerce_id
            )
            
            # 7. Retornar detalles de la liquidacion creada en un diccionario
            return {
                'success': True,
                'settlement_id': settlement_id,
                'commerce_id': commerce_id,
                'period': f"{period_start} - {period_end}",
                'total_sales': float(total_sales),
                'base_rent': float(base_rent),
                'commission_amount': float(commission_amount),
                'commission_percentage': float(commission_percentage),
                'settlement_amount': float(settlement_amount)
            }
        
        #Manejo de errores
        except Exception as e:
            if connection:
                connection.rollback()
            raise Exception(f"Error creando liquidación: {str(e)}")
        
        #Desconoexion de la base de datos
        finally:
            if connection:
                connection.close()
    
    #Obtener liquidacion por ID
    def get_settlement_by_id(self, settlement_id: int) -> Optional[Dict[str, Any]]:
        
        #Manejo de excepciones
        try:
            query = """
                SELECT 
                    cs.*, c.name as commerce_name
                FROM MKCommerceSettlement cs
                INNER JOIN MKCommerces c ON cs.IDCommerceFK6 = c.IdCommerce
                WHERE cs.IdCommerceSettlement = %s
            """
            
            #Resultado de la consulta
            result = self.execute_query(query, (settlement_id,))

            #Si no hay resultados, retorna None
            if not result:
                return None
            
            settlement = result[0]
            
            #Retorna un diccionario con los detalles de la liquidacion
            return {
                'settlement_id': settlement['IdCommerceSettlement'],
                'commerce_id': settlement['IDCommerceFK6'],
                'commerce_name': settlement['commerce_name'],
                'period_start': settlement['settlementPeriodStart'].isoformat() if settlement['settlementPeriodStart'] else None,
                'period_end': settlement['settlementPeriodEnd'].isoformat() if settlement['settlementPeriodEnd'] else None,
                'total_sales': float(settlement['totalSalesAmount']),
                'base_rent': float(settlement['totalRent']),
                'commission_amount': float(settlement['totalCommission']),
                'settlement_amount': float(settlement['totalSettlementAmount']),
                'settlement_date': settlement['settlementDate'].isoformat() if settlement['settlementDate'] else None
            }
        
        #Error obteniendo la liquidacion
        except Exception as e:
            raise Exception(f"Error obteniendo liquidacion {settlement_id}: {str(e)}")
    
    #Obtener la liquidacion por comercio
    def get_settlements_by_commerce(self, commerce_id: int, limit: int = 10) -> list:
        
        #Manejo de excepciones
        try:
            query = """
                SELECT 
                    IdCommerceSettlement, settlementPeriodStart, settlementPeriodEnd,
                    totalSalesAmount, totalRent, totalCommission, totalSettlementAmount,
                    settlementDate
                FROM MKCommerceSettlement
                WHERE IDCommerceFK6 = %s
                ORDER BY settlementPeriodStart DESC
                LIMIT %s
            """

            #Resultado de la consulta
            results = self.execute_query(query, (commerce_id, limit))
            
            #Retorna una lista de diccionarios con las liquidaciones
            return [
                {
                    'settlement_id': s['IdCommerceSettlement'],
                    'period_start': s['settlementPeriodStart'].isoformat() if s['settlementPeriodStart'] else None,
                    'period_end': s['settlementPeriodEnd'].isoformat() if s['settlementPeriodEnd'] else None,
                    'total_sales': float(s['totalSalesAmount']),
                    'settlement_amount': float(s['totalSettlementAmount']),
                    'settlement_date': s['settlementDate'].isoformat() if s['settlementDate'] else None
                }

                for s in results
            ]
        
        #Error obteniendo las liquidaciones
        except Exception as e:
            raise Exception(f"Error obteniendo liquidaciones: {str(e)}")
    
    #Validar si un comercio puede ser liquidado O NO segun sus ventas en el periodo
    def validate_settlement_eligibility(self, commerce_id: int, period_start: date, period_end: date) -> Dict[str, Any]:
        
        #Manejo de excepciones
        try:
            # Verificar liquidación existente
            existing = self._check_existing_settlement(commerce_id, period_start, period_end)
            if existing:
                return {
                    'eligible': False,
                    'reason': 'Ya existe liquidacion para este período'
                }
            
            # Verificar ventas en el periodo
            sales = self._get_period_sales(commerce_id, period_start, period_end)
            
            # Si no hay ventas, no es elegible
            return {
                'eligible': True,
                'sales_count': sales['sales_count'],
                'total_sales': float(sales['total_sales']),
                'message': 'Listo para liquidar'
            }
        
        # Manejo de errores
        except Exception as e:
            return {
                'eligible': False,
                'reason': f'Error: {str(e)}'
            }
    
    # Calcular preview de liquidacion sin crearla directamente
    def calculate_settlement_preview(self, commerce_id: int, period_start: date, period_end: date) -> Dict[str, Any]:
        
        #Manejo de excepciones
        try:
            # Obtener datos
            contract_terms = self._get_contract_terms(commerce_id)
            sales_totals = self._get_period_sales(commerce_id, period_start, period_end)
            
            # Calcular
            base_rent = contract_terms.get('base_rent', self.default_base_rent)
            commission_percentage = contract_terms.get('commission_percentage', self.default_commission_percentage)
            
            #Calculo de los montos
            total_sales = sales_totals['total_sales']
            commission_amount = total_sales * (commission_percentage / 100)
            settlement_amount = commission_amount - base_rent
            
            # Retornar preview
            return {
                'commerce_id': commerce_id,
                'period': f"{period_start} - {period_end}",
                'sales_count': sales_totals['sales_count'],
                'total_sales': float(total_sales),
                'base_rent': float(base_rent),
                'commission_percentage': float(commission_percentage),
                'commission_amount': float(commission_amount),
                'settlement_amount': float(settlement_amount),
                'settlement_type': 'POSITIVE' if settlement_amount >= 0 else 'NEGATIVE'
            }
        
        #Manejo de errores en caso de que no se pueda calcular el preview
        except Exception as e:
            raise Exception(f"Error calculando preview: {str(e)}")
    
    #Metodos privados para operaciones internas
    
    #Verifica si ya existe una liquidacion para el comercio en el periodo dado
    def _check_existing_settlement(self, commerce_id: int, period_start: date, period_end: date) -> bool:
        
        #Manejo de excepciones
        try:
            count = self.execute_scalar("""
                SELECT COUNT(*) FROM MKCommerceSettlement
                WHERE IDCommerceFK6 = %s 
                AND settlementPeriodStart = %s 
                AND settlementPeriodEnd = %s
            """, (commerce_id, period_start, period_end))
            
            return count > 0

        #En caso de error, retorna falso    
        except Exception:
            return False
    
    #Obtiene los terminos del contrato, en esta version simplificada retorna valores por defecto
    def _get_contract_terms(self, commerce_id: int) -> Dict[str, Any]:
        
        try:
            #Esto seria usando los valores por defecto
            return {
                'base_rent': self.default_base_rent,
                'commission_percentage': self.default_commission_percentage
            }
        except Exception:
            return {
                'base_rent': self.default_base_rent,
                'commission_percentage': self.default_commission_percentage
            }
    
    #Obtiene las ventas del periodo para el comercio
    def _get_period_sales(self, commerce_id: int, period_start: date, period_end: date) -> Dict[str, Any]:
        
        #Manejo de excepciones
        try:
            query = """
                SELECT 
                    COUNT(*) as sales_count,
                    COALESCE(SUM(totalAmount), 0) as total_sales
                FROM MKSales
                WHERE IDCommerceFK2 = %s
                AND DATE(saleDate) BETWEEN %s AND %s
                AND saleStatus = 'COMPLETED'
            """
            
            #Se ejecuta la consulta
            result = self.execute_query(query, (commerce_id, period_start, period_end))
            
            #Si hay resultados, los retorna en un diccionario
            if result:
                return {
                    'sales_count': result[0]['sales_count'],
                    'total_sales': Decimal(str(result[0]['total_sales']))
                }
            
            #Si no hay resultados, retorna ceros
            return {
                'sales_count': 0,
                'total_sales': Decimal('0.00')
            }
        
        #Manejo de errores en caso de que no se puedan calcular las ventas
        except Exception as e:
            raise Exception(f"Error calculando ventas: {str(e)}")