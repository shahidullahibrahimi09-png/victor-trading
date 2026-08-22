"""Chart data schemas."""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class CandleResponse(BaseModel):
    """Single candlestick schema."""
    time: datetime = Field(..., description="Candle open time")
    open: float = Field(..., description="Opening price")
    high: float = Field(..., description="Highest price")
    low: float = Field(..., description="Lowest price")
    close: float = Field(..., description="Closing price")
    volume: Optional[float] = Field(None, description="Trading volume")
    is_complete: bool = Field(True, description="Whether candle is complete")
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create from dictionary."""
        return cls(**data)

class ChartDataResponse(BaseModel):
    """Chart data response."""
    symbol: str = Field(..., description="Asset symbol")
    timeframe: str = Field(..., description="Chart timeframe")
    candles: List[CandleResponse] = Field(..., description="List of candles")
    current_price: float = Field(..., description="Current price")
    previous_close: Optional[float] = Field(None, description="Previous close price")
    price_change: Optional[float] = Field(None, description="Price change in units")
    price_change_percent: Optional[float] = Field(None, description="Price change percentage")
    timestamp: datetime = Field(..., description="Data timestamp")
    data_source: str = Field(default="binance", description="Data source")
    is_real_time: bool = Field(True, description="Whether data is real-time")
    
    class Config:
        from_attributes = True
