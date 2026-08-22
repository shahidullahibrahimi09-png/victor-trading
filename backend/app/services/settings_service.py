"""User settings service."""

import logging
from typing import Optional
from app.schemas.settings import SettingsUpdateRequest

logger = logging.getLogger(__name__)

class SettingsService:
    """Service for managing user settings."""
    
    async def get_settings(self) -> dict:
        """Get current settings."""
        try:
            logger.info("Getting settings")
            # Return default settings
            return {
                "theme": "dark",
                "language": "en",
                "chart_style": "candlestick",
                "default_timeframe": "1h",
                "enable_notifications": True,
                "notify_on_signal": True,
                "notify_on_analysis": False,
                "notify_on_error": True,
                "show_volume": True,
                "show_indicators": True,
                "selected_indicators": [],
                "confidence_threshold": "medium",
                "risk_tolerance": "medium",
                "primary_data_source": "binance",
                "update_frequency": "real-time"
            }
        except Exception as e:
            logger.error(f"Error getting settings: {e}")
            raise
    
    async def update_settings(self, request: SettingsUpdateRequest) -> dict:
        """Update settings."""
        try:
            # Get current settings
            current = await self.get_settings()
            
            # Update with provided values
            updates = request.dict(exclude_unset=True)
            current.update(updates)
            
            logger.info(f"Updated settings: {list(updates.keys())}")
            return current
        except Exception as e:
            logger.error(f"Error updating settings: {e}")
            raise
