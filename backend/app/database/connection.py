"""Database connection and session management."""

import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker
)
from sqlalchemy.pool import NullPool

from app.config import get_settings
from app.database.base import Base

logger = logging.getLogger(__name__)
settings = get_settings()

# Convert PostgreSQL URL to async version
async_database_url = settings.database_url.replace(
    "postgresql://", "postgresql+asyncpg://"
)

# Create async engine
engine = create_async_engine(
    async_database_url,
    echo=settings.database_echo,
    pool_size=10,
    max_overflow=20,
    poolclass=NullPool if settings.debug else None,
)

# Create session factory
Async_Session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

async def init_db():
    """Initialize database and create tables."""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

async def close_db():
    """Close database connection."""
    try:
        await engine.dispose()
        logger.info("Database connection closed")
    except Exception as e:
        logger.error(f"Failed to close database: {e}")
        raise

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get database session."""
    async with Async_Session() as session:
        try:
            yield session
        finally:
            await session.close()
