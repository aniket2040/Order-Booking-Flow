from __future__ import annotations

from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.orm import selectinload

from app.models.customer.customer import Customer
from app.repositories.base import BaseRepository


class CustomerRepository(BaseRepository[Customer]):
    """
    Repository for Customer entity.
    """

    def __init__(self, session):
        super().__init__(session, Customer)

    # ------------------------------------------------------------------
    # Customer Queries
    # ------------------------------------------------------------------

    async def get_by_email(
        self,
        email: str,
    ) -> Customer | None:

        result = await self.session.execute(
            select(Customer).where(
                Customer.email == email
            )
        )

        return result.scalar_one_or_none()

    async def get_by_phone(
        self,
        phone: str,
    ) -> Customer | None:

        result = await self.session.execute(
            select(Customer).where(
                Customer.phone == phone
            )
        )

        return result.scalar_one_or_none()

    async def find_customer(
        self,
        keyword: str,
    ) -> list[Customer]:

        result = await self.session.execute(
            select(Customer).where(
                or_(
                    Customer.full_name.ilike(f"%{keyword}%"),
                    Customer.email.ilike(f"%{keyword}%"),
                    Customer.phone.ilike(f"%{keyword}%"),
                )
            )
        )

        return list(result.scalars().all())

    async def get_with_addresses(
        self,
        customer_id: UUID,
    ) -> Customer | None:

        result = await self.session.execute(
            select(Customer)
            .options(
                selectinload(Customer.addresses)
            )
            .where(
                Customer.customer_id == customer_id
            )
        )

        return result.scalar_one_or_none()