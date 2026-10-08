from __future__ import annotations

from app.models.enums import WorkflowState
from app.schema.workflow import (
    WorkflowContext,
    WorkflowRequest,
)
from app.Services.draft.draft_service import DraftService
from app.Services.orchestrator.order_orchestrator import (
    OrderOrchestrator,
)

from .base_handler import BaseHandler


class CreateOrderHandler(BaseHandler):
    """
    Creates the final order after customer confirmation.
    """

    def __init__(
        self,
        draft_service: DraftService,
        order_orchestrator: OrderOrchestrator,
    ) -> None:

        self.draft_service = draft_service
        self.order_orchestrator = order_orchestrator

    async def handle(
        self,
        request: WorkflowRequest,
        context: WorkflowContext,
    ):

        draft = await self.draft_service.get_by_id(
            context.draft_id
        )

        order, confirmation_message = (
            await self.order_orchestrator.checkout(
                draft=draft,
            )
        )

        return self.transition(
            next_state=WorkflowState.ORDER_CONFIRMED,
            message=confirmation_message,
            order_id=order.order_id,
        )