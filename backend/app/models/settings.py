"""User settings model."""

from datetime import datetime
from sqlalchemy import Column, String, DateTime, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.database.base import Base

class Settings(Base):
    """User application settings."""
    __tablename__ = "user_settings"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=True, unique=True, index=True)
    
    # Theme and Display
    theme = Column(String(20), default="dark", nullable=False)  # dark, light
    language = Column(String(10), default="en", nullable=False)
    chart_style = Column(String(20), default="candlestick", nullable=False)
    
    # Notification Settings
    enable_notifications = Column(Boolean, default=True, nullable=False)
    notify_on_signal = Column(Boolean, default=True, nullable=False)
    notify_on_analysis = Column(Boolean, default=False, nullable=False)
    notify_on_error = Column(Boolean, default=True, nullable=False)
    
    # Chart Settings
    default_timeframe = Column(String(20), default="1h", nullable=False)
    show_volume = Column(Boolean, default=True, nullable=False)
    show_indicators = Column(Boolean, default=True, nullable=False)
    
    # Indicator Settings
    selected_indicators = Column(JSON, default=[], nullable=False)
    indicator_settings = Column(JSON, nullable=True)  # Custom indicator parameters
    
    # Analysis Settings
    confidence_threshold = Column(String(20), default="medium", nullable=False)
    risk_tolerance = Column(String(20), default="medium", nullable=False)
    
    # Data Source Settings
    primary_data_source = Column(String(50), default="binance", nullable=False)
    update_frequency = Column(String(20), default="real-time", nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<Settings user_id={self.user_id}>"
