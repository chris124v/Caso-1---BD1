"""
RESPONSABLE: COMPAÑERO
Modelos Pydantic para respuestas estandarizadas de la API
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from decimal import Decimal



# Base class
class BaseResponse(BaseModel):
    """Modelo base para todas las respuestas"""
    success: bool = Field(..., description="Indica si la operación fue exitosa")
    message: str = Field(..., description="Mensaje descriptivo de la respuesta")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp de la respuesta")


# TODO: Implementar SaleResponse
class RegisterSaleResponse(BaseResponse):
    """Modelo para respuesta del registro de ventas"""
    sale_id: Optional[int] = Field(None, description="ID único de la venta registrada")
    invoice_number: Optional[str] = Field(None, description="Número de factura generada")
    total_amount: Optional[Decimal] = Field(None, description="Monto total de la venta", decimal_places=2)
    commission_amount: Optional[Decimal] = Field(None, description="Monto de comisión calculada", decimal_places=2)

# TODO: Implementar SettlementResponse
class SettlementResponse(BaseResponse):
    """Modelo para respuesta de liquidación de comercios (settleCommerce procedure)"""
    settlement_id: Optional[int] = Field(None, description="ID único de la liquidación")
    store_name: Optional[str] = Field(None, description="Nombre del comercio liquidado")
    location_name: Optional[str] = Field(None, description="Nombre del local/premises")
    settlement_period: Optional[str] = Field(None, description="Período de liquidación (YYYY-MM)")
    
    # Financial details
    total_sales: Optional[Decimal] = Field(None, description="Total de ventas en el período", decimal_places=2)
    commission_percentage: Optional[Decimal] = Field(None, description="Porcentaje de comisión aplicado", decimal_places=2)
    commission_owed: Optional[Decimal] = Field(None, description="Comisión adeudada al administrador", decimal_places=2)
    net_amount: Optional[Decimal] = Field(None, description="Monto neto para el comercio (ventas - comisión)", decimal_places=2)
    base_rent: Optional[Decimal] = Field(None, description="Renta base mensual", decimal_places=2)
    final_balance: Optional[Decimal] = Field(None, description="Balance final (neto - renta)", decimal_places=2)
    
    # Settlement status flags
    was_already_settled: Optional[bool] = Field(False, description="Indica si ya estaba liquidado previamente")
    settlement_date: Optional[datetime] = Field(None, description="Fecha de la liquidación")
    
    # Audit information (logged by stored procedure)
    transaction_details: Optional[Dict[str, Any]] = Field(None, description="Detalles de transacciones ejecutadas")

# TODO: Implementar ErrorResponse
class ErrorResponse(BaseResponse):
    """Modelo para respuestas de error"""
    error_code: Optional[str] = Field(None, description="Código del error")
    error_details: Optional[Dict[str, Any]] = Field(None, description="Detalles adicionales del error")

# TODO: Implementar HealthCheckResponse
class HealthCheckResponse(BaseResponse):
    """Modelo para respuesta de health check"""
    version: str = Field(..., description="Versión de la API")
    database_status: str = Field(..., description="Estado de la conexión a la base de datos")
