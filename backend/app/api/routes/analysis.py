"""Analysis endpoints."""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.schemas.analysis import AnalysisRequest, AnalysisResponse
from app.services.analysis_service import AnalysisService
import logging

router = APIRouter()
analysis_service = AnalysisService()
logger = logging.getLogger(__name__)

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze(
    request: AnalysisRequest,
    background_tasks: BackgroundTasks
):
    """Run AI analysis on an asset and timeframe.
    
    Request Body:
    - symbol: Asset symbol (e.g., BTC/USDT)
    - timeframe: Candle timeframe (1m, 5m, 15m, 1h, 4h, 1d)
    - include_history: Include multiple timeframe analysis (optional)
    
    Returns:
    - signal: UP, DOWN, or WAIT
    - confidence: Confidence percentage (0-100)
    - reasons: List of analysis reasons
    - indicators: Technical indicator values
    - risk_level: Risk assessment (LOW, MEDIUM, HIGH)
    """
    try:
        logger.info(f"Analysis requested for {request.symbol} {request.timeframe}")
        
        # Run analysis
        analysis_result = await analysis_service.analyze(
            symbol=request.symbol,
            timeframe=request.timeframe,
            include_history=request.include_history
        )
        
        if not analysis_result:
            raise HTTPException(
                status_code=400,
                detail="Unable to perform analysis. Insufficient data available."
            )
        
        # Store result in background
        background_tasks.add_task(
            analysis_service.store_analysis,
            analysis_result
        )
        
        return AnalysisResponse.from_dict(analysis_result)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Analysis error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze/quick")
async def quick_analyze(request: AnalysisRequest):
    """Quick 5-second analysis for short-term predictions.
    
    Performs fast analysis with latest data only.
    """
    try:
        logger.info(f"Quick analysis requested for {request.symbol} {request.timeframe}")
        
        result = await analysis_service.quick_analyze(
            symbol=request.symbol,
            timeframe=request.timeframe
        )
        
        if not result:
            raise HTTPException(
                status_code=400,
                detail="Quick analysis unavailable"
            )
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Quick analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analyze/info")
async def analysis_info():
    """Get information about analysis capabilities."""
    return {
        "supported_timeframes": [
            "5s", "10s", "15s", "30s",
            "1m", "5m", "15m", "30m",
            "1h", "4h", "1d"
        ],
        "supported_indicators": [
            "RSI", "MACD", "Bollinger Bands", "Moving Averages",
            "Stochastic", "ATR", "Momentum", "Volume"
        ],
        "analysis_types": [
            "candlestick_patterns",
            "price_action",
            "technical_indicators",
            "trend_analysis",
            "support_resistance",
            "multi_timeframe"
        ],
        "signals": ["UP", "DOWN", "WAIT"],
        "risk_levels": ["LOW", "MEDIUM", "HIGH"],
        "confidence_scale": "0-100"
    }
