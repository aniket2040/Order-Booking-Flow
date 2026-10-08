from __future__ import annotations

from app.models.enums import WorkflowState
from app.schema.workflow import (
    WorkflowContext,
    WorkflowRequest,
)
from app.Services.draft.draft_service import DraftService
from app.Services.pricing.pricing_service import PricingService
from app.Services.response.response_builder import ResponseBuilder
from .base_handler import BaseHandler


class CalculatePricingHandler(BaseHandler):
    """
    Calculates the complete order pricing.
    """

    def __init__(
        self,
        draft_service: DraftService,
        pricing_service: PricingService,
        response_builder: ResponseBuilder,
    ) -> None:

        self.draft_service = draft_service
        self.pricing_service = pricing_service
        self.response_builder = response_builder

    async def handle(
        self,
        request: WorkflowRequest,
        context: WorkflowContext,
    ):

        draft = await self.draft_service.get_by_id(
            context.draft_id
        )

        pricing = await self.pricing_service.calculate_order_pricing(
            draft=draft,
        )

        context.slots["pricing"] = pricing
        draft = await self.draft_service.get_or_create_draft(
            context.customer_id,
            context.session_id,
        )

        await self.draft_service.update_from_slots(
            draft,
            context.slots,
        )
        return self.transition(
            next_state=WorkflowState.REVIEW_ORDER,
            message=self.response_builder.pricing_ready(
                subtotal=pricing.subtotal,
                tax=pricing.tax,
                shipping=pricing.shipping_charge,
                discount=pricing.discount,
                grand_total=pricing.grand_total,
            ),
            continue_processing=True,
        )