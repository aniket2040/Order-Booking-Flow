from __future__ import annotations

from datetime import timedelta

from app.models import Customer
from app.models.draft.draft import OrderDraft
from app.schema.pricing import PricingSummary
from app.schema.review import (
    DeliverySummary,
    OrderReview,
    OrderSummary,
    ReviewItem,
)


class SummaryBuilder:
    """
    Builds the order review presented to the customer.
    """

    def build(
        self,
        draft: OrderDraft,
        pricing: PricingSummary,
        customer  ,
    ) -> OrderReview:
        """
        Convert an OrderDraft into an OrderReview DTO.
        """

        items = [
            ReviewItem(
                variant_id=item.variant_id,
                product_name=item.variant.product.name,
                variant_name=item.variant.display_name,
                sku=item.variant.sku,
                quantity=item.quantity,
                unit_price=item.unit_price,
                subtotal=item.subtotal,
                image_url=None,
            )
            for item in draft.items
        ]

        delivery = DeliverySummary(
            recipient_name=customer.full_name,
            phone_number=customer.phone,
            address=draft.address.address_line1,
            city=draft.address.city,
            state=draft.address.state,
            postal_code=draft.address.postal_code,
            country=draft.address.country,
            estimated_delivery=(
                draft.created_at.date() + timedelta(days=5)
            ).strftime("%d %b %Y")
        )

        summary = OrderSummary(
            items=items,
            pricing=pricing,
            delivery=delivery,
        )

        return OrderReview(
            summary=summary,
            confirmation_required=True,
            confirmation_message=(
                "Please review your order and confirm."
            ),
        )