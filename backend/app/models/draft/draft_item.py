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
    from app.models.draft.draft import OrderDraft


class DraftItem(Base):
    """
    Represents a single product inside an OrderDraft.
    """

    __tablename__ = "draft_items"

    __table_args__ = (
        UniqueConstraint(
            "draft_id",
            "variant_id",
            name="uq_draft_variant",
        ),
        CheckConstraint(
            "quantity > 0",
            name="positive_quantity",
        ),
    )

    # -------------------------------------------------------
    # Primary Key
    # -------------------------------------------------------

    draft_item_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # -------------------------------------------------------
    # Foreign Keys
    # -------------------------------------------------------

    draft_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "order_drafts.draft_id",
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
    # Item Information
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

    draft: Mapped["OrderDraft"] = relationship(
        back_populates="items",
        lazy="noload",
    )

    variant: Mapped["ProductVariant"] = relationship(
        back_populates="draft_items",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return (
            f"DraftItem("
            f"variant={self.variant_id}, "
            f"qty={self.quantity}"
            f")"
        )