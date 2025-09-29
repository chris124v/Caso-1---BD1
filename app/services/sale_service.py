"""
Service layer para operaciones de ventas 

Este servicio implementa la logica de negocio compleja para ventas,
realizando multiples operaciones de repository y validaciones.

"""
#Importamos las librerias necesarias
from typing import List, Dict, Any, Optional
from datetime import datetime, date
from decimal import Decimal
from app.repositories.sale_repository import SaleRepository
from app.repositories.base_repository import BaseRepository
import logging

#Esta clase tiene la logica de negocio para ventas y por ende todos los metodos 
class SaleService:
    
    #Constructor para la creacion de la instancia, nos basamos en los repositories
    def __init__(self):
        self.sale_repository = SaleRepository()
        self.base_repository = BaseRepository()
        self.logger = logging.getLogger(__name__)
    
    #Procesa una venta con validaciones de negocio
    def process_sale(self, commerce_id: int, cashier_user_id: int, items: List[Dict], payment_method_id: int = 1) -> Dict[str, Any]:
        """
        Argumentos:
            commerce_id: ID del comercio
            cashier_user_id: ID del cajero
            items: [{'product_id': int, 'quantity': int, 'unit_price': float}]
            payment_method_id: ID metodo de pago
        """

        #Manejo de errores
        try:
            # Validar datos basicos
            if not items or len(items) == 0:
                raise ValueError("La venta debe tener al menos un producto")
        
            if commerce_id <= 0 or cashier_user_id <= 0:
                raise ValueError("IDs de comercio y cajero deben ser válidos")
        
            # Validar que el comercio existe y está activo
            commerce = self._validate_commerce(commerce_id)
        
            # Validar stock disponible para cada producto
            validated_items = self._validate_stock(items)
        
            # Crear venta usando repository (actualiza inventario automaticamente)
            sale_result = self.sale_repository.create_sale(
                commerce_id=commerce_id,
                cashier_user_id=cashier_user_id,
                items=validated_items,
                payment_method_id=payment_method_id
            )
        
            # Log de la venta procesada
            self.logger.info(f"Venta procesada: {sale_result['sale_id']}")
        
            # Retornar resumen de la venta
            return {
                'success': True,
                'sale_id': sale_result['sale_id'],
                'reference_number': sale_result['reference_number'],
                'total_amount': sale_result['total_amount'],
                'items_count': sale_result['items_count'],
                'commerce_name': commerce['name'],
                'timestamp': datetime.now().isoformat()
            }
    
        #ValueError específicamente para validaciones
        except ValueError as ve:
            self.logger.warning(f"Validacion falló: {str(ve)}")
            raise ve  
    
        # Capturamos cualquier otro error como Exception generica
        except Exception as e:
            self.logger.error(f"Error procesando venta: {str(e)}")
            raise Exception(f"Error procesando venta: {str(e)}")


    # Genera reporte de ventas para un comercio en un rango de fechas
    # Retorna diccionario con resumen y lista de ventas
    def get_sales_report(self, commerce_id: int, start_date: str, 
                        end_date: str) -> Dict[str, Any]:
    
        try:
            # Obtener ventas del periodo
            sales = self.sale_repository.get_sales_by_date_range(
                start_date=start_date,
                end_date=end_date,
                commerce_id=commerce_id
            )
            
            # Obtener totales calculados
            totals = self.sale_repository.get_total_sales_by_commerce(
                commerce_id=commerce_id,
                start_date=start_date,
                end_date=end_date
            )
            
            # Obtener terminos del contrato para cálculo de comision
            contract_terms = self._get_contract_terms(commerce_id)
            
            # Calcular comision sobre ventas
            commission_amount = Decimal(str(totals['total_sales_amount'])) * \
                              (contract_terms['commission_percentage'] / 100)
            
            #Retornar el reporte completo
            return {
                'commerce_id': commerce_id,
                'period': {
                    'start': start_date,
                    'end': end_date
                },
                'sales_count': totals['sales_count'],
                'total_sales': totals['total_sales_amount'],
                'subtotal': totals['total_subtotal'],
                'tax': totals['total_tax'],
                'commission_percentage': float(contract_terms['commission_percentage']),
                'commission_amount': float(commission_amount),
                'base_rent': float(contract_terms['base_rent']),
                'sales_list': sales,
                'generated_at': datetime.now().isoformat()
            }
        
        #Detecta cualquier error ocurrido generando el reporte
        except Exception as e:
            self.logger.error(f"Error generando reporte: {str(e)}")
            raise Exception(f"Error generando reporte: {str(e)}")
    
    #Resumen diario de ventas para un comercio
    def get_daily_sales_summary(self, commerce_id: int) -> Dict[str, Any]:
        
        #Manejo de excepciones
        try:
            today = str(date.today())
            
            # Obtener totales del dia actual
            totals = self.sale_repository.get_total_sales_by_commerce(
                commerce_id=commerce_id,
                start_date=today,
                end_date=today
            )
            
            # Obtener ultimas 10 ventas del dia
            recent_sales = self.sale_repository.get_sales_by_commerce(
                commerce_id=commerce_id,
                limit=10
            )
            
            #Retornar el resumen diario
            return {
                'date': today,
                'commerce_id': commerce_id,
                'total_sales_today': totals['total_sales_amount'],
                'transactions_today': totals['sales_count'],
                'recent_sales': recent_sales,
                'timestamp': datetime.now().isoformat()
            }
        
        #Error ocurrido obteniendo el resumen diario
        except Exception as e:
            self.logger.error(f"Error en resumen diario: {str(e)}")
            raise Exception(f"Error obteniendo resumen diario: {str(e)}")
    
    # Obtiene detalles completos de una venta especifica
    def get_sale_details(self, sale_id: int) -> Optional[Dict[str, Any]]:
       
       #Manejo de errores
        try:
            return self.sale_repository.get_sale_by_id(sale_id) #retorna el detalle de la venta
        
        #Exception capturada
        except Exception as e:
            self.logger.error(f"Error obteniendo detalles de venta: {str(e)}")
            return None
    
    #Validaciones internas
    
    #Valida que el comercio existe y esta activo
    def _validate_commerce(self, commerce_id: int) -> Dict[str, Any]:
        
        #Manejo de errores
        try:
            result = self.base_repository.execute_query(
                "SELECT IdCommerce, name, isActive FROM MKCommerces WHERE IdCommerce = %s",
                (commerce_id,)
            )
            
            #En caso de que no exista
            if not result:
                raise ValueError(f"Comercio {commerce_id} no existe")
            
            commerce = result[0]

            #En caso de que no este activo
            if not commerce['isActive']:
                raise ValueError(f"Comercio {commerce_id} no está activo")
            
            return commerce
        
        #Error ocurrido validando el comercio
        except Exception as e:
            raise Exception(f"Error validando comercio: {str(e)}")
    
    #Valida que hay stock disponible para todos los productos
    def _validate_stock(self, items: List[Dict]) -> List[Dict]:
        
        #Lista para items validados
        validated = []
        
        #Itera sobre cada producto de la venta
        for item in items:

            product_id = item['product_id']
            quantity = item['quantity']
            
            # Verificar stock actual, retorna un solo valor
            stock = self.base_repository.execute_scalar(
                "SELECT quantity FROM MKProducts WHERE IdProduct = %s",
                (product_id,)
            )
            
            #Si el producto no existe o no hay stock suficiente
            if stock is None:
                raise ValueError(f"Producto {product_id} no existe")
            
            if stock < quantity:
                raise ValueError(
                    f"Stock insuficiente para producto {product_id}. "
                    f"Disponible: {stock}, Solicitado: {quantity}"
                )
            
            validated.append(item)
        
        return validated
    
    #Obtiene terminos del contrato actual para el comercio
    def _get_contract_terms(self, commerce_id: int) -> Dict[str, Decimal]:
        
        #Manejo de errores
        try:
            result = self.base_repository.execute_query("""
                SELECT baseMonthlyRent, commisionPercentage
                FROM MKContractsPerCommerces
                WHERE IDCommerceFK = %s AND isCurrent = 1
                LIMIT 1
            """, (commerce_id,))
            
            #Si hay contrato actual, retornar sus terminos como decimal
            if result:
                return {
                    'base_rent': Decimal(str(result[0]['baseMonthlyRent'])),
                    'commission_percentage': Decimal(str(result[0]['commisionPercentage']))
                }
            
            # Valores por defecto si no hay contrato
            return {
                'base_rent': Decimal('50000.00'),
                'commission_percentage': Decimal('10.00')
            }
        
        #En caso de error, retornar valores por defecto
        except Exception:
            return {
                'base_rent': Decimal('50000.00'),
                'commission_percentage': Decimal('10.00')
            }