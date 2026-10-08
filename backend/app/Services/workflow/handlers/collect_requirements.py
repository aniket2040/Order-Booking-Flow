from __future__ import annotations

from app.ai.slot_extractor import SlotExtractor
from app.models.enums import WorkflowState
from app.schema.workflow import (
    WorkflowContext,
    WorkflowRequest,
    WorkflowResult,
)
from app.Services.validation.validation_service import ValidationService
from app.Services.response.response_builder import ResponseBuilder
from .base_handler import BaseHandler
from ...draft.draft_service import DraftService


class CollectRequirementsHandler(BaseHandler):
    """
    Collects the minimum information required
    to continue the order workflow.
    """

    REQUIRED_FIELDS = (
        "product",
        "quantity",
    )

    def __init__(
        self,
        validation_service: ValidationService,
        draft_service: DraftService,
        slot_extractor: SlotExtractor,
        response_builder: ResponseBuilder,
    ) -> None:
        self.validation_service = validation_service
        self.draft_service = draft_service
        self.slot_extractor = slot_extractor
        self.response_builder = response_builder

    async def handle(
            self,
            request: WorkflowRequest,
            context: WorkflowContext,
    ) -> WorkflowResult:
        print("=" * 60)
        print("Incoming message:", request.message)

        slots = await self.slot_extractor.extract(
            request.message,
        )

        print("Extracted:", slots)

        previous_slots = context.slots.copy()

        context.slots.update(slots)

        for field, value in slots.items():

            if previous_slots.get(field) != value:
                context.modified_fields.add(field)

        print("Context:", context.slots)

        print("Validation input:", context.slots)
        draft = await self.draft_service.get_or_create_draft(
            customer_id=context.customer_id,
            session_id=context.session_id,
        )

        await self.draft_service.update_from_slots(
            draft,
            context.slots,
        )

        print("Slots before validation:")
        print(context.slots)

        validation = self.validation_service.validate_required_fields(
            required_fields=list(self.REQUIRED_FIELDS),
            slots=context.slots,
        )

        print("Validation result:", validation.valid, validation.message)

        if not validation.valid:
            return self.transition(
                next_state=WorkflowState.COLLECT_REQUIREMENTS,
                message=self.response_builder.missing_required_fields(
                    validation.field,
                ),
            )

        return self.transition(
            next_state=WorkflowState.RESOLVE_PRODUCT,
            message=self.response_builder.requirements_collected(),
            continue_processing=True,
        )