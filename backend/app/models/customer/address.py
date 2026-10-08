from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.customer.customer import Customer
    from app.models.draft.draft import OrderDraft
    from app.models.order.order import Order


class Address(TimestampMixin, Base):
    """
    Represents a customer's delivery address.
    """

    __tablename__ = "addresses"

    __table_args__ = {
        "comment": "Stores customer delivery addresses."
    }

    # -------------------------------------------------------
    # Primary Key
    # -------------------------------------------------------

    address_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # -------------------------------------------------------
    # Foreign Key
    # -------------------------------------------------------

    customer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "customers.customer_id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    # -------------------------------------------------------
    # Address Information
    # -------------------------------------------------------

    address_line1: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    address_line2: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    state: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    country: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    postal_code: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    is_default: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    # -------------------------------------------------------
    # Relationships
    # -------------------------------------------------------

    customer: Mapped["Customer"] = relationship(
        back_populates="addresses",
        lazy="noload",
    )

    drafts: Mapped[list["OrderDraft"]] = relationship(
        back_populates="address",
        lazy="noload",
    )

    orders: Mapped[list["Order"]] = relationship(
        back_populates="address",
        lazy="noload",
    )

    # -------------------------------------------------------
    # Representation
    # -------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"Address("
            f"city='{self.city}', "
            f"postal_code='{self.postal_code}'"
            f")"
        )