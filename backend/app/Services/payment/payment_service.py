from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from app.models.enums import PaymentMethod, PaymentStatus
from app.models.order.payment import Payment
from app.repositories.order.payment_repository import PaymentRepository


class PaymentService:
    """
    Handles payment lifecycle.

    Version 1 supports only Cash on Delivery.
    """

    def __init__(
        self,
        payment_repository: PaymentRepository,
    ) -> None:
        self.payment_repository = payment_repository

    # ---------------------------------------------------------
    # Queries
    # ---------------------------------------------------------

    async def get_payment(
        self,
        order_id: UUID,
    ) -> Payment | None:
        """
        Retrieve payment by order ID.
        """
        return await self.payment_repository.get_by_order_id(order_id)

    # ---------------------------------------------------------
    # Payment Creation
    # ---------------------------------------------------------

    async def create_cod_payment(
        self,
        order_id: UUID,
        amount: Decimal,
    ) -> Payment:
        """
        Create a Cash on Delivery payment record.
        """

        payment = Payment(
            order_id=order_id,
            method=PaymentMethod.CASH_ON_DELIVERY,
            status=PaymentStatus.PENDING,
            amount=amount,
        )

        return await self.payment_repository.create(payment)

    # ---------------------------------------------------------
    # Status Updates
    # ---------------------------------------------------------

    async def mark_paid(
        self,
        payment: Payment,
    ) -> None:
        """
        Mark payment as paid.
        """
        payment.status = PaymentStatus.PAID

    async def mark_failed(
        self,
        payment: Payment,
    ) -> None:
        """
        Mark payment as failed.
        """
        payment.status = PaymentStatus.FAILED

    async def mark_cancelled(
        self,
        payment: Payment,
    ) -> None:
        """
        Mark payment as canceled.
        """
        payment.status = PaymentStatus.CANCELLED