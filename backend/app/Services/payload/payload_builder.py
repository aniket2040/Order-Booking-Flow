from __future__ import annotations

from decimal import Decimal

from app.models.catalog.product import Product
from app.models.catalog.product_variant import ProductVariant
from app.models.customer.address import Address
from app.models.draft.draft import OrderDraft
from app.schema.review import OrderReview


class PayloadBuilder:
    """
    Builds structured payloads for the frontend/UI.

    This class contains no business logic and no
    conversational text.
    """

    # ---------------------------------------------------------
    # Product
    # ---------------------------------------------------------

    def product(
        self,
        product: Product,
    ) -> dict:

        return {
            "type": "PRODUCT",
            "product": {
                "id": str(product.product_id),
                "name": product.name,
                "description": product.description,
            },
        }

    def product_selection(
        self,
        product: Product,
        variants: list[ProductVariant],
    ) -> dict:

        return {
            "type": "PRODUCT_SELECTION",
            "product": {
                "id": str(product.product_id),
                "name": product.name,
                "description": product.description,
            },
            "variants": [
                {
                    "variant_id": str(v.variant_id),
                    "sku": v.sku,
                    "color": v.color,
                    "size": v.size,
                    "price": float(v.price),
                }
                for v in variants
            ],
        }

    # ---------------------------------------------------------
    # Variant
    # ---------------------------------------------------------

    def variant(
        self,
        variant: ProductVariant,
        quantity: int,
    ) -> dict:

        return {
            "type": "VARIANT",
            "variant": {
                "variant_id": str(variant.variant_id),
                "sku": variant.sku,
                "color": variant.color,
                "size": variant.size,
                "price": float(variant.price),
                "quantity": quantity,
            },
        }

    # ---------------------------------------------------------
    # Inventory
    # ---------------------------------------------------------

    def inventory(
        self,
        available: bool,
        quantity: int,
    ) -> dict:

        return {
            "type": "INVENTORY",
            "available": available,
            "quantity": quantity,
        }

    # ---------------------------------------------------------
    # Address
    # ---------------------------------------------------------

    def address(
        self,
        address: Address,
    ) -> dict:

        return {
            "type": "ADDRESS",
            "address": {
                "address_id": str(address.address_id),
                "address_line1": address.address_line1,
                "address_line2": address.address_line2,
                "city": address.city,
                "state": address.state,
                "country": address.country,
                "postal_code": address.postal_code,
            },
        }

    # ---------------------------------------------------------
    # Pricing
    # ---------------------------------------------------------

    def pricing(
        self,
        draft: OrderDraft,
    ) -> dict:

        return {
            "type": "PRICING",
            "pricing": {
                "subtotal": float(draft.subtotal),
                "tax": float(draft.tax),
                "shipping": float(draft.shipping_charge),
                "discount": float(draft.discount),
                "grand_total": float(draft.grand_total),
                "currency": draft.currency,
            },
        }

    # ---------------------------------------------------------
    # Review
    # ---------------------------------------------------------

    def review(
        self,
        draft: OrderDraft,
        review: OrderReview,
    ) -> dict:

        return {
            "type": "ORDER_REVIEW",
            "review": review.model_dump(),
            "pricing": {
                "subtotal": float(draft.subtotal),
                "tax": float(draft.tax),
                "shipping": float(draft.shipping_charge),
                "discount": float(draft.discount),
                "grand_total": float(draft.grand_total),
            },
        }

    # ---------------------------------------------------------
    # Order
    # ---------------------------------------------------------

    def order_confirmed(
        self,
        order_id,
        order_number: str,
    ) -> dict:

        return {
            "type": "ORDER_CONFIRMED",
            "order": {
                "order_id": str(order_id),
                "order_number": order_number,
            },
        }

    # ---------------------------------------------------------
    # Generic
    # ---------------------------------------------------------

    def error(
        self,
        reason: str,
    ) -> dict:

        return {
            "type": "ERROR",
            "reason": reason,
        }