from __future__ import annotations
from app.Services.payload.payload_builder import PayloadBuilder
from app.models.enums import WorkflowState
from app.Services.response.response_builder import ResponseBuilder
from app.schema.workflow import (
    WorkflowContext,
    WorkflowRequest,
    WorkflowResult,
)
from app.Services.catalog.product_service import ProductService

from .base_handler import BaseHandler
from ...draft.draft_service import DraftService


class ResolveProductHandler(BaseHandler):
    """
    Resolves the requested product.
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
    ) -> WorkflowResult:

        print("=" * 60)
        print("Context slots:", context.slots)

        product_name = context.slots.get("product")

        print("Product name:", product_name)

        if not product_name:

            return self.transition(
                next_state=WorkflowState.COLLECT_REQUIREMENTS,
                message=self.response_builder.ask_product()
            )

        try:
            product = await self.product_service.resolve_product(product_name)
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise

        print("Resolved product:", product)

        if product is None:

            return self.transition(
                next_state=WorkflowState.COLLECT_REQUIREMENTS,
                message=self.response_builder.product_not_found(
                    product_name,
                ),
            )

        # Store resolved product for later handlers
        context.slots["product_id"] = product.product_id
        context.slots["product"] = product.name
        draft = await self.draft_service.get_or_create_draft(
            context.customer_id,
            context.session_id,
        )

        await self.draft_service.update_from_slots(
            draft,
            context.slots,
        )
        product = await self.product_service.resolve_product(product_name)

        variants = await self.product_service.get_product_variants(
            product.product_id,
        )


        return self.transition(
            next_state=WorkflowState.RESOLVE_VARIANT,
            message=self.response_builder.product_found(product),
            payload=self.payload_builder.product_selection(
                product,
                variants,
            ),
        )