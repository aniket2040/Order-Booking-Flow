from __future__ import annotations

from uuid import UUID

from sqlalchemy import select

from app.models.conversation.message import ConversationMessage
from app.repositories.base import BaseRepository


class MessageRepository(BaseRepository[ConversationMessage]):
    """
    Repository for ConversationMessage entity.
    """

    def __init__(self, session):
        super().__init__(session, ConversationMessage)

    # ------------------------------------------------------------------
    # Message Queries
    # ------------------------------------------------------------------

    async def get_by_session(
        self,
        session_id: UUID,
    ) -> list[ConversationMessage]:
        """
        Return all messages belonging to a conversation session.
        """

        result = await self.session.execute(
            select(ConversationMessage)
            .where(
                ConversationMessage.session_id == session_id
            )
            .order_by(
                ConversationMessage.created_at.asc()
            )
        )

        return list(result.scalars().all())

    async def get_last_message(
        self,
        session_id: UUID,
    ) -> ConversationMessage | None:
        """
        Return the latest message in a conversation session.
        """

        result = await self.session.execute(
            select(ConversationMessage)
            .where(
                ConversationMessage.session_id == session_id
            )
            .order_by(
                ConversationMessage.created_at.desc()
            )
            .limit(1)
        )

        return result.scalar_one_or_none()