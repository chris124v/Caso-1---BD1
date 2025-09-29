

from typing import Dict, Any
from app.services.settlement_service import SettlementService
from app.models.request_models import SettleCommerceRequest
from app.models.response_models import SettlementResponse, ErrorResponse
import logging
from datetime import datetime

class SettlementController:
    """Controlador para orquestrar la lógica de negocio de liquidaciones"""
    
    def __init__(self):
        self.settlement_service = SettlementService()
        self.logger = logging.getLogger(__name__)
    
    def settle_commerce(self, settlement_request: SettleCommerceRequest) -> Dict[str, Any]:
        """
        Orquestar la liquidación de un comercio
        """
        try:
            self.logger.info(f"Iniciando liquidación para comercio: {settlement_request.commerce_name}")
            
            # Validar datos básicos
            validation_result = self._validate_settlement_request(settlement_request)
            if not validation_result['valid']:
                return self._create_error_response(
                    message=validation_result['message'],
                    error_code="REQUEST_VALIDATION_FAILED"
                )
            
            # Procesar la liquidación
            result = self.settlement_service.process_settlement(settlement_request)
            
            if result['success']:
                return self._create_success_response(result)
            else:
                return self._create_error_response(
                    message=result['message'],
                    error_code=result.get('error_code', 'SETTLEMENT_PROCESSING_FAILED')
                )
                
        except Exception as e:
            error_message = f"Error en controlador de liquidaciones: {str(e)}"
            self.logger.error(error_message)
            return self._create_error_response(
                message=error_message,
                error_code="CONTROLLER_ERROR"
            )
    
    def check_settlement_status(self, commerce_name: str, location_name: str) -> Dict[str, Any]:
        """
        Verificar estado de liquidación de un comercio
        """
        try:
            self.logger.info(f"Verificando estado de liquidación: {commerce_name} - {location_name}")
            
            # Validar parámetros
            if not commerce_name or not commerce_name.strip():
                return self._create_error_response(
                    message="El nombre del comercio es requerido",
                    error_code="MISSING_COMMERCE_NAME"
                )
            
            if not location_name or not location_name.strip():
                return self._create_error_response(
                    message="El nombre del local/edificio es requerido",
                    error_code="MISSING_LOCATION_NAME"
                )
            
            # Verificar estado
            status = self.settlement_service.settlement_repository.check_settlement_status(
                commerce_name, location_name
            )
            
            return {
                'success': True,
                'message': 'Estado de liquidación obtenido exitosamente',
                'data': status,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            error_message = f"Error verificando estado de liquidación: {str(e)}"
            self.logger.error(error_message)
            return self._create_error_response(
                message=error_message,
                error_code="STATUS_CHECK_ERROR"
            )
    
    def get_settlement_history(self, commerce_name: str, limit: int = 10) -> Dict[str, Any]:
        """
        Obtener historial de liquidaciones de un comercio
        """
        try:
            self.logger.info(f"Obteniendo historial de liquidaciones para: {commerce_name}")
            
            # Validar parámetros
            if not commerce_name or not commerce_name.strip():
                return self._create_error_response(
                    message="El nombre del comercio es requerido",
                    error_code="MISSING_COMMERCE_NAME"
                )
            
            if limit <= 0 or limit > 100:
                limit = 10  # Valor por defecto
            
            # Obtener historial
            history = self.settlement_service.settlement_repository.get_settlement_history(
                commerce_name, limit
            )
            
            return {
                'success': True,
                'message': 'Historial de liquidaciones obtenido exitosamente',
                'data': {
                    'commerce_name': commerce_name,
                    'settlements': history,
                    'count': len(history)
                },
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            error_message = f"Error obteniendo historial de liquidaciones: {str(e)}"
            self.logger.error(error_message)
            return self._create_error_response(
                message=error_message,
                error_code="HISTORY_RETRIEVAL_ERROR"
            )
    
    def get_settlement_dashboard(self) -> Dict[str, Any]:
        """
        Obtener dashboard de liquidaciones del mes actual
        """
        try:
            self.logger.info("Generando dashboard de liquidaciones")
            
            # Obtener dashboard
            dashboard = self.settlement_service.get_settlement_dashboard()
            
            if dashboard['success']:
                return {
                    'success': True,
                    'message': 'Dashboard generado exitosamente',
                    'data': dashboard,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return self._create_error_response(
                    message=dashboard['message'],
                    error_code="DASHBOARD_GENERATION_FAILED"
                )
                
        except Exception as e:
            error_message = f"Error generando dashboard: {str(e)}"
            self.logger.error(error_message)
            return self._create_error_response(
                message=error_message,
                error_code="DASHBOARD_ERROR"
            )
    
    def get_monthly_settlements(self) -> Dict[str, Any]:
        """
        Obtener todas las liquidaciones del mes actual
        """
        try:
            self.logger.info("Obteniendo liquidaciones del mes actual")
            
            settlements = self.settlement_service.settlement_repository.get_current_month_settlements()
            
            # Calcular estadísticas básicas
            total_settlements = len(settlements)
            total_sales = sum(s['total_sales'] for s in settlements)
            total_commission = sum(s['total_commission'] for s in settlements)
            total_rent = sum(s['total_rent'] for s in settlements)
            
            return {
                'success': True,
                'message': 'Liquidaciones del mes obtenidas exitosamente',
                'data': {
                    'period': f"{datetime.now().strftime('%Y-%m')}",
                    'summary': {
                        'total_settlements': total_settlements,
                        'total_sales_amount': total_sales,
                        'total_commission': total_commission,
                        'total_rent': total_rent,
                        'average_sales': total_sales / total_settlements if total_settlements > 0 else 0
                    },
                    'settlements': settlements
                },
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            error_message = f"Error obteniendo liquidaciones mensuales: {str(e)}"
            self.logger.error(error_message)
            return self._create_error_response(
                message=error_message,
                error_code="MONTHLY_SETTLEMENTS_ERROR"
            )
    
    def _validate_settlement_request(self, request: SettleCommerceRequest) -> Dict[str, Any]:
        """Validar request de liquidación"""
        
        if not request.commerce_name or not request.commerce_name.strip():
            return {'valid': False, 'message': 'El nombre del comercio es requerido'}
        
        if not request.location_name or not request.location_name.strip():
            return {'valid': False, 'message': 'El nombre del local/edificio es requerido'}
        
        if request.approved_by_user_id <= 0:
            return {'valid': False, 'message': 'ID de usuario aprobador inválido'}
        
        return {'valid': True, 'message': 'Validación exitosa'}
    
    def _create_success_response(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Crear respuesta de éxito estandarizada"""
        return {
            'success': True,
            'message': result.get('message', 'Liquidación procesada exitosamente'),
            'data': {
                'settlement_id': result.get('settlement_id'),
                'commerce_name': result.get('commerce_name'),
                'settlement_period': result.get('settlement_period'),
                'total_sales_amount': result.get('total_sales_amount'),
                'total_commission': result.get('total_commission'),
                'total_rent': result.get('total_rent'),
                'net_settlement_amount': result.get('net_settlement_amount'),
                'already_settled': result.get('already_settled'),
                'pre_settlement_analysis': result.get('pre_settlement_analysis'),
                'settlement_metrics': result.get('settlement_metrics'),
                'recommendations': result.get('recommendations')
            },
            'timestamp': datetime.now().isoformat()
        }
    
    def _create_error_response(self, message: str, error_code: str, details: str = None) -> Dict[str, Any]:
        """Crear respuesta de error estandarizada"""
        return {
            'success': False,
            'message': message,
            'error_code': error_code,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }