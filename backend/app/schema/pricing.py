from __future__ import annotations

from decimal import Decimal

from pydantic import Field

from app.schema.common import BaseSchema


class PriceBreakdown(BaseSchema):
    """
    Represents a single pricing component.
    """

    label: str

    amount: Decimal = Field(
        ...,
        decimal_places=2,
    )


class PricingSummary(BaseSchema):
    """
    Represents the complete pricing calculation.
    """

    subtotal: Decimal = Field(
        default=Decimal("0.00"),
        decimal_places=2,
    )

    tax: Decimal = Field(
        default=Decimal("0.00"),
        decimal_places=2,
    )

    shipping_charge: Decimal = Field(
        default=Decimal("0.00"),
        decimal_places=2,
    )

    discount: Decimal = Field(
        default=Decimal("0.00"),
        decimal_places=2,
    )

    grand_total: Decimal = Field(
        default=Decimal("0.00"),
        decimal_places=2,
    )