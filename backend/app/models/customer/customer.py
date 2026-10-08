from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.customer.address import Address
    from app.models.conversation.session import ConversationSession
    from app.models.draft.draft import OrderDraft
    from app.models.order.order import Order


class Customer(TimestampMixin, Base):
    """
    Represents a customer in the system.
    """

    __tablename__ = "customers"

    __table_args__ = {
        "comment": "Stores customer information."
    }

    # -------------------------------------------------------
    # Primary Key
    # -------------------------------------------------------

    customer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # -------------------------------------------------------
    # Customer Information
    # -------------------------------------------------------

    full_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    phone: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        unique=True,
    )

    # -------------------------------------------------------
    # Relationships
    # -------------------------------------------------------

    addresses: Mapped[list["Address"]] = relationship(
        back_populates="customer",
        cascade="all, delete-orphan",
        lazy="noload",
    )

    conversations: Mapped[list["ConversationSession"]] = relationship(
        back_populates="customer",
        lazy="noload",
    )

    drafts: Mapped[list["OrderDraft"]] = relationship(
        back_populates="customer",
        lazy="noload",
    )

    orders: Mapped[list["Order"]] = relationship(
        back_populates="customer",
        lazy="noload",
    )

    # -------------------------------------------------------
    # Representation
    # -------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"Customer("
            f"id={self.customer_id}, "
            f"name='{self.full_name}'"
            f")"
        )