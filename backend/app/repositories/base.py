from __future__ import annotations

from typing import Generic, TypeVar, Any
from uuid import UUID

from sqlalchemy import select , inspect , exists
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base

# ----------------------------------------------------------------------
# Generic Type
# ----------------------------------------------------------------------

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Generic repository providing common database operations.

    Concrete repositories should inherit from this class.
    """

    def __init__(
        self,
        session: AsyncSession,
        model: type[ModelType],
    ) -> None:
        self.session = session
        self.model = model

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------

    async def get_by_id(
        self,
        entity_id: UUID,
    ) -> ModelType | None:

        pk = inspect(self.model).primary_key[0]

        result = await self.session.execute(
            select(self.model).where(pk==entity_id)
        )

        return result.scalar_one_or_none()

    async def get_all(self) -> list[ModelType]:

        result = await self.session.execute(
            select(self.model)
        )

        return list(result.scalars().all())

    # ------------------------------------------------------------------
    # Write
    # ------------------------------------------------------------------

    async def create(
        self,
        entity: ModelType,
    ) -> ModelType:

        self.session.add(entity)

        await self.session.flush()

        return entity

    async def delete(
        self,
        entity: ModelType,
    ) -> None:

        await self.session.delete(entity)

    async def refresh(
        self,
        entity: ModelType,
    ) -> Any:

        refreshed = await self.session.refresh(entity)

        return refreshed

    async def update(
            self,
            entity: ModelType,
    ) -> ModelType:
        """
        Persist changes made to an existing entity.
        """

        await self.session.flush()

        return entity

    async def exists(
            self,
            entity_id: UUID,
    ) -> bool:
        """
        Check whether an entity exists by its primary key.

        Args:
            entity_id: Primary key of the entity.

        Returns:
            True if the entity exists, otherwise False.
        """

        pk = inspect(self.model).primary_key[0]

        statement = select(
            exists().where(pk == entity_id)
        )

        result = await self.session.scalar(statement)

        return bool(result)