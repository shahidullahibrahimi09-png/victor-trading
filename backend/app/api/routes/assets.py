"""Assets/Instruments endpoints."""

from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.schemas.asset import AssetResponse, AssetListResponse
from app.services.asset_service import AssetService

router = APIRouter()
asset_service = AssetService()

@router.get("/assets", response_model=AssetListResponse)
async def get_assets(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    asset_type: str = Query(None),
    search: str = Query(None)
):
    """Get all available trading assets.
    
    Query Parameters:
    - skip: Number of records to skip (default: 0)
    - limit: Number of records to return (default: 100, max: 500)
    - asset_type: Filter by asset type (crypto, forex, stock, commodity)
    - search: Search by symbol or name
    """
    try:
        assets = await asset_service.get_assets(
            skip=skip,
            limit=limit,
            asset_type=asset_type,
            search=search
        )
        return AssetListResponse(assets=assets, total=len(assets))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/assets/{symbol}", response_model=AssetResponse)
async def get_asset(symbol: str):
    """Get specific asset by symbol.
    
    Path Parameters:
    - symbol: Asset symbol (e.g., BTC/USDT)
    """
    try:
        asset = await asset_service.get_asset_by_symbol(symbol)
        if not asset:
            raise HTTPException(status_code=404, detail=f"Asset {symbol} not found")
        return AssetResponse.from_orm(asset)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/assets/type/{asset_type}", response_model=List[AssetResponse])
async def get_assets_by_type(asset_type: str):
    """Get all assets of a specific type.
    
    Path Parameters:
    - asset_type: Type of asset (crypto, forex, stock, commodity)
    """
    try:
        assets = await asset_service.get_assets_by_type(asset_type)
        return [AssetResponse.from_orm(asset) for asset in assets]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/assets/refresh")
async def refresh_assets():
    """Refresh asset list from data source."""
    try:
        count = await asset_service.refresh_assets()
        return {
            "status": "success",
            "message": f"Refreshed {count} assets",
            "count": count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
