"""Settings endpoints."""

from fastapi import APIRouter, HTTPException
from app.schemas.settings import SettingsUpdateRequest, SettingsResponse
from app.services.settings_service import SettingsService

router = APIRouter()
settings_service = SettingsService()

@router.get("/settings", response_model=SettingsResponse)
async def get_settings():
    """Get current application settings."""
    try:
        settings = await settings_service.get_settings()
        return SettingsResponse.from_orm(settings)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/settings", response_model=SettingsResponse)
async def update_settings(request: SettingsUpdateRequest):
    """Update application settings.
    
    Request Body:
    - theme: Display theme (dark, light)
    - language: Application language
    - default_timeframe: Default chart timeframe
    - enable_notifications: Enable/disable notifications
    - selected_indicators: List of indicators to display
    - risk_tolerance: Risk tolerance level (low, medium, high)
    - And more...
    """
    try:
        settings = await settings_service.update_settings(request)
        return SettingsResponse.from_orm(settings)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/settings/indicators")
async def get_available_indicators():
    """Get list of available technical indicators."""
    return {
        "indicators": [
            {
                "name": "RSI",
                "description": "Relative Strength Index",
                "period": 14,
                "range": "0-100"
            },
            {
                "name": "MACD",
                "description": "Moving Average Convergence Divergence",
                "fast_period": 12,
                "slow_period": 26,
                "signal_period": 9
            },
            {
                "name": "Bollinger Bands",
                "description": "Volatility and Support/Resistance",
                "period": 20,
                "std_dev": 2
            },
            {
                "name": "Moving Average",
                "description": "Simple Moving Average",
                "periods": [20, 50, 100, 200]
            },
            {
                "name": "EMA",
                "description": "Exponential Moving Average",
                "periods": [12, 26, 50]
            },
            {
                "name": "Stochastic",
                "description": "Momentum Indicator",
                "k_period": 14,
                "d_period": 3
            },
            {
                "name": "ATR",
                "description": "Average True Range",
                "period": 14
            },
            {
                "name": "Momentum",
                "description": "Price Momentum",
                "period": 10
            }
        ]
    }

@router.get("/settings/timeframes")
async def get_available_timeframes():
    """Get list of available chart timeframes."""
    return {
        "timeframes": [
            {"code": "5s", "name": "5 Seconds", "seconds": 5},
            {"code": "10s", "name": "10 Seconds", "seconds": 10},
            {"code": "15s", "name": "15 Seconds", "seconds": 15},
            {"code": "30s", "name": "30 Seconds", "seconds": 30},
            {"code": "1m", "name": "1 Minute", "seconds": 60},
            {"code": "5m", "name": "5 Minutes", "seconds": 300},
            {"code": "15m", "name": "15 Minutes", "seconds": 900},
            {"code": "30m", "name": "30 Minutes", "seconds": 1800},
            {"code": "1h", "name": "1 Hour", "seconds": 3600},
            {"code": "4h", "name": "4 Hours", "seconds": 14400},
            {"code": "1d", "name": "1 Day", "seconds": 86400}
        ]
    }
