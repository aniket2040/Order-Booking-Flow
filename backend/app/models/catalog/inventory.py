from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.catalog.product_variant import ProductVariant


class Inventory(TimestampMixin, Base):
    """
    Represents the current inventory state for a product variant.

    One ProductVariant has exactly one Inventory record.
    """

    __tablename__ = "inventory"

    __table_args__ = (
        CheckConstraint(
            "available_stock >= 0",
            name="available_stock_non_negative",
        ),
        CheckConstraint(
            "reserved_stock >= 0",
            name="reserved_stock_non_negative",
        ),
        CheckConstraint(
            "reorder_level >= 0",
            name="reorder_level_non_negative",
        ),
        {
            "comment": "Stores inventory information for product variants.",
        },
    )

    # ------------------------------------------------------------------
    # Primary Key
    # ------------------------------------------------------------------

    inventory_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # ------------------------------------------------------------------
    # Foreign Key
    # ------------------------------------------------------------------

    variant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "product_variants.variant_id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        unique=True,
    )

    # ------------------------------------------------------------------
    # Inventory Information
    # ------------------------------------------------------------------

    available_stock: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    reserved_stock: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    reorder_level: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    variant: Mapped["ProductVariant"] = relationship(
        back_populates="inventory",
        lazy="noload",
    )

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"Inventory("
            f"variant_id={self.variant_id}, "
            f"available={self.available_stock}, "
            f"reserved={self.reserved_stock}"
            f")"
        )