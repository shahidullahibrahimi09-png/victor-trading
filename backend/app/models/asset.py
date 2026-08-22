"""Asset/Instrument model."""

from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.database.base import Base

class Asset(Base):
    """Trading asset/instrument model."""
    __tablename__ = "assets"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    symbol = Column(String(50), unique=True, nullable=False, index=True)  # e.g., BTC/USDT
    name = Column(String(255), nullable=False)  # e.g., Bitcoin
    asset_type = Column(String(50), nullable=False)  # crypto, forex, stock, commodity
    exchange = Column(String(100), nullable=False)  # e.g., binance, forex.com
    base_asset = Column(String(20), nullable=False)  # e.g., BTC
    quote_asset = Column(String(20), nullable=False)  # e.g., USDT
    current_price = Column(Float, nullable=True)
    price_updated_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_favorite = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<Asset {self.symbol}>"
