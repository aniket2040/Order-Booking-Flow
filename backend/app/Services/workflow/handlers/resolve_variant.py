from __future__ import annotations
from app.Services.payload.payload_builder import PayloadBuilder
from app.models.enums import WorkflowState
from app.Services.response.response_builder import ResponseBuilder
from app.schema.workflow import (
    WorkflowContext,
    WorkflowRequest,
)
from app.Services.catalog.product_service import ProductService

from .base_handler import BaseHandler
from ...draft.draft_service import DraftService


class ResolveVariantHandler(BaseHandler):
    """
    Resolves the requested product variant.
    """

    def __init__(
        self,
        product_service: ProductService,
        draft_service: DraftService,
        response_builder: ResponseBuilder,
        payload_builder: PayloadBuilder,
    ) -> None:

        self.product_service = product_service
        self.draft_service = draft_service
        self.response_builder = response_builder
        self.payload_builder = payload_builder

    async def handle(
        self,
        request: WorkflowRequest,
        context: WorkflowContext,
    ):

        product_id = context.slots.get("product_id")

        if product_id is None:
            return self.transition(
                next_state=WorkflowState.RESOLVE_PRODUCT,
                message="Please select a product first.",
            )

        color = context.slots.get("color")
        size = context.slots.get("size")

        attributes = {
            "color": color,
            "size": size,
        }

        variant = await self.product_service.resolve_variant(
            product_id=product_id,
            attributes=attributes,
        )

        if variant is None:

            return self.transition(
                next_state=WorkflowState.RESOLVE_VARIANT,
                message=self.response_builder.variant_not_found()
            )

        context.slots["variant_id"] = variant.variant_id
        context.slots["sku"] = variant.sku

        draft = await self.draft_service.get_or_create_draft(
            context.customer_id,
            context.session_id,
        )

        await self.draft_service.update_from_slots(
            draft,
            context.slots,
        )

        await self.draft_service.sync_item_from_variant(
            draft=draft,
            variant=variant,
            quantity=context.slots.get("quantity", 1),
        )

        return self.transition(
            next_state=WorkflowState.CHECK_AVAILABILITY,
            message=self.response_builder.variant_selected(
                product_name=context.slots["product"],
                variant=variant,
                quantity=context.slots["quantity"],
            ),
            payload=self.payload_builder.variant(
                variant,
                context.slots["quantity"],
            ),
            continue_processing=True,
        )