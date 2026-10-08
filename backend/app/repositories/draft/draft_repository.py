from __future__ import annotations

from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models import DraftItem, ProductVariant
from app.models.draft.draft import OrderDraft
from app.models.enums import DraftStatus
from app.repositories.base import BaseRepository


class DraftRepository(BaseRepository[OrderDraft]):
    """
    Repository for OrderDraft aggregate.
    """

    def __init__(self, session):
        super().__init__(session, OrderDraft)

    # ------------------------------------------------------------------
    # Draft Queries
    # ------------------------------------------------------------------




    async def get_active_draft(
        self,
        customer_id: UUID,
    ) -> OrderDraft | None:
        """
        Return the customer's active draft.
        """

        print("=" * 60)
        print("SESSION ID:", id(self.session))

        conn = await self.session.connection()

        print("CONNECTION:", conn)
        print("=" * 60)

        result = await self.session.execute(
            select(OrderDraft)
            .where(
                OrderDraft.customer_id == customer_id,
                OrderDraft.status == DraftStatus.ACTIVE,
            )
        )

        return result.scalar_one_or_none()

    async def update(
            self,
            draft: OrderDraft,
    ) -> OrderDraft:
        """
        Persist changes to an existing draft.
        """

        await self.session.flush()

        return draft

    async def get_by_session(
            self,
            session_id: UUID,
    ) -> OrderDraft | None:
        """
        Return the active draft for a conversation session.
        """

        result = await self.session.execute(
            select(OrderDraft)
            .where(
                OrderDraft.session_id == session_id,
                OrderDraft.status == DraftStatus.ACTIVE,
            )
        )


        return result.scalar_one_or_none()

    from sqlalchemy import select
    async def get_active_by_customer(
            self,
            customer_id: UUID,
    ) -> OrderDraft | None:
        """
        Return the customer's active draft.
        """

        result = await self.session.execute(
            select(OrderDraft).where(
                OrderDraft.customer_id == customer_id,
                OrderDraft.status == DraftStatus.ACTIVE,
            )
        )

        return result.scalar_one_or_none()

    async def get_review_draft(
            self,
            draft_id: UUID,
    ) -> OrderDraft | None:
        result = await self.session.execute(
            select(OrderDraft)
            .options(
                selectinload(OrderDraft.customer),
                selectinload(OrderDraft.address),
                selectinload(OrderDraft.items)
                .selectinload(DraftItem.variant)
                .selectinload(ProductVariant.product),
            )
            .where(
                OrderDraft.draft_id == draft_id,
            )
        )

        return result.scalar_one_or_none()

    async def get_active_by_session(
            self,
            session_id: UUID,
    ) -> OrderDraft | None:
        """
        Return the active draft for a conversation session.
        """

        result = await self.session.execute(
            select(OrderDraft).where(
                OrderDraft.session_id == session_id,
                OrderDraft.status == DraftStatus.ACTIVE,
            )
        )

        return result.scalar_one_or_none()

    async def get_complete_draft(
        self,
        draft_id: UUID,
    ) -> OrderDraft | None:
        """
        Load complete draft graph.
        """

        result = await self.session.execute(
            select(OrderDraft)
            .options(
                selectinload(OrderDraft.items)
                    .selectinload("variant"),
                selectinload(OrderDraft.customer),
                selectinload(OrderDraft.address),
            )
            .where(
                OrderDraft.draft_id == draft_id
            )
        )

        return result.scalar_one_or_none()

    async def get_draft_items(
        self,
        draft_id: UUID,
    ):
        """
        Return only draft items.
        """

        draft = await self.get_complete_draft(
            draft_id
        )

        if draft is None:
            return []

        return draft.items