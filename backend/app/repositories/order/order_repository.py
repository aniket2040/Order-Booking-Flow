from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.catalog.product import Product
from app.models.catalog.product_variant import ProductVariant
from app.models.customer.address import Address
from app.models.order.order import Order
from app.models.order.order_item import OrderItem
from app.repositories.base import BaseRepository


class OrderRepository(BaseRepository[Order]):
    """
    Repository for Order aggregate.
    """

    def __init__(self, session):
        super().__init__(session, Order)

    # ------------------------------------------------------------------
    # Order Queries
    # ------------------------------------------------------------------

    async def get_by_order_number(
        self,
        order_number: str,
    ) -> Order | None:

        result = await self.session.execute(
            select(Order)
            .where(Order.order_number == order_number)
        )

        return result.scalar_one_or_none()

    async def get_customer_orders(
        self,
        customer_id: UUID,
    ) -> list[Order]:

        result = await self.session.execute(
            select(Order)
            .where(Order.customer_id == customer_id)
            .order_by(Order.created_at.desc())
        )

        return list(result.scalars().all())

    async def get_order_with_details(
            self,
            order_id: UUID,
    ) -> Order:
        """
        Returns an order with all relationships eagerly loaded.
        """

        result = await self.session.execute(
            select(Order)
            .options(
                selectinload(Order.customer),
                selectinload(Order.address),
                selectinload(Order.payment),
                selectinload(Order.shipment),

                selectinload(Order.items)
                .selectinload(OrderItem.variant)
                .selectinload(ProductVariant.product),
            )
            .where(
                Order.order_id == order_id
            )
        )

        return result.scalar_one()

    async def get_complete_order(
        self,
        order_id: UUID,
    ) -> Order | None:

        result = await self.session.execute(
            select(Order)
            .options(
                selectinload(Order.customer),
                selectinload(Order.address),
                selectinload(Order.payment),
                selectinload(Order.shipment),
                selectinload(Order.status_history),
                selectinload(Order.items)
                    .selectinload(OrderItem.variant)
                    .selectinload(ProductVariant.product)
                    .selectinload(Product.brand),
                selectinload(Order.items)
                    .selectinload(OrderItem.variant)
                    .selectinload(ProductVariant.product)
                    .selectinload(Product.category),
            )
            .where(Order.order_id == order_id)
        )

        return result.scalar_one_or_none()