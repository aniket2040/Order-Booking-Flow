from __future__ import annotations

from typing import Any, TYPE_CHECKING
from uuid import UUID
from decimal import Decimal

from alembic import context
from sqlalchemy import select, inspect
from sqlalchemy.orm import selectinload

if TYPE_CHECKING:
    from app.models.catalog.product_variant import ProductVariant
from app.models.customer.address import Address
from app.models.draft.draft import OrderDraft
from app.models.draft.draft_item import DraftItem
from app.models.enums import WorkflowState, WorkflowMode, DraftStatus
from app.repositories.draft.draft_repository import DraftRepository
from app.Services.pricing.pricing_service import PricingService


class DraftService:
    """
    Handles OrderDraft business operations.

    Responsibilities
    ----------------
    - Manage active drafts
    - Manage draft items
    - Attach delivery address
    - Manage workflow state
    - Recalculate pricing
    """

    def __init__(
        self,
        draft_repository: DraftRepository,
        pricing_service: PricingService,
    ) -> None:
        self.draft_repository = draft_repository
        self.pricing_service = pricing_service

    # ------------------------------------------------------------------
    # Draft
    # ------------------------------------------------------------------
    async def update_from_slots(
            self,
            draft: OrderDraft,
            slots: dict[str, Any],
    ) -> OrderDraft:
        """
        Persist extracted slots into the draft.
        """

        mapping = {
            "product": "requested_product",
            "product_id": "product_id",
            "variant_id": "variant_id",
            "quantity": "quantity",
            "brand": "selected_brand",
            "color": "selected_color",
            "size": "selected_size",
            "address_id": "address_id",
        }

        for slot_name, model_field in mapping.items():

            if slot_name in slots and slots[slot_name] is not None:
                setattr(
                    draft,
                    model_field,
                    slots[slot_name],
                )

        return await self.draft_repository.update(
            draft
        )

    async def get_by_id(
            self,
            draft_id: UUID,
    ) -> OrderDraft | None:
        """
        Retrieve a draft by its ID.
        """

        return await self.draft_repository.get_by_id(
            draft_id,
        )

    async def get_active_draft(
        self,
        customer_id: UUID,
    ) -> OrderDraft | None:
        """
        Retrieve the customer's active draft.
        """

        return await self.draft_repository.get_active_draft(
            customer_id
        )

    async def get_or_create_draft(
        self,
        customer_id: UUID,
        session_id: UUID,
    ) -> OrderDraft:
        """
        Retrieve the customer's active draft or
        create a new one if none exists.
        """

        draft = await self.draft_repository.get_by_session(
            session_id,
        )

        if draft:
            return draft

        return await self.create_draft(
            OrderDraft(
                customer_id=customer_id,
                session_id=session_id,
            )
        )

    async def create_draft(
        self,
        draft: OrderDraft,
    ) -> OrderDraft:
        """
        Create a new draft.
        """

        return await self.draft_repository.create(
            draft
        )

    async def build_context(
            self,
            draft: OrderDraft,
    ) -> dict:

        return {
            "product": draft.requested_product,
            "product_id": draft.product_id,
            "variant_id": draft.variant_id,
            "quantity": draft.quantity,
            "color": draft.selected_color,
            "size": draft.selected_size,
            "brand": draft.selected_brand,
            "address_id": draft.address_id,
        }

    async def clear(
        self,
        draft: OrderDraft,
    ) -> None:
        """
        Reset the draft.
        """

        draft.items.clear()

        draft.address = None
        draft.address_id = None

        draft.subtotal = Decimal("0.00")
        draft.tax = Decimal("0.00")
        draft.shipping_charge = Decimal("0.00")
        draft.discount = Decimal("0.00")
        draft.grand_total = Decimal("0.00")

    async def mark_completed(
        self,
        draft: OrderDraft | None,
    ) -> None:
        """
        Mark the draft as completed.
        """

        print("Before:", draft.status)

        draft.status = DraftStatus.COMPLETED

        print("After:", draft.status)

        print(
            inspect(draft).attrs.status.history
        )

        await self.draft_repository.update(
            draft,
        )

    async def is_complete(
        self,
        draft: OrderDraft,
    ) -> bool:
        """
        Returns True when the draft contains all
        information required for checkout.
        """

        return (
            len(draft.items) > 0
            and draft.address is not None
        )

    # ------------------------------------------------------------------
    # Draft Items
    # ------------------------------------------------------------------

    async def add_item(
        self,
        draft: OrderDraft,
        item: DraftItem,
    ) -> None:
        """
        Add a product to the draft.

        If the variant already exists,
        increase the quantity instead.
        """

        for existing in draft.items:

            if existing.variant_id == item.variant_id:

                existing.quantity += item.quantity
                existing.subtotal = (
                    existing.unit_price
                    * existing.quantity
                )

                await self.recalculate_totals(
                    draft
                )

                return

        draft.items.append(item)

        await self.recalculate_totals(
            draft,
        )

        await self.draft_repository.update(
            draft,
        )

    async def remove_item(
        self,
        draft: OrderDraft,
        variant_id: UUID,
    ) -> None:
        """
        Remove an item from the draft.
        """

        draft.items = [
            item
            for item in draft.items
            if item.variant_id != variant_id
        ]

        await self.recalculate_totals(
            draft,
        )

        await self.draft_repository.update(
            draft,
        )

    async def update_quantity(
        self,
        draft: OrderDraft,
        variant_id: UUID,
        quantity: int,
    ) -> None:
        """
        Update the quantity of a draft item.
        """

        for item in draft.items:

            if item.variant_id == variant_id:

                item.quantity = quantity

                item.subtotal = (
                    item.unit_price
                    * quantity
                )

                break

        await self.recalculate_totals(
            draft,
        )

        await self.draft_repository.update(
            draft,
        )

    async def sync_item_from_variant(
            self,
            draft: OrderDraft,
            variant: ProductVariant,
            quantity: int,
    ) -> None:
        """
        Synchronize the draft item with the selected variant.

        - Creates a new DraftItem if none exists.
        - Updates quantity if the same variant already exists.
        - Replaces the existing DraftItem if the variant changed.
        """

        # -----------------------------------------
        # No existing item
        # -----------------------------------------

        if not draft.items:
            item = DraftItem(
                variant_id=variant.variant_id,
                quantity=quantity,
                unit_price=variant.price,
                subtotal=variant.price * quantity,
            )

            await self.add_item(
                draft,
                item,
            )

            return

        existing = draft.items[0]

        # -----------------------------------------
        # Same variant
        # -----------------------------------------

        if existing.variant_id == variant.variant_id:
            await self.update_quantity(
                draft,
                variant.variant_id,
                quantity,
            )

            return

        # -----------------------------------------
        # Different variant
        # -----------------------------------------

        await self.remove_item(
            draft,
            existing.variant_id,
        )

        item = DraftItem(
            variant_id=variant.variant_id,
            quantity=quantity,
            unit_price=variant.price,
            subtotal=variant.price * quantity,
        )

        await self.add_item(
            draft,
            item,
        )

    # ------------------------------------------------------------------
    # Address
    # ------------------------------------------------------------------

    async def attach_address(
            self,
            draft: OrderDraft,
            address: Address,
    ) -> None:
        """
        Attach a delivery address to the draft.
        """

        draft.address = address
        draft.address_id = address.address_id

        await self.draft_repository.update(
            draft,
        )



    # ------------------------------------------------------------------
    # Workflow
    # ------------------------------------------------------------------

    async def update_workflow(
        self,
        draft: OrderDraft,
        state: WorkflowState,
    ) -> None:
        """
        Update the workflow state.
        """

        draft.workflow_state = state
        await self.draft_repository.update(draft)

    async def update_workflow_mode(
            self,
            draft: OrderDraft,
            mode: WorkflowMode,
    ) -> None:

        draft.workflow_mode = mode

        await self.draft_repository.update(
            draft,
        )

    # ------------------------------------------------------------------
    # Pricing
    # ------------------------------------------------------------------

    async def recalculate_totals(
        self,
        draft: OrderDraft,
    ) -> None:
        """
        Recalculate draft totals.
        """

        pricing = (
            await self.pricing_service.calculate_order_pricing(
                draft
            )
        )

        draft.subtotal = pricing.subtotal
        draft.tax = pricing.tax
        draft.shipping_charge = (
            pricing.shipping_charge
        )
        draft.discount = pricing.discount
        draft.grand_total = pricing.grand_total

    async def abandon_active_draft(
            self,
            customer_id: UUID,
    ) -> None:
        """
        Mark the customer's active draft as abandoned.
        """

        draft = await self.draft_repository.get_active_by_customer(
            customer_id,
        )

        if draft is None:
            return

        draft.status = DraftStatus.ABANDONED

        await self.draft_repository.update(
            draft,
        )

    async def get_review_draft(
            self,
            draft_id: UUID,
    ) -> OrderDraft | None:

        return await self.draft_repository.get_review_draft(
            draft_id,
        )