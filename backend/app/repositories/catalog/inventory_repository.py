from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.catalog.inventory import Inventory
from app.models.catalog.product_variant import ProductVariant
from app.repositories.base import BaseRepository


class InventoryRepository(BaseRepository[Inventory]):
    """
    Repository for Inventory entity.
    """

    def __init__(self, session):
        super().__init__(session, Inventory)

    # ------------------------------------------------------------------
    # Inventory Queries
    # ------------------------------------------------------------------

    async def get_by_variant_id(
        self,
        variant_id: UUID,
    ) -> Inventory | None:
        """
        Get inventory for a product variant.
        """

        result = await self.session.execute(
            select(Inventory).where(
                Inventory.variant_id == variant_id
            )
        )

        return result.scalar_one_or_none()

    async def get_with_variant(
        self,
        variant_id: UUID,
    ) -> Inventory | None:
        """
        Load inventory together with its product variant.
        """

        result = await self.session.execute(
            select(Inventory)
            .options(
                selectinload(Inventory.variant)
            )
            .where(
                Inventory.variant_id == variant_id
            )
        )

        return result.scalar_one_or_none()

    async def get_low_stock(
        self,
    ) -> list[Inventory]:
        """
        Return all inventory records where
        available stock is below the reorder level.
        """

        result = await self.session.execute(
            select(Inventory).where(
                Inventory.available_stock <= Inventory.reorder_level
            )
        )

        return list(result.scalars().all())

    async def get_out_of_stock(
        self,
    ) -> list[Inventory]:
        """
        Return all variants that are out of stock.
        """

        result = await self.session.execute(
            select(Inventory).where(
                Inventory.available_stock <= 0
            )
        )

        return list(result.scalars().all())