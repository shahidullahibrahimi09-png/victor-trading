"""Analysis history endpoints."""

from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.schemas.analysis import AnalysisResponse
from app.services.history_service import HistoryService

router = APIRouter()
history_service = HistoryService()

@router.get("/history", response_model=List[AnalysisResponse])
async def get_analysis_history(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    symbol: str = Query(None),
    timeframe: str = Query(None),
    signal: str = Query(None)
):
    """Get analysis history with optional filters.
    
    Query Parameters:
    - skip: Number of records to skip
    - limit: Number of records to return
    - symbol: Filter by asset symbol
    - timeframe: Filter by timeframe
    - signal: Filter by signal (UP, DOWN, WAIT)
    """
    try:
        analyses = await history_service.get_analysis_history(
            skip=skip,
            limit=limit,
            symbol=symbol,
            timeframe=timeframe,
            signal=signal
        )
        return [AnalysisResponse.from_dict(a) for a in analyses]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/accuracy")
async def get_accuracy_stats(
    symbol: str = Query(None),
    timeframe: str = Query(None),
    days: int = Query(30, ge=1, le=365)
):
    """Get accuracy statistics for predictions.
    
    Query Parameters:
    - symbol: Filter by symbol
    - timeframe: Filter by timeframe
    - days: Number of days to include (default: 30)
    """
    try:
        stats = await history_service.get_accuracy_stats(
            symbol=symbol,
            timeframe=timeframe,
            days=days
        )
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{analysis_id}")
async def get_analysis_detail(analysis_id: str):
    """Get detailed information about a specific analysis.
    
    Path Parameters:
    - analysis_id: UUID of the analysis
    """
    try:
        analysis = await history_service.get_analysis_by_id(analysis_id)
        if not analysis:
            raise HTTPException(status_code=404, detail="Analysis not found")
        return AnalysisResponse.from_dict(analysis)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/history/{analysis_id}/outcome")
async def update_analysis_outcome(
    analysis_id: str,
    outcome: str = Query(..., regex="^(UP|DOWN|SIDEWAYS)$"),
    actual_price: float = Query(...)
):
    """Update analysis with actual outcome for accuracy tracking.
    
    Path Parameters:
    - analysis_id: UUID of the analysis
    
    Query Parameters:
    - outcome: Actual market outcome (UP, DOWN, SIDEWAYS)
    - actual_price: Actual closing price at outcome time
    """
    try:
        result = await history_service.update_outcome(
            analysis_id=analysis_id,
            outcome=outcome,
            actual_price=actual_price
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
