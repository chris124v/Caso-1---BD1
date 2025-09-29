"""
Controlador para orquestar la logica de negocio de ventas
"""

#Librerias estandar
from typing import Dict, Any
import logging
from decimal import Decimal
from datetime import datetime, date

from ..models.request_models import RegisterSaleRequest
from ..models.response_models import RegisterSaleResponse, ErrorResponse
from ..services.sale_service import SaleService

logger = logging.getLogger(__name__)

#Clase Controlador para la gestion de ventas, orquesta operaciones relacionadas con ventas
class SaleController:
    
    #Inicializador del controlador con el servicio de ventas
    def __init__(self):
        
        self.sale_service = SaleService()
    
    #Procesa el registro de una nueva venta
    def register_sale(self, sale_data: RegisterSaleRequest) -> Dict[str, Any]:
        
        # Logica de negocio para registrar una venta
        try:
            logger.info(f"Iniciando registro de venta para '{sale_data.store_name}'")
            logger.debug(f"Detalles: Producto='{sale_data.product_name}', Cantidad={sale_data.quantity_sold}, Monto=${sale_data.amount_paid}")
            
            # Validaciones de negocio de alto nivel
            self._validate_sale_business_rules(sale_data)
            
            # Obtenemos Ids necesarios
            commerce_id = self._get_commerce_id_by_name(sale_data.store_name)
            payment_method_id = self._map_payment_method_to_id(sale_data.payment_method)
            cashier_user_id = 2  # TODO: Obtener del contexto de autenticacion
            
            # Construir items para el servicio
            items = [{
                'product_id': 1,  # TODO: Lookup real del producto
                'quantity': sale_data.quantity_sold,
                'unit_price': float(sale_data.amount_paid / sale_data.quantity_sold)
            }]
            
            # Llamar al servicio
            result = self.sale_service.process_sale(
                commerce_id=commerce_id,
                cashier_user_id=cashier_user_id,
                items=items,
                payment_method_id=payment_method_id
            )
            
            # Preparar respuesta estandarizada
            response_data = RegisterSaleResponse(
                success=True,
                message="Venta registrada exitosamente",
                sale_id=result['sale_id'],
                invoice_number=sale_data.invoice_number,
                total_amount=Decimal(str(result['total_amount'])),
                commission_amount=Decimal('0.00')
            )
            
            logger.info(f"Venta registrada - ID: {result['sale_id']}")
            return response_data.model_dump()
        
        #Excepciones y manejo de errores
        except ValueError as ve:
            logger.warning(f"Error de validacion: {str(ve)}")
            error_response = ErrorResponse(
                success=False,
                message="Error de validacion en los datos de venta",
                error_code="VALIDATION_ERROR",
                error_details={
                    "validation_error": str(ve),
                    "store": sale_data.store_name,
                    "invoice": sale_data.invoice_number
                }
            )
            return error_response.model_dump()
            
        except Exception as e:
            logger.error(f"Error inesperado al registrar venta: {str(e)}", exc_info=True)
            error_response = ErrorResponse(
                success=False,
                message="Error interno al procesar la venta",
                error_code="INTERNAL_ERROR",
                error_details={
                    "error": str(e),
                    "store": sale_data.store_name
                }
            )
            return error_response.model_dump()
    
    #Valida reglas de negocio de alto nivel
    def _validate_sale_business_rules(self, sale_data: RegisterSaleRequest) -> None:
        
        logger.debug(f"Validando reglas de negocio para venta: {sale_data.invoice_number}")
        
        if sale_data.applied_discounts and sale_data.applied_discounts >= sale_data.amount_paid:
            raise ValueError(
                f"Los descuentos (${sale_data.applied_discounts}) no pueden ser "
                f">= al monto pagado (${sale_data.amount_paid})"
            )
        
        if sale_data.quantity_sold > 1000:
            raise ValueError(f"Cantidad excesiva: {sale_data.quantity_sold} unidades")
        
        if not sale_data.invoice_number.replace('-', '').replace('_', '').isalnum():
            raise ValueError(f"Formato de factura invalido: '{sale_data.invoice_number}'")
        
        min_amount = Decimal('0.50')
        if sale_data.amount_paid < min_amount:
            raise ValueError(f"Monto minimo no alcanzado: ${sale_data.amount_paid} < ${min_amount}")
        
        logger.debug("Validaciones de reglas de negocio completadas")
    
    #Obtiene detalles de una venta especifica
    def get_sale_by_id(self, sale_id: int) -> Dict[str, Any]:
        
        try:
            logger.info(f"Obteniendo venta ID: {sale_id}")
            
            sale_details = self.sale_service.get_sale_details(sale_id)
            
            if not sale_details:
                logger.warning(f"Venta no encontrada: ID {sale_id}")
                return {
                    "success": False,
                    "message": f"Venta con ID {sale_id} no encontrada",
                    "timestamp": datetime.now().isoformat(),
                    "error_code": "SALE_NOT_FOUND"
                }
            
            logger.info(f"Venta encontrada: ID {sale_id}")
            return {
                "success": True,
                "message": "Detalles de venta obtenidos exitosamente",
                "timestamp": datetime.now().isoformat(),
                "data": sale_details
            }
            
        except Exception as e:
            logger.error(f"Error obteniendo venta: {str(e)}", exc_info=True)
            return {
                "success": False,
                "message": "Error al obtener detalles de venta",
                "timestamp": datetime.now().isoformat(),
                "error_code": "SALE_DETAILS_ERROR",
                "error_details": {"error": str(e), "sale_id": sale_id}
            }
    
    # Get reporte de ventas para un comercio en un rango de fechas
    def get_sales_report(self, store_name: str, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        
        # Logica para obtener reporte de ventas
        try:
            logger.info(f"Generando reporte de ventas para '{store_name}'")
            
            # Fechas por defecto: mes actual
            if not start_date:
                today = date.today()
                start_date = date(today.year, today.month, 1).isoformat()
            if not end_date:
                end_date = date.today().isoformat()
            
            commerce_id = self._get_commerce_id_by_name(store_name)
            
            report = self.sale_service.get_sales_report(
                commerce_id=commerce_id,
                start_date=start_date,
                end_date=end_date
            )
            
            # Preparar respuesta
            return {
                "success": True,
                "message": "Reporte generado exitosamente",
                "timestamp": datetime.now().isoformat(),
                "data": report
            }
        
        # Manejo de errores o excepciones
        except Exception as e:
            logger.error(f"Error generando reporte: {str(e)}", exc_info=True)
            return {
                "success": False,
                "message": "Error al generar reporte",
                "timestamp": datetime.now().isoformat(),
                "error_code": "REPORT_ERROR",
                "error_details": {"error": str(e), "store": store_name}
            }
    
    #Obtiene un resumen diario de ventas para un comercio
    def get_daily_summary(self, store_name: str) -> Dict[str, Any]:
        
        # Logica para obtener resumen diario
        try:
            logger.info(f"Obteniendo resumen diario para '{store_name}'")
            
            commerce_id = self._get_commerce_id_by_name(store_name)
            
            summary = self.sale_service.get_daily_sales_summary(commerce_id)
            
            #Diccionario de respuesta
            return {
                "success": True,
                "message": "Resumen diario obtenido exitosamente",
                "timestamp": datetime.now().isoformat(),
                "data": {
                    "store_name": store_name,
                    **summary
                }
            }
        
        #Dicionario de errores
        except Exception as e:
            logger.error(f"Error en resumen diario: {str(e)}", exc_info=True)
            return {
                "success": False,
                "message": "Error al obtener resumen diario",
                "timestamp": datetime.now().isoformat(),
                "error_code": "DAILY_SUMMARY_ERROR",
                "error_details": {"error": str(e), "store": store_name}
            }
    
    # Metodos auxiliares
    
    def _map_payment_method_to_id(self, payment_method: str) -> int:
        """Mapea nombre de método de pago a ID"""
        payment_methods = {
            'Efectivo': 1,
            'Tarjeta de Crédito': 2,
            'Tarjeta de Débito': 3,
            'Transferencia': 4
        }
        return payment_methods.get(payment_method, 1)
    
    def _get_commerce_id_by_name(self, store_name: str) -> int:
        """Obtiene el ID del comercio desde su nombre"""
        commerce_map = {
            'Café Central': 2,
            'Burger Express': 4,
            'Pizza Corner': 10,
            'El Buen Sabor': 1
        }
        
        commerce_id = commerce_map.get(store_name)
        if not commerce_id:
            raise ValueError(f"Comercio '{store_name}' no encontrado")
        
        return commerce_id