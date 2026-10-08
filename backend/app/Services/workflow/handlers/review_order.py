from __future__ import annotations

from sqlalchemy import inspect

from app.models.enums import WorkflowState
from app.Services.response.response_builder import ResponseBuilder
from app.schema.pricing import PricingSummary
from app.schema.workflow import (
    WorkflowContext,
    WorkflowRequest,
)
from app.Services.draft.draft_service import DraftService
from app.Services.review.summary_builder import SummaryBuilder

from .base_handler import BaseHandler

from app.Services.customer.customer_service import CustomerService

class ReviewOrderHandler(BaseHandler):

    def __init__(
        self,
        draft_service: DraftService,
        customer_service: CustomerService,
        summary_builder: SummaryBuilder,
        response_builder: ResponseBuilder,
    ) -> None:

        self.draft_service = draft_service
        self.customer_service = customer_service
        self.summary_builder = summary_builder
        self.response_builder = response_builder

    async def handle(
        self,
        request: WorkflowRequest,
        context: WorkflowContext,
    ):
        draft = await self.draft_service.get_review_draft(
            context.draft_id,
        )
        print("=" * 80)
        print("Draft Items Count:", len(draft.items))
        print("Draft Items:", draft.items)

        for item in draft.items:
            print("DraftItem:", item)
            print("Variant:", item.variant)
            if item.variant:
                print("Product:", item.variant.product)

        print("=" * 80)
        
        customer = await self.customer_service.get_by_id(
            draft.customer_id,
        )

        print("=" * 80)
        print("Draft:", draft)
        print("Customer ID:", draft.customer_id)
        print("Customer Relationship:", draft.customer)

        insp = inspect(draft)

        print("Customer loaded:", insp.attrs.customer.loaded_value)
        print("Address loaded:", insp.attrs.address.loaded_value)
        print("=" * 80)



        pricing = PricingSummary(
            subtotal=draft.subtotal,
            tax=draft.tax,
            shipping_charge=draft.shipping_charge,
            discount=draft.discount,
            grand_total=draft.grand_total,
        )

        review = self.summary_builder.build(
            draft=draft,
            pricing=pricing,
            customer=customer,
        )

        return self.transition(
            next_state=WorkflowState.CONFIRM_ORDER,
            message= self.response_builder.review_ready(
                review,
            ),
            order_review=review,
        )