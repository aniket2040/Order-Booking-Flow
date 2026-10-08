from __future__ import annotations

import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.catalog.product_variant import ProductVariant
    from app.models.order.order import Order


class OrderItem(Base):
    """
    Represents a single purchased product within an Order.

    Stores a snapshot of the purchased product variant,
    quantity, and unit price at the time of purchase.
    """

    __tablename__ = "order_items"

    __table_args__ = (
        UniqueConstraint(
            "order_id",
            "variant_id",
            name="uq_order_variant",
        ),
        CheckConstraint(
            "quantity > 0",
            name="ck_order_item_positive_quantity",
        ),
        {
            "comment": "Stores purchased product variants for an order."
        },
    )

    # -------------------------------------------------------
    # Primary Key
    # -------------------------------------------------------

    order_item_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # -------------------------------------------------------
    # Foreign Keys
    # -------------------------------------------------------

    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "orders.order_id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    variant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "product_variants.variant_id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    # -------------------------------------------------------
    # Purchase Snapshot
    # -------------------------------------------------------

    quantity: Mapped[int] = mapped_column(
        nullable=False,
    )

    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    # -------------------------------------------------------
    # Relationships
    # -------------------------------------------------------

    order: Mapped["Order"] = relationship(
        back_populates="items",
        lazy="noload",
    )

    variant: Mapped["ProductVariant"] = relationship(
        back_populates="order_items",
        lazy="noload",
    )

    # -------------------------------------------------------
    # Representation
    # -------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"OrderItem("
            f"order_id={self.order_id}, "
            f"variant_id={self.variant_id}, "
            f"quantity={self.quantity}"
            f")"
        )