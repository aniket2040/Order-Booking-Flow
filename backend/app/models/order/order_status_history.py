from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums import OrderStatus
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.order.order import Order


class OrderStatusHistory(TimestampMixin, Base):
    """
    Stores the history of status changes for an order.

    Every status transition creates a new record.
    """

    __tablename__ = "order_status_history"

    __table_args__ = {
        "comment": "Stores order status change history."
    }

    # -------------------------------------------------------
    # Primary Key
    # -------------------------------------------------------

    history_id: Mapped[uuid.UUID] = mapped_column(
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
    )

    # -------------------------------------------------------
    # Status Information
    # -------------------------------------------------------

    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus),
        nullable=False,
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    changed_by: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="SYSTEM",
    )

    # -------------------------------------------------------
    # Relationships
    # -------------------------------------------------------

    order: Mapped["Order"] = relationship(
        back_populates="status_history",
        lazy="noload",
    )

    # -------------------------------------------------------
    # Representation
    # -------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"OrderStatusHistory("
            f"order_id={self.order_id}, "
            f"status={self.status}"
            f")"
        )