from __future__ import annotations

from uuid import UUID

from app.models.catalog.product import Product
from app.models.catalog.product_variant import ProductVariant
from app.repositories.catalog.product_repository import ProductRepository


class ProductService:
    """
    Handles product catalog operations.

    Responsibilities
    ----------------
    - Search products
    - Resolve customer requested products
    - Resolve product variants
    - Suggest alternative products
    """

    def __init__(
        self,
        product_repository: ProductRepository,
    ) -> None:
        self.product_repository = product_repository

    # ------------------------------------------------------------------
    # Query Operations
    # ------------------------------------------------------------------

    async def search_products(
        self,
        query: str,
    ) -> list[Product]:
        """
        Search active products.
        """



        return await self.product_repository.search(query)

    async def get_product_variants(
            self,
            product_id: UUID,
    ) -> list[ProductVariant]:
        """
        Return all active variants of a product.
        """

        return await self.product_repository.get_variants(
            product_id,
        )

    async def get_product(
        self,
        product_id: UUID,
    ) -> Product | None:
        """
        Retrieve a product by its ID.
        """

        return await self.product_repository.get_by_id(
            product_id
        )

    async def get_variant(
        self,
        sku: str,
    ) -> ProductVariant | None:
        """
        Retrieve a product variant using SKU.
        """

        return await self.product_repository.get_variant_by_sku(
            sku
        )

    # ------------------------------------------------------------------
    # Product Resolution
    # ------------------------------------------------------------------

    async def resolve_product(
        self,
        query: str,
    ) -> Product | None:
        """
        Resolve the customer's requested product.

        Version 1:
            Returns the first matching active product.
        """
        print("Searching for :", query)
        products = await self.product_repository.search(
            query
        )

        print("Products found:", len(products))

        if not products:
            return None

        print("Matching products:", products[0].name)

        return products[0]

    async def resolve_variant(
        self,
        product_id: UUID,
        attributes: dict[str, str],
    ) -> ProductVariant | None:
        """
        Resolve the exact product variant.

        Version 1:
            Delegates variant lookup to the repository.
        """

        return await self.product_repository.find_variant(
            product_id=product_id,
            attributes=attributes,
        )

    async def find_best_variant(
        self,
        product_id: UUID,
    ) -> ProductVariant | None:
        """
        Return the best matching variant.

        Version 1:
            Returns the first active variant.
        """

        variants = await self.product_repository.get_with_variants(
            product_id,
        )

        if not variants:
            return None

        return variants[0]

    # ------------------------------------------------------------------
    # Recommendations
    # ------------------------------------------------------------------

    async def suggest_alternatives(
        self,
        query: str,
        limit: int = 5,
    ) -> list[Product]:
        """
        Return alternative products.
        """

        products = await self.product_repository.search(
            query
        )

        return products[:limit]