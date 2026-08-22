"""Analysis request/response schemas."""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID

class AnalysisRequest(BaseModel):
    """Analysis request schema."""
    symbol: str = Field(..., description="Asset symbol (e.g., BTC/USDT)")
    timeframe: str = Field(..., description="Chart timeframe (1m, 5m, 15m, 1h, 4h, 1d)")
    include_history: bool = Field(False, description="Include multi-timeframe analysis")

class IndicatorValue(BaseModel):
    """Single indicator value."""
    name: str
    value: float
    signal: Optional[str] = None  # bullish, bearish, neutral
    status: str = Field(default="calculating")  # calculating, valid, stale

class AnalysisResponse(BaseModel):
    """Analysis response schema."""
    id: Optional[UUID] = None
    symbol: str = Field(..., description="Asset symbol")
    timeframe: str = Field(..., description="Chart timeframe")
    signal: str = Field(..., description="Signal: UP, DOWN, or WAIT", regex="^(UP|DOWN|WAIT)$")
    confidence: float = Field(..., ge=0, le=100, description="Confidence percentage (0-100)")
    risk_level: str = Field(..., description="Risk level: LOW, MEDIUM, HIGH", regex="^(LOW|MEDIUM|HIGH)$")
    trend: Optional[str] = Field(None, description="Market trend")
    reasons: List[str] = Field(default=[], description="List of analysis reasons")
    indicators: List[IndicatorValue] = Field(default=[], description="Indicator values")
    support_level: Optional[float] = Field(None, description="Support level")
    resistance_level: Optional[float] = Field(None, description="Resistance level")
    current_price: float = Field(..., description="Current asset price")
    main_reason: Optional[str] = Field(None, description="Primary analysis reason")
    secondary_reasons: List[str] = Field(default=[], description="Secondary reasons")
    market_structure: Optional[str] = Field(None, description="Current market structure")
    volatility: Optional[str] = Field(None, description="Volatility level")
    multi_timeframe_confirmation: Optional[Dict[str, Any]] = Field(None, description="Multi-timeframe data")
    created_at: Optional[datetime] = None
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create from dictionary."""
        return cls(**data)
    
    class Config:
        from_attributes = True
