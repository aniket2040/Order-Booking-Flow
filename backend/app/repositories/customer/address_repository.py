from __future__ import annotations

from uuid import UUID

from sqlalchemy import select

from app.models.customer.address import Address
from app.repositories.base import BaseRepository


class AddressRepository(BaseRepository[Address]):
    """
    Repository for Address entity.
    """

    def __init__(self, session):
        super().__init__(session, Address)

    # ------------------------------------------------------------------
    # Address Queries
    # ------------------------------------------------------------------

    async def get_default_address(
        self,
        customer_id: UUID,
    ) -> Address | None:

        result = await self.session.execute(
            select(Address).where(
                Address.customer_id == customer_id,
                Address.is_default.is_(True),
            )
        )

        return result.scalar_one_or_none()

    async def get_customer_addresses(
        self,
        customer_id: UUID,
    ) -> list[Address]:

        result = await self.session.execute(
            select(Address)
            .where(
                Address.customer_id == customer_id
            )
            .order_by(Address.is_default.desc())
        )

        return list(result.scalars().all())