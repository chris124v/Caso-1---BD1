"""
RESPONSABLE: COMPAÑERO
Controlador para orquestar la lógica de negocio de ventas
"""
from typing import Dict, Any
import logging
from decimal import Decimal
from datetime import datetime

from ..models.request_models import RegisterSaleRequest
from ..models.response_models import RegisterSaleResponse, ErrorResponse
from ..services.sale_service import SaleService

logger = logging.getLogger(__name__)

# TODO: Implementar SaleController
class SaleController:
    """
    Controlador para la gestión de ventas
    Capa de lógica de negocio que orquesta las operaciones relacionadas con ventas
    
    Responsabilidades:
    - Orquestar llamadas a SaleService
    - Manejar errores y validaciones de negocio de alto nivel
    - Preparar respuestas estandarizadas según modelos Pydantic
    - Transformar datos entre formato API y formato de servicio
    """
    
    def __init__(self, sale_service: SaleService):
        """
        Inicializa el controlador con el servicio de ventas
        
        Args:
            sale_service: Instancia del servicio de ventas
        """
        self.sale_service = sale_service
    
    async def register_sale(self, sale_data: RegisterSaleRequest) -> Dict[str, Any]:
        """
        Procesa el registro de una nueva venta
        
        IMPORTANTE: Este método transforma el RegisterSaleRequest (formato API)
        al formato que espera el SaleService (commerce_id, cashier_user_id, items)
        
        Args:
            sale_data: Datos de la venta desde la API (RegisterSaleRequest)
            
        Returns:
            Diccionario con RegisterSaleResponse o ErrorResponse
        """
        try:
            logger.info(f"🛒 Iniciando registro de venta para '{sale_data.store_name}'")
            logger.debug(f"Detalles: Producto='{sale_data.product_name}', Cantidad={sale_data.quantity_sold}, Monto=${sale_data.amount_paid}")
            
            # ✅ Validaciones de negocio de alto nivel ANTES de llamar al servicio
            self._validate_sale_business_rules(sale_data)
            
            # 🔄 TRANSFORMACIÓN: De RegisterSaleRequest a formato del servicio
            # El servicio espera: commerce_id, cashier_user_id, items, payment_method_id
            # Necesitaremos obtener estos IDs desde los nombres
            
            # TODO: Implementar lookup de IDs (por ahora usamos valores mock)
            # En producción, necesitarías:
            # commerce_id = await self._get_commerce_id_by_name(sale_data.store_name)
            # product_id = await self._get_product_id_by_name(sale_data.product_name)
            # payment_method_id = await self._get_payment_method_id(sale_data.payment_method)
            
            # MOCK DATA - Reemplazar con lookups reales
            commerce_id = 1  # TODO: Lookup real
            cashier_user_id = 1  # TODO: Obtener del contexto de autenticación
            payment_method_id = self._map_payment_method_to_id(sale_data.payment_method)
            
            # Construir items en el formato que espera el servicio
            items = [{
                'product_id': 1,  # TODO: Lookup real desde sale_data.product_name
                'quantity': sale_data.quantity_sold,
                'unit_price': float(sale_data.amount_paid / sale_data.quantity_sold)
            }]
            
            # ✅ Orquestar llamada al servicio
            result = self.sale_service.process_sale(
                commerce_id=commerce_id,
                cashier_user_id=cashier_user_id,
                items=items,
                payment_method_id=payment_method_id
            )
            
            # ✅ Preparar respuesta estandarizada según modelo Pydantic
            response_data = RegisterSaleResponse(
                success=True,
                message="Venta registrada exitosamente",
                sale_id=result.get('sale_id'),
                invoice_number=sale_data.invoice_number,
                total_amount=Decimal(str(result.get('total_amount', sale_data.amount_paid))),
                commission_amount=Decimal('0.00')  # El servicio no retorna comisión aquí
            )
            
            logger.info(f"✅ Venta registrada - ID: {result.get('sale_id')}, Referencia: {result.get('reference_number')}")
            return response_data.model_dump()
            
        except ValueError as ve:
            # ✅ Manejo de errores de validación (del servicio o del controller)
            logger.warning(f"⚠️ Error de validación: {str(ve)}")
            error_response = ErrorResponse(
                success=False,
                message="Error de validación en los datos de venta",
                error_code="VALIDATION_ERROR",
                error_details={
                    "validation_error": str(ve),
                    "store": sale_data.store_name,
                    "invoice": sale_data.invoice_number
                }
            )
            return error_response.model_dump()
            
        except Exception as e:
            # ✅ Manejo de errores inesperados
            logger.error(f"❌ Error inesperado al registrar venta: {str(e)}", exc_info=True)
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
    
    def _validate_sale_business_rules(self, sale_data: RegisterSaleRequest) -> None:
        """
        Valida reglas de negocio específicas de alto nivel
        
        Estas son validaciones ADICIONALES a las que hace el servicio.
        El servicio valida stock, comercio activo, etc.
        Aquí validamos reglas de la capa de API/presentación.
        
        Args:
            sale_data: Datos de la venta a validar
            
        Raises:
            ValueError: Si alguna regla no se cumple
        """
        logger.debug(f"🔍 Validando reglas de negocio para venta: {sale_data.invoice_number}")
        
        # Regla 1: Descuentos razonables
        if sale_data.applied_discounts and sale_data.applied_discounts >= sale_data.amount_paid:
            raise ValueError(
                f"Los descuentos (${sale_data.applied_discounts}) no pueden ser "
                f">= al monto pagado (${sale_data.amount_paid})"
            )
        
        # Regla 2: Cantidad razonable
        if sale_data.quantity_sold > 1000:
            raise ValueError(f"Cantidad excesiva: {sale_data.quantity_sold} unidades")
        
        # Regla 3: Formato de factura válido
        if not sale_data.invoice_number.replace('-', '').replace('_', '').isalnum():
            raise ValueError(f"Formato de factura inválido: '{sale_data.invoice_number}'")
        
        # Regla 4: Monto mínimo
        min_amount = Decimal('0.50')
        if sale_data.amount_paid < min_amount:
            raise ValueError(f"Monto mínimo no alcanzado: ${sale_data.amount_paid} < ${min_amount}")
        
        logger.debug("✅ Validaciones de reglas de negocio completadas")
    
    async def get_sale_summary(
        self, 
        store_name: str, 
        date_from: datetime = None, 
        date_to: datetime = None
    ) -> Dict[str, Any]:
        """
        Obtiene resumen de ventas usando el get_sales_report del servicio
        
        Args:
            store_name: Nombre del comercio
            date_from: Fecha inicial (opcional, default: inicio del mes)
            date_to: Fecha final (opcional, default: hoy)
            
        Returns:
            Diccionario con resumen de ventas
        """
        try:
            logger.info(f"📊 Obteniendo resumen de ventas para '{store_name}'")
            
            # Preparar fechas por defecto si no se proporcionan
            if not date_from:
                date_from = datetime(date.today().year, date.today().month, 1)
            if not date_to:
                date_to = datetime.now()
            
            # Convertir datetime a string formato YYYY-MM-DD
            start_date = date_from.strftime('%Y-%m-%d')
            end_date = date_to.strftime('%Y-%m-%d')
            
            logger.debug(f"Período: {start_date} a {end_date}")
            
            # TODO: Lookup de commerce_id desde store_name
            commerce_id = 1  # Mock - reemplazar con lookup real
            
            # Llamar al servicio (método síncrono)
            report = self.sale_service.get_sales_report(
                commerce_id=commerce_id,
                start_date=start_date,
                end_date=end_date
            )
            
            logger.info(f"✅ Resumen obtenido: {report.get('sales_count', 0)} ventas")
            
            # Preparar respuesta estandarizada
            return {
                "success": True,
                "message": "Resumen de ventas obtenido exitosamente",
                "timestamp": datetime.now(),
                "data": {
                    "store_name": store_name,
                    "period": report.get('period'),
                    "total_sales": report.get('sales_count'),
                    "total_amount": report.get('total_sales'),
                    "commission_amount": report.get('commission_amount'),
                    "base_rent": report.get('base_rent'),
                    "sales_list": report.get('sales_list', [])
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Error al obtener resumen: {str(e)}", exc_info=True)
            return {
                "success": False,
                "message": "Error al obtener resumen de ventas",
                "timestamp": datetime.now(),
                "error_code": "SUMMARY_ERROR",
                "error_details": {"error": str(e), "store": store_name}
            }
    
    async def get_daily_summary(self, store_name: str) -> Dict[str, Any]:
        """
        Obtiene resumen diario de ventas
        
        Args:
            store_name: Nombre del comercio
            
        Returns:
            Diccionario con resumen del día
        """
        try:
            logger.info(f"📅 Obteniendo resumen diario para '{store_name}'")
            
            # TODO: Lookup de commerce_id
            commerce_id = 1  # Mock
            
            # Llamar al servicio
            summary = self.sale_service.get_daily_sales_summary(commerce_id)
            
            return {
                "success": True,
                "message": "Resumen diario obtenido exitosamente",
                "timestamp": datetime.now(),
                "data": {
                    "store_name": store_name,
                    "date": summary.get('date'),
                    "total_sales_today": summary.get('total_sales_today'),
                    "transactions_count": summary.get('transactions_today'),
                    "recent_sales": summary.get('recent_sales', [])
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Error en resumen diario: {str(e)}", exc_info=True)
            return {
                "success": False,
                "message": "Error al obtener resumen diario",
                "timestamp": datetime.now(),
                "error_code": "DAILY_SUMMARY_ERROR",
                "error_details": {"error": str(e), "store": store_name}
            }
    
    async def get_sale_by_id(self, sale_id: int) -> Dict[str, Any]:
        """
        Obtiene detalles de una venta específica
        
        Args:
            sale_id: ID de la venta
            
        Returns:
            Diccionario con detalles de la venta
        """
        try:
            logger.info(f"🔍 Obteniendo venta ID: {sale_id}")
            
            # Llamar al servicio (método síncrono)
            sale_details = self.sale_service.get_sale_details(sale_id)
            
            if not sale_details:
                logger.warning(f"⚠️ Venta no encontrada: ID {sale_id}")
                return {
                    "success": False,
                    "message": f"Venta con ID {sale_id} no encontrada",
                    "timestamp": datetime.now(),
                    "error_code": "SALE_NOT_FOUND"
                }
            
            logger.info(f"✅ Venta encontrada: ID {sale_id}")
            return {
                "success": True,
                "message": "Detalles de venta obtenidos exitosamente",
                "timestamp": datetime.now(),
                "data": sale_details
            }
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo venta: {str(e)}", exc_info=True)
            return {
                "success": False,
                "message": "Error al obtener detalles de venta",
                "timestamp": datetime.now(),
                "error_code": "SALE_DETAILS_ERROR",
                "error_details": {"error": str(e), "sale_id": sale_id}
            }
    
    # Métodos auxiliares privados
    
    def _map_payment_method_to_id(self, payment_method: str) -> int:
        """
        Mapea nombre de método de pago a ID
        
        TODO: Reemplazar con lookup real en base de datos
        """
        payment_methods = {
            'Efectivo': 1,
            'Tarjeta de Crédito': 2,
            'Tarjeta de Débito': 3,
            'Transferencia': 4,
            'SINPE Móvil': 5,
            'PayPal': 6
        }
        return payment_methods.get(payment_method, 1)  # Default: Efectivo
    
    async def _get_commerce_id_by_name(self, store_name: str) -> int:
        """
        Obtiene el ID del comercio desde su nombre
        
        TODO: Implementar lookup real
        Args:
            store_name: Nombre del comercio
            
        Returns:
            ID del comercio
            
        Raises:
            ValueError: Si el comercio no existe
        """
        # Mock implementation
        # En producción, hacer query a base de datos:
        # SELECT IdCommerce FROM MKCommerces WHERE name = %s
        return 1
    
    async def _get_product_id_by_name(self, product_name: str, commerce_id: int) -> int:
        """
        Obtiene el ID del producto desde su nombre
        
        TODO: Implementar lookup real
        Args:
            product_name: Nombre del producto
            commerce_id: ID del comercio
            
        Returns:
            ID del producto
            
        Raises:
            ValueError: Si el producto no existe
        """
        # Mock implementation
        # En producción, hacer query:
        # SELECT IdProduct FROM MKProducts 
        # WHERE name = %s AND IdCommerceFK = %s
        return 1    