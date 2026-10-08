from __future__ import annotations

from app.models.order.order import Order


class NotificationService:
    """
    Builds customer-facing notifications.

    Version 1 only generates notification messages.
    """

    def build_order_confirmation(
        self,
        order: Order,
    ) -> str:
        """
        Build the order confirmation message.
        """

        estimated_delivery = (
            order.shipment.expected_delivery_date.strftime("%d %b %Y")
            if order.shipment
            and order.shipment.expected_delivery_date
            else "To be announced"
        )

        payment_status = (
            order.payment.status.value
            if order.payment
            else "Pending"
        )

        return (
            f"🎉 Your order has been placed successfully!\n\n"
            f"Order ID: {order.order_number}\n"
            f"Payment Method: Cash on Delivery\n"
            f"Payment Status: {payment_status}\n"
            f"Total Amount: ₹{order.grand_total}\n"
            f"Estimated Delivery: {estimated_delivery}\n\n"
            f"Thank you for shopping with us!"
        )

    def build_order_cancelled(
        self,
        order: Order,
    ) -> str:
        """
        Build the order cancellation message.
        """

        return (
            f"Your order {order.order_number} "
            "has been cancelled successfully."
        )

    def build_payment_received(
        self,
        order: Order,
    ) -> str:
        """
        Build the payment received message.
        """

        return (
            f"Payment received for Order "
            f"{order.order_number}. Thank you!"
        )