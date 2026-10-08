from __future__ import annotations

from app.models.catalog.product import Product
from app.models.catalog.product_variant import ProductVariant
from app.models.customer.address import Address
from app.schema.review import OrderReview


class ResponseBuilder:
    """
    Builds user-facing chatbot responses.

    This class contains no business logic.
    It only formats responses for the user.
    """

    # ---------------------------------------------------------
    # Product
    # ---------------------------------------------------------

    def product_found(
        self,
        product: Product,
    ) -> str:

        return (
            f"✅ I found **{product.name}**.\n\n"
            "Let's choose the variant."
        )

    def product_not_found(
        self,
        query: str,
    ) -> str:

        return (
            f"❌ I couldn't find **{query}**.\n\n"
            "Please try another product."
        )

    # ---------------------------------------------------------
    # Variant
    # ---------------------------------------------------------

    def availability_confirmed_modify(self):
        return (
            "The updated item is available. "
            "Recalculating your order."
        )

    def variant_selected(
        self,
        product_name: str,
        variant: ProductVariant,
        quantity: int,
    ) -> str:

        return (
            "✅ Variant selected.\n\n"
            f"Product : {product_name}\n"
            f"Color   : {variant.color}\n"
            f"Size    : {variant.size}\n"
            f"Quantity: {quantity}\n"
            f"Price   : ₹{variant.price}"
        )

    def variant_not_found(self) -> str:

        return (
            "❌ The requested color or size is unavailable.\n\n"
            "Please choose another variant."
        )

    # ---------------------------------------------------------
    # Inventory
    # ---------------------------------------------------------

    def item_available(self) -> str:

        return (
            "✅ The requested item is available.\n\n"
            "Please provide your delivery address "
            "or type **Use my default address**."
        )

    def out_of_stock(
        self,
        requested_quantity: int,
    ) -> str:

        return (
            f"❌ Requested quantity ({requested_quantity}) "
            "is currently unavailable.\n\n"
            "Please choose another quantity."
        )

    # ---------------------------------------------------------
    # Address
    # ---------------------------------------------------------

    def address_required(self) -> str:

        return (
            "Please provide your delivery address.\n\n"
            "Or type:\n"
            "**Use my default address**"
        )

    def address_saved(
        self,
        address: Address,
    ) -> str:

        return (
            "✅ Delivery address saved.\n\n"
            f"{address.address_line1}\n"
            f"{address.city}, {address.state}\n"
            f"{address.country} - {address.postal_code}"
        )

    def address_selected(
        self,
        address: Address,
    ) -> str:

        return (
            "✅ Using your default address.\n\n"
            f"{address.address_line1}\n"
            f"{address.city}, {address.state}\n"
            f"{address.country} - {address.postal_code}"
        )

    # ---------------------------------------------------------
    # Pricing
    # ---------------------------------------------------------

    def pricing_ready(
        self,
        subtotal,
        tax,
        shipping,
        discount,
        grand_total,
    ) -> str:

        return (
            "💰 Pricing calculated.\n\n"
            f"Subtotal : ₹{subtotal}\n"
            f"Tax      : ₹{tax}\n"
            f"Shipping : ₹{shipping}\n"
            f"Discount : ₹{discount}\n"
            "----------------------\n"
            f"Total    : ₹{grand_total}"
        )

    # ---------------------------------------------------------
    # Review
    # ---------------------------------------------------------

    def review_ready(
            self,
            review
    ) -> str:
        lines = ["📋 Order Review", ""]

        for item in review.summary.items:
            lines.append(
                f"• {item.product_name}"
            )
            lines.append(
                f"  Qty: {item.quantity}"
            )
            lines.append(
                f"  ₹{item.subtotal}"
            )
            lines.append("")

        p = review.summary.pricing

        lines.extend([
            f"Subtotal : ₹{p.subtotal}",
            f"Tax      : ₹{p.tax}",
            f"Shipping : ₹{p.shipping_charge}",
            f"Total    : ₹{p.grand_total}",
            "",
            "Reply YES to confirm."
        ])

        return "\n".join(lines)

    def missing_required_fields(
            self,
            fields: str,
    ) -> str:
        return (
            "I need a little more information.\n\n"
            f"Missing: {fields}"
        )

    def requirements_collected(self) -> str:
        return (
            "Thanks! I have the required product details."
        )

    def ask_product(self):
        return (
            "Which product would you like to order?"
        )
    # ---------------------------------------------------------
    # Confirmation
    # ---------------------------------------------------------

    def confirmation_required(self) -> str:

        return (
            "If everything looks correct,\n"
            "reply with **Confirm** to place the order."
        )

    # ---------------------------------------------------------
    # Order
    # ---------------------------------------------------------

    def order_confirmed(
        self,
        order_number: str,
    ) -> str:

        return (
            "🎉 Order placed successfully!\n\n"
            f"Order Number: {order_number}"
        )

    def order_failed(
        self,
        reason: str,
    ) -> str:

        return (
            "❌ Unable to place your order.\n\n"
            f"Reason: {reason}"
        )

    # ---------------------------------------------------------
    # Generic
    # ---------------------------------------------------------

    def generic_error(self) -> str:

        return (
            "Something went wrong.\n"
            "Please try again."
        )