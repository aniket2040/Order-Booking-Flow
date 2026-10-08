from __future__ import annotations

from app.schema.workflow import (
    WorkflowContext,
    WorkflowRequest,
    WorkflowResponse,
    WorkflowResult,
)


class WorkflowService:
    """
    Coordinates the order booking workflow.

    This service is responsible only for routing the current
    workflow state to the appropriate handler and converting
    the handler result into a response.
    """

    def __init__(
        self,
        handlers,
    ) -> None:

        self._handlers = handlers

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    async def process(
            self,
            request: WorkflowRequest,
            context: WorkflowContext,
    ) -> WorkflowResponse:

        result: WorkflowResult | None = None

        while True:

            print("=" * 60)
            print("Workflow State:", context.workflow_state)

            handler = self._get_handler(
                context.workflow_state,
            )

            print("Handler:", handler.__class__.__name__)

            result = await self._execute_handler(
                handler,
                request,
                context,
            )

            print("Next State:", result.next_state)
            print("Auto Continue:", result.continue_processing)
            print("=" * 60)

            self._update_context(
                context,
                result,
            )

            if not result.continue_processing:
                break

        return self._build_response(
            context,
            result,
        )

    # ---------------------------------------------------------
    # Internal
    # ---------------------------------------------------------

    def _get_handler(
        self,
        workflow_state,
    ):

        handler = self._handlers.get(workflow_state)

        if handler is None:

            raise ValueError(
                f"No handler registered for "
                f"{workflow_state}"
            )

        return handler

    async def _execute_handler(
        self,
        handler,
        request,
        context,
    ) -> WorkflowResult:

        return await handler.execute(
            request,
            context,
        )

    def _update_context(
        self,
        context: WorkflowContext,
        result: WorkflowResult,
    ) -> None:

        context.workflow_state = result.next_state

    def _build_response(
        self,
        context: WorkflowContext,
        result: WorkflowResult,
    ) -> WorkflowResponse:

        return WorkflowResponse(
            success=result.success,
            message=result.message,
            current_state=context.workflow_state,
            next_state=result.next_state,
            payload=result.payload,
            review=result.order_review,
            order_id=result.order_id,
        )