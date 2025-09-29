"""
RESPONSABLE: COMPAÑERO
Modelos Pydantic para validar datos de entrada de la API
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal

# TODO: Implementar RegisterSaleRequest

class RegisterSaleRequest (BaseModel):
    """Modelo para el registro de ventas"""
    product_name : str = Field(..., description = "Nombre del producto", min_length= 1, max_length= 255)
    store_name: str = Field(..., description="Nombre del comercio", min_length=1, max_length=255)
    quantity_sold: int = Field(..., description="Cantidad vendida", gt=0)
    amount_paid: Decimal = Field(..., description="Monto pagado", gt=0, decimal_places=2)
    payment_method: str = Field(..., description="Medio de pago", min_length=1, max_length=100)
    payment_confirmations: Optional[str] = Field(None, description="Confirmaciones de pago", max_length=500)
    reference_numbers: Optional[str] = Field(None, description="Números de referencia", max_length=500)
    invoice_number: str = Field(..., description="Número de factura", min_length=1, max_length=100)
    customer: Optional[str] = Field(None, description="Cliente", max_length=255)
    applied_discounts: Optional[Decimal] = Field(0, description="Descuentos aplicados", ge=0, decimal_places=2)


# TODO: Implementar SettleCommerceRequest

class SettleCommerceRequest(BaseModel):
    """Modelo para la liquidación de comercios (settleCommerce stored procedure)"""
    store_name: str = Field(
        ..., 
        description="Nombre del comercio (commerce/store name)",
        min_length=1, 
        max_length=255,
        alias="comercio"
    )
    location_name: str = Field(
        ..., 
        description="Nombre del local/premises (location name)",
        min_length=1, 
        max_length=255,
        alias="local"
    )

# TODO: Validaciones con Pydantic
