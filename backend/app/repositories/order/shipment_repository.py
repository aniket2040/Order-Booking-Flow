from __future__ import annotations

from uuid import UUID

from sqlalchemy import select

from app.models.order.shipment import Shipment
from app.repositories.base import BaseRepository


class ShipmentRepository(BaseRepository[Shipment]):
    """
    Repository for Shipment entity.
    """

    def __init__(self, session):
        super().__init__(session, Shipment)

    async def get_by_order_id(
        self,
        order_id: UUID,
    ) -> Shipment | None:

        result = await self.session.execute(
            select(Shipment).where(
                Shipment.order_id == order_id
            )
        )

        return result.scalar_one_or_none()