"""Settings schemas."""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID

class SettingsUpdateRequest(BaseModel):
    """Settings update request."""
    theme: Optional[str] = Field(None, description="Display theme: dark, light")
    language: Optional[str] = Field(None, description="Application language")
    chart_style: Optional[str] = Field(None, description="Chart display style")
    default_timeframe: Optional[str] = Field(None, description="Default chart timeframe")
    enable_notifications: Optional[bool] = None
    notify_on_signal: Optional[bool] = None
    notify_on_analysis: Optional[bool] = None
    notify_on_error: Optional[bool] = None
    show_volume: Optional[bool] = None
    show_indicators: Optional[bool] = None
    selected_indicators: Optional[List[str]] = None
    confidence_threshold: Optional[str] = Field(None, description="low, medium, high")
    risk_tolerance: Optional[str] = Field(None, description="low, medium, high")
    primary_data_source: Optional[str] = None
    update_frequency: Optional[str] = None

class SettingsResponse(BaseModel):
    """Settings response."""
    id: UUID
    user_id: Optional[UUID] = None
    theme: str = "dark"
    language: str = "en"
    chart_style: str = "candlestick"
    default_timeframe: str = "1h"
    enable_notifications: bool = True
    notify_on_signal: bool = True
    notify_on_analysis: bool = False
    notify_on_error: bool = True
    show_volume: bool = True
    show_indicators: bool = True
    selected_indicators: List[str] = []
    confidence_threshold: str = "medium"
    risk_tolerance: str = "medium"
    primary_data_source: str = "binance"
    update_frequency: str = "real-time"
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
