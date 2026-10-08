from __future__ import annotations

from app.models.enums import (
    WorkflowState,
    WorkflowMode
)
from app.schema.workflow import (
    WorkflowContext,
    WorkflowRequest,
)

from .base_handler import BaseHandler


class ConfirmOrderHandler(BaseHandler):
    """
    Handles the customer's decision after reviewing
    the order summary.
    """



    async def handle(
        self,
        request: WorkflowRequest,
        context: WorkflowContext,
    ):

        print("=" * 60)
        print("CREATE ORDER HANDLER")
        print("Draft ID:", context.draft_id)
        print("=" * 60)

        decision = request.message.strip().lower()

        # ---------------------------------------------
        # Confirm
        # ---------------------------------------------

        if decision in (
            "yes",
            "confirm",
            "ok",
            "place order",
        ):

            return self.transition(
                next_state=WorkflowState.CREATE_ORDER,
                message="Order confirmed.",
            )

        # ---------------------------------------------
        # Modify
        # ---------------------------------------------

        # ---------------------------------------------
        # Modify
        # ---------------------------------------------

        if decision in (
                "modify",
                "change",
                "edit",
        ):
            context.workflow_mode = WorkflowMode.MODIFY_ORDER

            return self.transition(
                next_state=WorkflowState.COLLECT_REQUIREMENTS,
                message="Let's update your order.",
            )

        # ---------------------------------------------
        # Cancel
        # ---------------------------------------------

        if decision in (
            "cancel",
            "stop",
        ):

            return self.transition(
                next_state=WorkflowState.DETECT_INTENT,
                message="Order cancelled.",
            )

        # ---------------------------------------------
        # Unknown
        # ---------------------------------------------

        return self.transition(
            next_state=WorkflowState.CONFIRM_ORDER,
            message=(
                "Please reply with "
                "'confirm', 'modify', or 'cancel'."
            ),
        )