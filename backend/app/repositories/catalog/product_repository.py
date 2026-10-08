from __future__ import annotations

from sqlalchemy import or_, select, UUID
from sqlalchemy.orm import selectinload
from app.models.catalog.product import Product
from app.models.catalog.product_variant import ProductVariant
from app.repositories.base import BaseRepository


class ProductRepository(BaseRepository[Product]):
    """
    Repository for Product entity.
    """

    def __init__(self, session):
        super().__init__(session, Product)

    # ------------------------------------------------------------------
    # Product Queries
    # ------------------------------------------------------------------

    async def get_by_name(
        self,
        name: str,
    ) -> Product | None:

        result = await self.session.execute(
            select(Product)
            .where(Product.name.ilike(name))
        )

        return result.scalar_one_or_none()

    async def search(
            self,
            query: str,
    ) -> list[Product]:

        print(">>> Enter ProductRepository.search")

        stmt = (
            select(Product)
            .where(
                Product.is_active.is_(True),
                or_(
                    Product.name.ilike(f"%{query}%"),
                    Product.description.ilike(f"%{query}%"),
                ),
            )
            .order_by(Product.name)
        )

        print(">>> About to execute SQL")

        result = await self.session.execute(stmt)

        print(">>> SQL executed")

        products = result.scalars().all()

        print(">>> Products:", products)

        return list(products)

    async def get_variants(
            self,
            product_id: UUID,
    ) -> list[ProductVariant]:
        """
        Return all active variants for a product.
        """

        result = await self.session.execute(
            select(ProductVariant)
            .where(
                ProductVariant.product_id == product_id,
                ProductVariant.is_active.is_(True),
            )
            .order_by(
                ProductVariant.color,
                ProductVariant.size,
            )
        )

        return list(result.scalars().all())

    async def get_active_products(self) -> list[Product]:

        result = await self.session.execute(
            select(Product)
            .where(Product.is_active.is_(True))
            .order_by(Product.name)
        )

        return list(result.scalars().all())

    async def get_with_variants(
        self,
        product_id,
    ) -> Product | None:

        result = await self.session.execute(
            select(Product)
            .options(
                selectinload(Product.variants)
            )
            .where(Product.product_id == product_id)
        )

        return result.scalar_one_or_none()

    async def get_variant_by_sku(
        self,
        sku: str,
    ) -> ProductVariant | None:

        result = await self.session.execute(
            select(ProductVariant)
            .where(
                ProductVariant.sku == sku,
                ProductVariant.is_active.is_(True),
            )
        )

        return result.scalar_one_or_none()

    async def find_variant(
            self,
            product_id: UUID,
            attributes: dict[str, str],
    ) -> ProductVariant | None:
        """
        Find a product variant matching the supplied attributes.
        """

        query = select(ProductVariant).where(
            ProductVariant.product_id == product_id
        )

        if color := attributes.get("color"):
            query = query.where(
                ProductVariant.color == color
            )

        if size := attributes.get("size"):
            query = query.where(
                ProductVariant.size == size
            )

        result = await self.session.execute(query)

        return result.scalar_one_or_none()