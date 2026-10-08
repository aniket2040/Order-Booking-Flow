from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums import MessageRole

if TYPE_CHECKING:
    from app.models.conversation.session import ConversationSession


class ConversationMessage(Base):
    """
    Represents a single message exchanged during a conversation.
    """

    __tablename__ = "conversation_messages"

    __table_args__ = {
        "comment": "Stores individual chat messages."
    }

    # -------------------------------------------------------
    # Primary Key
    # -------------------------------------------------------

    message_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # -------------------------------------------------------
    # Foreign Key
    # -------------------------------------------------------

    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "conversation_sessions.session_id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    # -------------------------------------------------------
    # Message
    # -------------------------------------------------------

    role: Mapped[MessageRole] = mapped_column(
        Enum(MessageRole),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # -------------------------------------------------------
    # Relationships
    # -------------------------------------------------------

    session: Mapped["ConversationSession"] = relationship(
        back_populates="messages",
        lazy="noload",
    )

    # -------------------------------------------------------
    # Representation
    # -------------------------------------------------------

    def __repr__(self):

        return (
            f"ConversationMessage("
            f"role={self.role}"
            f")"
        )