"""
Service layer para operaciones de liquidación mensual

Este servicio implementa la logica de negocio para liquidaciones mensuales,
calculando comisiones, rentas y generando reportes financieros.

"""

#Importamos librerias necesarias
from typing import Dict, Any, Optional, List
from datetime import datetime, date, timedelta
from decimal import Decimal
from app.repositories.settlement_repository import SettlementRepository
from app.repositories.sale_repository import SaleRepository
from app.repositories.base_repository import BaseRepository
import logging

#Servicio de liquidaciones
class SettlementService:
    
    #Llamamos a los repositories necesarios
    def __init__(self):
        self.settlement_repository = SettlementRepository()
        self.sale_repository = SaleRepository()
        self.base_repository = BaseRepository()
        self.logger = logging.getLogger(__name__)
    
    # Metodo principal para crear una liquidacion mensual, da el resultado de la liquidacion
    def create_monthly_settlement(self, commerce_id: int, year: int, month: int,
                             created_by_user_id: int) -> Dict[str, Any]:

        try:
            # Validar mes y año
            if month < 1 or month > 12:
                raise ValueError("Mes debe estar entre 1 y 12")
        
            if year < 2020 or year > 2030:
                raise ValueError("Año fuera de rango válido")
        
            # Calcular fechas del período
            period_start = date(year, month, 1)
        
            # Calcular último día del mes
            if month == 12:
                period_end = date(year, 12, 31)

            else:
                next_month = date(year, month + 1, 1)
                period_end = next_month - timedelta(days=1)
        
            self.logger.info(f"Creando liquidación - Comercio: {commerce_id}, Período: {period_start} - {period_end}")
        
            # Validar elegibilidad para liquidación
            eligibility = self.settlement_repository.validate_settlement_eligibility(
                commerce_id=commerce_id,
                period_start=period_start,
                period_end=period_end
            )

            # Si no es elegible, lanzar error
            if not eligibility['eligible']:
                raise ValueError(f"No elegible para liquidación: {eligibility['reason']}")
        
            # Crear la liquidación usando repository
            settlement_result = self.settlement_repository.create_settlement(
                commerce_id=commerce_id,
                period_start=period_start,
                period_end=period_end,
                created_by_user_id=created_by_user_id
            )
        
            # Obtener detalles del comercio para el resultado
            commerce_info = self._get_commerce_info(commerce_id)
        
            self.logger.info(f"Liquidación creada exitosamente: {settlement_result['settlement_id']}")

            # Retornar resultado detallado
            return {
                'success': True,
                'settlement_id': settlement_result['settlement_id'],
                'commerce_id': commerce_id,
                'commerce_name': commerce_info['name'],
                'period': {
                    'year': year,
                    'month': month,
                    'start_date': str(period_start),
                    'end_date': str(period_end)
                },
                'financial_summary': {
                    'total_sales': settlement_result['total_sales'],
                    'base_rent': settlement_result['base_rent'],
                    'commission_percentage': settlement_result['commission_percentage'],
                    'commission_amount': settlement_result['commission_amount'],
                    'settlement_amount': settlement_result['settlement_amount']
                },
                'created_at': datetime.now().isoformat(),
                'created_by': created_by_user_id
            }
    
        # Capturar errores de validación
        except ValueError as ve:
            self.logger.warning(f"Validación falló: {str(ve)}")
            raise ve  # Re-lanzar el ValueError original
    
        # Capturar otros errores
        except Exception as e:
            self.logger.error(f"Error creando liquidación: {str(e)}")
            raise Exception(f"Error creando liquidación: {str(e)}")
    
    # Metodo para calcular preview de liquidacion sin crearla
    def calculate_settlement_preview(self, commerce_id: int, year: int, 
                                    month: int) -> Dict[str, Any]:
        try:
            # Calcular fechas del período
            period_start = date(year, month, 1)
            
            if month == 12:
                period_end = date(year, 12, 31)
            else:
                next_month = date(year, month + 1, 1)
                period_end = next_month - timedelta(days=1)
            
            # Obtener preview del repository
            preview = self.settlement_repository.calculate_settlement_preview(
                commerce_id=commerce_id,
                period_start=period_start,
                period_end=period_end
            )
            
            # Agregar información adicional del comercio
            commerce_info = self._get_commerce_info(commerce_id)
            
            # Calcular métricas 
            metrics = self._calculate_settlement_metrics(preview)
            
            # Retornar resultado completo
            return {
                'commerce_id': commerce_id,
                'commerce_name': commerce_info['name'],
                'period': f"{year}-{month:02d}",
                'preview': preview,
                'metrics': metrics,
                'can_settle': preview['sales_count'] > 0,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error calculando preview: {str(e)}")
            raise Exception(f"Error calculando preview: {str(e)}")
    
    # Metodo para obtener historial de liquidaciones de un comercio
    def get_settlement_history(self, commerce_id: int, limit: int = 12) -> Dict[str, Any]:
        
        # Validar límite razonable
        try:
            settlements = self.settlement_repository.get_settlements_by_commerce(
                commerce_id=commerce_id,
                limit=limit
            )
            
            # Obtener info del comercio
            commerce_info = self._get_commerce_info(commerce_id)
            
            # Calcular totales acumulados
            total_accumulated = sum(s['settlement_amount'] for s in settlements)
            
            # Retornar resultado
            return {
                'commerce_id': commerce_id,
                'commerce_name': commerce_info['name'],
                'settlements_count': len(settlements),
                'settlements': settlements,
                'total_accumulated': total_accumulated,
                'retrieved_at': datetime.now().isoformat()
            }
        
        # Capturar errores
        except Exception as e:
            self.logger.error(f"Error obteniendo historial: {str(e)}")
            raise Exception(f"Error obteniendo historial: {str(e)}")
    
    # Metodo para obtener detalles completos de una liquidacion
    def get_settlement_details(self, settlement_id: int) -> Optional[Dict[str, Any]]:
        
        #Manejo de excepciones
        try:
            settlement = self.settlement_repository.get_settlement_by_id(settlement_id)
            
            if not settlement:
                return None
            
            # Agregar información de ventas del periodo
            sales = self.sale_repository.get_sales_by_date_range(
                start_date=settlement['period_start'],
                end_date=settlement['period_end'],
                commerce_id=settlement['commerce_id']
            )
            
            # Retornar resultado completo
            return {
                'settlement': settlement,
                'sales_in_period': sales,
                'sales_count': len(sales)
            }
            
        except Exception as e:
            self.logger.error(f"Error obteniendo detalles: {str(e)}")
            return None
    
    # Metodos privados
    
    #Obtiene informacion basica del comercio
    def _get_commerce_info(self, commerce_id: int) -> Dict[str, Any]:
        

        try:
            result = self.base_repository.execute_query(
                "SELECT IdCommerce, name, isActive FROM MKCommerces WHERE IdCommerce = %s",
                (commerce_id,)
            )
            
            if not result:
                raise ValueError(f"Comercio {commerce_id} no existe")
            
            return result[0]
            
        except Exception as e:
            raise Exception(f"Error obteniendo info de comercio: {str(e)}")
    
    # Calcula metricas adicionales para el preview
    def _calculate_settlement_metrics(self, preview: Dict[str, Any]) -> Dict[str, Any]:
        
        try:
            total_sales = Decimal(str(preview['total_sales']))
            commission = Decimal(str(preview['commission_amount']))
            base_rent = Decimal(str(preview['base_rent']))
            
            # Calcular porcentaje de comision sobre renta
            if base_rent > 0:
                commission_vs_rent = (commission / base_rent) * 100
            else:
                commission_vs_rent = 0
            
            # Calcular ingreso neto del comercio
            net_income = total_sales - commission
            
            return {
                'commission_vs_rent_percentage': float(commission_vs_rent),
                'net_income_commerce': float(net_income),
                'effective_commission_rate': float(preview['commission_percentage']),
                'settlement_type': preview['settlement_type']
            }
        
        # Manejo de excepciones
        except Exception:
            return {}