"""Analysis result model."""

from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, JSON, Integer
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.database.base import Base

class Analysis(Base):
    """Stored analysis result."""
    __tablename__ = "analyses"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    asset_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    symbol = Column(String(50), nullable=False)  # e.g., BTC/USDT
    timeframe = Column(String(20), nullable=False)  # e.g., 1h, 4h, 1d
    signal = Column(String(10), nullable=False)  # UP, DOWN, WAIT
    confidence = Column(Float, nullable=False)  # 0-100
    risk_level = Column(String(20), nullable=False)  # LOW, MEDIUM, HIGH
    trend = Column(String(50), nullable=True)  # e.g., Bullish, Bearish
    reasons = Column(JSON, nullable=True)  # List of analysis reasons
    indicators = Column(JSON, nullable=True)  # Indicator values and signals
    support_level = Column(Float, nullable=True)
    resistance_level = Column(Float, nullable=True)
    current_price = Column(Float, nullable=False)
    analysis_data = Column(JSON, nullable=True)  # Full analysis data for reference
    is_correct = Column(String(10), nullable=True)  # CORRECT, INCORRECT, PENDING
    actual_result = Column(String(10), nullable=True)  # UP, DOWN, SIDEWAYS
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    def __repr__(self):
        return f"<Analysis {self.symbol} {self.timeframe} {self.signal}>"
