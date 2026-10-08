from __future__ import annotations

from app.models.enums import (
    IntentType,
    WorkflowState,
)
from app.schema.workflow import (
    WorkflowContext,
    WorkflowRequest,
    WorkflowResult,
)

from .base_handler import BaseHandler


class DetectIntentHandler(BaseHandler):
    """
    Detects the user's intent.

    Version 1 uses simple keyword matching.
    Later this will delegate to the AI IntentExtractor.
    """

    async def handle(
        self,
        request: WorkflowRequest,
        context: WorkflowContext,
    ) -> WorkflowResult:

        message = request.message.lower()

        # --------------------------------------------------
        # Place Order
        # --------------------------------------------------

        if any(
            keyword in message
            for keyword in (
                "buy",
                "order",
                "purchase",
            )
        ):

            context.intent = IntentType.PLACE_ORDER

            return self.transition(
                next_state=WorkflowState.COLLECT_REQUIREMENTS,
                message="Let's place your order.",
            )

        product_keywords = {
            "nike",
            "adidas",
            "samsung",
            "shoe",
            "shoes",
            "air max",
            "earbuds",
            "black",
            "white",
            "size",
        }

        if any(keyword in message for keyword in product_keywords):
            context.intent = IntentType.PLACE_ORDER

            context.slots["raw_query"] = request.message

            return self.transition(
                next_state=WorkflowState.COLLECT_REQUIREMENTS,
                message="I'll help you find that product.",
                continue_processing=True,
            )

        # --------------------------------------------------
        # Confirm Order
        # --------------------------------------------------

        if message in (
            "yes",
            "confirm",
            "ok",
        ):

            request.intent = IntentType.CONFIRM_ORDER

            return self.transition(
                next_state=WorkflowState.CREATE_ORDER,
                message="Order confirmed.",
            )

        # --------------------------------------------------
        # Cancel
        # --------------------------------------------------

        if "cancel" in message:

            request.intent = IntentType.CANCEL_ORDER

            return self.transition(
                next_state=WorkflowState.END,
                message="Order cancelled.",
            )

        # --------------------------------------------------
        # Unknown
        # --------------------------------------------------

        request.intent = IntentType.UNKNOWN

        return self.transition(
            next_state=WorkflowState.DETECT_INTENT,
            message=(
                "I couldn't understand your request. "
                "Can you please rephrase it?"
            ),
        )