"""
Settlement Controller para orquestar liquidaciones
"""
from typing import Dict, Any
import logging
from datetime import datetime

from app.services.settlement_service import SettlementService
from app.models.request_models import SettleCommerceRequest
from app.models.response_models import SettlementResponse, ErrorResponse

# Controlador para la gestion de liquidaciones
class SettlementController:
    
    # Inicialización del controlador
    def __init__(self):
        self.settlement_service = SettlementService()
        self.logger = logging.getLogger(__name__)
    
    #Procesa la liquidación de un comercio
    def settle_commerce(self, settlement_request: SettleCommerceRequest) -> Dict[str, Any]:
        
        # Logging
        try:
            self.logger.info(f"Iniciando liquidacion para comercio: {settlement_request.store_name}")
            
            # Validar datos básicos
            validation_result = self._validate_settlement_request(settlement_request)
            if not validation_result['valid']:
                return self._create_error_response(
                    message=validation_result['message'],
                    error_code="REQUEST_VALIDATION_FAILED"
                )
            
            # Obtener commerce_id
            commerce_id = self._get_commerce_id_by_name(settlement_request.store_name)
            
            # Obtener mes y año actuales
            today = datetime.now()
            
            # Llamar al servicio para crear liquidación
            result = self.settlement_service.create_monthly_settlement(
                commerce_id=commerce_id,
                year=today.year,
                month=today.month,
                created_by_user_id=1  # TODO: Obtener del contexto
            )
            
            #Si la liquidación fue exitosa regresar resultado
            if result['success']:
                return self._create_success_response(result)
            else:
                return self._create_error_response(
                    message=result.get('message', 'Error en liquidación'),
                    error_code='SETTLEMENT_ERROR'
                )
        
        # Manejo de errores
        except ValueError as ve:
            self.logger.warning(f"Error de validacion: {str(ve)}")
            return self._create_error_response(
                message=str(ve),
                error_code="VALIDATION_ERROR"
            )
            
        except Exception as e:
            error_message = f"Error en controlador de liquidaciones: {str(e)}"
            self.logger.error(error_message, exc_info=True)
            return self._create_error_response(
                message=error_message,
                error_code="CONTROLLER_ERROR"
            )
    
    # Obtener detalles de una liquidación por ID o en este caso una liquidación específica
    def get_settlement_by_id(self, settlement_id: int) -> Dict[str, Any]:
        
        try:
            self.logger.info(f"Obteniendo liquidación ID: {settlement_id}")
            
            settlement = self.settlement_service.get_settlement_details(settlement_id)
            
            # Si no se encuentra la liquidación
            if not settlement:
                return {
                    "success": False,
                    "message": f"Liquidación con ID {settlement_id} no encontrada",
                    "timestamp": datetime.now().isoformat(),
                    "error_code": "SETTLEMENT_NOT_FOUND"
                }
            
            # Regresar detalles de la liquidación si se encuentra
            return {
                "success": True,
                "message": "Detalles de liquidación obtenidos exitosamente",
                "timestamp": datetime.now().isoformat(),
                "data": settlement
            }
        
        #Error handling
        except Exception as e:
            self.logger.error(f"Error obteniendo liquidación: {str(e)}", exc_info=True)
            return {
                "success": False,
                "message": "Error al obtener detalles de liquidación",
                "timestamp": datetime.now().isoformat(),
                "error_code": "SETTLEMENT_DETAILS_ERROR",
                "error_details": {"error": str(e)}
            }
    
    #Obtiene historial de liquidaciones de un comercio
    def get_settlement_history(self, commerce_name: str, limit: int = 10) -> Dict[str, Any]:
        
        try:
            self.logger.info(f"Obteniendo historial para: {commerce_name}")
            
            #Si no se proporciona nombre del comercio
            if not commerce_name or not commerce_name.strip():
                return self._create_error_response(
                    message="El nombre del comercio es requerido",
                    error_code="MISSING_COMMERCE_NAME"
                )
            
            commerce_id = self._get_commerce_id_by_name(commerce_name)
            
            history = self.settlement_service.get_settlement_history(
                commerce_id=commerce_id,
                limit=limit
            )
            
            # Regresar historial
            return {
                'success': True,
                'message': 'Historial obtenido exitosamente',
                'data': history,
                'timestamp': datetime.now().isoformat()
            }
        
        #Error handling DEL historial
        except Exception as e:
            error_message = f"Error obteniendo historial: {str(e)}"
            self.logger.error(error_message, exc_info=True)
            return self._create_error_response(
                message=error_message,
                error_code="HISTORY_RETRIEVAL_ERROR"
            )
    
    # Calcula preview de liquidación sin crearla directamente
    def calculate_settlement_preview(self, commerce_name: str) -> Dict[str, Any]:
        
        #Calculo del preview
        try:
            self.logger.info(f"Calculando preview para: {commerce_name}")
            
            commerce_id = self._get_commerce_id_by_name(commerce_name)
            today = datetime.now()
            
            # Llamar al servicio para calcular preview
            preview = self.settlement_service.calculate_settlement_preview(
                commerce_id=commerce_id,
                year=today.year,
                month=today.month
            )
            
            # Regresar preview calculado
            return {
                'success': True,
                'message': 'Preview calculado exitosamente',
                'data': preview,
                'timestamp': datetime.now().isoformat()
            }
        
        # Manejo de errores
        except Exception as e:
            error_message = f"Error calculando preview: {str(e)}"
            self.logger.error(error_message, exc_info=True)
            return self._create_error_response(
                message=error_message,
                error_code="PREVIEW_CALCULATION_ERROR"
            )
    
    # Metodos auxiliares
    
    # Validar request de liquidación
    def _validate_settlement_request(self, request: SettleCommerceRequest) -> Dict[str, Any]:
        
        if not request.store_name or not request.store_name.strip():
            return {'valid': False, 'message': 'El nombre del comercio es requerido'}
        
        if not request.location_name or not request.location_name.strip():
            return {'valid': False, 'message': 'El nombre del local/edificio es requerido'}
        
        return {'valid': True, 'message': 'Validación exitosa'}
    
    # Crear respuesta de éxito
    def _create_success_response(self, result: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'success': True,
            'message': result.get('message', 'Liquidación procesada exitosamente'),
            'data': result,
            'timestamp': datetime.now().isoformat()
        }
    
    # Crear respuesta de error estandarizada
    def _create_error_response(self, message: str, error_code: str, details: str = None) -> Dict[str, Any]:
        return {
            'success': False,
            'message': message,
            'error_code': error_code,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
    
    #Obtiene el ID del comercio desde su nombre
    def _get_commerce_id_by_name(self, commerce_name: str) -> int:
        commerce_map = {
            'Café Central': 2,
            'Burger Express': 4,
            'Pizza Corner': 10,
            'El Buen Sabor': 1,
            'Panadería Doña María': 3,
            'Jugos Tropicales': 5
        }
        
        commerce_id = commerce_map.get(commerce_name)
        if not commerce_id:
            raise ValueError(f"Comercio '{commerce_name}' no encontrado")
        
        return commerce_id