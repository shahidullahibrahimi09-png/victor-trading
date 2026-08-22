import os
from pydantic_settings import BaseSettings
from functools import lru_cache
from datetime import timedelta

class Settings(BaseSettings):
    """Application configuration settings."""
    
    # Application
    app_name: str = "VICTOR Trading"
    app_version: str = "0.1.0"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Database
    database_url: str = os.getenv("DATABASE_URL", "postgresql://victor:victor_password@localhost/victor_db")
    database_echo: bool = debug
    
    # Redis
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    redis_timeout: int = 5
    
    # API
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8000"))
    api_reload: bool = os.getenv("API_RELOAD", "True").lower() == "true"
    
    # CORS
    allowed_origins: list = os.getenv("ALLOWED_ORIGINS", "http://localhost:8000,http://localhost:3000,http://localhost:8080").split(",")
    allowed_methods: list = os.getenv("ALLOWED_METHODS", "GET,POST,PUT,DELETE,OPTIONS").split(",")
    allow_credentials: bool = True
    
    # Security
    secret_key: str = os.getenv("SECRET_KEY", "change-this-in-production")
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "change-this-in-production")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    jwt_expiration_hours: int = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))
    jwt_expiration: timedelta = timedelta(hours=jwt_expiration_hours)
    
    # Binance API
    binance_api_key: str = os.getenv("BINANCE_API_KEY", "")
    binance_api_secret: str = os.getenv("BINANCE_API_SECRET", "")
    binance_testnet: bool = os.getenv("BINANCE_TESTNET", "True").lower() == "true"
    binance_base_url: str = "https://testnet.binance.vision" if binance_testnet else "https://api.binance.com"
    
    # WebSocket
    ws_host: str = os.getenv("WS_HOST", "0.0.0.0")
    ws_port: int = int(os.getenv("WS_PORT", "8000"))
    ws_pool_size: int = int(os.getenv("WS_POOL_SIZE", "100"))
    
    # Data
    update_interval: int = int(os.getenv("UPDATE_INTERVAL", "1"))
    chart_cache_duration: int = int(os.getenv("CHART_CACHE_DURATION", "300"))
    
    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_file: str = os.getenv("LOG_FILE", "logs/victor.log")
    
    # AI Configuration
    model_cache_dir: str = os.getenv("MODEL_CACHE_DIR", "./models")
    backtest_cache_dir: str = os.getenv("BACKTEST_CACHE_DIR", "./backtest_cache")
    
    # Rate Limiting
    rate_limit_per_minute: int = 60
    rate_limit_per_hour: int = 1000
    
    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
