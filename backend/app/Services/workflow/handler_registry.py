from __future__ import annotations

from app.models.enums import WorkflowState

from app.Services.workflow.handlers.base_handler import BaseHandler


class HandlerRegistry:
    """
    Stores and resolves workflow handlers.
    """

    def __init__(self) -> None:

        self._handlers: dict[
            WorkflowState,
            BaseHandler,
        ] = {}

    # ---------------------------------------------------------
    # Registration
    # ---------------------------------------------------------

    def register(
        self,
        workflow_state: WorkflowState,
        handler: BaseHandler,
    ) -> None:
        """
        Register a handler for a workflow state.
        """

        self._handlers[workflow_state] = handler

    # ---------------------------------------------------------
    # Lookup
    # ---------------------------------------------------------

    def get(
        self,
        workflow_state: WorkflowState,
    ) -> BaseHandler:
        """
        Return the registered handler.
        """

        handler = self._handlers.get(
            workflow_state
        )

        if handler is None:

            raise ValueError(
                f"No handler registered for "
                f"{workflow_state}"
            )

        return handler

    # ---------------------------------------------------------
    # Utility
    # ---------------------------------------------------------

    def exists(
        self,
        workflow_state: WorkflowState,
    ) -> bool:

        return workflow_state in self._handlers