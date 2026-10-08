from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.api.order import router as order_router
from app.core.database import check_database_connection
from app.core.logging import get_logger

logger = get_logger(__name__)


# ==========================================================
# Lifespan
# ==========================================================

@asynccontextmanager
async def lifespan(
    app: FastAPI,
):
    """
    Application startup and shutdown events.
    """

    logger.info("Starting application...")

    connected = await check_database_connection()

    if not connected:
        raise RuntimeError(
            "Unable to connect to PostgreSQL."
        )

    logger.info("Database connection established.")

    yield

    logger.info("Shutting down application...")


# ==========================================================
# FastAPI
# ==========================================================

app = FastAPI(
    title="AI E-Commerce Assistant",
    version="1.0.0",
    lifespan=lifespan,
)


# ==========================================================
# Routers
# ==========================================================

app.include_router(chat_router)
app.include_router(order_router)


# ==========================================================
# Health Check
# ==========================================================

@app.get(
    "/",
    tags=["Health"],
)
async def root():
    """
    Root endpoint.
    """

    return {
        "status": "running",
        "message": "AI E-Commerce Assistant",
    }


@app.get(
    "/health",
    tags=["Health"],
)
async def health():
    """
    Health check endpoint.
    """

    return {
        "status": "healthy",
    }