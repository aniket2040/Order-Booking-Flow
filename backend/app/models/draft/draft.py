from __future__ import annotations

import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums import (
    DraftStatus,
    WorkflowState, WorkflowMode,
)
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.conversation.session import ConversationSession
    from app.models.customer.address import Address
    from app.models.customer.customer import Customer
    from app.models.draft.draft_item import DraftItem
    from app.models.order.order import Order
    from app.models.catalog.product import Product
    from app.models.catalog.product_variant import ProductVariant


class OrderDraft(TimestampMixin, Base):
    """
    Represents the working copy of an order while the
    customer is interacting with the chatbot.
    """

    __tablename__ = "order_drafts"

    __table_args__ = {
        "comment": "Stores temporary order drafts before confirmation."
    }

    # -------------------------------------------------------
    # Primary Key
    # -------------------------------------------------------

    draft_id: Mapped[uuid.UUID] = mapped_column(
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
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "conversation_sessions.session_id",
            ondelete="CASCADE",
        ),
        nullable=False,
        unique=True,
    )

    address_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "addresses.address_id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    product_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "products.product_id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    variant_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "product_variants.variant_id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    # -------------------------------------------------------
    # Draft State
    # -------------------------------------------------------

    status: Mapped[DraftStatus] = mapped_column(
        Enum(DraftStatus),
        nullable=False,
        default=DraftStatus.ACTIVE,
    )



    workflow_state: Mapped[WorkflowState] = mapped_column(
        Enum(WorkflowState),
        nullable=False,
        default=WorkflowState.DETECT_INTENT,
    )

    workflow_mode: Mapped[WorkflowMode] = mapped_column(
        Enum(WorkflowMode),
        nullable=False,
        default=WorkflowMode.NEW_ORDER,
    )

    # -------------------------------------------------------
    # Pricing Snapshot
    # -------------------------------------------------------

    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=0,
    )

    tax: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=0,
    )

    shipping_charge: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=0,
    )

    discount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=0,
    )

    grand_total: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=0,
    )

    currency: Mapped[str] = mapped_column(
        nullable=False,
        default="INR",
    )

    # -------------------------------------------------------
    # Relationships
    # -------------------------------------------------------

    customer: Mapped["Customer"] = relationship(
        back_populates="drafts",
        lazy="noload",
    )

    session: Mapped["ConversationSession"] = relationship(
        back_populates="draft",
        lazy="noload",
    )

    address: Mapped["Address | None"] = relationship(
        back_populates="drafts",
        lazy="noload",
    )

    items: Mapped[list["DraftItem"]] = relationship(
        back_populates="draft",
        cascade="all, delete-orphan",
        lazy="noload",
    )

    order: Mapped["Order | None"] = relationship(
        back_populates="draft",
        uselist=False,
        lazy="noload",
    )

    quantity: Mapped[int | None] = mapped_column(
        nullable=True,
    )

    selected_color: Mapped[str | None] = mapped_column(
        nullable=True,
    )

    selected_size: Mapped[str | None] = mapped_column(
        nullable=True,
    )

    selected_brand: Mapped[str | None] = mapped_column(
        nullable=True,
    )

    product: Mapped["Product | None"] = relationship(
        lazy="noload",
    )

    variant: Mapped["ProductVariant | None"] = relationship(
        lazy="noload",
    )

    requested_product: Mapped[str | None] = mapped_column(
        nullable=True,
    )

    def __repr__(self) -> str:
        return (
            f"OrderDraft("
            f"id={self.draft_id}, "
            f"status={self.status}"
            f")"
        )