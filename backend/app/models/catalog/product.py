from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.catalog.brand import Brand
    from app.models.catalog.category import Category
    from app.models.catalog.product_variant import ProductVariant


class Product(TimestampMixin, Base):
    """
    Represents a product.

    Examples:
        - Nike Air Max
        - iPhone 16
        - Samsung Galaxy S25
    """

    __tablename__ = "products"

    __table_args__ = {
        "comment": "Stores master product information."
    }

    # ------------------------------------------------------------------
    # Primary Key
    # ------------------------------------------------------------------

    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # ------------------------------------------------------------------
    # Foreign Keys
    # ------------------------------------------------------------------

    category_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "categories.category_id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    brand_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "brands.brand_id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    # ------------------------------------------------------------------
    # Product Information
    # ------------------------------------------------------------------

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    category: Mapped["Category"] = relationship(
        "Category",
        lazy="noload",
    )

    brand: Mapped["Brand"] = relationship(
        back_populates="products",
        lazy="noload",
    )

    variants: Mapped[list["ProductVariant"]] = relationship(
        back_populates="product",
        lazy="noload",
    )

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"Product("
            f"id={self.product_id}, "
            f"name='{self.name}'"
            f")"
        )