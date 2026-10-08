from __future__ import annotations

import uuid
from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums import ShipmentStatus
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.order.order import Order


class Shipment(TimestampMixin, Base):
    """
    Represents shipment information for a customer order.

    A shipment is created once an order is prepared
    for fulfillment.
    """

    __tablename__ = "shipments"

    __table_args__ = {
        "comment": "Stores shipment and delivery information."
    }

    # -------------------------------------------------------
    # Primary Key
    # -------------------------------------------------------

    shipment_id: Mapped[uuid.UUID] = mapped_column(
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
    # Shipment Information
    # -------------------------------------------------------

    status: Mapped[ShipmentStatus] = mapped_column(
        Enum(ShipmentStatus),
        nullable=False,
        default=ShipmentStatus.PENDING,
    )

    carrier: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    tracking_number: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        unique=True,
    )

    expected_delivery_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    # -------------------------------------------------------
    # Relationships
    # -------------------------------------------------------

    order: Mapped["Order"] = relationship(
        back_populates="shipment",
        lazy="noload",
    )

    # -------------------------------------------------------
    # Representation
    # -------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"Shipment("
            f"shipment_id={self.shipment_id}, "
            f"status={self.status}"
            f")"
        )