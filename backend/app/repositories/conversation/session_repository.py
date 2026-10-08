from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.conversation.session import ConversationSession
from app.models.enums import ConversationStatus
from app.repositories.base import BaseRepository


class SessionRepository(BaseRepository[ConversationSession]):
    """
    Repository for ConversationSession entity.
    """

    def __init__(self, session):
        super().__init__(session, ConversationSession)

    # ------------------------------------------------------------------
    # Session Queries
    # ------------------------------------------------------------------

    async def get_active_session(
            self,
            customer_id: UUID,
    ) -> ConversationSession | None:
        """
        Return the active conversation session for a customer.
        """

        result = await self.session.execute(
            select(ConversationSession)
            .options(
                selectinload(ConversationSession.draft)
            )
            .where(
                ConversationSession.customer_id == customer_id,
                ConversationSession.status == ConversationStatus.ACTIVE,
            )
        )

        return result.scalar_one_or_none()

    async def get_with_messages(
        self,
        session_id: UUID,
    ) -> ConversationSession | None:
        """
        Load a conversation session together with all messages.
        """

        result = await self.session.execute(
            select(ConversationSession)
            .options(
                selectinload(ConversationSession.messages)
            )
            .where(
                ConversationSession.session_id == session_id
            )
        )

        return result.scalar_one_or_none()

    async def get_with_draft(
        self,
        session_id: UUID,
    ) -> ConversationSession | None:
        """
        Load a conversation session together with its active draft.
        """

        result = await self.session.execute(
            select(ConversationSession)
            .options(
                selectinload(ConversationSession.draft)
            )
            .where(
                ConversationSession.session_id == session_id
            )
        )

        return result.scalar_one_or_none()

    async def get_full_session(
        self,
        session_id: UUID,
    ) -> ConversationSession | None:
        """
        Load the complete conversation graph:
        Session -> Messages -> Draft.
        """

        result = await self.session.execute(
            select(ConversationSession)
            .options(
                selectinload(ConversationSession.messages),
                selectinload(ConversationSession.draft),
            )
            .where(
                ConversationSession.session_id == session_id
            )
        )

        return result.scalar_one_or_none()