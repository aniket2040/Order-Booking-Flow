from __future__ import annotations
from datetime import datetime

from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    func,
)
import uuid
from typing import TYPE_CHECKING

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums import (
    WorkflowState,
    ConversationStatus,
)

if TYPE_CHECKING:
    from app.models.conversation.message import ConversationMessage
    from app.models.customer.customer import Customer
    from app.models.draft.draft import OrderDraft


class ConversationSession(Base):
    """
    Represents a chatbot conversation session.
    """

    __tablename__ = "conversation_sessions"

    __table_args__ = {
        "comment": "Stores chatbot conversation sessions."
    }

    # -------------------------------------------------------
    # Primary Key
    # -------------------------------------------------------

    session_id: Mapped[uuid.UUID] = mapped_column(
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
    # Conversation State
    # -------------------------------------------------------

    current_state: Mapped[WorkflowState] = mapped_column(
        Enum(WorkflowState),
        nullable=False,
        default=WorkflowState.DETECT_INTENT,
    )

    status: Mapped[ConversationStatus] = mapped_column(
        Enum(ConversationStatus),
        nullable=False,
        default=ConversationStatus.ACTIVE,
    )

    # -------------------------------------------------------
    # Timestamps
    # -------------------------------------------------------

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    last_activity_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    # -------------------------------------------------------
    # Relationships
    # -------------------------------------------------------

    customer: Mapped["Customer"] = relationship(
        back_populates="conversations",
        lazy="noload",
    )

    messages: Mapped[list["ConversationMessage"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
        lazy="noload",
    )

    draft: Mapped["OrderDraft | None"] = relationship(
        back_populates="session",
        uselist=False,
        lazy="noload",
    )

    # -------------------------------------------------------
    # Representation
    # -------------------------------------------------------

    def __repr__(self):

        return (
            f"ConversationSession("
            f"id={self.session_id}, "
            f"state={self.current_state}"
            f")"
        )