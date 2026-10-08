from __future__ import annotations

from app.models.enums import WorkflowState
from app.Services.response.response_builder import ResponseBuilder
from app.schema.workflow import (
    WorkflowContext,
    WorkflowRequest,
)
from app.Services.customer.customer_service import CustomerService
from app.Services.validation.validation_service import ValidationService
from app.Services.payload.payload_builder import PayloadBuilder
from .base_handler import BaseHandler
from ...draft.draft_service import DraftService


class CollectAddressHandler(BaseHandler):
    """
    Collects or selects the delivery address.
    """

    def __init__(
        self,
        customer_service: CustomerService,
        validation_service: ValidationService,
        draft_service: DraftService,
        response_builder: ResponseBuilder,
        payload_builder: PayloadBuilder,
    ) -> None:

        self.customer_service = customer_service
        self.validation_service = validation_service
        self.draft_service = draft_service
        self.response_builder = response_builder
        self.payload_builder = payload_builder

    async def handle(
        self,
        request: WorkflowRequest,
        context: WorkflowContext,
    ):

        # ----------------------------------------------------
        # Use customer's default address
        # ----------------------------------------------------



        message = request.message.strip().lower()

        print(request.message)
        print(message)

        if "default" in message:

            address = await self.customer_service.get_default_address(
                request.customer_id,
            )

            if address is not None:
                draft = await self.draft_service.get_or_create_draft(
                    context.customer_id,
                    context.session_id,
                )

                await self.draft_service.attach_address(
                    draft,
                    address,
                )

                context.slots["address_id"] = address.address_id

                return self.transition(
                    next_state=WorkflowState.CALCULATE_PRICING,
                    message=self.response_builder.address_selected(
                        address,
                    ),
                    payload=self.payload_builder.address(
                        address,
                    ),
                    continue_processing=True,
                )


        # ----------------------------------------------------
        # Manual address entry
        # ----------------------------------------------------

        validation = self.validation_service.validate_required_fields(
            required_fields=[
                "address_line1",
                "city",
                "state",
                "postal_code",
                "country",
            ],
            slots=context.slots,
        )

        if not validation.valid:

            return self.transition(
                next_state=WorkflowState.COLLECT_ADDRESS,
                message=self.response_builder.address_required()
            )

        address = await self.customer_service.save_address(
            customer_id=request.customer_id,
            address=context.slots,
        )

        draft = await self.draft_service.get_or_create_draft(
            context.customer_id,
            context.session_id,
        )

        await self.draft_service.attach_address(
            draft,
            address,
        )

        context.slots["address_id"] = address.address_id

        await self.draft_service.update_from_slots(
            draft,
            context.slots,
        )

        return self.transition(
            next_state=WorkflowState.CALCULATE_PRICING,
            message=self.response_builder.address_saved(
                address,
            ),
            payload=self.payload_builder.address(
                address,
            ),
        )