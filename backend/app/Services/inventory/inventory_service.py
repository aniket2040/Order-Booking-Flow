from __future__ import annotations

from uuid import UUID

from app.models.catalog.inventory import Inventory
from app.repositories.catalog.inventory_repository import (
    InventoryRepository,
)


class InventoryService:
    """
    Handles inventory-related business operations.
    """

    def __init__(
        self,
        inventory_repository: InventoryRepository,
    ) -> None:

        self.inventory_repository = inventory_repository

    # ------------------------------------------------------------------
    # Inventory
    # ------------------------------------------------------------------

    async def get_inventory(
        self,
        variant_id: UUID,
    ) -> Inventory | None:
        """
        Return inventory for a product variant.
        """

        return await self.inventory_repository.get_by_variant_id(
            variant_id
        )

    async def check_availability(
        self,
        variant_id: UUID,
        quantity: int,
    ) -> bool:
        """
        Check whether the requested quantity is available.
        """

        inventory = await self.get_inventory(
            variant_id
        )

        if inventory is None:
            return False

        available = (
            inventory.available_stock -
            inventory.reserved_stock
        )

        return available >= quantity

    async def reserve_stock(
        self,
        variant_id: UUID,
        quantity: int,
    ) -> bool:
        """
        Reserve inventory for an order draft.
        """

        inventory = await self.get_inventory(
            variant_id
        )

        if inventory is None:
            return False

        available = (
            inventory.available_stock -
            inventory.reserved_stock
        )

        if available < quantity:
            return False

        inventory.reserved_stock += quantity

        await self.inventory_repository.refresh(
            inventory
        )

        return True

    async def release_stock(
        self,
        variant_id: UUID,
        quantity: int,
    ) -> bool:
        """
        Release previously reserved inventory.
        """

        inventory = await self.get_inventory(
            variant_id
        )

        if inventory is None:
            return False

        inventory.reserved_stock = max(
            inventory.reserved_stock - quantity,
            0,
        )

        await self.inventory_repository.refresh(
            inventory
        )

        return True

    async def deduct_stock(
        self,
        variant_id: UUID,
        quantity: int,
    ) -> bool:
        """
        Deduct stock after order creation.
        """

        inventory = await self.get_inventory(
            variant_id
        )

        if inventory is None:
            return False

        if inventory.reserved_stock >= quantity:
            inventory.reserved_stock -= quantity

        inventory.available_stock -= quantity

        await self.inventory_repository.refresh(
            inventory
        )

        return True