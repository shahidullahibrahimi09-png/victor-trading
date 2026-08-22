"""Prediction tracking model."""

from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, JSON, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.database.base import Base

class Prediction(Base):
    """Prediction history for backtesting and accuracy tracking."""
    __tablename__ = "predictions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    analysis_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    symbol = Column(String(50), nullable=False, index=True)
    timeframe = Column(String(20), nullable=False)
    predicted_signal = Column(String(10), nullable=False)  # UP, DOWN, WAIT
    predicted_confidence = Column(Float, nullable=False)
    predicted_at = Column(DateTime, nullable=False)
    entry_price = Column(Float, nullable=False)
    target_price = Column(Float, nullable=True)
    stop_loss = Column(Float, nullable=True)
    
    # Outcome
    outcome_signal = Column(String(10), nullable=True)  # UP, DOWN, SIDEWAYS
    exit_price = Column(Float, nullable=True)
    exit_time = Column(DateTime, nullable=True)
    is_correct = Column(Boolean, nullable=True)
    profit_loss_percent = Column(Float, nullable=True)
    hold_duration_minutes = Column(Integer, nullable=True)
    
    # Analysis metadata
    model_version = Column(String(20), nullable=False)
    analysis_factors = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<Prediction {self.symbol} {self.predicted_signal}>"
