from __future__ import annotations

from app.models.draft.draft import OrderDraft
from app.models.order.order import Order
from app.Services.draft.draft_service import DraftService
from app.Services.inventory.inventory_service import InventoryService
from app.Services.notification.notification_service import (
    NotificationService,
)
from app.Services.order.order_service import OrderService
from app.Services.payment.payment_service import PaymentService


class OrderOrchestrator:
    """
    Executes the complete order booking transaction.
    """

    def __init__(
        self,
        inventory_service: InventoryService,
        order_service: OrderService,
        payment_service: PaymentService,
        notification_service: NotificationService,
        draft_service: DraftService,
    ) -> None:

        self.inventory_service = inventory_service
        self.order_service = order_service
        self.payment_service = payment_service
        self.notification_service = notification_service
        self.draft_service = draft_service

    # ---------------------------------------------------------
    # Checkout
    # ---------------------------------------------------------

    async def checkout(
        self,
        draft: OrderDraft ,
    ) -> tuple[Order, str]:
        """
        Complete the checkout process.
        """

        # ---------------------------------------------
        # Reserve Inventory
        # ---------------------------------------------

        for item in draft.items:
            await self.inventory_service.reserve_stock(
                item.variant_id,
                item.quantity,
            )

        # ---------------------------------------------
        # Create Order
        # ---------------------------------------------

        order_number = self.order_service.generate_order_number()

        order = await self.order_service.create_order(
            draft,
            order_number,
        )

        # ---------------------------------------------
        # Create COD Payment
        # ---------------------------------------------

        await self.payment_service.create_cod_payment(
            order.order_id,
            order.grand_total,
        )

        # ---------------------------------------------
        # Deduct Inventory
        # ---------------------------------------------

        for item in draft.items:
            await self.inventory_service.deduct_stock(
                item.variant_id,
                item.quantity,
            )

        # ---------------------------------------------
        # Complete Draft
        # ---------------------------------------------
        print("Checkout Draft ID:", draft.draft_id)
        print("Checkout Draft Status:", draft.status)

        await self.draft_service.mark_completed(
            draft,
        )

        print("After mark_completed:", draft.status)

        # ---------------------------------------------
        # Reload Complete Order
        # ---------------------------------------------

        order = await self.order_service.get_complete_order(
            order.order_id,
        )

        print("Order Draft ID:", order.draft_id)

        draft = await self.draft_service.get_by_id(
            order.draft_id,
        )

        print("Loaded Draft ID:", draft.draft_id)
        print("Loaded Draft Status:", draft.status)

        # ---------------------------------------------
        # Build Notification
        # ---------------------------------------------

        message = self.notification_service.build_order_confirmation(
            order,
        )

        return order, message