"""
RESPONSABLE: COMPAÑERO
Modelos Pydantic para respuestas estandarizadas de la API
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


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


# TODO: Implementar ErrorResponse


# TODO: Implementar HealthCheckResponse
