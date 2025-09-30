"""
Settlement Handler - Endpoints para operaciones de liquidaciones
"""

from fastapi import APIRouter, HTTPException, Query, Path, status
from typing import Optional
from datetime import datetime
import logging

from app.controllers.settlement_controller import SettlementController
from app.models.request_models import SettleCommerceRequest

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/settlements", tags=["Settlements"])
controller = SettlementController()

# ENDPOINTS

@router.post("/settle", status_code=status.HTTP_201_CREATED)
async def settle_commerce(request: SettleCommerceRequest):
    """Liquidar un comercio usando stored procedure settleCommerce"""
    try:
        logger.info(f"Liquidando comercio: {request.store_name}")
        result = controller.settle_commerce(request)
        
        if not result.get('success'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.get('message', 'Error al liquidar comercio')
            )
        
        # Verificar si ya estaba liquidado
        data = result.get('data', {})
        already_settled = data.get('already_settled', False)
        
        return {
            "success": True,
            "message": result.get('message'),
            "already_settled": already_settled,
            "data": {
                "settlement_id": data.get('settlement_id'),
                "commerce_name": data.get('commerce_name'),
                "period": data.get('period'),
                "financial_summary": data.get('financial_summary')
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al liquidar comercio: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno: {str(e)}"
        )


@router.get("/{settlement_id}")
async def get_settlement(settlement_id: int = Path(..., gt=0)):
    """Obtener detalles de una liquidación por ID"""
    try:
        result = controller.get_settlement_by_id(settlement_id)
        
        if not result.get('success'):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Liquidación {settlement_id} no encontrada"
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo liquidación: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/history/{commerce_name}")
async def get_history(
    commerce_name: str,
    limit: int = Query(10, ge=1, le=50, description="Límite de resultados")
):
    """Obtener historial de liquidaciones de un comercio"""
    try:
        result = controller.get_settlement_history(commerce_name, limit)
        
        if not result.get('success'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.get('message')
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo historial: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/preview/{commerce_name}")
async def get_preview(commerce_name: str):
    """Calcular preview de liquidación sin crearla"""
    try:
        result = controller.calculate_settlement_preview(commerce_name)
        
        if not result.get('success'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.get('message')
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error calculando preview: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )