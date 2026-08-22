"""Asset/Instrument schemas."""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class AssetBase(BaseModel):
    """Base asset schema."""
    symbol: str = Field(..., description="Asset symbol (e.g., BTC/USDT)")
    name: str = Field(..., description="Asset name")
    asset_type: str = Field(..., description="Asset type: crypto, forex, stock, commodity")
    exchange: str = Field(..., description="Trading exchange")
    base_asset: str = Field(..., description="Base asset (e.g., BTC)")
    quote_asset: str = Field(..., description="Quote asset (e.g., USDT)")

class AssetCreate(AssetBase):
    """Create asset schema."""
    pass

class AssetResponse(AssetBase):
    """Asset response schema."""
    id: UUID
    current_price: Optional[float] = Field(None, description="Current market price")
    price_updated_at: Optional[datetime] = None
    is_active: bool = True
    is_favorite: bool = False
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class AssetListResponse(BaseModel):
    """Asset list response."""
    assets: List[AssetResponse]
    total: int = Field(..., description="Total number of assets")
