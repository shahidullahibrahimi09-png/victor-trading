"""Data validation utilities."""

import logging
from typing import List, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

def validate_ohlc_data(candles: List[Dict[str, Any]]) -> bool:
    """Validate OHLC candle data.
    
    Checks for:
    - Required OHLC fields
    - Valid price relationships (high >= low >= close >= open)
    - Valid timestamps
    - Non-negative volumes
    """
    if not candles:
        logger.warning("Empty candle list")
        return False
    
    try:
        for i, candle in enumerate(candles):
            # Check required fields
            required = ['time', 'open', 'high', 'low', 'close']
            if not all(field in candle for field in required):
                logger.error(f"Missing OHLC field in candle {i}")
                return False
            
            # Validate price relationships
            high = candle['high']
            low = candle['low']
            open_price = candle['open']
            close = candle['close']
            
            if not (high >= low > 0):
                logger.error(f"Invalid high/low in candle {i}: high={high}, low={low}")
                return False
            
            if not (low <= open_price <= high and low <= close <= high):
                logger.error(f"OHLC outside high/low range in candle {i}")
                return False
            
            # Validate volume if present
            if 'volume' in candle and candle['volume'] is not None:
                if candle['volume'] < 0:
                    logger.error(f"Negative volume in candle {i}")
                    return False
        
        return True
    
    except Exception as e:
        logger.error(f"OHLC validation error: {e}")
        return False

def detect_missing_candles(candles: List[Dict[str, Any]], timeframe_seconds: int) -> List[int]:
    """Detect missing candles in sequence.
    
    Returns list of indices where gaps were found.
    """
    if len(candles) < 2:
        return []
    
    missing_indices = []
    
    try:
        for i in range(len(candles) - 1):
            current_time = candles[i]['time']
            next_time = candles[i + 1]['time']
            
            # Convert to timestamps if needed
            if isinstance(current_time, datetime):
                current_time = int(current_time.timestamp())
            if isinstance(next_time, datetime):
                next_time = int(next_time.timestamp())
            
            time_diff = next_time - current_time
            expected_diff = timeframe_seconds
            
            if time_diff > expected_diff:
                missing_count = (time_diff // expected_diff) - 1
                logger.warning(f"Found {missing_count} missing candles at index {i}")
                missing_indices.append(i)
    
    except Exception as e:
        logger.error(f"Error detecting missing candles: {e}")
    
    return missing_indices
