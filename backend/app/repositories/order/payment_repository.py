from __future__ import annotations

from uuid import UUID

from sqlalchemy import select

from app.models.base import Base
from app.models.order.payment import Payment
from app.repositories.base import BaseRepository


class PaymentRepository(BaseRepository[Payment]):
    """
    Repository for Payment entities.
    """

    def __init__(self, session):
        super().__init__(session, Payment)

    # ---------------------------------------------------------
    # Queries
    # ---------------------------------------------------------

    async def get_by_id(
        self,
        payment_id: UUID,
    ) -> Base | None:
        """
        Retrieve a payment by its ID.
        """

        return await super().get_by_id(
            payment_id
        )

    async def get_by_order_id(
        self,
        order_id: UUID,
    ) -> Payment | None:
        """
        Retrieve the payment associated
        with an order.
        """

        stmt = (
            select(Payment)
            .where(Payment.order_id == order_id)
        )

        result = await self.session.execute(
            stmt
        )

        return result.scalar_one_or_none()

    # ---------------------------------------------------------
    # Persistence
    # ---------------------------------------------------------

    async def create(
        self,
        payment: Payment,
    ) -> Payment:
        """
        Persist a payment.
        """

        return await super().create(
            payment
        )

    async def update(
            self,
            payment: Payment,
    ) -> Payment:
        """
        Persist modifications to a payment.
        """

        return await super().update(
            payment
        )

    
    async def exists(
        self,
        payment_id: UUID,
    ) -> bool:
        """
        Check whether a payment exists.
        """

        return await super().exists(
            payment_id
        )