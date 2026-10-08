from __future__ import annotations

import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums import OrderStatus
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.customer.customer import Customer
    from app.models.customer.address import Address
    from app.models.draft.draft import OrderDraft
    from app.models.order.order_item import OrderItem
    from app.models.order.payment import Payment
    from app.models.order.shipment import Shipment
    from app.models.order.order_status_history import OrderStatusHistory


class Order(TimestampMixin, Base):
    """
    Represents a confirmed customer order.

    Once created, an Order is considered a historical
    business record and should not be modified directly.
    """

    __tablename__ = "orders"

    __table_args__ = {
        "comment": "Stores confirmed customer orders."
    }

    # -------------------------------------------------------
    # Primary Key
    # -------------------------------------------------------

    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # -------------------------------------------------------
    # Foreign Keys
    # -------------------------------------------------------

    customer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "customers.customer_id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    address_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "addresses.address_id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    draft_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "order_drafts.draft_id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    # -------------------------------------------------------
    # Order Information
    # -------------------------------------------------------

    order_number: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
    )

    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus),
        nullable=False,
        default=OrderStatus.CREATED,
    )

    # -------------------------------------------------------
    # Pricing Snapshot
    # -------------------------------------------------------

    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    tax: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    shipping_charge: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    discount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    grand_total: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        default="INR",
    )

    # -------------------------------------------------------
    # Relationships
    # -------------------------------------------------------

    customer: Mapped["Customer"] = relationship(
        back_populates="orders",
        lazy="noload"
    )

    address: Mapped["Address"] = relationship(
        back_populates="orders",
        lazy="noload"
    )

    draft: Mapped["OrderDraft | None"] = relationship(
        back_populates="order",
        lazy="noload"
    )

    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
        lazy="noload",
    )

    payment: Mapped["Payment"] = relationship(
        back_populates="order",
        uselist=False,
        lazy="noload",
    )

    shipment: Mapped["Shipment | None"] = relationship(
        back_populates="order",
        uselist=False,
        lazy="noload",
    )

    status_history: Mapped[list["OrderStatusHistory"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
        lazy="noload",
    )

    # -------------------------------------------------------
    # Representation
    # -------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"Order("
            f"order_number='{self.order_number}', "
            f"status={self.status}"
            f")"
        )