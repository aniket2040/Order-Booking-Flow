from __future__ import annotations

from abc import ABC, abstractmethod

from app.schema.common import ValidationResult
from app.schema.workflow import (
    WorkflowContext,
    WorkflowRequest,
    WorkflowResult,
)


class BaseHandler(ABC):
    """
    Base class for all workflow handlers.

    Every workflow handler follows the same lifecycle:

        execute()
            ↓
        validate()
            ↓
        handle()
            ↓
        WorkflowResult
    """

    def transition(
            self,
            *,
            next_state,
            message: str,
            success: bool = True,
            payload=None,
            continue_processing: bool = False,
            order_review=None,
            order_id=None,
    ) -> WorkflowResult:
        """
        Helper to create a WorkflowResult for a state transition.
        """

        return WorkflowResult(
            success=success,
            next_state=next_state,
            message=message,
            payload=payload,
            continue_processing=continue_processing,
            order_review=order_review,
            order_id=order_id,
        )

    async def execute(
        self,
        request: WorkflowRequest,
        context: WorkflowContext,
    ) -> WorkflowResult:
        """
        Execute the workflow step.
        """

        validation = await self.validate(
            request,
            context,
        )

        if not validation.valid:

            return WorkflowResult(
                success=False,
                next_state=context.workflow_state,
                message=validation.message or "Validation failed.",
                continue_processing=False,
            )

        return await self.handle(
            request,
            context,
        )

    async def validate(
        self,
        request: WorkflowRequest,
        context: WorkflowContext,
    ) -> ValidationResult:
        """
        Optional validation hook.

        Override only when validation is required.
        """

        return ValidationResult(valid=True)

    @abstractmethod
    async def handle(
        self,
        request: WorkflowRequest,
        context: WorkflowContext,
    ) -> WorkflowResult:
        """
        Execute the workflow logic.
        """
        raise NotImplementedError