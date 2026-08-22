"""Chart data endpoints."""

from fastapi import APIRouter, HTTPException, Query
from app.schemas.chart import ChartDataResponse, CandleResponse
from app.services.chart_service import ChartService
from typing import List

router = APIRouter()
chart_service = ChartService()

@router.get("/chart/{symbol}/{timeframe}", response_model=ChartDataResponse)
async def get_chart_data(
    symbol: str,
    timeframe: str,
    limit: int = Query(100, ge=1, le=1000)
):
    """Get chart data for an asset.
    
    Path Parameters:
    - symbol: Asset symbol (e.g., BTC/USDT)
    - timeframe: Candle timeframe (5s, 10s, 15s, 30s, 1m, 5m, 15m, 30m, 1h, 4h, 1d)
    
    Query Parameters:
    - limit: Number of candles to return (default: 100, max: 1000)
    """
    try:
        chart_data = await chart_service.get_chart_data(
            symbol=symbol,
            timeframe=timeframe,
            limit=limit
        )
        if not chart_data:
            raise HTTPException(status_code=404, detail="Chart data not available")
        return chart_data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chart/{symbol}/{timeframe}/latest", response_model=CandleResponse)
async def get_latest_candle(symbol: str, timeframe: str):
    """Get the latest candle for an asset.
    
    Path Parameters:
    - symbol: Asset symbol (e.g., BTC/USDT)
    - timeframe: Candle timeframe
    """
    try:
        candle = await chart_service.get_latest_candle(symbol, timeframe)
        if not candle:
            raise HTTPException(status_code=404, detail="Candle data not available")
        return CandleResponse.from_dict(candle)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chart/{symbol}/info")
async def get_asset_info(symbol: str):
    """Get current asset information including price and market data.
    
    Path Parameters:
    - symbol: Asset symbol
    """
    try:
        info = await chart_service.get_asset_info(symbol)
        if not info:
            raise HTTPException(status_code=404, detail=f"Asset {symbol} not found")
        return info
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
