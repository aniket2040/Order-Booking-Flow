from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from app.repositories.catalog.inventory_repository import (
    InventoryRepository,
)
from app.repositories.catalog.product_repository import (
    ProductRepository,
)

from app.repositories.conversation.message_repository import (
    MessageRepository,
)
from app.repositories.conversation.session_repository import (
    SessionRepository,
)

from app.repositories.customer.address_repository import (
    AddressRepository,
)
from app.repositories.customer.customer_repository import (
    CustomerRepository,
)

from app.repositories.draft.draft_repository import (
    DraftRepository,
)

from app.repositories.order.order_repository import (
    OrderRepository,
)
from app.repositories.order.payment_repository import (
    PaymentRepository,
)
from app.repositories.order.shipment_repository import (
    ShipmentRepository,
)


# ==========================================================
# Catalog
# ==========================================================


def get_product_repository(
    db: AsyncSession = Depends(get_db),
) -> ProductRepository:

    return ProductRepository(db)


def get_inventory_repository(
    db: AsyncSession = Depends(get_db),
) -> InventoryRepository:

    return InventoryRepository(db)


# ==========================================================
# Customer
# ==========================================================

def get_customer_repository(
    db: AsyncSession = Depends(get_db),
) -> CustomerRepository:

    return CustomerRepository(db)


def get_address_repository(
    db: AsyncSession = Depends(get_db),
) -> AddressRepository:

    return AddressRepository(db)


# ==========================================================
# Conversation
# ==========================================================

def get_session_repository(
    db: AsyncSession = Depends(get_db),
) -> SessionRepository:

    return SessionRepository(db)


def get_message_repository(
    db: AsyncSession = Depends(get_db),
) -> MessageRepository:

    return MessageRepository(db)


# ==========================================================
# Draft
# ==========================================================

def get_draft_repository(
    db: AsyncSession = Depends(get_db),
) -> DraftRepository:

    return DraftRepository(db)


# ==========================================================
# Orders
# ==========================================================

def get_order_repository(
    db: AsyncSession = Depends(get_db),
) -> OrderRepository:

    return OrderRepository(db)


def get_payment_repository(
    db: AsyncSession = Depends(get_db),
) -> PaymentRepository:

    return PaymentRepository(db)


def get_shipment_repository(
    db: AsyncSession = Depends(get_db),
) -> ShipmentRepository:

    return ShipmentRepository(db)