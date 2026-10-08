from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.catalog.product import Product


class Category(TimestampMixin, Base):
    """
    Represents a product category.

    Examples:
        - Shoes
        - Electronics
        - Clothing
    """

    __tablename__ = "categories"

    # ------------------------------------------------------------------
    # Primary Key
    # ------------------------------------------------------------------

    category_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # ------------------------------------------------------------------
    # Basic Information
    # ------------------------------------------------------------------

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
        index=True,
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

    products: Mapped[list["Product"]] = relationship(
        back_populates="category",
        cascade="save-update, merge",
        lazy="noload",
    )

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"Category("
            f"id={self.category_id}, "
            f"name='{self.name}'"
            f")"
        )