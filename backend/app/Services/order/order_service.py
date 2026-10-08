from __future__ import annotations
from uuid import UUID

from app.models.draft.draft import OrderDraft
from app.models.enums import (
    OrderStatus,
    ShipmentStatus,
)
from datetime import datetime
import uuid
from app.models.order.order import Order
from app.models.order.order_item import OrderItem
from app.models.order.order_status_history import OrderStatusHistory
from app.models.order.shipment import Shipment
from app.repositories.order.order_repository import OrderRepository
from app.Services.pricing.pricing_service import PricingService


class OrderService:
    """
    Handles Order domain operations.
    """

    def __init__(
        self,
        order_repository: OrderRepository,
        pricing_service: PricingService,
    ) -> None:

        self.order_repository = order_repository
        self.pricing_service = pricing_service

    # ---------------------------------------------------------
    # Queries
    # ---------------------------------------------------------

    async def get_order(
        self,
        order_id,
    ) -> Order | None:

        return await self.order_repository.get_complete_order(
            order_id
        )

    async def get_customer_orders(
        self,
        customer_id,
    ):

        return await self.order_repository.get_customer_orders(
            customer_id
        )

    # ---------------------------------------------------------
    # Order Creation
    # ---------------------------------------------------------

    async def get_complete_order(
            self,
            order_id: UUID,
    ) -> Order | None:
        return await self.order_repository.get_complete_order(
            order_id,
        )

    async def create_order(
        self,
        draft: OrderDraft,
        order_number: str,
    ) -> Order:
        """
        Convert a draft into an Order.
        """

        pricing = (
            await self.pricing_service.calculate_order_pricing(
                draft
            )
        )

        order = self._create_order(
            draft,
            pricing,
            order_number,
        )

        print("=" * 60)
        print("Draft:", draft.draft_id)
        print("Draft Items:", len(draft.items))

        for item in draft.items:
            print(
                "Variant:",
                item.variant_id,
                "Qty:",
                item.quantity,
            )

        print("=" * 60)

        self._create_items(
            order,
            draft,
        )

        print("=" * 60)
        print("Draft ID:", draft.draft_id)
        print("Draft Items:", len(draft.items))

        for item in draft.items:
            print(
                item.variant_id,
                item.quantity,
                item.unit_price,
            )

        print("=" * 60)

        self._create_shipment(
            order,
        )

        self._create_history(
            order,
        )

        return await self.order_repository.create(
            order
        )

    async def get_order_with_details(
            self,
            order_id: UUID,
    ) -> Order:
        """
        Returns a fully populated order.
        """

        return await self.order_repository.get_order_with_details(
            order_id,
        )



    def generate_order_number(self) -> str:
        """
        Generate a unique order number.

        Example:
            ORD-20260805-A3F91C
        """

        date = datetime.now().strftime("%Y%m%d")
        random = uuid.uuid4().hex[:6].upper()

        return f"ORD-{date}-{random}"

    # ---------------------------------------------------------
    # Private Builders
    # ---------------------------------------------------------

    def _create_order(
        self,
        draft: OrderDraft,
        pricing,
        order_number: str,
    ) -> Order:

        return Order(
            order_number=order_number,
            customer_id=draft.customer_id,
            address_id=draft.address_id,
            draft_id=draft.draft_id,
            subtotal=pricing.subtotal,
            tax=pricing.tax,
            shipping_charge=pricing.shipping_charge,
            discount=pricing.discount,
            grand_total=pricing.grand_total,
            currency=draft.currency,
            status=OrderStatus.CREATED,
        )

    def _create_items(
        self,
        order: Order,
        draft: OrderDraft,
    ) -> None:

        for item in draft.items:

            order.items.append(
                OrderItem(
                    variant_id=item.variant_id,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    subtotal=item.subtotal,
                )
            )

    def _create_shipment(
        self,
        order: Order,
    ) -> None:

        order.shipment = Shipment(
            status=ShipmentStatus.PENDING,
        )

    def _create_history(
        self,
        order: Order,
    ) -> None:

        order.status_history.append(
            OrderStatusHistory(
                status=OrderStatus.CREATED,
                remarks="Order created successfully.",
            )
        )

    # ---------------------------------------------------------
    # Status
    # ---------------------------------------------------------

    async def change_status(
        self,
        order: Order,
        status: OrderStatus,
        remarks: str | None = None,
    ) -> None:

        order.status = status

        order.status_history.append(
            OrderStatusHistory(
                status=status,
                remarks=remarks,
            )
        )