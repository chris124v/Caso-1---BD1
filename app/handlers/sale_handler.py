"""
Sales Handler - Endpoints para operaciones de ventas
"""

from fastapi import APIRouter, HTTPException, Query, Path, status
from typing import Optional
from datetime import datetime
import logging

from app.controllers.sale_controller import SaleController
from app.models.request_models import RegisterSaleRequest

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/sales", tags=["Sales"])
controller = SaleController()


# Eendpoints


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_sale(sale_data: RegisterSaleRequest):
    """Registrar nueva venta usando stored procedure registerSale"""
    try:
        logger.info(f"Registrando venta para {sale_data.store_name}")
        result = controller.register_sale(sale_data)
        
        if not result.get('success'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.get('message', 'Error al registrar venta')
            )
        
        return {
            "success": True,
            "message": "Venta registrada exitosamente",
            "data": {
                "sale_id": result.get('sale_id'),
                "invoice_number": result.get('invoice_number'),
                "total_amount": float(result.get('total_amount', 0))
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al registrar venta: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno: {str(e)}"
        )


@router.get("/{sale_id}")
async def get_sale(sale_id: int = Path(..., gt=0)):
    """Obtener detalles de una venta por ID"""
    try:
        result = controller.get_sale_by_id(sale_id)
        
        if not result.get('success'):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Venta {sale_id} no encontrada"
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo venta: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/report/{store_name}")
async def get_report(
    store_name: str,
    start_date: Optional[str] = Query(None, description="YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="YYYY-MM-DD")
):
    """Generar reporte de ventas por comercio"""
    try:
        result = controller.get_sales_report(store_name, start_date, end_date)
        
        if not result.get('success'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.get('message')
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generando reporte: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/daily/{store_name}")
async def get_daily(store_name: str):
    """Resumen de ventas del día"""
    try:
        result = controller.get_daily_summary(store_name)
        
        if not result.get('success'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.get('message')
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo resumen: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )