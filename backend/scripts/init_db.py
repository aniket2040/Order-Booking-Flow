from __future__ import annotations

import sys
from pathlib import Path

# Add project root (backend/) to Python path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

import asyncio

from app.core.database import Base, engine

# ==========================================================
# Import Models
# ==========================================================
#
# These imports are REQUIRED so SQLAlchemy registers every
# model before Base.metadata.create_all() is executed.
#

# Catalog
from app.models.catalog.category import Category
from app.models.catalog.brand import Brand
from app.models.catalog.product import Product
from app.models.catalog.product_variant import ProductVariant
from app.models.catalog.inventory import Inventory

# Customer
from app.models.customer.customer import Customer
from app.models.customer.address import Address

# Conversation
from app.models.conversation.session import ConversationSession
from app.models.conversation.message import ConversationMessage

# Draft
from app.models.draft.draft import OrderDraft
from app.models.draft.draft_item import DraftItem

# Order
from app.models.order.order import Order
from app.models.order.order_item import OrderItem
from app.models.order.payment import Payment
from app.models.order.shipment import Shipment
from app.models.order.order_status_history import (
    OrderStatusHistory,
)


async def create_tables() -> None:
    """
    Create all database tables.
    """

    async with engine.begin() as connection:

        await connection.run_sync(
            Base.metadata.create_all
        )

    print("✅ Database tables created successfully.")


async def drop_tables() -> None:
    """
    Drop all database tables.

    Useful during development.
    """

    async with engine.begin() as connection:

        await connection.run_sync(
            Base.metadata.drop_all
        )

    print("🗑️ Database tables dropped successfully.")


async def recreate_database() -> None:
    """
    Drop and recreate all tables.
    """

    print("\nRegistered Tables:")
    print(list(Base.metadata.tables.keys()))
    print()

    await drop_tables()
    await create_tables()


if __name__ == "__main__":

    asyncio.run(
        recreate_database()
    )