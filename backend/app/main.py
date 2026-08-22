"""VICTOR Trading - FastAPI Application Main Entry Point"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZIPMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.config import get_settings
from app.database.connection import init_db, close_db
from app.api.routes import health, assets, chart, analysis, history, settings as settings_routes

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

settings = get_settings()

# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown."""
    # Startup
    logger.info(f"🚀 Starting {settings.app_name} v{settings.app_version}")
    await init_db()
    logger.info("✅ Database initialized")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down application")
    await close_db()
    logger.info("✅ Application shutdown complete")

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="Professional AI-powered trading chart analysis platform",
    version=settings.app_version,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=settings.allow_credentials,
    allow_methods=settings.allowed_methods,
    allow_headers=["*"],
)

# Add GZIP compression middleware
app.add_middleware(GZIPMiddleware, minimum_size=1000)

# Include routers
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(assets.router, prefix="/api", tags=["assets"])
app.include_router(chart.router, prefix="/api", tags=["chart"])
app.include_router(analysis.router, prefix="/api", tags=["analysis"])
app.include_router(history.router, prefix="/api", tags=["history"])
app.include_router(settings_routes.router, prefix="/api", tags=["settings"])

# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """Handle validation errors."""
    return JSONResponse(
        status_code=400,
        content={
            "detail": "Invalid request",
            "errors": exc.errors()
        }
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    """Handle generic exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "message": str(exc) if settings.debug else "An unexpected error occurred"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload
    )
