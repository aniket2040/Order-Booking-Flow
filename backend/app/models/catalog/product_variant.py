from __future__ import annotations

import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    ForeignKey,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.catalog.inventory import Inventory
    from app.models.catalog.product import Product
    from app.models.draft.draft_item import DraftItem
    from app.models.order.order_item import OrderItem


class ProductVariant(TimestampMixin, Base):
    """
    Represents a sellable product variant (SKU).

    Example:
        Nike Air Max
        Color : Black
        Size  : 9
        Price : ₹4999
    """

    __tablename__ = "product_variants"

    __table_args__ = (
        UniqueConstraint(
            "product_id",
            "color",
            "size",
            name="uq_product_variant",
        ),
        {
            "comment": "Stores sellable product variants."
        },
    )

    # -------------------------------------------------------
    # Primary Key
    # -------------------------------------------------------

    variant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # -------------------------------------------------------
    # Foreign Key
    # -------------------------------------------------------

    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "products.product_id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    # -------------------------------------------------------
    # Variant Information
    # -------------------------------------------------------

    sku: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
    )

    color: Mapped[str | None] = mapped_column(
        String(50),
    )

    size: Mapped[str | None] = mapped_column(
        String(50),
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    weight: Mapped[Decimal | None] = mapped_column(
        Numeric(8, 2),
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    @property
    def display_name(self) -> str:
        """
        Human-readable variant name.

        Example:
            Black / Size 9
        """

        parts = []

        if self.color:
            parts.append(self.color)

        if self.size:
            parts.append(f"Size {self.size}")

        return " / ".join(parts)

    # -------------------------------------------------------
    # Relationships
    # -------------------------------------------------------

    product: Mapped["Product"] = relationship(
        back_populates="variants",
        lazy="selectin"
    )

    inventory: Mapped["Inventory"] = relationship(
        back_populates="variant",
        uselist=False,
        lazy="noload",
    )

    draft_items: Mapped[list["DraftItem"]] = relationship(
        back_populates="variant",
        lazy="selectin"
    )

    order_items: Mapped[list["OrderItem"]] = relationship(
        back_populates="variant",
        lazy="noload",
    )

    # -------------------------------------------------------
    # Representation
    # -------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"ProductVariant("
            f"sku='{self.sku}', "
            f"price={self.price}"
            f")"
        )