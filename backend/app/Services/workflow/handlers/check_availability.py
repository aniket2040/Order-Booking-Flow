from __future__ import annotations

from app.models.enums import WorkflowState, WorkflowMode
from app.Services.response.response_builder import ResponseBuilder
from app.schema.workflow import (
    WorkflowContext,
    WorkflowRequest,
)
from app.Services.inventory.inventory_service import InventoryService
from app.Services.payload.payload_builder import PayloadBuilder
from .base_handler import BaseHandler


class CheckAvailabilityHandler(BaseHandler):
    """
    Checks whether the requested product variant
    is available in the requested quantity.
    """

    def __init__(
        self,
        inventory_service: InventoryService,
        response_builder: ResponseBuilder,
        payload_builder: PayloadBuilder,
    ) -> None:
        self.inventory_service = inventory_service
        self.response_builder = response_builder
        self.payload_builder = payload_builder

    async def handle(
        self,
        request: WorkflowRequest,
        context: WorkflowContext,
    ):

        variant_id = context.slots.get("variant_id")
        quantity = context.slots.get("quantity")

        available = await self.inventory_service.check_availability(
            variant_id=variant_id,
            quantity=quantity,
        )

        if not available:

            return self.transition(
                next_state=WorkflowState.CHECK_AVAILABILITY,
                message=self.response_builder.out_of_stock(
                    quantity,
                ),
                payload=self.payload_builder.inventory(
                    available=False,
                    quantity=quantity,
                ),
            )

        if context.workflow_mode == WorkflowMode.MODIFY_ORDER:
            return self.transition(
                next_state=WorkflowState.CALCULATE_PRICING,
                message=self.response_builder.availability_confirmed_modify(),
                continue_processing=True,
            )

        return self.transition(
            next_state=WorkflowState.COLLECT_ADDRESS,
            message=self.response_builder.item_available(),
            payload=self.payload_builder.inventory(
                available=True,
                quantity=quantity,
            ),
            continue_processing=True,
        )