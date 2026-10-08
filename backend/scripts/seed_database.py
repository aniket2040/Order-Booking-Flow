from __future__ import annotations
import sys
from pathlib import Path

# Add project root (backend/) to Python path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

import asyncio
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal

# ==========================================================
# Catalog Models
# ==========================================================

from app.models.catalog.category import Category
from app.models.catalog.brand import Brand
from app.models.catalog.product import Product
from app.models.catalog.product_variant import ProductVariant
from app.models.catalog.inventory import Inventory

# ==========================================================
# Customer Models
# ==========================================================

from app.models.customer.customer import Customer
from app.models.customer.address import Address

# ==========================================================
# Conversation Models
# ==========================================================

from app.models.conversation.session import ConversationSession
from app.models.conversation.message import ConversationMessage

# ==========================================================
# Draft Models
# ==========================================================

from app.models.draft.draft import OrderDraft
from app.models.draft.draft_item import DraftItem

# ==========================================================
# Order Models
# ==========================================================

from app.models.order.order import Order
from app.models.order.order_item import OrderItem
from app.models.order.payment import Payment
from app.models.order.shipment import Shipment
from app.models.order.order_status_history import (
    OrderStatusHistory,
)


# ==========================================================
# Seed Constants
# ==========================================================

DEFAULT_REORDER_LEVEL = 5

DEFAULT_COUNTRY = "India"

DEFAULT_STATE = "Karnataka"

DEFAULT_CITY = "Bengaluru"

DEFAULT_CURRENCY = "INR"


def money(
    value: str,
) -> Decimal:
    """
    Convert string to Decimal.
    """
    return Decimal(value)


async def flush(
    session: AsyncSession,
) -> None:
    """
    Flush pending changes.
    """
    await session.flush()


async def commit(
    session: AsyncSession,
) -> None:
    """
    Commit current transaction.
    """
    await session.commit()

async def rollback(
    session: AsyncSession,
) -> None:
    """
    Roll back current transaction.
    """
    await session.rollback()


async def database_already_seeded(
    session: AsyncSession,
) -> bool:
    """
    Check whether the database already contains seed data.
    """

    result = await session.execute(
        select(Category)
    )

    return result.scalars().first() is not None

async def seed_categories(
    session: AsyncSession,
) -> dict[str, Category]:
    """
    Seed product categories.
    """

    print("→ Seeding Categories...")

    categories = [
        Category(
            name="Shoes",
            description="Footwear and sports shoes",
        ),
        Category(
            name="Electronics",
            description="Electronic gadgets and accessories",
        ),
        Category(
            name="Clothing",
            description="Apparel and fashion products",
        ),
    ]

    session.add_all(categories)

    await flush(session)

    print(f"   ✓ {len(categories)} categories inserted.")

    return {
        category.name: category
        for category in categories
    }

async def seed_brands(
    session: AsyncSession,
) -> dict[str, Brand]:
    """
    Seed product brands.
    """

    print("→ Seeding Brands...")

    brands = [
        Brand(
            name="Nike",
            description="Global sportswear brand",
        ),
        Brand(
            name="Adidas",
            description="Sports apparel and footwear",
        ),
        Brand(
            name="Puma",
            description="Athletic footwear and apparel",
        ),
        Brand(
            name="Samsung",
            description="Consumer electronics",
        ),
        Brand(
            name="Apple",
            description="Consumer electronics and accessories",
        ),
    ]

    session.add_all(brands)

    await flush(session)

    print(f"   ✓ {len(brands)} brands inserted.")

    return {
        brand.name: brand
        for brand in brands
    }



async def seed_products(
    session: AsyncSession,
    categories: dict[str, Category],
    brands: dict[str, Brand],
) -> dict[str, Product]:
    """
    Seed products.
    """

    print("→ Seeding Products...")

    products = [

        # --------------------------------------------------
        # Nike
        # --------------------------------------------------

        Product(
            name="Nike Air Max",
            category_id=categories["Shoes"].category_id,
            brand_id=brands["Nike"].brand_id,
            description="Comfortable running shoes with Air cushioning.",
        ),

        Product(
            name="Nike Revolution 7",
            category_id=categories["Shoes"].category_id,
            brand_id=brands["Nike"].brand_id,
            description="Daily running shoes designed for comfort.",
        ),

        # --------------------------------------------------
        # Adidas
        # --------------------------------------------------

        Product(
            name="Adidas Ultraboost",
            category_id=categories["Shoes"].category_id,
            brand_id=brands["Adidas"].brand_id,
            description="Premium performance running shoes.",
        ),

        Product(
            name="Adidas Samba",
            category_id=categories["Shoes"].category_id,
            brand_id=brands["Adidas"].brand_id,
            description="Classic lifestyle sneakers.",
        ),

        # --------------------------------------------------
        # Puma
        # --------------------------------------------------

        Product(
            name="Puma RS-X",
            category_id=categories["Shoes"].category_id,
            brand_id=brands["Puma"].brand_id,
            description="Chunky sneakers with modern design.",
        ),

        # --------------------------------------------------
        # Samsung
        # --------------------------------------------------

        Product(
            name="Samsung Galaxy Buds Pro",
            category_id=categories["Electronics"].category_id,
            brand_id=brands["Samsung"].brand_id,
            description="Wireless earbuds with active noise cancellation.",
        ),

        Product(
            name="Samsung Galaxy Watch 7",
            category_id=categories["Electronics"].category_id,
            brand_id=brands["Samsung"].brand_id,
            description="Smartwatch with health and fitness tracking.",
        ),

        # --------------------------------------------------
        # Apple
        # --------------------------------------------------

        Product(
            name="Apple AirPods Pro 2",
            category_id=categories["Electronics"].category_id,
            brand_id=brands["Apple"].brand_id,
            description="Premium wireless earbuds with ANC.",
        ),
    ]

    session.add_all(products)

    await flush(session)

    print(f"   ✓ {len(products)} products inserted.")

    return {
        product.name: product
        for product in products
    }

async def seed_product_variants(
    session: AsyncSession,
    products: dict[str, Product],
) -> dict[str, ProductVariant]:
    """
    Seed product variants.
    """

    print("→ Seeding Product Variants...")

    variants = [

        # ==================================================
        # Nike Air Max
        # ==================================================

        ProductVariant(
            product_id=products["Nike Air Max"].product_id,
            sku="NIKE-AM-BLK-08",
            color="Black",
            size="8",
            price=money("5999.00"),
            weight=money("0.80"),
        ),

        ProductVariant(
            product_id=products["Nike Air Max"].product_id,
            sku="NIKE-AM-BLK-09",
            color="Black",
            size="9",
            price=money("5999.00"),
            weight=money("0.80"),
        ),

        ProductVariant(
            product_id=products["Nike Air Max"].product_id,
            sku="NIKE-AM-BLK-10",
            color="Black",
            size="10",
            price=money("5999.00"),
            weight=money("0.80"),
        ),

        ProductVariant(
            product_id=products["Nike Air Max"].product_id,
            sku="NIKE-AM-WHT-09",
            color="White",
            size="9",
            price=money("5999.00"),
            weight=money("0.80"),
        ),

        ProductVariant(
            product_id=products["Nike Air Max"].product_id,
            sku="NIKE-AM-WHT-10",
            color="White",
            size="10",
            price=money("5999.00"),
            weight=money("0.80"),
        ),

        # ==================================================
        # Nike Revolution 7
        # ==================================================

        ProductVariant(
            product_id=products["Nike Revolution 7"].product_id,
            sku="NIKE-R7-BLK-08",
            color="Black",
            size="8",
            price=money("4499.00"),
            weight=money("0.75"),
        ),

        ProductVariant(
            product_id=products["Nike Revolution 7"].product_id,
            sku="NIKE-R7-BLK-09",
            color="Black",
            size="9",
            price=money("4499.00"),
            weight=money("0.75"),
        ),

        ProductVariant(
            product_id=products["Nike Revolution 7"].product_id,
            sku="NIKE-R7-BLU-09",
            color="Blue",
            size="9",
            price=money("4499.00"),
            weight=money("0.75"),
        ),

        # ==================================================
        # Adidas Ultraboost
        # ==================================================

        ProductVariant(
            product_id=products["Adidas Ultraboost"].product_id,
            sku="ADI-UB-BLK-08",
            color="Black",
            size="8",
            price=money("7999.00"),
            weight=money("0.82"),
        ),

        ProductVariant(
            product_id=products["Adidas Ultraboost"].product_id,
            sku="ADI-UB-BLK-09",
            color="Black",
            size="9",
            price=money("7999.00"),
            weight=money("0.82"),
        ),

        ProductVariant(
            product_id=products["Adidas Ultraboost"].product_id,
            sku="ADI-UB-WHT-09",
            color="White",
            size="9",
            price=money("7999.00"),
            weight=money("0.82"),
        ),

        # ==================================================
        # Adidas Samba
        # ==================================================

        ProductVariant(
            product_id=products["Adidas Samba"].product_id,
            sku="ADI-SAM-WHT-08",
            color="White",
            size="8",
            price=money("6999.00"),
            weight=money("0.78"),
        ),

        ProductVariant(
            product_id=products["Adidas Samba"].product_id,
            sku="ADI-SAM-WHT-09",
            color="White",
            size="9",
            price=money("6999.00"),
            weight=money("0.78"),
        ),

        # ==================================================
        # Puma RS-X
        # ==================================================

        ProductVariant(
            product_id=products["Puma RS-X"].product_id,
            sku="PUMA-RSX-RED-08",
            color="Red",
            size="8",
            price=money("6499.00"),
            weight=money("0.79"),
        ),

        ProductVariant(
            product_id=products["Puma RS-X"].product_id,
            sku="PUMA-RSX-RED-09",
            color="Red",
            size="9",
            price=money("6499.00"),
            weight=money("0.79"),
        ),

        # ==================================================
        # Samsung Galaxy Buds Pro
        # ==================================================

        ProductVariant(
            product_id=products["Samsung Galaxy Buds Pro"].product_id,
            sku="SAM-BUDS-BLK",
            color="Black",
            size="Standard",
            price=money("9999.00"),
            weight=money("0.05"),
        ),

        ProductVariant(
            product_id=products["Samsung Galaxy Buds Pro"].product_id,
            sku="SAM-BUDS-WHT",
            color="White",
            size="Standard",
            price=money("9999.00"),
            weight=money("0.05"),
        ),

        ProductVariant(
            product_id=products["Samsung Galaxy Buds Pro"].product_id,
            sku="SAM-BUDS-PRP",
            color="Purple",
            size="Standard",
            price=money("9999.00"),
            weight=money("0.05"),
        ),

        # ==================================================
        # Samsung Galaxy Watch 7
        # ==================================================

        ProductVariant(
            product_id=products["Samsung Galaxy Watch 7"].product_id,
            sku="SAM-WATCH-40",
            color="Black",
            size="40mm",
            price=money("24999.00"),
            weight=money("0.15"),
        ),

        ProductVariant(
            product_id=products["Samsung Galaxy Watch 7"].product_id,
            sku="SAM-WATCH-44",
            color="Black",
            size="44mm",
            price=money("26999.00"),
            weight=money("0.17"),
        ),

        # ==================================================
        # Apple AirPods Pro 2
        # ==================================================

        ProductVariant(
            product_id=products["Apple AirPods Pro 2"].product_id,
            sku="APPLE-AIRPODS-PRO2",
            color="White",
            size="Standard",
            price=money("24900.00"),
            weight=money("0.06"),
        ),
    ]

    session.add_all(variants)

    await flush(session)

    print(f"   ✓ {len(variants)} product variants inserted.")

    return {
        variant.sku: variant
        for variant in variants
    }


async def seed_inventory(
    session: AsyncSession,
    variants: dict[str, ProductVariant],
) -> None:
    """
    Seed inventory for every product variant.
    """

    print("→ Seeding Inventory...")

    inventory = [

        # ==================================================
        # Nike Air Max
        # ==================================================

        Inventory(
            variant_id=variants["NIKE-AM-BLK-08"].variant_id,
            available_stock=20,
            reserved_stock=0,
            reorder_level=DEFAULT_REORDER_LEVEL,
        ),

        Inventory(
            variant_id=variants["NIKE-AM-BLK-09"].variant_id,
            available_stock=15,
            reserved_stock=2,
            reorder_level=DEFAULT_REORDER_LEVEL,
        ),

        # Intentionally Out of Stock
        Inventory(
            variant_id=variants["NIKE-AM-BLK-10"].variant_id,
            available_stock=0,
            reserved_stock=0,
            reorder_level=DEFAULT_REORDER_LEVEL,
        ),

        Inventory(
            variant_id=variants["NIKE-AM-WHT-09"].variant_id,
            available_stock=8,
            reserved_stock=1,
            reorder_level=DEFAULT_REORDER_LEVEL,
        ),

        Inventory(
            variant_id=variants["NIKE-AM-WHT-10"].variant_id,
            available_stock=6,
            reserved_stock=0,
            reorder_level=DEFAULT_REORDER_LEVEL,
        ),

        # ==================================================
        # Nike Revolution
        # ==================================================

        Inventory(
            variant_id=variants["NIKE-R7-BLK-08"].variant_id,
            available_stock=12,
            reserved_stock=1,
            reorder_level=DEFAULT_REORDER_LEVEL,
        ),

        Inventory(
            variant_id=variants["NIKE-R7-BLK-09"].variant_id,
            available_stock=5,
            reserved_stock=0,
            reorder_level=DEFAULT_REORDER_LEVEL,
        ),

        Inventory(
            variant_id=variants["NIKE-R7-BLU-09"].variant_id,
            available_stock=3,
            reserved_stock=0,
            reorder_level=DEFAULT_REORDER_LEVEL,
        ),

        # ==================================================
        # Adidas Ultraboost
        # ==================================================

        Inventory(
            variant_id=variants["ADI-UB-BLK-08"].variant_id,
            available_stock=9,
            reserved_stock=0,
            reorder_level=DEFAULT_REORDER_LEVEL,
        ),

        Inventory(
            variant_id=variants["ADI-UB-BLK-09"].variant_id,
            available_stock=4,
            reserved_stock=0,
            reorder_level=DEFAULT_REORDER_LEVEL,
        ),

        Inventory(
            variant_id=variants["ADI-UB-WHT-09"].variant_id,
            available_stock=0,
            reserved_stock=0,
            reorder_level=DEFAULT_REORDER_LEVEL,
        ),

        # ==================================================
        # Adidas Samba
        # ==================================================

        Inventory(
            variant_id=variants["ADI-SAM-WHT-08"].variant_id,
            available_stock=11,
            reserved_stock=0,
            reorder_level=DEFAULT_REORDER_LEVEL,
        ),

        Inventory(
            variant_id=variants["ADI-SAM-WHT-09"].variant_id,
            available_stock=9,
            reserved_stock=1,
            reorder_level=DEFAULT_REORDER_LEVEL,
        ),

        # ==================================================
        # Puma RS-X
        # ==================================================

        Inventory(
            variant_id=variants["PUMA-RSX-RED-08"].variant_id,
            available_stock=7,
            reserved_stock=0,
            reorder_level=DEFAULT_REORDER_LEVEL,
        ),

        Inventory(
            variant_id=variants["PUMA-RSX-RED-09"].variant_id,
            available_stock=0,
            reserved_stock=0,
            reorder_level=DEFAULT_REORDER_LEVEL,
        ),

        # ==================================================
        # Samsung Galaxy Buds Pro
        # ==================================================

        Inventory(
            variant_id=variants["SAM-BUDS-BLK"].variant_id,
            available_stock=25,
            reserved_stock=3,
            reorder_level=5,
        ),

        Inventory(
            variant_id=variants["SAM-BUDS-WHT"].variant_id,
            available_stock=18,
            reserved_stock=1,
            reorder_level=5,
        ),

        Inventory(
            variant_id=variants["SAM-BUDS-PRP"].variant_id,
            available_stock=0,
            reserved_stock=0,
            reorder_level=5,
        ),

        # ==================================================
        # Samsung Galaxy Watch
        # ==================================================

        Inventory(
            variant_id=variants["SAM-WATCH-40"].variant_id,
            available_stock=10,
            reserved_stock=1,
            reorder_level=3,
        ),

        Inventory(
            variant_id=variants["SAM-WATCH-44"].variant_id,
            available_stock=8,
            reserved_stock=0,
            reorder_level=3,
        ),

        # ==================================================
        # Apple AirPods Pro 2
        # ==================================================

        Inventory(
            variant_id=variants["APPLE-AIRPODS-PRO2"].variant_id,
            available_stock=30,
            reserved_stock=5,
            reorder_level=10,
        ),
    ]

    session.add_all(inventory)

    await flush(session)

    print(f"   ✓ {len(inventory)} inventory records inserted.")


async def seed_customer(
    session: AsyncSession,
) -> Customer:
    """
    Seed a demo customer.
    """

    print("→ Seeding Customer...")

    customer = Customer(
        full_name="Aniket Kumar",
        email="aniket@example.com",
        phone="9876543210",
    )

    session.add(customer)

    await flush(session)

    print("   ✓ Demo customer inserted.")

    return customer

async def seed_addresses(
    session: AsyncSession,
    customer: Customer,
) -> list[Address]:
    """
    Seed customer addresses.
    """

    print("→ Seeding Customer Addresses...")

    addresses = [

        # --------------------------------------------------
        # Home
        # --------------------------------------------------

        Address(
            customer_id=customer.customer_id,
            address_line1="221B MG Road",
            address_line2="Near City Mall",
            city="Bengaluru",
            state="Karnataka",
            country="India",
            postal_code="560001",
            is_default=True,
        ),

        # --------------------------------------------------
        # Office
        # --------------------------------------------------

        Address(
            customer_id=customer.customer_id,
            address_line1="Electronic City Phase 1",
            address_line2="Tech Park",
            city="Bengaluru",
            state="Karnataka",
            country="India",
            postal_code="560100",
            is_default=False,
        ),
    ]

    session.add_all(addresses)

    await flush(session)

    print(f"   ✓ {len(addresses)} addresses inserted.")

    return addresses


async def seed_database() -> None:
    """
    Seed the development database with demo data.
    """

    async with AsyncSessionLocal() as session:

        try:

            # --------------------------------------------------
            # Already Seeded?
            # --------------------------------------------------

            if await database_already_seeded(session):

                print("✓ Database already contains seed data.")
                return

            print("=" * 60)
            print("Starting Database Seeding")
            print("=" * 60)

            # --------------------------------------------------
            # Master Data
            # --------------------------------------------------

            categories = await seed_categories(session)

            brands = await seed_brands(session)

            products = await seed_products(
                session,
                categories,
                brands,
            )

            variants = await seed_product_variants(
                session,
                products,
            )

            await seed_inventory(
                session,
                variants,
            )

            # --------------------------------------------------
            # Customer Data
            # --------------------------------------------------

            customer = await seed_customer(
                session,
            )

            await seed_addresses(
                session,
                customer,
            )

            # --------------------------------------------------
            # Commit
            # --------------------------------------------------

            await commit(session)

            print()
            print("=" * 60)
            print("Database seeded successfully.")
            print("=" * 60)

            print("Categories        : 3")
            print("Brands            : 5")
            print("Products          : 8")
            print("Product Variants  : 21")
            print("Inventory Records : 21")
            print("Customers         : 1")
            print("Addresses         : 2")
            print("=" * 60)

        except Exception as exc:

            await rollback(session)

            print()
            print("=" * 60)
            print("Database seeding failed.")
            print("=" * 60)

            raise exc


if __name__ == "__main__":
    asyncio.run(seed_database())