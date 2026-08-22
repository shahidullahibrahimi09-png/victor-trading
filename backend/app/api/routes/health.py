"""Health check endpoint."""

from fastapi import APIRouter
from app.config import get_settings

router = APIRouter()
settings = get_settings()

@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.app_version,
        "message": "VICTOR Trading API is running"
    }

@router.get("/status")
async def status():
    """Detailed status endpoint."""
    return {
        "status": "operational",
        "app_name": settings.app_name,
        "version": settings.app_version,
        "debug": settings.debug,
        "database_connected": True,  # Would be checked dynamically in production
        "redis_connected": True
    }
