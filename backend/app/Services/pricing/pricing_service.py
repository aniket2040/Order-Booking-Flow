from __future__ import annotations

from decimal import Decimal

from app.models.draft.draft import OrderDraft
from app.schema.pricing import PricingSummary


class PricingService:
    """
    Handles pricing calculations for order drafts
    and orders.
    """

    TAX_RATE = Decimal("0.18")
    SHIPPING_CHARGE = Decimal("100.00")
    FREE_SHIPPING_THRESHOLD = Decimal("1000.00")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def calculate_order_pricing(
        self,
        draft: OrderDraft,
    ) -> PricingSummary:
        """
        Calculate the complete pricing summary
        for an order draft.
        """

        subtotal = self.calculate_subtotal(
            draft
        )

        tax = self.calculate_tax(
            subtotal
        )

        shipping = self.calculate_shipping(
            subtotal
        )

        discount = self.calculate_discount(
            draft,
            subtotal,
        )

        grand_total = (
            subtotal
            + tax
            + shipping
            - discount
        )

        return PricingSummary(
            subtotal=subtotal,
            tax=tax,
            shipping_charge=shipping,
            discount=discount,
            grand_total=grand_total,
        )

    # ------------------------------------------------------------------
    # Individual Calculations
    # ------------------------------------------------------------------

    def calculate_subtotal(
        self,
        draft: OrderDraft,
    ) -> Decimal:
        """
        Calculate the subtotal of all draft items.
        """

        return sum(
            (
                item.subtotal
                for item in draft.items
            ),
            start=Decimal("0.00"),
        )

    def calculate_tax(
        self,
        subtotal: Decimal,
    ) -> Decimal:
        """
        Calculate tax.
        """

        return (
            subtotal * self.TAX_RATE
        ).quantize(
            Decimal("0.01")
        )

    def calculate_shipping(
        self,
        subtotal: Decimal,
    ) -> Decimal:
        """
        Calculate shipping charges.
        """

        if (
            subtotal
            >= self.FREE_SHIPPING_THRESHOLD
        ):
            return Decimal("0.00")

        return self.SHIPPING_CHARGE

    def calculate_discount(
        self,
        draft: OrderDraft,
        subtotal: Decimal,
    ) -> Decimal:
        """
        Calculate discounts.

        Version 1:
            No promotional discounts.
        """

        return Decimal("0.00")