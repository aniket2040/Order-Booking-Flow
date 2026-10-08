from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from pydantic import Field

from app.schema.common import BaseSchema
from app.schema.pricing import PricingSummary


class ReviewItem(BaseSchema):
    """
    Represents a single item displayed in the order review.
    """

    variant_id: UUID

    product_name: str

    variant_name: str

    sku: str

    quantity: int = Field(..., ge=1)

    unit_price: Decimal = Field(
        ...,
        decimal_places=2,
    )

    subtotal: Decimal = Field(
        ...,
        decimal_places=2,
    )
    image_url : str | None = None


class DeliverySummary(BaseSchema):
    """
    Delivery information shown during review.
    """

    recipient_name: str

    phone_number: str

    address: str

    city: str

    state: str

    postal_code: str

    country: str

    estimated_delivery: str | None = None



class OrderSummary(BaseSchema):
    """
    Complete order summary.
    """

    items: list[ReviewItem]

    pricing: PricingSummary

    delivery: DeliverySummary


class OrderReview(BaseSchema):
    """
    Review presented to the customer before order confirmation.
    """

    summary: OrderSummary

    confirmation_required: bool = True

    confirmation_message: str = (
        "Please review your order and confirm."
    )


