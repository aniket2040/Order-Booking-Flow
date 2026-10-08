from __future__ import annotations

import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums import PaymentMethod, PaymentStatus
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.order.order import Order


class Payment(TimestampMixin, Base):
    """
    Represents payment information for an order.

    Version 1 supports only Cash on Delivery (COD).
    """

    __tablename__ = "payments"

    __table_args__ = {
        "comment": "Stores payment information for customer orders."
    }

    # -------------------------------------------------------
    # Primary Key
    # -------------------------------------------------------

    payment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # -------------------------------------------------------
    # Foreign Key
    # -------------------------------------------------------

    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "orders.order_id",
            ondelete="CASCADE",
        ),
        nullable=False,
        unique=True,
    )

    # -------------------------------------------------------
    # Payment Information
    # -------------------------------------------------------

    method: Mapped[PaymentMethod] = mapped_column(
        Enum(PaymentMethod),
        nullable=False,
        default=PaymentMethod.CASH_ON_DELIVERY,
    )

    status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus),
        nullable=False,
        default=PaymentStatus.PENDING,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    transaction_reference: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    # -------------------------------------------------------
    # Relationships
    # -------------------------------------------------------

    order: Mapped["Order"] = relationship(
        back_populates="payment",
        lazy="noload",
    )

    # -------------------------------------------------------
    # Representation
    # -------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"Payment("
            f"payment_id={self.payment_id}, "
            f"method={self.method}, "
            f"status={self.status}"
            f")"
        )