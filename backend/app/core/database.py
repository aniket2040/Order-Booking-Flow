from __future__ import annotations

from collections.abc import AsyncGenerator
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy import text
from app.core.config import settings


# ==========================================================
# SQLAlchemy Base
# ==========================================================

from app.models.base import Base


# ==========================================================
# Database Engine
# ==========================================================

engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    future=True,
    poolclass=NullPool
)


# ==========================================================
# Session Factory
# ==========================================================

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


# ==========================================================
# Dependency
# ==========================================================

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that provides
    a database session.
    """

    async with AsyncSessionLocal() as session:

        try:

            yield session

            await session.commit()

        except Exception:

            await session.rollback()
            raise

        finally:

            await session.close()




async def check_database_connection() -> bool:
    """
    Verify that the database is reachable.
    """

    try:

        async with AsyncSessionLocal() as session:

            await session.execute(
                text("SELECT 1")
            )

        return True

    except Exception:

        return False


