from __future__ import annotations

from uuid import UUID

from app.exceptions.customer import (
    CustomerNotFoundError,
)
from app.Services.customer.customer_service import CustomerService
from app.Services.draft.draft_service import DraftService
from app.models.conversation.message import ConversationMessage
from app.models.conversation.session import ConversationSession
from app.models.enums import (
    ConversationStatus,
    MessageRole, WorkflowState,
)
from app.repositories.conversation import session_repository
from app.repositories.conversation.message_repository import (
    MessageRepository,
)
from app.repositories.conversation.session_repository import (
    SessionRepository,
)
from app.schema.workflow import WorkflowContext


class ConversationService:
    """
    Handles conversation lifecycle and message persistence.
    """

    def __init__(
        self,
        session_repository: SessionRepository,
        message_repository: MessageRepository,
        draft_service: DraftService,
        customer_service: CustomerService,
    ) -> None:
        self.session_repository = session_repository
        self.message_repository = message_repository
        self.draft_service = draft_service
        self.customer_service = customer_service

    # ------------------------------------------------------------------
    # Session
    # ------------------------------------------------------------------

    async def get_active_session(
        self,
        customer_id: UUID,
    ) -> ConversationSession | None:
        """
        Retrieve the customer's active conversation session.
        """

        return await self.session_repository.get_active_session(
            customer_id
        )

    async def get_or_create_session(
            self,
            customer_id: UUID,
            session_id: UUID,
    ) -> ConversationSession:

        session = await self.session_repository.get_by_id(
            session_id,
        )

        if session:
            if session.customer_id != customer_id:
                raise ValueError(
                    "Session does not belong to customer."
                )
            return session

        session = ConversationSession(
            session_id=session_id,
            customer_id=customer_id,
            status=ConversationStatus.ACTIVE,
        )

        return await self.session_repository.create(
            session,
        )

    async def start_session(
        self,
        session: ConversationSession,
    ) -> ConversationSession:
        """
        Start a new conversation session.
        """

        session.status = ConversationStatus.ACTIVE

        return await self.session_repository.create(
            session
        )

    async def end_session(
        self,
        session: ConversationSession,
    ) -> None:
        """
        End the conversation session.
        """

        session.status = ConversationStatus.COMPLETED

    async def load_workflow_context(
            self,
            customer_id: UUID,
            session_id: UUID,
    ) -> WorkflowContext:

        customer = await self.customer_service.get_by_id(
            customer_id,
        )

        if customer is None:
            raise CustomerNotFoundError(
                customer_id,
            )



        session = await self.get_or_create_session(
            customer_id = customer_id,
            session_id = session_id,
        )

        print("=" * 80)
        print("Customer :", customer_id)
        print("Session  :", session_id)
        print("=" * 80)

        draft = await self.draft_service.get_or_create_draft(
            customer_id=session.customer_id,
            session_id=session.session_id,
        )
        print("=" * 80)
        print("Draft ID       :", draft.draft_id)
        print("Draft Customer :", draft.customer_id)
        print("Draft Session  :", draft.session_id)
        print("Draft Status   :", draft.status)
        print("=" * 80)

        print(
            "Workflow mode:",
            draft.workflow_mode,
        )

        return WorkflowContext(
            customer_id=session.customer_id,
            session_id=session.session_id,
            workflow_state=draft.workflow_state,
            workflow_mode=draft.workflow_mode,
            draft_id=draft.draft_id,
            slots=await self.draft_service.build_context(draft),
        )

    async def save_workflow_state(
            self,
            session: ConversationSession,
            next_state: WorkflowState,
    ) -> None:
        session.current_state = next_state

        await self.session_repository.update(session)

    # ------------------------------------------------------------------
    # Messages
    # ------------------------------------------------------------------

    async def append_message(
        self,
        session: ConversationSession,
        role: MessageRole,
        content: str,
    ) -> ConversationMessage:
        """
        Append a message to the conversation.
        """

        message = ConversationMessage(
            session_id=session.session_id,
            role=role,
            content=content,
        )

        return await self.message_repository.create(
            message
        )

    async def get_conversation_history(
        self,
        session_id: UUID,
    ) -> list[ConversationMessage]:
        """
        Retrieve conversation history.
        """

        return await self.message_repository.get_by_session(
            session_id
        )